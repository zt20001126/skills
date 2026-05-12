---
name: yohji-yamamoto-inspired
description: Generate fashion image prompts and garment concepts inspired by Yohji Yamamoto's poetic Japanese avant-garde tailoring, black draped silhouettes, oversized proportions, asymmetry, deconstructed suiting, and quiet monochrome runway mood. Use when a product user selects this designer-inspired fashion style skill to create clothing images, editorial looks, conceptual garments, or image-model prompts.
---

# Yohji Yamamoto Inspired Fashion Image Skill

Use this skill to turn a user's fashion image request into a product-ready image generation prompt inspired by poetic Japanese avant-garde tailoring and dark, fluid runway silhouettes.

## Product Use

When this skill is selected in the product:

1. Read `style_config.json`.
2. Merge the user's request into the fields from `style_config.json`.
3. Render `prompt_template.md` with the merged values.
4. Send the final `positive_prompt` and `negative_prompt` to the image model.

Do not describe the output as an exact copy of Yohji Yamamoto or any brand garment. Use inspiration-based language built from the style attributes instead.

## Style Direction

Prioritize:

- Poetic Japanese avant-garde tailoring
- Loose, draped, oversized silhouettes
- Black-centered monochrome palette
- Soft deconstruction and asymmetric balance
- Long coats, layered suiting, wide trousers, and flowing shirts
- Quiet, melancholic, intellectual runway mood
- Natural fabric movement and negative space around the body

Avoid:

- Bright decorative color stories
- Cute, sweet, glossy, or overly youthful styling
- Tight bodycon silhouettes
- Sportswear-heavy or streetwear-logo styling
- Conventional business suits
- Literal brand logos, trademarks, or direct replicas

## Prompt Requirements

The final prompt should include:

- User garment request
- Designer-inspired visual direction
- Silhouette and tailoring language
- Color palette
- Materials, fabric weight, and drape
- Runway/editorial presentation
- Camera, lighting, and image quality notes
- Negative prompt terms

Output in English for image models unless the product explicitly requires another language.
