#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Module tạo tài sản game bằng AI
# Module này sử dụng các API của OpenAI, Claude và Midjourney để tạo tài sản game dựa trên prompt

import os
import sys
import uuid
import requests
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime
import base64

import config
from prompt_generator import PromptGenerator

class AssetGenerator:
    """Generator for AI-based game assets"""
    # Lớp tạo tài sản game bằng AI
    # Hỗ trợ nhiều mô hình AI khác nhau (OpenAI, Claude, Midjourney)

    def __init__(self, api_key: Optional[str] = None, model_type: str = "openai"):
        """
        Initialize asset generator

        Args:
            api_key: API key for the AI model service
            model_type: Type of AI model to use (openai, anthropic, midjourney)
        """
        # Khởi tạo tài sản bằng cách xác định loại mô hình AI và API key
        self.model_type = model_type.lower()
        self.api_key = api_key or self._get_api_key()
        self.prompt_generator = PromptGenerator()

        # Ensure output directories exist
        # Đảm bảo thư mục đầu ra tồn tại
        os.makedirs(config.GENERATED_DIR, exist_ok=True)

    def _get_api_key(self) -> str:
        """Get API key based on model type"""
        # Lấy API key dựa vào loại mô hình AI
        if self.model_type == "openai":
            return config.OPENAI_API_KEY
        elif self.model_type == "anthropic" or self.model_type == "claude":
            return config.ANTHROPIC_API_KEY
        elif self.model_type == "midjourney":
            return config.MIDJOURNEY_API_KEY
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def generate_asset(self,
                      asset_type: str,
                      params: Dict[str, str],
                      model: Optional[str] = None,
                      output_path: Optional[str] = None) -> str:
        # Phương thức chính để tạo tài sản game
        # Sử dụng prompt_generator để tạo prompt và gọi phương thức tương ứng với mô hình AI
        """
        Generate asset using AI model

        Args:
            asset_type: Type of game asset (character, environment, item, ui)
            params: Dictionary of parameters for prompt generation
            model: Specific model name to use (e.g., "dalle3")
            output_path: Path to save generated asset

        Returns:
            Path to the generated asset
        """
        # Generate prompt
        prompt = self.prompt_generator.generate_prompt(asset_type, params)

        # Generate unique filename if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{asset_type}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
            output_path = os.path.join(config.GENERATED_DIR, output_filename)

        # Generate asset using appropriate AI model
        if self.model_type == "openai":
            return self._generate_with_openai(prompt, params, model, output_path)
        elif self.model_type == "anthropic" or self.model_type == "claude":
            return self._generate_with_claude(prompt, params, model, output_path)
        elif self.model_type == "midjourney":
            return self._generate_with_midjourney(prompt, params, output_path)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def _generate_with_openai(self,
                             prompt: str,
                             params: Dict[str, str],
                             model: Optional[str] = None,
                             output_path: str = None) -> str:
        """Generate asset using OpenAI's DALL-E models"""
        # Tạo tài sản bằng API của OpenAI DALL-E
        # Hỗ trợ các mô hình DALL-E 2 và DALL-E 3
        try:
            import openai

            # Configure API key
            openai.api_key = self.api_key

            # Xác định mô hình sẽ sử dụng
            model_name = model or "dall-e-3"
            if model in config.OPENAI_MODELS:
                model_name = config.OPENAI_MODELS[model]["name"]

            # Lấy độ phân giải từ tham số
            width = int(params.get("width", 1024))
            height = int(params.get("height", 1024))

            # Đảm bảo kích thước hình ảnh phù hợp với mô hình DALL-E
            valid_sizes = [(1024, 1024), (1024, 1792), (1792, 1024)]
            if (width, height) not in valid_sizes:
                print(f"Warning: Invalid dimensions {width}x{height} for DALL-E. Using default 1024x1024")
                width, height = 1024, 1024

            # Tạo hình ảnh bằng API của OpenAI
            response = openai.images.generate(
                model=model_name,
                prompt=prompt,
                size=f"{width}x{height}",
                quality="standard",
                n=1,
                response_format="b64_json"
            )

            # Lưu hình ảnh vào file
            if response.data:
                image_data = base64.b64decode(response.data[0].b64_json)

                # Tạo thư mục cha nếu chưa tồn tại
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, "wb") as f:
                    f.write(image_data)

                print(f"Generated asset saved to: {output_path}")
                return output_path
            else:
                raise Exception("No image data returned from API")

        except Exception as e:
            print(f"Error generating asset with OpenAI: {str(e)}")
            raise

    def _generate_with_claude(self,
                            prompt: str,
                            params: Dict[str, str],
                            model: Optional[str] = None,
                            output_path: str = None) -> str:
        """Generate asset using Anthropic's Claude models"""
        # Tạo tài sản bằng API của Anthropic Claude
        # Claude có thể tạo hình ảnh qua chức năng Messages API
        try:
            import anthropic

            # Configure API key
            client = anthropic.Anthropic(api_key=self.api_key)

            # Xác định mô hình Claude sẽ sử dụng
            model_name = "claude-3-opus-20240229"  # Mô hình mặc định
            if model in config.CLAUDE_MODELS:
                model_name = config.CLAUDE_MODELS[model]["name"]
            elif model:
                model_name = model

            # Gọi API của Claude để tạo hình ảnh
            message = client.messages.create(
                model=model_name,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Generate an image based on this description: {prompt}"
                            }
                        ]
                    }
                ],
                stream=False
            )

            # Trích xuất và lưu hình ảnh từ phản hồi
            for content in message.content:
                if content.type == "image":
                    image_data = base64.b64decode(content.source.data)

                    # Tạo thư mục cha nếu chưa tồn tại
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    print(f"Generated asset saved to: {output_path}")
                    return output_path

            raise Exception("No image generated in Claude response")

        except Exception as e:
            print(f"Error generating asset with Claude: {str(e)}")
            raise

    def _generate_with_midjourney(self,
                                prompt: str,
                                params: Dict[str, str],
                                output_path: str = None) -> str:
        """
        Generate asset using Midjourney API
        This is a placeholder implementation since there is no official Midjourney API
        """
        # Tạo tài sản bằng Midjourney (chức năng giả định)
        # Đây chỉ là phần giữ chỗ vì Midjourney không có API chính thức
        try:
            # NOTE: This is a placeholder implementation since Midjourney doesn't have an official API
            # In a real implementation, you might use a third-party API service that provides access to Midjourney

            print("Warning: Midjourney API implementation is a placeholder")

            # For demonstration purposes, we'll create a simple placeholder image
            # In a real implementation, this would make an API call to a service that provides Midjourney access

            # Create a placeholder text file with the prompt
            with open(output_path.replace('.png', '.txt'), "w") as f:
                f.write(f"Midjourney Prompt:\n\n{prompt}")

            print(f"Midjourney integration placeholder created at: {output_path.replace('.png', '.txt')}")
            print("Note: In a production environment, integrate with a real Midjourney API service")

            return output_path.replace('.png', '.txt')

        except Exception as e:
            print(f"Error with Midjourney placeholder: {str(e)}")
            raise

    def generate_variations(self,
                           base_asset: str,
                           num_variations: int = 3,
                           variation_params: Optional[List[Dict[str, str]]] = None) -> List[str]:
        """
        Generate variations of an existing asset

        Args:
            base_asset: Path to base asset
            num_variations: Number of variations to generate
            variation_params: Optional list of parameters for each variation

        Returns:
            List of paths to generated variations
        """
        # Tạo các biến thể từ một tài sản cơ bản
        # Hữu ích để tạo nhiều phiên bản khác nhau của cùng một tài sản
        # Implementation depends on the specific AI model being used
        # This would be implemented separately for each model type
        raise NotImplementedError("Asset variation generation not yet implemented")


if __name__ == "__main__":
    print("Asset Generator Tool")
    print("====================")
    # Phần mã chạy trực tiếp khi gọi module này như một script

    # Kiểm tra biến môi trường cho API keys
    if not config.OPENAI_API_KEY and not config.ANTHROPIC_API_KEY:
        print("Error: No API keys found in environment variables.")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables.")
        sys.exit(1)

    # Determine which model to use based on available API keys
    model_type = "openai" if config.OPENAI_API_KEY else "anthropic"
    print(f"Using {model_type} API for asset generation")

    # Create asset generator
    generator = AssetGenerator(model_type=model_type)

    # Example character asset parameters
    character_params = {
        "asset_type": "character",
        "game_genre": "fantasy RPG",
        "style_descriptor": "pixel art",
        "color_palette": "vibrant blues and purples with gold accents",
        "viewpoint": "front-facing isometric",
        "specific_style_reference": "similar to Final Fantasy VI characters",
        "width": "1024",
        "height": "1024"
    }

    # Generate the asset
    print("Generating character asset...")
    output_path = generator.generate_asset("character", character_params)
    print(f"Asset generated: {output_path}")
