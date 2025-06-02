#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chương trình tự động hóa chính cho Assignment 1
Main automation program for Assignment 1
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Import các module tự tạo
# Import custom modules
from sheets_reader import GoogleSheetsReader
from ai_generator import AIGenerator
from drive_uploader import GoogleDriveUploader
from notifier import EmailNotifier, SlackNotifier
from database import DatabaseManager
from report_generator import ReportGenerator
import config

def setup_logging():
    """
    Thiết lập logging cho ứng dụng
    Setup logging for the application
    """
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"automation_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def parse_arguments():
    """
    Phân tích các đối số dòng lệnh
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Automation workflow for AI asset generation')
    parser.add_argument('--sheet-id', help='Google Sheet ID to process')
    parser.add_argument('--config', help='Path to custom config file')
    return parser.parse_args()

def process_item(item, db_manager, drive_uploader, email_notifier, slack_notifier, logger):
    """
    Xử lý một mục từ Google Sheet và tạo nội dung
    Process a single item from Google Sheet and generate content

    Args:
        item (dict): Item data from Google Sheet
        db_manager (DatabaseManager): Database manager instance
        drive_uploader (GoogleDriveUploader): Drive uploader instance
        email_notifier (EmailNotifier): Email notifier instance
        slack_notifier (SlackNotifier): Slack notifier instance
        logger (Logger): Logger instance

    Returns:
        bool: Success or failure
    """
    try:
        logger.info(f"Xử lý mục: {item['id']} - {item['description']}")
        logger.info(f"Processing item: {item['id']} - {item['description']}")

        # Tạo nội dung bằng AI
        # Generate content using AI
        ai_generator = AIGenerator(config.AI_API_KEY)
        output_file = ai_generator.generate(
            description=item['description'],
            reference_url=item.get('example_asset_url'),
            output_format=item['output_format'],
            model=item['model']
        )

        if not output_file:
            raise Exception("Không thể tạo nội dung / Failed to generate content")

        # Tải lên Google Drive
        # Upload to Google Drive
        drive_url = drive_uploader.upload(output_file, item['description'])

        # Lưu vào cơ sở dữ liệu
        # Save to database
        db_manager.log_success(
            item_id=item['id'],
            description=item['description'],
            output_format=item['output_format'],
            model=item['model'],
            drive_url=drive_url
        )

        # Gửi thông báo thành công
        # Send success notification
        email_notifier.send_success_notification(item, drive_url)
        slack_notifier.send_success_notification(item, drive_url)

        logger.info(f"Xử lý thành công mục: {item['id']}")
        logger.info(f"Successfully processed item: {item['id']}")
        return True

    except Exception as e:
        logger.error(f"Lỗi khi xử lý mục {item['id']}: {str(e)}")
        logger.error(f"Error processing item {item['id']}: {str(e)}")

        # Lưu vào cơ sở dữ liệu
        # Save to database
        db_manager.log_failure(
            item_id=item['id'],
            description=item['description'],
            output_format=item['output_format'],
            model=item['model'],
            error_message=str(e)
        )

        # Gửi thông báo lỗi
        # Send failure notification
        email_notifier.send_failure_notification(item, str(e))
        slack_notifier.send_failure_notification(item, str(e))
        return False

def main():
    """
    Hàm chính của ứng dụng
    Main function of the application
    """
    # Thiết lập logging
    # Setup logging
    logger = setup_logging()
    logger.info("Bắt đầu quy trình tự động hóa")
    logger.info("Starting automation workflow")

    # Phân tích đối số
    # Parse arguments
    args = parse_arguments()

    # Đọc dữ liệu từ Google Sheets
    # Read data from Google Sheets
    sheet_id = args.sheet_id or config.GOOGLE_SHEET_ID
    sheets_reader = GoogleSheetsReader(config.GOOGLE_CREDENTIALS_FILE)
    items = sheets_reader.read_sheet(sheet_id)

    if not items:
        logger.error("Không có dữ liệu để xử lý hoặc lỗi đọc Google Sheet")
        logger.error("No data to process or error reading Google Sheet")
        return

    # Khởi tạo các thành phần
    # Initialize components
    db_manager = DatabaseManager(config.DATABASE_PATH)
    drive_uploader = GoogleDriveUploader(config.GOOGLE_CREDENTIALS_FILE, config.DRIVE_FOLDER_ID)
    email_notifier = EmailNotifier(config.EMAIL_CONFIG)
    slack_notifier = SlackNotifier(config.SLACK_WEBHOOK_URL)

    # Xử lý từng mục
    # Process each item
    success_count = 0
    failure_count = 0

    for item in items:
        success = process_item(item, db_manager, drive_uploader, email_notifier, slack_notifier, logger)
        if success:
            success_count += 1
        else:
            failure_count += 1

    # Tạo báo cáo hàng ngày
    # Generate daily report
    logger.info("Tạo báo cáo hàng ngày")
    logger.info("Generating daily report")

    report_generator = ReportGenerator(config.DATABASE_PATH, config.REPORT_OUTPUT_DIR)
    report_path = report_generator.generate_daily_report()

    # Gửi báo cáo qua email
    # Send report via email
    email_notifier.send_report(
        report_path,
        success_count,
        failure_count
    )

    logger.info("Hoàn thành quy trình tự động hóa")
    logger.info("Automation workflow completed")
    logger.info(f"Kết quả: {success_count} thành công, {failure_count} thất bại")
    logger.info(f"Results: {success_count} successes, {failure_count} failures")

if __name__ == "__main__":
    main()
