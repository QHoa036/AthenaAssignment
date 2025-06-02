#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File cấu hình sử dụng biến môi trường
Configuration file using environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
# Load environment variables from .env file
load_dotenv()

# Thư mục gốc của dự án
# Root directory of the project
BASE_DIR = Path(__file__).parent.parent.absolute()

# Thư mục lưu trữ dữ liệu
# Data storage directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Thư mục lưu trữ logs
# Logs directory
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Thư mục lưu trữ báo cáo
# Reports directory
REPORT_OUTPUT_DIR = os.path.join(BASE_DIR, "reports")

# Đường dẫn đến file cơ sở dữ liệu
# Path to the database file
DATABASE_PATH = os.path.join(DATA_DIR, "automation.db")

# ID Google Sheet chứa dữ liệu đầu vào
# Google Sheet ID containing input data
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

# Đường dẫn đến file credential Google API
# Path to Google API credentials file
GOOGLE_CREDENTIALS_FILE = os.path.join(DATA_DIR, "google_credentials.json")

# ID thư mục Google Drive để lưu trữ tài sản đã tạo
# Google Drive folder ID to store generated assets
DRIVE_FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")

# API key cho các dịch vụ AI
# API key for AI services
AI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Hoặc ANTHROPIC_API_KEY

# Cấu hình email
# Email configuration
EMAIL_CONFIG = {
    "smtp_server": os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.environ.get("EMAIL_SMTP_PORT", "587")),
    "sender_email": os.environ.get("EMAIL_SENDER"),
    "sender_password": os.environ.get("EMAIL_PASSWORD"),
    "admin_email": os.environ.get("ADMIN_EMAIL")
}

# URL webhook Slack
# Slack webhook URL
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Đảm bảo các thư mục tồn tại
# Ensure directories exist
for dir_path in [DATA_DIR, LOG_DIR, REPORT_OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)
