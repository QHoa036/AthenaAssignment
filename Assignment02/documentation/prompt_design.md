# Game Asset Prompt Engineering Methodology

This document outlines our structured approach to designing prompts for generating high-quality game assets with AI models.

## Prompt Structure Framework

### 1. Core Asset Definition

```
{asset_type} for {game_genre} with {style_descriptor} style
```

Example: "Character sprite for 2D platformer game with pixel art style"

### 2. Visual Attribute Layers

```
Visual Attributes:
- Primary colors: {color_palette}
- Lighting: {lighting_condition}
- Perspective: {viewpoint}
- Level of detail: {detail_level}
- Art style: {specific_style_reference}
```

Example:
```
Visual Attributes:
- Primary colors: vibrant blue and orange with dark purple accents
- Lighting: dramatic side lighting with high contrast
- Perspective: front-facing isometric view
- Level of detail: medium-high with clear silhouette
- Art style: similar to Hollow Knight with clean lines
```

### 3. Technical Specifications

```
Technical Specifications:
- Resolution: {width}x{height}
- Format: {file_format}
- Background: {background_type}
- Animation frames: {frame_count} [if applicable]
- Transparency: {yes/no}
```

Example:
```
Technical Specifications:
- Resolution: 512x512
- Format: PNG
- Background: transparent
- Animation frames: static pose
- Transparency: yes
```

### 4. Contextual Reference Integration

```
Reference Integration:
- Reference similar to: {reference_description or URL}
- Key elements to maintain: {specific_elements}
- Avoid these aspects: {elements_to_avoid}
```

Example:
```
Reference Integration:
- Reference similar to: the character design of Hollow Knight's protagonist
- Key elements to maintain: silhouette clarity, limb proportions, mask-like face
- Avoid these aspects: excessive detail in small areas, realistic textures
```

### 5. Aesthetic Direction Guidance

```
Aesthetic Direction:
- Mood: {mood_descriptor}
- Theme: {thematic_elements}
- Cultural influences: {cultural_references}
- Target audience: {audience_demographic}
```

Example:
```
Aesthetic Direction:
- Mood: mysterious and slightly melancholic
- Theme: ancient civilization reclaimed by nature
- Cultural influences: blend of Art Nouveau decorative elements
- Target audience: teen to adult players who appreciate artistic indie games
```

### 6. Technical Optimization Directives

```
Optimization Directives:
- Prioritize: {priority_aspect}
- Ensure compatibility with: {environment}
- Maintain consistency with: {related_assets}
```

Example:
```
Optimization Directives:
- Prioritize: clear readability at smaller scales
- Ensure compatibility with: dark game environments
- Maintain consistency with: previously established character design language
```

## Parameter Optimization

For each AI model, we fine-tune these parameters:

1. **Temperature Setting**: Controls randomness
   - Low (0.2-0.4): More predictable results
   - Medium (0.5-0.7): Balanced creativity
   - High (0.8-1.0): Maximum variation

2. **Detail Level**: Adjust based on asset complexity
   - Low: Iconographic, symbolic representations
   - Medium: Standard game assets with clear details
   - High: Showcase pieces with intricate details

3. **Style Emphasis**: Weight between different style aspects
   - Technical specifications (higher weight for technical assets)
   - Artistic expression (higher weight for key art)
   - Functional design (higher weight for interactive elements)

4. **Negative Prompting**: Elements to explicitly avoid
   - Technical issues: blurriness, artifacts, inconsistent lighting
   - Design problems: cluttered composition, poor readability
   - Style mismatches: inappropriate art style for the game genre

## Model-Specific Considerations

### Stable Diffusion

- Strengths: Detailed textures, style consistency
- Optimization: Emphasize composition keywords, use LoRA models for style

### Midjourney

- Strengths: Aesthetic coherence, creative interpretation
- Optimization: Use version parameters, stylization settings

### DALL-E

- Strengths: Following specific instructions, layout accuracy
- Optimization: Clear structural descriptions, specific placement instructions

### ComfyUI/Automatic1111

- Strengths: Technical control, consistent results with saved settings
- Optimization: Develop and save specific workflows for each asset type
