#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File cấu hình cho Assignment 2: AI Prompt Engineering cho Game Assets
# Tệp này chứa tất cả các cài đặt cần thiết cho hệ thống

import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).parent.parent.absolute()

# Cấu trúc thư mục
# - prompts: chứa các mẫu prompt
# - assets: chứa tài sản game (gồm hai thư mục con: reference và generated)
# - validation: chứa kết quả xác thực và báo cáo
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")  # Thư mục chứa các mẫu prompt
ASSETS_DIR = os.path.join(BASE_DIR, "assets")    # Thư mục chứa tài sản game
REFERENCE_DIR = os.path.join(ASSETS_DIR, "reference")  # Thư mục chứa tài sản tham chiếu
GENERATED_DIR = os.path.join(ASSETS_DIR, "generated")  # Thư mục chứa tài sản được tạo ra
VALIDATION_DIR = os.path.join(BASE_DIR, "validation")  # Thư mục chứa kết quả xác thực

# Cấu hình các mô hình AI
# OpenAI - DALL-E cho tạo hình ảnh
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # API key cho OpenAI, lấy từ biến môi trường
OPENAI_MODELS = {
    "dalle2": {  # Cấu hình cho DALL-E 2
        "name": "dall-e-2",
        "max_resolution": 1024,  # Độ phân giải tối đa
        "formats": ["png"]      # Định dạng hỗ trợ
    },
    "dalle3": {  # Cấu hình cho DALL-E 3
        "name": "dall-e-3",
        "max_resolution": 1024,
        "formats": ["png"]
    }
}

# Anthropic/Claude - mô hình ngôn ngữ lớn có khả năng tạo hình ảnh
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # API key cho Anthropic, lấy từ biến môi trường
CLAUDE_MODELS = {
    "claude3_opus": {  # Cấu hình cho Claude 3 Opus (mô hình mạnh nhất)
        "name": "claude-3-opus-20240229",
        "max_resolution": 1024,
        "formats": ["png", "jpg"]
    },
    "claude3_sonnet": {  # Cấu hình cho Claude 3 Sonnet (mô hình cân bằng)
        "name": "claude-3-sonnet-20240229",
        "max_resolution": 1024,
        "formats": ["png", "jpg"]
    }
}

# Cấu hình cho Midjourney (thông qua API)
# Lưu ý: Đây là giữ chỗ vì Midjourney không có API chính thức
MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY", "")

# Cấu hình Layer.ai API để xác thực và đánh giá chất lượng của các tài sản được tạo ra
LAYER_API_KEY = os.getenv("LAYER_API_KEY", "")

# Cấu hình mặc định cho các loại tài sản game khác nhau
ASSET_TYPES = {
    "character": {  # Nhân vật
        "default_resolution": "1024x1024",  # Độ phân giải mặc định
        "formats": ["png"],                # Định dạng được hỗ trợ
        "prompt_template": "character_template.txt",  # Mẫu prompt để sử dụng
    },
    "environment": {  # Môi trường/Bối cảnh
        "default_resolution": "1024x1024",
        "formats": ["png"],
        "prompt_template": "environment_template.txt",
    },
    "item": {  # Vật phẩm
        "default_resolution": "512x512",
        "formats": ["png"],
        "prompt_template": "item_template.txt",
    },
    "ui": {  # Giao diện người dùng
        "default_resolution": "1024x512",
        "formats": ["png"],
        "prompt_template": "ui_template.txt",
    }
}

# Ngưỡng xác thực chất lượng tài sản
# Mỗi chỉ số có ba mức: reject (từ chối), acceptable (chấp nhận được), excellent (xuất sắc)
VALIDATION_THRESHOLDS = {
    "ssim": {  # Structural Similarity Index - Đo lường sự tương đồng về cấu trúc
        "reject": 0.6,       # Dưới 0.6 sẽ bị từ chối
        "acceptable": 0.8,   # Từ 0.6 đến 0.9 là chấp nhận được
        "excellent": 0.9     # Trên 0.9 là xuất sắc
    },
    "color_match": {  # Độ tương đồng về màu sắc
        "reject": 0.7,
        "acceptable": 0.9,
        "excellent": 0.95
    },
    "edge_accuracy": {  # Độ chính xác của các cạnh/viền
        "reject": 0.75,
        "acceptable": 0.9,
        "excellent": 0.95
    }
}

# Đảm bảo tất cả các thư mục cần thiết đều tồn tại
# Tự động tạo thư mục nếu chưa có để tránh lỗi khi chạy chương trình
for dir_path in [PROMPTS_DIR, REFERENCE_DIR, GENERATED_DIR, VALIDATION_DIR]:
    os.makedirs(dir_path, exist_ok=True)
