#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File cấu hình cho quy trình tự động hóa
"""

import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("config")

# Tải biến môi trường từ .env.local
# .env.example chỉ là mẫu và không nên được tải
env_local_path = Path(__file__).parent / ".env.local"

if env_local_path.exists():
    logger.info(f"Đang tải biến môi trường từ {env_local_path}")
    load_dotenv(env_local_path)
else:
    logger.warning("Không tìm thấy file .env.local. Sử dụng biến môi trường hệ thống.")
    logger.info("Lưu ý: .env.example có sẵn như một mẫu nhưng sẽ không được tải tự động.")

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).parent.absolute()

# Thư mục lưu trữ dữ liệu
DATA_DIR = os.path.join(BASE_DIR, "data")

# Thư mục lưu trữ logs
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Thư mục lưu trữ báo cáo
REPORT_OUTPUT_DIR = os.path.join(BASE_DIR, "reports")

# Đường dẫn đến file cơ sở dữ liệu
DATABASE_PATH = os.path.join(DATA_DIR, "automation.db")

# Đường dẫn đến file credential Google API
GOOGLE_CREDENTIALS_FILE = os.path.join(DATA_DIR, "google_credentials.json")

# ID Google Sheet chứa dữ liệu đầu vào
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
if not GOOGLE_SHEET_ID:
    logger.warning("GOOGLE_SHEET_ID không được đặt trong biến môi trường")

# ID thư mục Google Drive để lưu trữ tài sản đã tạo
DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
if not DRIVE_FOLDER_ID:
    logger.warning("GOOGLE_DRIVE_FOLDER_ID không được đặt trong biến môi trường")

# API key cho các dịch vụ AI (ưu tiên OpenAI, dự phòng Anthropic)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Sử dụng API key phù hợp dựa trên tính khả dụng
if OPENAI_API_KEY:
    AI_API_KEY = OPENAI_API_KEY
    AI_SERVICE = "openai"
elif ANTHROPIC_API_KEY:
    AI_API_KEY = ANTHROPIC_API_KEY
    AI_SERVICE = "anthropic"
else:
    logger.warning("Không tìm thấy API key AI trong biến môi trường")
    AI_API_KEY = None
    AI_SERVICE = None

# Cấu hình email
EMAIL_CONFIG = {
    "smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
    "sender_email": os.getenv("EMAIL_SENDER"),
    "sender_password": os.getenv("EMAIL_PASSWORD"),
    "admin_email": os.getenv("ADMIN_EMAIL")
}

# Xác thực cấu hình email
if not all([
    EMAIL_CONFIG["sender_email"],
    EMAIL_CONFIG["sender_password"],
    EMAIL_CONFIG["admin_email"]
]):
    logger.warning("Cấu hình email không đầy đủ trong biến môi trường")

# URL webhook Slack
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    logger.warning("SLACK_WEBHOOK_URL không được đặt trong biến môi trường")

# Đảm bảo các thư mục tồn tại
for dir_path in [DATA_DIR, LOG_DIR, REPORT_OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Ghi log trạng thái cấu hình
logger.info("Đã tải cấu hình xong")