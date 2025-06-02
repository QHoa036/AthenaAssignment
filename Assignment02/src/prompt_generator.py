#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import config

class PromptGenerator:
    def __init__(self):
        self.templates_dir = config.PROMPTS_DIR
        self.load_templates()
        
    def load_templates(self):
        self.templates = {}
        template_files = Path(self.templates_dir).glob("*.txt")
        
        for template_file in template_files:
            template_name = template_file.stem
            with open(template_file, "r") as f:
                self.templates[template_name] = f.read()
        
        # Create default templates if none exist
        if not self.templates:
            self.create_default_templates()
    
    def create_default_templates(self):
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Character template
        character_template = """
{asset_type} for {game_genre} with {style_descriptor} style

Visual Attributes:
- Primary colors: {color_palette}
- Lighting: {lighting_condition}
- Perspective: {viewpoint}
- Level of detail: {detail_level}
- Art style: {specific_style_reference}

Technical Specifications:
- Resolution: {width}x{height}
- Format: {file_format}
- Background: {background_type}
- Animation frames: {frame_count}
- Transparency: {transparency}

Reference Integration:
- Reference similar to: {reference_description}
- Key elements to maintain: {specific_elements}
- Avoid these aspects: {elements_to_avoid}

Aesthetic Direction:
- Mood: {mood_descriptor}
- Theme: {thematic_elements}
- Cultural influences: {cultural_references}
- Target audience: {audience_demographic}

Optimization Directives:
- Prioritize: {priority_aspect}
- Ensure compatibility with: {environment}
- Maintain consistency with: {related_assets}

DO NOT include:
{negative_prompt}
"""
        with open(os.path.join(self.templates_dir, "character_template.txt"), "w") as f:
            f.write(character_template)
        self.templates["character_template"] = character_template
        
        # Similar templates for other asset types
        environment_template = character_template.replace("{asset_type}", "Environment asset")
        with open(os.path.join(self.templates_dir, "environment_template.txt"), "w") as f:
            f.write(environment_template)
        self.templates["environment_template"] = environment_template
        
        item_template = character_template.replace("{asset_type}", "Item asset")
        with open(os.path.join(self.templates_dir, "item_template.txt"), "w") as f:
            f.write(item_template)
        self.templates["item_template"] = item_template
        
        ui_template = character_template.replace("{asset_type}", "UI element")
        with open(os.path.join(self.templates_dir, "ui_template.txt"), "w") as f:
            f.write(ui_template)
        self.templates["ui_template"] = ui_template
    
    def generate_prompt(self, 
                        asset_type: str,
                        asset_params: Dict[str, str],
                        template_name: Optional[str] = None) -> str:
        """
        Generate a prompt based on template and parameters
        
        Args:
            asset_type: Type of game asset (character, environment, item, ui)
            asset_params: Dictionary of parameters to fill in the template
            template_name: Optional template name override
            
        Returns:
            Formatted prompt string
        """
        if asset_type not in config.ASSET_TYPES:
            raise ValueError(f"Unsupported asset type: {asset_type}")
        
        if not template_name:
            template_name = config.ASSET_TYPES[asset_type].get("prompt_template", f"{asset_type}_template")
        
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
            
        template = self.templates[template_name]
        
        # Create default parameters for any missing values
        default_params = {
            "asset_type": asset_type.capitalize(),
            "game_genre": "generic game",
            "style_descriptor": "digital",
            "color_palette": "game-appropriate",
            "lighting_condition": "neutral lighting",
            "viewpoint": "front view",
            "detail_level": "medium",
            "specific_style_reference": "standard game art",
            "width": config.ASSET_TYPES[asset_type]["default_resolution"].split("x")[0],
            "height": config.ASSET_TYPES[asset_type]["default_resolution"].split("x")[1],
            "file_format": config.ASSET_TYPES[asset_type]["formats"][0],
            "background_type": "transparent",
            "frame_count": "single static frame",
            "transparency": "yes",
            "reference_description": "standard game asset references",
            "specific_elements": "core visual elements",
            "elements_to_avoid": "non-game-appropriate elements",
            "mood_descriptor": "neutral",
            "thematic_elements": "game-appropriate themes",
            "cultural_references": "generic",
            "audience_demographic": "general gaming audience",
            "priority_aspect": "visual clarity",
            "environment": "general game environment",
            "related_assets": "existing game assets",
            "negative_prompt": "- Poor composition or unclear silhouette\n- Inappropriate textures or details\n- Text or writing unless specifically requested"
        }
        
        # Merge provided parameters with defaults
        params = {**default_params, **asset_params}
        
        # Format the template with the parameters
        try:
            return template.format(**params)
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise ValueError(f"Missing required parameter in template: {missing_key}")
    
    def save_prompt(self, prompt: str, filename: str) -> str:
        """
        Save generated prompt to file
        
        Args:
            prompt: Generated prompt text
            filename: Name to save the prompt as
            
        Returns:
            Path to saved prompt file
        """
        if not filename.endswith(".txt"):
            filename = f"{filename}.txt"
        
        prompt_path = os.path.join(self.templates_dir, filename)
        with open(prompt_path, "w") as f:
            f.write(prompt)
        
        return prompt_path
    
    def load_prompt_from_json(self, json_file: str) -> str:
        """
        Load prompt parameters from JSON file and generate prompt
        
        Args:
            json_file: Path to JSON file with prompt parameters
            
        Returns:
            Generated prompt
        """
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file not found: {json_file}")
            
        with open(json_file, "r") as f:
            data = json.load(f)
            
        if "asset_type" not in data:
            raise ValueError("JSON must contain 'asset_type' field")
            
        asset_type = data.pop("asset_type")
        template_name = data.pop("template_name", None)
        
        return self.generate_prompt(asset_type, data, template_name)
    
    def generate_variations(self, 
                           base_params: Dict[str, str],
                           variation_params: List[Dict[str, str]]) -> List[str]:
        """
        Generate variations of a prompt by modifying specific parameters
        
        Args:
            base_params: Base parameters dictionary
            variation_params: List of parameter dictionaries for variations
            
        Returns:
            List of generated prompt variations
        """
        if "asset_type" not in base_params:
            raise ValueError("base_params must contain 'asset_type' field")
            
        asset_type = base_params.get("asset_type")
        template_name = base_params.get("template_name")
        
        prompts = []
        for variation in variation_params:
            # Merge base parameters with variation parameters
            params = {**base_params, **variation}
            # Remove template_name from parameters if it exists
            if "template_name" in params:
                template_name = params.pop("template_name")
            
            prompt = self.generate_prompt(asset_type, params, template_name)
            prompts.append(prompt)
            
        return prompts


if __name__ == "__main__":
    # Example usage
    generator = PromptGenerator()
    
    character_params = {
        "asset_type": "character",
        "game_genre": "fantasy RPG",
        "style_descriptor": "pixel art",
        "color_palette": "vibrant blues and purples with gold accents",
        "viewpoint": "front-facing isometric",
        "specific_style_reference": "similar to Final Fantasy VI characters",
        "width": "32",
        "height": "64"
    }
    
    prompt = generator.generate_prompt("character", character_params)
    print(prompt)
    
    # Save the prompt
    generator.save_prompt(prompt, "fantasy_character_prompt.txt")
