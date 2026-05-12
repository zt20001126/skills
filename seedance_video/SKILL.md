---
name: seedance_video
description: 为 Seedance 视频创作生成可复用的视频方案、分镜结构、参数建议和英文视频 Prompt。用于文生视频、图生视频、服装/商品展示、社媒广告、电商详情视频、Lookbook、短视频创意和多镜头分镜提示词；不用于普通视频剪辑、非 Seedance 平台执行或泛文案写作。
---

# Seedance 视频创作 Skill

用于将用户输入的商品、场景、平台、时长、画幅、视觉风格、运镜、动作和展示重点，整理成适合 Seedance 使用的视频创作方案、参数建议和最终英文视频 Prompt。

## 触发场景

- 用户明确提到 Seedance、视频生成、文生视频、图生视频或视频 Prompt。
- 用户需要商品视频、服装视频、电商详情页视频、社媒广告、Lookbook 或短片分镜。
- 用户需要把一个较长创意拆成多个 Seedance 分镜 Prompt。

不要用于普通视频剪辑、剪映脚本、非 Seedance API 任务或纯营销文案任务。

## 支持模式

- `text_to_video`：根据文字需求生成视频 brief、参数建议和英文 Prompt。
- `image_to_video`：根据用户提供的产品图、人物图或参考图生成图生视频 Prompt，强调保持主体一致。
- `shot_list`：把 15-30 秒创意拆成多个可生成的镜头段落，每段都有画面、动作、运镜和 Prompt。

## 工作流

1. 读取 `style_config.json`，获得默认平台、时长、比例、生成模式、运镜、场景、参数建议和避免项。
2. 解析用户需求，提取主体、场景、平台、时长、画幅、风格、人物、动作、镜头、参考图和输出重点。
3. 选择生成模式：默认 `text_to_video`；如果用户提供参考图，使用 `image_to_video`；如果用户要求拆片或多镜头，使用 `shot_list`。
4. 做安全和版权检查；涉及真人、品牌、IP、参考图授权时，读取 `references/safety-and-rights.md`。
5. 生成中文视频创作方案和镜头结构。
6. 使用 `prompt_template.md` 或 `scripts/prompt_builder.py` 组合最终英文 Seedance Video Prompt。
7. 输出 `creative_plan`、`shot_structure`、`parameters`、`positive_prompt`、`negative_prompt` 和 `warnings`。

## 输出格式

- 视频创作方案：中文，说明视频目标、内容策略和平台适配。
- 镜头结构：按时间段描述主体、动作、运镜、构图和展示重点。
- 参数建议：生成模式、时长、比例、分辨率、帧率、运动强度等建议。具体 API 字段需要以 Seedance 官方文档为准。
- Seedance English Prompt：英文，面向视频生成模型。
- Negative Prompt：英文，描述需要避免的低质画面、错误表现和不安全内容。
- Warnings：当用户输入缺少字段、平台不支持、涉及授权风险或 API 能力未确认时给出提示。

## 视频创作原则

- 主体必须明确，商品、人物或场景不要在镜头中失焦。
- 文生视频要描述可见画面，不堆抽象营销词。
- 图生视频要强调保留参考图主体、颜色、材质、结构和身份一致性。
- 多镜头视频要保持主体、场景、服装、光线和运动方向一致。
- 镜头语言保持可生成：推近、拉远、跟拍、环绕、摇镜、手持、航拍、景深、转场等只选必要项。
- 平台节奏要清楚：短视频重开头钩子，电商视频重细节和可信展示，Lookbook 重质感和节奏。

## 文件使用

- `style_config.json`：产品后端或 Agent 读取的默认配置。
- `prompt_template.md`：人工或 Agent 拼接 Prompt 时的模板。
- `scripts/prompt_builder.py`：需要自动拼接、批量生成或参数默认值处理时使用。
- `references/safety-and-rights.md`：涉及真实人物、品牌、IP、参考图、肖像或高风险内容时读取。

## API 边界

当前 Skill 不直接调用 Seedance API，只输出 Prompt 和参数建议。后续接入 API 时，在 `scripts/` 下新增独立客户端文件，例如 `seedance_client.py`，并从环境变量读取 API Key。不要把密钥、真实接口地址或未经验证的 API 参数写进 `SKILL.md`。
