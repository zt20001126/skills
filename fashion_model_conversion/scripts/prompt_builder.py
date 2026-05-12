"""Build high-converting fashion model image prompts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_DIR / "style_config.json"


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load skill configuration."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
    if isinstance(value, dict):
        return ", ".join(f"{key}: {item}" for key, item in value.items() if item)
    return str(value).strip()


def _pick_platform(config: Mapping[str, Any], platform: str | None, warnings: list[str]) -> tuple[str, Mapping[str, Any]]:
    platforms = config.get("platforms", {})
    default_platform = config.get("default_platform", "xiaohongshu")
    platform_key = platform or default_platform
    if platform_key not in platforms:
        warnings.append(f"Unknown platform '{platform_key}', fallback to '{default_platform}'.")
        platform_key = default_platform
    return platform_key, platforms.get(platform_key, {})


def build_fashion_model_prompt(
    user_request: Mapping[str, Any],
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a product-ready fashion model image prompt."""
    cfg = dict(config or load_config())
    warnings: list[str] = []
    platform_key, platform_info = _pick_platform(cfg, _as_text(user_request.get("platform")) or None, warnings)

    garment = _as_text(user_request.get("garment") or user_request.get("product") or user_request.get("user_input"))
    if not garment:
        garment = "fashion garment"
        warnings.append("Missing garment/product; using generic 'fashion garment'.")

    target_customer = _as_text(user_request.get("target_customer") or "target ecommerce shopper")
    model_type = _as_text(user_request.get("model_type") or cfg.get("default_model_type"))
    pose = _as_text(user_request.get("pose") or cfg.get("default_pose"))
    scene = _as_text(user_request.get("scene") or cfg.get("default_scene"))
    visual_style = _as_text(user_request.get("visual_style") or cfg.get("default_visual_style"))
    conversion_focus = _as_text(user_request.get("conversion_focus") or cfg.get("default_conversion_focus"))
    lighting = _as_text(user_request.get("lighting") or cfg.get("default_lighting"))
    composition = _as_text(user_request.get("composition") or cfg.get("default_composition"))
    avoid = _as_text(user_request.get("avoid") or cfg.get("avoid"))
    aspect_ratio = _as_text(user_request.get("aspect_ratio") or platform_info.get("aspect_ratio") or cfg.get("default_aspect_ratio"))
    platform_name = _as_text(platform_info.get("name") or platform_key)
    style_note = _as_text(platform_info.get("style_note"))

    reference_note = ""
    if user_request.get("reference_image"):
        reference_note = cfg.get("reference_image_note", "")
    else:
        warnings.append("No reference_image provided; prompt will rely on text description.")

    styling_plan = (
        f"为{platform_name}生成高转化服装模特图，商品是{garment}，面向{target_customer}。"
        f"整体采用{visual_style}，重点突出{conversion_focus}。"
    )
    composition_plan = (
        f"使用{model_type}，姿势为{pose}，场景为{scene}，"
        f"构图要求：{composition}。平台方向：{style_note}"
    )

    positive_prompt = (
        f"{cfg.get('prompt_prefix', 'Create a high-converting ecommerce fashion model image.')} "
        f"Garment: {garment}. "
        f"Platform: {platform_name}, aspect ratio {aspect_ratio}. "
        f"Target customer: {target_customer}. "
        f"Model: {model_type}. "
        f"Pose: {pose}. "
        f"Scene: {scene}. "
        f"Visual style: {visual_style}. "
        f"Conversion focus: {conversion_focus}. "
        f"Lighting: {lighting}. "
        f"Composition: {composition}. "
        f"Reference image requirements: {reference_note} "
        f"{cfg.get('prompt_suffix', '')}"
    ).strip()

    return {
        "styling_plan": styling_plan,
        "composition_plan": composition_plan,
        "positive_prompt": positive_prompt,
        "negative_prompt": f"Avoid: {avoid}",
        "warnings": warnings,
    }


__all__ = ["build_fashion_model_prompt", "load_config"]
