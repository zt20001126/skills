# 贡献指南

本指南定义新增和维护 skill 的最低标准。每个 skill 保持独立、可发现，并能让使用者只阅读必要内容即可正确调用。

## 新建 Skill

1. 选择一个明确任务边界，确认现有 skill 没有覆盖相同职责。
2. 复制 [`templates/skill-template/SKILL.md`](templates/skill-template/SKILL.md)，新建根目录子目录。
3. 目录名和 frontmatter `name` 使用相同的唯一标识。新目录统一使用小写 kebab-case，例如 `fashion-image-review`。
4. 编写完整的触发描述、操作流程、输出要求和限制。
5. 仅在确有复用价值时增加 `references/`、`scripts/`、`agents/`、配置或 Prompt 模板。
6. 更新根目录 README 的分类索引和用途说明。
7. 运行 `python scripts/validate_skills.py`。

现存的下划线命名目录是历史标识。新 skill 不新增下划线命名；不要仅为格式统一而重命名已发布目录。

## SKILL.md 约定

Frontmatter 至少包含：

```yaml
---
name: fashion-image-review
description: Review fashion product images for garment accuracy, presentation quality, and e-commerce readiness. Use when a user asks to assess or improve a fashion product image.
---
```

`name` 和 `description` 使用单行纯文本值；如需加引号，使用成对的单引号或双引号。不要使用 YAML 多行折叠块作为 `description`。

正文建议包含以下内容，按任务选择合适的小节名称：

- **用途与触发条件**：说明何时使用，以及相邻但不适用的任务。
- **工作流程**：列出可执行的步骤和必要的判断点。
- **输入与输出**：说明所需资料、交付格式和质量标准。
- **边界与限制**：说明必须遵守的约束、风险处理或禁止操作。
- **资源索引**：说明何时读取本目录中的参考资料、脚本或模板。

无需为了匹配模板而添加空章节。核心规则留在 `SKILL.md`；较长、低频查阅的细节放到 `references/`，并从核心流程链接过去。

## 支持文件布局

```text
<skill-name>/
├── SKILL.md                 # 必需
├── agents/                   # 可选：Codex 等工具的展示/调用元数据
├── references/               # 可选：领域细节和长篇说明
├── scripts/                  # 可选：可执行且可复用的辅助程序
├── prompt_template.md        # 可选：稳定复用的 Prompt 框架
└── config.json               # 可选：结构化且由脚本消费的配置
```

- 文件名使用小写、清晰的英文词组；同类配置在 skill 内保持一致。
- 脚本应注明运行方式和依赖。不要把仅适用于某个用户机器的路径写成仓库通用依赖。
- 配置应使用机器可读格式；如被脚本读取，应检查必需字段和格式。
- 参考资料应有明确来源或维护背景，并避免复制无关的大段内容。

## 提交前检查

- [ ] `SKILL.md` 存在，frontmatter 的 `name` 与目录名相同且唯一。
- [ ] `description` 能帮助使用者判断何时触发该 skill。
- [ ] 工作流程、输入输出和限制足够明确，没有互相矛盾的规则。
- [ ] README 索引已更新，目录链接正确，用途说明具体。
- [ ] 支持文件在主文档中有必要的说明或引用。
- [ ] 未包含秘密、私人数据、无关缓存或生成产物。
- [ ] `python scripts/validate_skills.py` 通过。

GitHub Actions 会在推送和 Pull Request 时运行相同的仓库结构校验。
