#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo nội dung bằng AI (OpenAI/Claude)
Module for generating content using AI (OpenAI/Claude)
"""

import os
import logging
import time
import requests
from pathlib import Path
import base64
import json
import tempfile
import anthropic
import openai

class AIGenerator:
    """
    Lớp để tạo nội dung sử dụng các mô hình AI
    Class to generate content using AI models
    """
    
    def __init__(self, api_key):
        """
        Khởi tạo đối tượng AIGenerator
        Initialize AIGenerator object
        
        Args:
            api_key (str): API key cho dịch vụ AI
                          API key for AI service
        """
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.openai_client = openai.OpenAI(api_key=api_key)
        self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        
        # Tạo thư mục tạm để lưu các file được tạo ra
        # Create temp directory to store generated files
        self.temp_dir = tempfile.mkdtemp()
        self.logger.info(f"Sử dụng thư mục tạm cho tệp đầu ra: {self.temp_dir}")
        self.logger.info(f"Using temp directory for output files: {self.temp_dir}")
    
    def generate(self, description, reference_url=None, output_format="png", model="openai"):
        """
        Tạo nội dung dựa trên mô tả và URL tham chiếu
        Generate content based on description and reference URL
        
        Args:
            description (str): Mô tả nội dung cần tạo
                              Description of content to generate
            reference_url (str): URL của tài sản tham chiếu (tùy chọn)
                               URL of reference asset (optional)
            output_format (str): Định dạng đầu ra (png, jpg, gif, mp3)
                               Output format (png, jpg, gif, mp3)
            model (str): Mô hình AI sử dụng (openai, claude)
                        AI model to use (openai, claude)
        
        Returns:
            str: Đường dẫn đến file đã tạo hoặc None nếu có lỗi
                Path to generated file or None if error
        """
        try:
            output_format = output_format.lower()
            
            if output_format not in ["png", "jpg", "gif", "mp3"]:
                raise ValueError(f"Định dạng không được hỗ trợ: {output_format}")
                raise ValueError(f"Unsupported format: {output_format}")
            
            if output_format == "mp3":
                return self._generate_audio(description, model)
            else:
                return self._generate_image(description, reference_url, output_format, model)
                
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo nội dung: {e}")
            self.logger.error(f"Error generating content: {e}")
            return None

    def _generate_image(self, description, reference_url, output_format, model):
        """
        Tạo hình ảnh bằng AI
        Generate image using AI
        
        Args:
            description (str): Mô tả hình ảnh
                              Image description
            reference_url (str): URL của hình ảnh tham chiếu (tùy chọn)
                               URL of reference image (optional)
            output_format (str): Định dạng đầu ra (png, jpg, gif)
                               Output format (png, jpg, gif)
            model (str): Mô hình AI sử dụng (openai, claude)
                        AI model to use (openai, claude)
        
        Returns:
            str: Đường dẫn đến file hình ảnh đã tạo
                Path to generated image file
        """
        # Tạo đường dẫn đầu ra
        # Create output path
        timestamp = int(time.time())
        output_filename = f"image_{timestamp}.{output_format}"
        output_path = os.path.join(self.temp_dir, output_filename)
        
        self.logger.info(f"Tạo hình ảnh với mô hình {model}: {description}")
        self.logger.info(f"Generating image with model {model}: {description}")
        
        # Tham chiếu hình ảnh nếu có
        # Reference image if available
        reference_image = None
        if reference_url:
            try:
                response = requests.get(reference_url)
                if response.status_code == 200:
                    temp_ref_file = os.path.join(self.temp_dir, f"reference_{timestamp}")
                    with open(temp_ref_file, "wb") as f:
                        f.write(response.content)
                    reference_image = temp_ref_file
                    self.logger.info("Đã tải hình ảnh tham chiếu")
                    self.logger.info("Reference image downloaded")
            except Exception as e:
                self.logger.warning(f"Không thể tải hình ảnh tham chiếu: {e}")
                self.logger.warning(f"Could not download reference image: {e}")
        
        if model.lower() == "openai":
            try:
                # Tạo hình ảnh bằng OpenAI DALL-E
                # Generate image using OpenAI DALL-E
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=description,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                # Tải hình ảnh từ URL trong kết quả
                # Download image from URL in response
                image_url = response.data[0].url
                image_response = requests.get(image_url)
                
                with open(output_path, "wb") as f:
                    f.write(image_response.content)
                
                return output_path
                
            except Exception as e:
                self.logger.error(f"Lỗi khi tạo hình ảnh với OpenAI: {e}")
                self.logger.error(f"Error generating image with OpenAI: {e}")
                return None
                
        elif model.lower() == "claude":
            try:
                # Tạo hình ảnh bằng Claude (giả định API hình ảnh)
                # Generate image using Claude (assuming image API)
                
                # Lưu ý: Claude hiện tại chưa có API tạo hình ảnh chính thức
                # Note: Claude currently doesn't have an official image generation API
                # Đây là mã mẫu sẽ cần được cập nhật khi Claude có API hình ảnh
                # This is sample code that would need to be updated when Claude releases image API
                
                self.logger.warning("Tạo hình ảnh với Claude chưa được hỗ trợ chính thức, sẽ sử dụng OpenAI làm dự phòng")
                self.logger.warning("Image generation with Claude not officially supported, will use OpenAI as fallback")
                
                # Fallback sang OpenAI
                # Fallback to OpenAI
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=description,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                image_response = requests.get(image_url)
                
                with open(output_path, "wb") as f:
                    f.write(image_response.content)
                
                return output_path
                
            except Exception as e:
                self.logger.error(f"Lỗi khi tạo hình ảnh với Claude: {e}")
                self.logger.error(f"Error generating image with Claude: {e}")
                return None
        else:
            self.logger.error(f"Mô hình không được hỗ trợ: {model}")
            self.logger.error(f"Unsupported model: {model}")
            return None

    def _generate_audio(self, description, model):
        """
        Tạo âm thanh bằng AI
        Generate audio using AI
        
        Args:
            description (str): Mô tả âm thanh hoặc văn bản để chuyển thành giọng nói
                              Audio description or text to convert to speech
            model (str): Mô hình AI sử dụng (openai, claude)
                        AI model to use (openai, claude)
        
        Returns:
            str: Đường dẫn đến file âm thanh đã tạo
                Path to generated audio file
        """
        # Tạo đường dẫn đầu ra
        # Create output path
        timestamp = int(time.time())
        output_filename = f"audio_{timestamp}.mp3"
        output_path = os.path.join(self.temp_dir, output_filename)
        
        self.logger.info(f"Tạo âm thanh với mô hình {model}: {description[:50]}...")
        self.logger.info(f"Generating audio with model {model}: {description[:50]}...")
        
        if model.lower() == "openai":
            try:
                # Tạo âm thanh bằng OpenAI TTS
                # Generate audio using OpenAI TTS
                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=description
                )
                
                response.stream_to_file(output_path)
                return output_path
                
            except Exception as e:
                self.logger.error(f"Lỗi khi tạo âm thanh với OpenAI: {e}")
                self.logger.error(f"Error generating audio with OpenAI: {e}")
                return None
                
        elif model.lower() == "claude":
            try:
                # Claude hiện tại không có API tạo âm thanh, sử dụng OpenAI làm dự phòng
                # Claude currently doesn't have audio generation API, use OpenAI as fallback
                self.logger.warning("Tạo âm thanh với Claude không được hỗ trợ, sẽ sử dụng OpenAI làm dự phòng")
                self.logger.warning("Audio generation with Claude not supported, will use OpenAI as fallback")
                
                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=description
                )
                
                response.stream_to_file(output_path)
                return output_path
                
            except Exception as e:
                self.logger.error(f"Lỗi khi tạo âm thanh với Claude: {e}")
                self.logger.error(f"Error generating audio with Claude: {e}")
                return None
        else:
            self.logger.error(f"Mô hình không được hỗ trợ: {model}")
            self.logger.error(f"Unsupported model: {model}")
            return None
