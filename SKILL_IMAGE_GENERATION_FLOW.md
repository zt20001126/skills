# Skill 图片生成实现流程

本文说明前端用户勾选设计师 Skill 后，如何通过后端读取 Skill 配置、组装 Prompt，并调用图片大模型生成服装图片。

## 示例场景

用户操作：

```text
勾选 Skill：yohji-yamamoto-inspired
输入提示词：绘制一张夏季男款短袖图片
点击发送
```

目标结果：

```text
生成一张受山本耀司风格启发的夏季男款短袖服装图片。
```

## 1. 前端记录用户选择

前端页面中的每个 Skill 都应该有唯一 `skill_id`。

示例：

```json
{
  "skill_id": "yohji-yamamoto-inspired",
  "display_name": "Yohji Yamamoto Inspired",
  "zh_name": "山本耀司"
}
```

当用户勾选山本耀司 Skill 后，前端保存：

```text
selected_skill_id = yohji-yamamoto-inspired
```

用户点击发送时，前端向后端提交：

```json
{
  "message": "绘制一张夏季男款短袖图片",
  "selected_skill_id": "yohji-yamamoto-inspired",
  "task_type": "image_generation"
}
```

## 2. 后端定位 Skill

后端根据 `selected_skill_id` 找到对应目录：

```text
skills/yohji-yamamoto-inspired/
├── SKILL.md
├── style_config.json
└── prompt_template.md
```

其中：

- `SKILL.md`：给 Agent 或开发者阅读，说明 Skill 的用途和工作流。
- `style_config.json`：给后端读取，提供风格、色彩、廓形、材质、负面词等结构化配置。
- `prompt_template.md`：定义如何组合用户输入和 Skill 配置。

## 3. 读取 Skill 配置

后端读取 `style_config.json`。

示例字段：

```json
{
  "style_summary": "poetic Japanese avant-garde tailoring, black draped monochrome fashion, oversized fluid silhouettes",
  "silhouette": ["oversized", "loose", "draped", "fluid"],
  "palette": ["deep black", "charcoal black", "soft white"],
  "materials": ["matte wool gabardine", "washed cotton", "soft linen"],
  "negative_prompt": ["cute", "sweet", "pastel colors", "tight bodycon fit"]
}
```

这些配置就是该 Skill 的风格 DNA。

## 4. 解析用户输入

用户输入：

```text
绘制一张夏季男款短袖图片
```

后端可以解析成：

```json
{
  "category": "short-sleeve shirt",
  "season": "summer",
  "gender": "menswear",
  "image_type": "fashion design image"
}
```

如果第一版系统不做复杂 NLP，也可以直接把原始输入作为 `user_input`，交给 Prompt 模板处理。

## 5. 组装最终 Prompt

后端将用户输入和 Skill 配置合并。

用户需求：

```text
summer menswear short-sleeve shirt
```

Skill 风格：

```text
poetic Japanese avant-garde tailoring,
black draped monochrome fashion,
oversized fluid silhouette,
asymmetric deconstructed suiting,
quiet melancholic runway mood
```

最终 `positive_prompt` 示例：

```text
summer menswear short-sleeve shirt, poetic Japanese avant-garde tailoring, black draped monochrome fashion, oversized fluid silhouette, asymmetric deconstructed construction, loose elongated proportion, deep black and charcoal palette, washed cotton and soft linen fabric, quiet conceptual runway styling, full-body fashion editorial, clean dark runway background, soft directional studio lighting, sharp garment detail, professional high-resolution fashion photography
```

最终 `negative_prompt` 示例：

```text
cute, sweet, pastel colors, neon colors, glossy glamour, tight bodycon fit, sportswear logo, streetwear logo, conventional business suit, fast fashion, visible logo, brand text, direct replica, low quality, blurry, bad anatomy, extra limbs
```

## 6. 调用图片大模型

后端将 Prompt 传给图片生成模型。

示例请求：

```json
{
  "model": "your-image-model",
  "prompt": "summer menswear short-sleeve shirt, poetic Japanese avant-garde tailoring...",
  "negative_prompt": "cute, sweet, pastel colors...",
  "size": "1024x1536",
  "num_images": 1
}
```

图片模型返回图片 URL、文件路径或任务 ID。

## 7. 后端返回结果

后端返回给前端：

```json
{
  "status": "success",
  "skill_id": "yohji-yamamoto-inspired",
  "final_prompt": "summer menswear short-sleeve shirt, poetic Japanese avant-garde tailoring...",
  "image_url": "https://example.com/generated-image.png"
}
```

前端展示图片，并可选择展示最终 Prompt、重新生成、保存或下载。

## 完整链路

```text
用户勾选 Skill
→ 前端记录 skill_id
→ 用户输入提示词
→ 前端发送 message + skill_id
→ 后端读取对应 Skill 配置
→ 后端解析用户需求
→ 后端合并用户需求 + Skill 风格配置
→ 后端生成 positive_prompt / negative_prompt
→ 后端调用图片模型
→ 图片模型返回结果
→ 后端保存图片和任务记录
→ 前端展示图片
```

## 后端核心伪代码

```python
def generate_image(message, selected_skill_id):
    skill = load_skill(selected_skill_id)

    user_intent = parse_user_message(message)

    positive_prompt = build_prompt(
        user_input=user_intent,
        style_config=skill["style_config"],
        template=skill["prompt_template"]
    )

    negative_prompt = build_negative_prompt(skill["style_config"])

    result = call_image_model(
        prompt=positive_prompt,
        negative_prompt=negative_prompt
    )

    return result
```

## 核心理解

Skill 本身不是直接画图的模型。

它在系统中的作用是：

```text
可复用的风格配置 + Prompt 组装规则
```

用户勾选 Skill 后，后端读取该 Skill 的配置，并将它和用户输入组合成更专业、更稳定的最终 Prompt，再交给图片大模型生成图片。
