#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chương trình tự động hóa chính cho Assignment 1
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Thêm thư mục gốc vào đường dẫn để import config
sys.path.append(str(Path(__file__).parent.parent))

# Import các module tự tạo
from integrations import GoogleSheetsReader, GoogleDriveUploader
from notifications import EmailNotifier, SlackNotifier
from persistence import DatabaseManager
from generators import ReportGenerator, AIGenerator
import config

# Đảm bảo dotenv được tải trước khi import config
from dotenv import load_dotenv

def setup_logging():
    """
    Thiết lập logging cho ứng dụng
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
    """
    parser = argparse.ArgumentParser(description='Quy trình tự động hóa cho việc tạo tài sản AI')
    parser.add_argument('--sheet-id', help='ID Google Sheet cần xử lý')
    parser.add_argument('--config', help='Đường dẫn đến tệp cấu hình tùy chỉnh')
    parser.add_argument('--env', help='Đường dẫn đến tệp .env để sử dụng')
    parser.add_argument('--openai-key', help='Khóa API OpenAI')
    parser.add_argument('--anthropic-key', help='Khóas API Anthropic')
    parser.add_argument('--skip-google-auth', action='store_true', help='Bỏ qua kiểm tra xác thực Google (chỉ dùng cho debug)')
    parser.add_argument('--debug', action='store_true', help='Chạy ở chế độ debug, bỏ qua một số kiểm tra')
    return parser.parse_args()

def process_item(item, db_manager, drive_uploader, email_notifier, slack_notifier, logger, debug_mode=False):
    """
    Xử lý một mục từ Google Sheet và tạo nội dung

    Args:
        item (dict): Dữ liệu mục từ Google Sheet
        db_manager (DatabaseManager): Thể hiện của quản lý cơ sở dữ liệu
        drive_uploader (GoogleDriveUploader): Thể hiện của trình tải lên Drive
        email_notifier (EmailNotifier): Thể hiện của thông báo email
        slack_notifier (SlackNotifier): Thể hiện của thông báo Slack
        logger (Logger): Thể hiện của logger
        debug_mode (bool): Chế độ debug, bỏ qua một số kiểm tra và sử dụng giả lập

    Returns:
        bool: Thành công hoặc thất bại
    """
    try:
        logger.info(f"Xử lý mục: {item['id']} - {item['description']}")

        # Tạo nội dung bằng AI
        if not config.AI_API_KEY and not debug_mode:
            raise Exception("Không có khóa API AI. Vui lòng thiết lập OPENAI_API_KEY hoặc ANTHROPIC_API_KEY trong tệp .env")

        if debug_mode:
            # Tạo giả lập đầu ra trong chế độ debug
            logger.warning("Chế độ debug: Giả lập tạo nội dung AI")
            temp_dir = Path(config.DATA_DIR) / "temp"
            temp_dir.mkdir(exist_ok=True)
            output_file = temp_dir / f"debug_output_{item['id']}.{item['output_format'].lower()}"
            
            # Tạo file giả lập trống
            with open(output_file, 'w') as f:
                f.write(f"Dữ liệu giả lập cho {item['description']}")
        else:
            # Sử dụng AIGenerator thực tế
            ai_generator = AIGenerator(config.AI_API_KEY, service=config.AI_SERVICE)
            output_file = ai_generator.generate(
                description=item['description'],
                reference_url=item.get('example_asset_url'),
                output_format=item['output_format'],
                model=item['model']
            )

        if not output_file:
            raise Exception("Không thể tạo nội dung")

        # Tải lên Google Drive
        drive_url = drive_uploader.upload(output_file, item['description'])

        # Lưu vào cơ sở dữ liệu
        db_manager.log_success(
            item_id=item['id'],
            description=item['description'],
            output_format=item['output_format'],
            model=item['model'],
            drive_url=drive_url
        )

        # Gửi thông báo thành công
        email_notifier.send_success_notification(item, drive_url)
        slack_notifier.send_success_notification(item, drive_url)

        logger.info(f"Xử lý thành công mục: {item['id']}")
        return True

    except Exception as e:
        logger.error(f"Lỗi khi xử lý mục {item['id']}: {str(e)}")

        # Lưu vào cơ sở dữ liệu
        db_manager.log_failure(
            item_id=item['id'],
            description=item['description'],
            output_format=item['output_format'],
            model=item['model'],
            error_message=str(e)
        )

        # Gửi thông báo lỗi
        email_notifier.send_failure_notification(item, str(e))
        slack_notifier.send_failure_notification(item, str(e))
        return False

