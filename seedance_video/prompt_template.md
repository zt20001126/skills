# Seedance Video Prompt Template

## 输入字段

- `generation_mode`: `text_to_video`、`image_to_video` 或 `shot_list`。
- `subject`: 视频主体，例如 black wool coat、coffee bottle、cyberpunk city skyline。
- `reference_image`: 是否使用参考图；图生视频时描述参考图用途，不在 Prompt 中编造图片路径。
- `scene`: 拍摄场景，例如 clean studio background、modern city street。
- `platform`: 投放平台，例如 douyin、xiaohongshu、tiktok、instagram_reels、ecommerce、lookbook。
- `duration`: 视频时长，例如 5s、10s、15s、30s。
- `aspect_ratio`: 视频比例，例如 9:16、3:4、16:9。
- `visual_style`: 视觉风格。
- `camera_movement`: 运镜方式。
- `subject_focus`: 主体展示重点。
- `action`: 主体或人物动作。
- `lighting`: 光线。
- `parameters`: 分辨率、帧率、运动强度等建议。
- `avoid`: 避免项。

## Positive Prompt 组合方式

```text
{prompt_prefix}
Generation mode: {generation_mode}.
Subject: {subject}.
Video type: {video_type}.
Platform: {platform}, aspect ratio {aspect_ratio}, duration {duration}.
Scene: {scene}.
Visual style: {visual_style}.
Action: {action}.
Camera movement: {camera_movement}.
Subject focus: {subject_focus}.
Lighting: {lighting}.
Shot structure: {shot_structure}.
Continuity requirements: keep the subject identity, color, material, scale, and scene lighting consistent throughout the video.
{image_to_video_note}
{prompt_suffix}
```

## Negative Prompt 组合方式

```text
Avoid: {avoid}
```

## 推荐输出格式

```text
视频创作方案：
{creative_plan}

镜头结构：
{shot_structure}

参数建议：
{parameters}

Seedance English Prompt：
{positive_prompt}

Negative Prompt：
{negative_prompt}

Warnings：
{warnings}
```
