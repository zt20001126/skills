# Skill 系统开发文档

本文档用于设计“前端勾选 Skill，并通过对话框生成服装图片/视频 Prompt”的后端实现方案。

适用场景：

- 设计师风格图片生成，例如山本耀司、川久保玲。
- 电商转化图片生成，例如 AI 造型师：高转化模特图。
- 视频 Prompt 生成，例如 Seedance 视频创作。

## 1. 核心概念

Skill 不是模型本身，而是一组可复用的配置、模板和工作流。

推荐存储方式：

```text
文件系统 / 对象存储：保存 Skill 文件内容
数据库：保存 Skill 索引、展示信息、状态、版本和文件路径
```

示例 Skill 目录：

```text
skills/
  yohji-yamamoto-inspired/
    SKILL.md
    style_config.json
    prompt_template.md

  fashion_model_conversion/
    SKILL.md
    style_config.json
    prompt_template.md
    references/
      safety-and-rights.md
    scripts/
      prompt_builder.py
```

## 2. 功能流程

```text
前端展示 Skill 列表
→ 用户勾选一个 Skill
→ 用户在对话框输入需求
→ 前端提交 message + selected_skill_id
→ 后端查询 Skill 数据
→ 后端读取 style_config.json 和 prompt_template.md
→ 后端解析用户输入
→ 后端组装 positive_prompt / negative_prompt
→ 后端调用图片或视频模型
→ 后端保存生成任务和结果
→ 前端展示生成结果
```

## 3. 数据库设计

### 3.1 Skill 主表：`ai_skills`

用于管理 Skill 的展示、分类、状态和版本。