def main():
    """
    Hàm chính của ứng dụng
    """
    # Thiết lập logging
    logger = setup_logging()
    logger.info("Bắt đầu quy trình tự động hóa")

    # Phân tích đối số
    args = parse_arguments()

    # Tải tệp môi trường tùy chỉnh nếu được chỉ định
    if args.env:
        env_path = Path(args.env)
        if env_path.exists():
            logger.info(f"Đang tải môi trường từ {env_path}")
            load_dotenv(env_path, override=True)
        else:
            logger.error(f"Không tìm thấy tệp môi trường: {env_path}")
            return
    # Nếu không, chúng ta dựa vào config.py đã tải .env.local trước đó

    # Ghi đè các khóa API từ dòng lệnh nếu được cung cấp
    if args.openai_key:
        os.environ["OPENAI_API_KEY"] = args.openai_key
        config.OPENAI_API_KEY = args.openai_key
        config.AI_API_KEY = args.openai_key
        config.AI_SERVICE = "openai"
    elif args.anthropic_key:
        os.environ["ANTHROPIC_API_KEY"] = args.anthropic_key
        config.ANTHROPIC_API_KEY = args.anthropic_key
        config.AI_API_KEY = args.anthropic_key
        config.AI_SERVICE = "anthropic"

    # Đọc dữ liệu từ Google Sheets
    sheet_id = args.sheet_id or config.GOOGLE_SHEET_ID

    if not sheet_id:
        logger.error("Không có Google Sheet ID được cung cấp. Vui lòng đặt GOOGLE_SHEET_ID trong .env hoặc sử dụng --sheet-id")
        return

    # Kiểm tra xác thực Google tồn tại, trừ khi được bỏ qua trong chế độ debug
    if not os.path.exists(config.GOOGLE_CREDENTIALS_FILE) and not (args.skip_google_auth or args.debug):
        logger.error(f"Không tìm thấy tệp xác thực Google: {config.GOOGLE_CREDENTIALS_FILE}")
        logger.error("Vui lòng đặt tệp xác thực của bạn trong thư mục dữ liệu")
        logger.error("Hoặc chạy với cờ --skip-google-auth hoặc --debug để bỏ qua kiểm tra này")
        return
    
    if args.skip_google_auth or args.debug:
        logger.warning("Chế độ debug: Bỏ qua kiểm tra xác thực Google")
        # Sử dụng dữ liệu mẫu cho mục đích debug
        items = [
            {
                'id': 'debug-1',
                'description': 'Hình ảnh mẫu cho debug',
                'example_asset_url': 'https://example.com/sample.jpg',
                'output_format': 'PNG',
                'model': 'openai'
            }
        ]
    else:
        # Đọc dữ liệu thực tế từ Google Sheets
        sheets_reader = GoogleSheetsReader(config.GOOGLE_CREDENTIALS_FILE)
        items = sheets_reader.read_sheet(sheet_id)

    if not items:
        logger.error("Không có dữ liệu để xử lý hoặc lỗi đọc Google Sheet")
        return

    # Khởi tạo các thành phần
    db_manager = DatabaseManager(config.DATABASE_PATH)

    # Kiểm tra ID thư mục Google Drive
    if not config.DRIVE_FOLDER_ID and not (args.skip_google_auth or args.debug):
        logger.error("Không có ID thư mục Google Drive được cung cấp. Vui lòng đặt GOOGLE_DRIVE_FOLDER_ID trong .env")
        return

    if args.skip_google_auth or args.debug:
        # Tạo đối tượng giả lập trong chế độ debug
        class DebugDriveUploader:
            def upload(self, file_path, description):
                logger.info(f"CHẾ ĐỘ DEBUG: Giả lập tải lên {file_path} với mô tả '{description}'")
                return f"https://drive.google.com/debug-file-url"
        
        drive_uploader = DebugDriveUploader()
        logger.warning("Chế độ debug: Sử dụng trình tải lên Drive giả lập")
    else:
        drive_uploader = GoogleDriveUploader(config.GOOGLE_CREDENTIALS_FILE, config.DRIVE_FOLDER_ID)

    # Kiểm tra cấu hình email
    if not all([
        config.EMAIL_CONFIG["sender_email"],
        config.EMAIL_CONFIG["sender_password"],
        config.EMAIL_CONFIG["admin_email"]
    ]):
        logger.warning("Cấu hình email không đầy đủ. Thông báo email sẽ không hoạt động đúng.")

    email_notifier = EmailNotifier(config.EMAIL_CONFIG)

    # Kiểm tra URL webhook Slack
    if not config.SLACK_WEBHOOK_URL:
        logger.warning("URL webhook Slack không được cung cấp. Thông báo Slack sẽ không hoạt động.")

    slack_notifier = SlackNotifier(config.SLACK_WEBHOOK_URL)

    # Xử lý từng mục
    success_count = 0
    failure_count = 0

    for item in items:
        success = process_item(item, db_manager, drive_uploader, email_notifier, slack_notifier, logger, debug_mode=(args.skip_google_auth or args.debug))
        if success:
            success_count += 1
        else:
            failure_count += 1

    # Tạo báo cáo hàng ngày
    logger.info("Tạo báo cáo hàng ngày")

    report_generator = ReportGenerator(config.DATABASE_PATH, config.REPORT_OUTPUT_DIR)
    report_path = report_generator.generate_daily_report()

    # Gửi báo cáo qua email
    email_notifier.send_report(
        report_path,
        success_count,
        failure_count
    )

    logger.info("Hoàn thành quy trình tự động hóa")
    logger.info(f"Kết quả: {success_count} thành công, {failure_count} thất bại")

if __name__ == "__main__":
    main()
