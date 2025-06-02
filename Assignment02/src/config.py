#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).parent.parent.absolute()

# Directories
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
REFERENCE_DIR = os.path.join(ASSETS_DIR, "reference")
GENERATED_DIR = os.path.join(ASSETS_DIR, "generated")
VALIDATION_DIR = os.path.join(BASE_DIR, "validation")

# AI model configuration
# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODELS = {
    "dalle2": {
        "name": "dall-e-2",
        "max_resolution": 1024,
        "formats": ["png"]
    },
    "dalle3": {
        "name": "dall-e-3",
        "max_resolution": 1024,
        "formats": ["png"]
    }
}

# Anthropic/Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODELS = {
    "claude3_opus": {
        "name": "claude-3-opus-20240229",
        "max_resolution": 1024,
        "formats": ["png", "jpg"]
    },
    "claude3_sonnet": {
        "name": "claude-3-sonnet-20240229",
        "max_resolution": 1024,
        "formats": ["png", "jpg"]
    }
}

# Midjourney configuration (via API)
MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY", "")

# Layer.ai API configuration for validation
LAYER_API_KEY = os.getenv("LAYER_API_KEY", "")

# Asset type configurations with default parameters
ASSET_TYPES = {
    "character": {
        "default_resolution": "1024x1024",
        "formats": ["png"],
        "prompt_template": "character_template.txt",
    },
    "environment": {
        "default_resolution": "1024x1024",
        "formats": ["png"],
        "prompt_template": "environment_template.txt",
    },
    "item": {
        "default_resolution": "512x512",
        "formats": ["png"],
        "prompt_template": "item_template.txt",
    },
    "ui": {
        "default_resolution": "1024x512",
        "formats": ["png"],
        "prompt_template": "ui_template.txt",
    }
}

# Validation thresholds
VALIDATION_THRESHOLDS = {
    "ssim": {
        "reject": 0.6,
        "acceptable": 0.8,
        "excellent": 0.9
    },
    "color_match": {
        "reject": 0.7,
        "acceptable": 0.9,
        "excellent": 0.95
    },
    "edge_accuracy": {
        "reject": 0.75,
        "acceptable": 0.9,
        "excellent": 0.95
    }
}

# Ensure directories exist
for dir_path in [PROMPTS_DIR, REFERENCE_DIR, GENERATED_DIR, VALIDATION_DIR]:
    os.makedirs(dir_path, exist_ok=True)
