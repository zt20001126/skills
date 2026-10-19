# 仓库协作约定

本仓库的正式名称是 **Codex Skills Library**，项目标识为 `codex-skills-library`。这是一个可复用 skill 集合，不是单一应用程序。

## 目录与边界

- 每个可发布 skill 必须位于仓库根目录下的独立目录，并包含 `SKILL.md`。
- 一个 skill 的专属模板、参考资料、脚本和配置应放在该 skill 目录中，不要放入其他 skill 目录。
- 仓库级说明、模板和维护工具分别放在根目录、`templates/` 和 `scripts/`。
- 新 skill 目录使用小写 kebab-case，且目录名必须与 `SKILL.md` 的 `name` 一致。已有下划线目录名暂时保留，避免破坏现有引用。

## Skill 文档要求

- `SKILL.md` 必须以 YAML frontmatter 开始，并提供非空 `name` 与 `description`。
- `name` 是稳定、唯一的调用标识；重命名目录或标识前，先检查 README、文档和外部集成中的引用。
- `description` 写清适用任务、触发情形和主要范围，避免泛化描述或仅重复标题。
- 主文件应优先说明触发条件、工作流程、输入输出和限制。较长的背景材料放入 `references/`，并从主文件明确链接。
- 每项 skill 资源都应服务于该 skill 的使用；不要提交密钥、用户数据或无关构建产物。

## 修改流程

1. 阅读相关 skill 和 [`CONTRIBUTING.md`](CONTRIBUTING.md)，沿用仓库既有的语言与领域约定。
2. 新增或修改 skill 后，更新根目录 [`README.md`](README.md) 的索引和用途说明。
3. 运行 `python scripts/validate_skills.py` 检查 frontmatter、标识唯一性和 README 索引。
4. 变更说明应指出新增或调整的 skill，以及对调用标识和支持文件的影响。

不要为了风格统一批量重命名已有 skill；如确需迁移，需同步更新全部引用并说明兼容影响。
