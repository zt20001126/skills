---
name: rei-kawakubo-inspired
description: Generate fashion image prompts and garment concepts inspired by avant-garde Japanese deconstruction, sculptural silhouettes, anti-fashion runway styling, asymmetry, body distortion, and monochrome black-white-red palettes. Use when a product user selects this designer-inspired fashion style skill to create clothing images, editorial runway looks, conceptual garments, or image-model prompts.
---

# Rei Kawakubo Inspired Fashion Image Skill

Use this skill to turn a user's fashion image request into a product-ready image generation prompt inspired by avant-garde deconstruction and conceptual runway fashion.

## Product Use

When this skill is selected in the product:

1. Read `style_config.json`.
2. Merge the user's request into the fields from `style_config.json`.
3. Render `prompt_template.md` with the merged values.
4. Send the final `positive_prompt` and `negative_prompt` to the image model.

Do not describe the output as an exact copy of Rei Kawakubo or Comme des Garcons. Use inspiration-based language built from the style attributes instead.

## Style Direction

Prioritize:

- Avant-garde deconstruction
- Asymmetrical garment construction
- Sculptural and distorted body volume
- Oversized, irregular, layered silhouettes
- Conceptual anti-fashion runway presentation
- Black, white, grey, and controlled red accents
- Editorial or museum-grade fashion photography

Avoid:

- Cute, sweet, pastel, or romantic styling
- Mainstream minimalism
- Basic slim-fit commercial clothing
- Conventional elegance or body-flattering fast fashion
- Literal brand logos, trademarks, or direct replicas

## Prompt Requirements

The final prompt should include:

- User garment request
- Designer-inspired visual direction
- Silhouette and construction
- Color palette
- Materials and surface texture
- Runway/editorial presentation
- Camera, lighting, and image quality notes
- Negative prompt terms

Output in English for image models unless the product explicitly requires another language.
