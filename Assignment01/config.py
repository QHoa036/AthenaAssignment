#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File cấu hình cho quy trình tự động hóa
Configuration file for automation workflow
"""

import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("config")

# Load environment variables from .env.local only
# .env.example is only a template and should not be loaded
env_local_path = Path(__file__).parent / ".env.local"

if env_local_path.exists():
    logger.info(f"Loading environment from {env_local_path}")
    load_dotenv(env_local_path)
else:
    logger.warning("No .env.local file found. Using system environment variables.")
    logger.info("Note: .env.example is available as a template but will not be loaded automatically.")

# Thư mục gốc của dự án
# Root directory of the project
BASE_DIR = Path(__file__).parent.absolute()

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

# Đường dẫn đến file credential Google API
# Path to Google API credentials file
GOOGLE_CREDENTIALS_FILE = os.path.join(DATA_DIR, "google_credentials.json")

# ID Google Sheet chứa dữ liệu đầu vào
# Google Sheet ID containing input data
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
if not GOOGLE_SHEET_ID:
    logger.warning("GOOGLE_SHEET_ID not set in environment variables")

# ID thư mục Google Drive để lưu trữ tài sản đã tạo
# Google Drive folder ID to store generated assets
DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
if not DRIVE_FOLDER_ID:
    logger.warning("GOOGLE_DRIVE_FOLDER_ID not set in environment variables")

# API key cho các dịch vụ AI
# API key for AI services (prioritize OpenAI, fallback to Anthropic)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Use the appropriate API key based on availability
if OPENAI_API_KEY:
    AI_API_KEY = OPENAI_API_KEY
    AI_SERVICE = "openai"
elif ANTHROPIC_API_KEY:
    AI_API_KEY = ANTHROPIC_API_KEY
    AI_SERVICE = "anthropic"
else:
    logger.warning("No AI API keys found in environment variables")
    AI_API_KEY = None
    AI_SERVICE = None

# Cấu hình email
# Email configuration
EMAIL_CONFIG = {
    "smtp_server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
    "sender_email": os.getenv("EMAIL_SENDER"),
    "sender_password": os.getenv("EMAIL_PASSWORD"),
    "admin_email": os.getenv("ADMIN_EMAIL")
}

# Validate email configuration
if not all([
    EMAIL_CONFIG["sender_email"],
    EMAIL_CONFIG["sender_password"],
    EMAIL_CONFIG["admin_email"]
]):
    logger.warning("Email configuration incomplete in environment variables")

# URL webhook Slack
# Slack webhook URL
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    logger.warning("SLACK_WEBHOOK_URL not set in environment variables")

# Đảm bảo các thư mục tồn tại
# Ensure directories exist
for dir_path in [DATA_DIR, LOG_DIR, REPORT_OUTPUT_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Log configuration status
logger.info("Configuration loaded")