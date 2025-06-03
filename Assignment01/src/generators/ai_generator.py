#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo nội dung bằng AI (OpenAI/Claude)
"""

import os
import logging
import time
import requests
import tempfile
import anthropic
import openai

class AIGenerator:
    """
    Lớp để tạo nội dung sử dụng các mô hình AI
    """

    def __init__(self, api_key, service=None):
        """
        Khởi tạo đối tượng AIGenerator

        Args:
            api_key (str): API key cho dịch vụ AI
            service (str, optional): Dịch vụ AI để sử dụng ('openai' hoặc 'anthropic')
        """
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.service = service or 'openai'  # Mặc định là OpenAI nếu không chỉ định

        # Initialize clients based on available API keys
        if self.service == 'openai':
            if not api_key:
                self.logger.error("Không có khóa API OpenAI nào được cung cấp")
                raise ValueError("Khóa API OpenAI là bắt buộc")
            self.openai_client = openai.OpenAI(api_key=api_key)
            self.anthropic_client = None  # Không khởi tạo Anthropic nếu sử dụng OpenAI
        elif self.service == 'anthropic':
            if not api_key:
                self.logger.error("Không có khóa API Anthropic nào được cung cấp")
                raise ValueError("Khóa API Anthropic là bắt buộc")
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
            self.openai_client = None  # Không khởi tạo OpenAI nếu sử dụng Anthropic
        else:
            # Khởi tạo cả hai nếu dịch vụ không được chỉ định
            if not api_key:
                self.logger.error("Không có khóa API nào được cung cấp")
                raise ValueError("Cần có khóa API")
            self.openai_client = openai.OpenAI(api_key=api_key)
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)

        # Tạo thư mục tạm để lưu các file được tạo ra
        self.temp_dir = tempfile.mkdtemp()
        self.logger.info(f"Sử dụng thư mục tạm cho tệp đầu ra: {self.temp_dir}")

    def generate(self, description, reference_url=None, output_format="png", model="openai"):
        """
        Tạo nội dung dựa trên mô tả và URL tham chiếu

        Args:
            description (str): Mô tả nội dung cần tạo
            reference_url (str): URL của tài sản tham chiếu (tùy chọn)
            output_format (str): Định dạng đầu ra (png, jpg, gif, mp3)
            model (str): Mô hình AI sử dụng (openai, claude)

        Returns:
            str: Đường dẫn đến file đã tạo hoặc None nếu có lỗi
        """
        try:
            output_format = output_format.lower()

            if output_format not in ["png", "jpg", "gif", "mp3"]:
                raise ValueError(f"Định dạng không được hỗ trợ: {output_format}")

            if output_format == "mp3":
                return self._generate_audio(description, model)
            else:
                return self._generate_image(description, reference_url, output_format, model)

        except Exception as e:
            self.logger.error(f"Lỗi khi tạo nội dung: {e}")
            return None

    def _generate_image(self, description, reference_url, output_format, model):
        """
        Tạo hình ảnh bằng AI

        Args:
            description (str): Mô tả hình ảnh
            reference_url (str): URL của hình ảnh tham chiếu (tùy chọn)
            output_format (str): Định dạng đầu ra (png, jpg, gif)
            model (str): Mô hình AI sử dụng (openai, claude)

        Returns:
            str: Đường dẫn đến file hình ảnh đã tạo
        """
        # Tạo đường dẫn đầu ra
        timestamp = int(time.time())
        output_filename = f"image_{timestamp}.{output_format}"
        output_path = os.path.join(self.temp_dir, output_filename)

        self.logger.info(f"Tạo hình ảnh với mô hình {model}: {description[:50]}...")

        # Tham chiếu hình ảnh nếu có
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
            except Exception as e:
                self.logger.warning(f"Không thể tải hình ảnh tham chiếu: {e}")

        if model.lower() == "openai":
            try:
                # Tạo hình ảnh bằng OpenAI DALL-E
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=description,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                # Tải hình ảnh từ URL trong kết quả
                image_url = response.data[0].url
                image_response = requests.get(image_url)

                with open(output_path, "wb") as f:
                    f.write(image_response.content)

                return output_path

            except Exception as e:
                self.logger.error(f"Lỗi khi tạo hình ảnh với OpenAI: {e}")
                return None

        elif model.lower() == "claude":
            try:
                # Tạo hình ảnh bằng Claude (giả định API hình ảnh)

                # Claude chưa có API tạo hình ảnh chính thức, sử dụng OpenAI làm dự phòng

                self.logger.warning("Tạo hình ảnh với Claude không được hỗ trợ chính thức, sẽ sử dụng OpenAI làm dự phòng")

                # Fallback sang OpenAI
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
                return None
        else:
            self.logger.error(f"Mô hình không được hỗ trợ: {model}")

            return None

    def _generate_audio(self, description, model):
        """
        Tạo âm thanh bằng AI

        Args:
            description (str): Mô tả âm thanh hoặc văn bản để chuyển thành giọng nói
            model (str): Mô hình AI sử dụng (openai, claude)

        Returns:
            str: Đường dẫn đến file âm thanh đã tạo
        """
        # Tạo đường dẫn đầu ra
        timestamp = int(time.time())
        output_filename = f"audio_{timestamp}.mp3"
        output_path = os.path.join(self.temp_dir, output_filename)

        self.logger.info(f"Tạo âm thanh với mô hình {model}: {description[:50]}...")

        if model.lower() == "openai":
            try:
                # Tạo âm thanh bằng OpenAI TTS
                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=description
                )

                response.stream_to_file(output_path)
                return output_path

            except Exception as e:
                self.logger.error(f"Lỗi khi tạo âm thanh với OpenAI: {e}")
                return None

        elif model.lower() == "claude":
            try:
                # Claude hiện tại không có API tạo âm thanh, sử dụng OpenAI làm dự phòng
                self.logger.warning("Tạo âm thanh với Claude không được hỗ trợ, sẽ sử dụng OpenAI làm dự phòng")

                response = self.openai_client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=description
                )

                response.stream_to_file(output_path)
                return output_path

            except Exception as e:
                self.logger.error(f"Lỗi khi tạo âm thanh với Claude: {e}")
                return None
        else:
            self.logger.error(f"Mô hình không được hỗ trợ: {model}")

            return None