```sql
CREATE TABLE ai_skills (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  skill_id VARCHAR(100) NOT NULL UNIQUE COMMENT 'Skill 唯一标识，例如 yohji-yamamoto-inspired',
  display_name VARCHAR(100) NOT NULL COMMENT '前端展示名称',
  zh_name VARCHAR(100) COMMENT '中文名称，例如 山本耀司',
  skill_type VARCHAR(50) NOT NULL COMMENT 'Skill 类型，例如 image_style、image_conversion、video_prompt',
  category VARCHAR(50) COMMENT '分类，例如 designer_style、ecommerce_conversion、video_creation',
  version VARCHAR(30) NOT NULL DEFAULT '1.0.0',
  status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'active、inactive、draft',
  description TEXT COMMENT '简短介绍',
  icon_url VARCHAR(500) COMMENT '图标地址',
  cover_url VARCHAR(500) COMMENT '封面图地址',
  config_path VARCHAR(500) NOT NULL COMMENT 'style_config.json 路径',
  template_path VARCHAR(500) COMMENT 'prompt_template.md 路径',
  skill_doc_path VARCHAR(500) COMMENT 'SKILL.md 路径',
  default_model VARCHAR(100) COMMENT '默认调用模型',
  sort_order INT NOT NULL DEFAULT 0,
  created_by BIGINT,
  updated_by BIGINT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

推荐索引：

```sql
CREATE INDEX idx_ai_skills_status ON ai_skills(status);
CREATE INDEX idx_ai_skills_category ON ai_skills(category);
CREATE INDEX idx_ai_skills_type ON ai_skills(skill_type);
```

### 3.2 Skill 文件表：`ai_skill_files`

用于记录一个 Skill 下的所有文件。

```sql
CREATE TABLE ai_skill_files (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  skill_id VARCHAR(100) NOT NULL COMMENT '关联 ai_skills.skill_id',
  file_type VARCHAR(50) NOT NULL COMMENT 'skill_doc、config、template、script、reference、asset',
  file_path VARCHAR(500) NOT NULL COMMENT '文件路径或对象存储地址',
  version VARCHAR(30) NOT NULL DEFAULT '1.0.0',
  is_required BOOLEAN NOT NULL DEFAULT TRUE,
  checksum VARCHAR(100) COMMENT '文件摘要，用于缓存校验',
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

推荐索引：

```sql
CREATE INDEX idx_ai_skill_files_skill_id ON ai_skill_files(skill_id);
CREATE INDEX idx_ai_skill_files_type ON ai_skill_files(file_type);
```

### 3.3 生成任务表：`ai_generation_tasks`

用于记录用户每次生成请求。

```sql
CREATE TABLE ai_generation_tasks (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_id VARCHAR(100) NOT NULL UNIQUE COMMENT '业务任务 ID',
  user_id BIGINT NOT NULL,
  skill_id VARCHAR(100) NOT NULL,
  task_type VARCHAR(50) NOT NULL COMMENT 'image_generation、video_prompt、video_generation',
  input_message TEXT NOT NULL COMMENT '用户原始输入',
  parsed_intent JSON COMMENT '解析后的用户意图',
  positive_prompt TEXT COMMENT '最终正向 Prompt',
  negative_prompt TEXT COMMENT '最终负向 Prompt',
  model_name VARCHAR(100) COMMENT '调用的模型',
  model_params JSON COMMENT '模型参数，例如 size、ratio、seed',
  status VARCHAR(30) NOT NULL DEFAULT 'pending' COMMENT 'pending、running、success、failed',
  error_message TEXT,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

推荐索引：

```sql
CREATE INDEX idx_generation_tasks_user_id ON ai_generation_tasks(user_id);
CREATE INDEX idx_generation_tasks_skill_id ON ai_generation_tasks(skill_id);
CREATE INDEX idx_generation_tasks_status ON ai_generation_tasks(status);
```

### 3.4 生成结果表：`ai_generation_results`

用于保存图片、视频或 Prompt 结果。

```sql
CREATE TABLE ai_generation_results (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  task_id VARCHAR(100) NOT NULL,
  result_type VARCHAR(30) NOT NULL COMMENT 'image、video、prompt',
  result_url VARCHAR(1000) COMMENT '图片或视频 URL',
  result_path VARCHAR(1000) COMMENT '本地路径或对象存储路径',
  result_text TEXT COMMENT 'Prompt 类结果',
  width INT,
  height INT,
  duration_seconds INT,
  sort_order INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL
);
```

推荐索引：

```sql
CREATE INDEX idx_generation_results_task_id ON ai_generation_results(task_id);
```

## 4. 接口设计

接口统一前缀：

```text
/api/ai
```

### 4.1 获取 Skill 列表

用于前端展示可选 Skill。

请求方式：

```http
GET /api/ai/skills
```

请求参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `category` | string | 否 | Skill 分类，例如 `designer_style` |
| `skill_type` | string | 否 | Skill 类型，例如 `image_style` |
| `status` | string | 否 | 默认 `active` |

请求示例：

```http
GET /api/ai/skills?category=designer_style&status=active
```

返回参数：

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "skill_id": "yohji-yamamoto-inspired",
      "display_name": "Yohji Yamamoto Inspired",
      "zh_name": "山本耀司",
      "skill_type": "image_style",
      "category": "designer_style",
      "description": "生成受山本耀司风格启发的服装图片 Prompt",
      "icon_url": "",
      "cover_url": "",
      "version": "1.0.0"
    }
  ]
}
```

### 4.2 获取 Skill 详情

用于前端展示 Skill 说明，或后端调试。

请求方式：

```http
GET /api/ai/skills/{skill_id}
```

返回示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "skill_id": "yohji-yamamoto-inspired",
    "display_name": "Yohji Yamamoto Inspired",
    "zh_name": "山本耀司",
    "skill_type": "image_style",
    "category": "designer_style",
    "description": "生成受山本耀司风格启发的服装图片 Prompt",
    "version": "1.0.0",
    "status": "active",
    "files": [
      {
        "file_type": "config",
        "file_path": "/app/skills/yohji-yamamoto-inspired/style_config.json"
      },
      {
        "file_type": "template",
        "file_path": "/app/skills/yohji-yamamoto-inspired/prompt_template.md"
      }
    ]
  }
}
```

### 4.3 生成图片

用于用户勾选 Skill 后，在对话框中发送图片生成需求。

请求方式：

```http
POST /api/ai/image/generate
```

请求参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `message` | string | 是 | 用户输入内容 |
| `selected_skill_id` | string | 是 | 用户勾选的 Skill ID |
| `user_id` | number | 是 | 用户 ID |
| `image_count` | number | 否 | 生成数量，默认 1 |
| `size` | string | 否 | 图片尺寸，例如 `1024x1536` |
| `reference_image_url` | string | 否 | 商品图或参考图 |
| `extra_params` | object | 否 | 额外模型参数 |

请求示例：

```json
{
  "user_id": 10001,
  "selected_skill_id": "yohji-yamamoto-inspired",
  "message": "绘制一张夏季男款短袖图片",
  "image_count": 1,
  "size": "1024x1536",
  "extra_params": {
    "quality": "high"
  }
}
```

后端处理逻辑：

```text
1. 校验用户和 Skill 是否存在。
2. 查询 ai_skills，确认 Skill 状态为 active。
3. 读取 config_path 对应的 style_config.json。
4. 读取 template_path 对应的 prompt_template.md。
5. 解析 message，提取服装品类、季节、性别、场景等。
6. 合并用户输入和 Skill 配置。
7. 生成 positive_prompt 和 negative_prompt。
8. 创建 ai_generation_tasks 记录。
9. 调用图片大模型。
10. 保存 ai_generation_results。
11. 返回任务和图片结果。
```

返回示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task_id": "img_20260512_000001",
    "status": "success",
    "skill_id": "yohji-yamamoto-inspired",
    "positive_prompt": "summer menswear short-sleeve shirt, poetic Japanese avant-garde tailoring...",
    "negative_prompt": "cute, sweet, pastel colors, tight bodycon fit, low quality, blurry...",
    "results": [
      {
        "result_type": "image",
        "result_url": "https://cdn.example.com/generated/img_20260512_000001.png",
        "width": 1024,
        "height": 1536
      }
    ]
  }
}
```

