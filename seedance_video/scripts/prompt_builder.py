"""Build Seedance video prompts from skill configuration.

This module is API-agnostic. It reads style_config.json, merges user
parameters, adds lightweight validation warnings, and returns prompt text that
a backend can pass to Seedance after mapping parameters to the official API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_DIR / "style_config.json"


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load the Seedance video skill config."""
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


def _pick_platform(
    config: Mapping[str, Any],
    platform: str | None,
    warnings: list[str],
) -> tuple[str, Mapping[str, Any]]:
    platforms = config.get("platforms", {})
    default_platform = config.get("default_platform", "douyin")
    platform_key = platform or default_platform
    if platform_key not in platforms:
        warnings.append(f"Unknown platform '{platform_key}', fallback to '{default_platform}'.")
        platform_key = default_platform
    return platform_key, platforms.get(platform_key, {})


def _pick_generation_mode(
    config: Mapping[str, Any],
    requested_mode: str | None,
    user_request: Mapping[str, Any],
    warnings: list[str],
) -> str:
    modes = set(config.get("generation_modes", []))
    default_mode = config.get("default_generation_mode", "text_to_video")
    mode = requested_mode or default_mode
    if user_request.get("reference_image"):
        mode = "image_to_video"
    if user_request.get("shots") or user_request.get("shot_count"):
        mode = "shot_list"
    if mode not in modes:
        warnings.append(f"Unknown generation_mode '{mode}', fallback to '{default_mode}'.")
        mode = default_mode
    return mode


def build_shot_structure(
    duration: str,
    subject_focus: str,
    generation_mode: str = "text_to_video",
    shot_count: int | None = None,
) -> str:
    """Create a compact shot structure suitable for a video prompt."""
    if generation_mode == "shot_list":
        count = shot_count or 3
        return (
            f"Split the video into {count} coherent shots across {duration}. "
            f"Each shot should keep the same subject, scene direction, lighting, and visual style, "
            f"while varying framing, action, and camera movement. Focus on {subject_focus}."
        )
    return (
        f"Opening seconds establish the subject clearly; "
        f"middle section shows motion and {subject_focus}; "
        f"final seconds hold a polished hero frame with stable composition for {duration}."
    )


def _build_parameters(config: Mapping[str, Any], user_request: Mapping[str, Any], platform_info: Mapping[str, Any]) -> dict[str, str]:
    suggestions = dict(config.get("parameter_suggestions", {}))
    return {
        "generation_mode": _as_text(user_request.get("generation_mode") or config.get("default_generation_mode")),
        "duration": _as_text(user_request.get("duration") or platform_info.get("recommended_duration") or config.get("default_duration")),
        "aspect_ratio": _as_text(user_request.get("aspect_ratio") or platform_info.get("aspect_ratio") or config.get("default_aspect_ratio")),
        "resolution": _as_text(user_request.get("resolution") or suggestions.get("resolution")),
        "fps": _as_text(user_request.get("fps") or suggestions.get("fps")),
        "motion_strength": _as_text(user_request.get("motion_strength") or suggestions.get("motion_strength")),
        "camera_stability": _as_text(user_request.get("camera_stability") or suggestions.get("camera_stability")),
        "note": _as_text(suggestions.get("note")),
    }


def build_seedance_prompt(
    user_request: Mapping[str, Any],
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a structured Seedance video prompt.

    Args:
        user_request: Creative requirements from the user or backend.
        config: Optional config dictionary. If omitted, style_config.json is loaded.

    Returns:
        Dictionary with creative_plan, shot_structure, parameters,
        positive_prompt, negative_prompt, and warnings.
    """
    cfg = dict(config or load_config())
    warnings: list[str] = []

    platform_key, platform_info = _pick_platform(cfg, _as_text(user_request.get("platform")) or None, warnings)
    generation_mode = _pick_generation_mode(
        cfg,
        _as_text(user_request.get("generation_mode")) or None,
        user_request,
        warnings,
    )

    subject = _as_text(
        user_request.get("subject")
        or user_request.get("product")
        or user_request.get("user_input")
        or "main subject"
    )
    if subject == "main subject":
        warnings.append("Missing subject/product; using generic 'main subject'.")

    video_type = _as_text(user_request.get("video_type") or cfg.get("video_types", ["商品展示视频"])[0])
    duration = _as_text(user_request.get("duration") or platform_info.get("recommended_duration") or cfg.get("default_duration"))
    aspect_ratio = _as_text(user_request.get("aspect_ratio") or platform_info.get("aspect_ratio") or cfg.get("default_aspect_ratio"))
    scene = _as_text(user_request.get("scene") or cfg.get("default_scene"))
    visual_style = _as_text(user_request.get("visual_style") or cfg.get("default_visual_style"))
    camera_movement = _as_text(user_request.get("camera_movement") or cfg.get("default_camera_movement"))
    subject_focus = _as_text(
        user_request.get("subject_focus")
        or user_request.get("garment_focus")
        or cfg.get("default_subject_focus")
    )
    action = _as_text(user_request.get("action") or user_request.get("model_action") or cfg.get("default_action"))
    lighting = _as_text(user_request.get("lighting") or cfg.get("default_lighting"))
    avoid = _as_text(user_request.get("avoid") or cfg.get("avoid"))
    shot_count = user_request.get("shot_count")
    shot_count_int = int(shot_count) if str(shot_count).isdigit() else None
    shot_structure = _as_text(user_request.get("shot_structure")) or build_shot_structure(
        duration,
        subject_focus,
        generation_mode,
        shot_count_int,
    )

    platform_name = _as_text(platform_info.get("name") or platform_key)
    style_note = _as_text(platform_info.get("style_note"))
    image_note = ""
    if generation_mode == "image_to_video":
        image_note = cfg.get("image_to_video_note", "")
        if not user_request.get("reference_image"):
            warnings.append("image_to_video mode selected but reference_image is missing.")

    parameters = _build_parameters(cfg, user_request, platform_info)
    parameters["generation_mode"] = generation_mode

    creative_plan = (
        f"为{platform_name}生成{duration}视频，主体是{subject}。"
        f"画面采用{visual_style}，场景为{scene}，重点展示{subject_focus}。"
    )

    positive_prompt = (
        f"{cfg.get('prompt_prefix', 'Create a high-quality Seedance video.')} "
        f"Generation mode: {generation_mode}. "
        f"Subject: {subject}. "
        f"Video type: {video_type}. "
        f"Platform: {platform_name}, aspect ratio {aspect_ratio}, duration {duration}. "
        f"Platform direction: {style_note}. "
        f"Scene: {scene}. "
        f"Visual style: {visual_style}. "
        f"Action: {action}. "
        f"Camera movement: {camera_movement}. "
        f"Subject focus: {subject_focus}. "
        f"Lighting: {lighting}. "
        f"Shot structure: {shot_structure}. "
        f"Continuity requirements: keep the subject identity, color, material, scale, and scene lighting consistent throughout the video. "
        f"{image_note} "
        f"{cfg.get('prompt_suffix', '')}"
    ).strip()

    return {
        "creative_plan": creative_plan,
        "shot_structure": shot_structure,
        "parameters": parameters,
        "positive_prompt": positive_prompt,
        "negative_prompt": f"Avoid: {avoid}",
        "warnings": warnings,
    }


__all__ = ["build_seedance_prompt", "load_config", "build_shot_structure"]
