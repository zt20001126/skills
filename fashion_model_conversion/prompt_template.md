# Fashion Model Conversion Prompt Template

## 输入字段

- `garment`: 服装商品，例如 black wool coat、floral summer dress、wide-leg jeans。
- `reference_image`: 是否使用商品参考图；有参考图时强调保留服装结构和细节。
- `platform`: 平台，例如 taobao、douyin、xiaohongshu、independent_site、instagram、lookbook。
- `target_customer`: 目标人群，例如 通勤女性、年轻辣妹、轻熟女、欧美独立站用户。
- `model_type`: 模特类型。
- `pose`: 姿势。
- `scene`: 场景。
- `visual_style`: 视觉风格。
- `conversion_focus`: 转化重点。
- `lighting`: 光线。
- `composition`: 构图。
- `avoid`: 避免项。

## Positive Prompt 组合方式

```text
{prompt_prefix}
Garment: {garment}.
Platform: {platform}, aspect ratio {aspect_ratio}.
Target customer: {target_customer}.
Model: {model_type}.
Pose: {pose}.
Scene: {scene}.
Visual style: {visual_style}.
Conversion focus: {conversion_focus}.
Lighting: {lighting}.
Composition: {composition}.
Reference image requirements: {reference_image_note}
{prompt_suffix}
```

## Negative Prompt 组合方式

```text
Avoid: {avoid}
```

## 推荐输出格式

```text
造型方案：
{styling_plan}

构图方案：
{composition_plan}

Image Prompt：
{positive_prompt}

Negative Prompt：
{negative_prompt}

Warnings：
{warnings}
```