### 4.4 仅生成 Prompt

用于调试、预览或不立即调用模型的场景。

请求方式：

```http
POST /api/ai/prompt/build
```

请求示例：

```json
{
  "selected_skill_id": "fashion_model_conversion",
  "message": "生成一张黑色羊毛大衣的小红书高转化模特图",
  "reference_image_url": "https://cdn.example.com/product/coat.png"
}
```

返回示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "skill_id": "fashion_model_conversion",
    "positive_prompt": "Create a high-converting ecommerce fashion model image. Garment: black wool coat...",
    "negative_prompt": "Avoid: blurry image, low resolution, bad anatomy...",
    "warnings": []
  }
}
```

### 4.5 查询生成任务

用于异步生成模型或视频任务。

请求方式：

```http
GET /api/ai/tasks/{task_id}
```

返回示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task_id": "img_20260512_000001",
    "status": "success",
    "skill_id": "yohji-yamamoto-inspired",
    "task_type": "image_generation",
    "results": [
      {
        "result_type": "image",
        "result_url": "https://cdn.example.com/generated/img_20260512_000001.png"
      }
    ],
    "error_message": null
  }
}
```

## 5. 后端核心模块

建议拆分为以下服务：

```text
SkillService
  - 查询 Skill 列表
  - 查询 Skill 详情
  - 读取 Skill 文件

PromptBuildService
  - 解析用户输入
  - 合并 style_config.json
  - 渲染 prompt_template.md
  - 生成 positive_prompt / negative_prompt

GenerationTaskService
  - 创建任务
  - 更新任务状态
  - 保存生成结果

ImageModelClient
  - 调用图片大模型
  - 处理模型返回
```

## 6. Prompt 组装逻辑

核心伪代码：

```python
def generate_image(user_id, selected_skill_id, message, reference_image_url=None):
    skill = skill_service.get_active_skill(selected_skill_id)

    config = skill_service.load_json(skill.config_path)
    template = skill_service.load_text(skill.template_path)

    user_intent = prompt_service.parse_message(message)

    prompt_result = prompt_service.build_prompt(
        message=message,
        user_intent=user_intent,
        config=config,
        template=template,
        reference_image_url=reference_image_url
    )

    task = task_service.create_task(
        user_id=user_id,
        skill_id=selected_skill_id,
        task_type="image_generation",
        input_message=message,
        positive_prompt=prompt_result.positive_prompt,
        negative_prompt=prompt_result.negative_prompt
    )

    model_result = image_model_client.generate(
        prompt=prompt_result.positive_prompt,
        negative_prompt=prompt_result.negative_prompt
    )

    task_service.save_results(task.task_id, model_result)
    task_service.mark_success(task.task_id)

    return task_service.get_task_result(task.task_id)
```

## 7. 错误码设计

| code | 说明 |
| --- | --- |
| `0` | 成功 |
| `40001` | 请求参数错误 |
| `40002` | Skill 不存在 |
| `40003` | Skill 未启用 |
| `40004` | Skill 配置文件缺失 |
| `40005` | Prompt 生成失败 |
| `40006` | 模型调用失败 |
| `40007` | 参考图无效或无权限 |
| `50000` | 系统内部错误 |

错误返回示例：

```json
{
  "code": 40002,
  "message": "Skill not found",
  "data": null
}
```

## 8. 第一版上线建议

第一版不建议把 Skill 文件全文全部存数据库。

推荐：

```text
Skill 文件：存服务器文件系统或对象存储
数据库：存 Skill 元信息和文件路径
```

第一版最小表：

```text
ai_skills
ai_skill_files
ai_generation_tasks
ai_generation_results
```

第一版最小接口：

```text
GET  /api/ai/skills
GET  /api/ai/skills/{skill_id}
POST /api/ai/image/generate
POST /api/ai/prompt/build
GET  /api/ai/tasks/{task_id}
```

第一版必须支持：

- Skill 列表展示
- 用户勾选 Skill
- 后端读取 Skill 配置
- 生成最终 Prompt
- 调用图片模型
- 保存任务和结果
- 返回图片 URL

后续再扩展：

- Skill 后台管理
- Skill 版本发布
- Prompt A/B 测试
- 用户收藏 Skill
- 图片重新生成
- 多模型路由
- 视频生成任务轮询
