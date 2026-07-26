"""静态检查 Hookshot 后端中容易违反的关键开发规范。"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
import re
import sys


EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "selection_agent",
    "listing_agent",
    "spacex",
}
BUSINESS_LAYER_PARTS = {"router", "service", "tasks", "task", "nodes", "node", "tools"}
RAW_SQL_IMPORTS = {"select", "update", "delete"}
RAW_EXCEPTION_PATTERNS = (
    re.compile(r"Result\.error\s*\(\s*(?:str\s*\(\s*\w+\s*\)|f[\"'][^\"']*\{\s*\w+\s*\})"),
    re.compile(r"[\"'](?:message|msg|error|detail)[\"']\s*:\s*str\s*\(\s*\w+\s*\)"),
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    code: str
    message: str


def is_excluded(path: Path) -> bool:
    """判断路径是否属于明确排除或工具生成的目录。"""
    return any(part in EXCLUDED_PARTS for part in path.parts)


def iter_python_files(root: Path, selected: list[Path]) -> list[Path]:
    """获取需要检查的 Python 文件。"""
    if selected:
        files = [path if path.is_absolute() else root / path for path in selected]
    else:
        files = list(root.rglob("*.py"))
    return sorted(
        path.resolve()
        for path in files
        if path.is_file() and path.suffix == ".py" and not is_excluded(path)
    )


def belongs_to_business_layer(path: Path) -> bool:
    """判断文件是否位于禁止直接执行 SQL 的业务层。"""
    lowered_parts = {part.lower() for part in path.parts}
    return bool(lowered_parts & BUSINESS_LAYER_PARTS)


def inspect_ast(path: Path, source: str) -> list[Finding]:
    """使用 AST 检查直接 SQL 调用和缺失返回类型。"""
    findings: list[Finding] = []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return [Finding(path, exc.lineno or 1, "H001", f"Python 语法错误：{exc.msg}")]

    if belongs_to_business_layer(path):
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imported = {alias.name for alias in node.names}
                illegal = imported & RAW_SQL_IMPORTS
                if illegal:
                    findings.append(
                        Finding(
                            path,
                            node.lineno,
                            "H101",
                            f"业务层导入了 SQL 构造器：{', '.join(sorted(illegal))}；请封装到 CRUD。",
                        )
                    )
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"exec", "execute", "query"}:
                    findings.append(
                        Finding(
                            path,
                            node.lineno,
                            "H102",
                            f"业务层调用了 session.{node.func.attr}()；请封装到 CRUD。",
                        )
                    )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns is None:
            if node.name.startswith("__") and node.name.endswith("__"):
                continue
            findings.append(
                Finding(path, node.lineno, "H201", f"函数 {node.name} 缺少返回类型标注。")
            )
    return findings


def inspect_text(path: Path, source: str) -> list[Finding]:
    """检查常见的原始异常泄漏写法。"""
    findings: list[Finding] = []
    for pattern in RAW_EXCEPTION_PATTERNS:
        for match in pattern.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            findings.append(
                Finding(path, line, "H301", "疑似向用户或 LLM 暴露原始异常，请改为安全消息并记录内部日志。")
            )
    return findings


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="检查 Hookshot 后端关键开发规范")
    parser.add_argument("--root", type=Path, required=True, help="Hookshot 项目根目录")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        type=Path,
        help="仅检查指定文件，可重复传入；相对路径基于项目根目录",
    )
    return parser.parse_args()


def main() -> int:
    """执行检查并返回适合 CI 使用的退出码。"""
    args = parse_args()
    root = args.root.resolve()
    if not (root / "AGENTS.md").is_file():
        print(f"错误：{root} 不是有效的 Hookshot 项目根目录。", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    files = iter_python_files(root, args.file)
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding(path, 1, "H002", "文件不是有效的 UTF-8 编码。"))
            continue
        findings.extend(inspect_ast(path, source))
        findings.extend(inspect_text(path, source))

    for finding in sorted(findings, key=lambda item: (str(item.path), item.line, item.code)):
        relative_path = finding.path.relative_to(root)
        print(f"{relative_path}:{finding.line}: {finding.code} {finding.message}")

    print(f"已检查 {len(files)} 个 Python 文件，发现 {len(findings)} 个问题。")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
