#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module gửi thông báo qua email và Slack
"""

import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime

class EmailNotifier:
    """
    Lớp để gửi thông báo qua email
    """

    def __init__(self, email_config):
        """
        Khởi tạo đối tượng EmailNotifier

        Args:
            email_config (dict): Cấu hình email (smtp_server, smtp_port, sender_email, sender_password, admin_email)
        """
        self.logger = logging.getLogger(__name__)
        self.config = email_config

    def send_success_notification(self, item, drive_url):
        """
        Gửi thông báo thành công qua email

        Args:
            item (dict): Mục đã được xử lý
            drive_url (str): URL của tệp trên Google Drive
        """
        try:
            subject = f"Thông báo thành công: {item['id']} - {item['description'][:30]}..."

            body = f"""
            <html>
            <body>
            <h2>Thành công tạo nội dung AI</h2>
            <p><strong>ID:</strong> {item['id']}</p>
            <p><strong>Mô tả:</strong> {item['description']}</p>
            <p><strong>Định dạng đầu ra:</strong> {item['output_format']}</p>
            <p><strong>Mô hình:</strong> {item['model']}</p>
            <p><strong>URL Google Drive:</strong> <a href="{drive_url}">{drive_url}</a></p>
            <p>Nội dung đã được tạo thành công và tải lên Google Drive.</p>
            </body>
            </html>
            """

            self._send_email(subject, body, self.config['admin_email'], html=True)

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi thông báo email thành công: {e}")

    def send_failure_notification(self, item, error_message):
        """
        Gửi thông báo lỗi qua email

        Args:
            item (dict): Mục đã được xử lý
            error_message (str): Thông báo lỗi
        """
        try:
            subject = f"Thông báo lỗi: {item['id']} - {item['description'][:30]}..."

            body = f"""
            <html>
            <body>
            <h2>Lỗi khi tạo nội dung AI</h2>
            <p><strong>ID:</strong> {item['id']}</p>
            <p><strong>Mô tả:</strong> {item['description']}</p>
            <p><strong>Định dạng đầu ra:</strong> {item['output_format']}</p>
            <p><strong>Mô hình:</strong> {item['model']}</p>
            <p><strong>Lỗi:</strong> {error_message}</p>
            </body>
            </html>
            """

            self._send_email(subject, body, self.config['admin_email'], html=True)

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi thông báo email lỗi: {e}")

    def send_report(self, report_path, success_count, failure_count):
        """
        Gửi báo cáo hàng ngày qua email

        Args:
            report_path (str): Đường dẫn đến file báo cáo
            success_count (int): Số lượng xử lý thành công
            failure_count (int): Số lượng xử lý thất bại
        """
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            subject = f"Báo cáo hàng ngày - Tự động hóa tạo nội dung AI - {date_str}"

            body = f"""
            <html>
            <body>
            <h2>Báo cáo hàng ngày - Tự động hóa tạo nội dung AI</h2>
            <p><strong>Ngày:</strong> {date_str}</p>
            <p><strong>Tổng số xử lý:</strong> {success_count + failure_count}</p>
            <p><strong>Thành công:</strong> {success_count}</p>
            <p><strong>Thất bại:</strong> {failure_count}</p>
            <p><strong>Tỷ lệ thành công:</strong> {(success_count / (success_count + failure_count)) * 100:.2f}%</p>
            <p>Vui lòng xem file đính kèm để biết chi tiết.</p>
            </body>
            </html>
            """

            self._send_email(subject, body, self.config['admin_email'], html=True, attachment_path=report_path)

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi báo cáo email: {e}")

    def _send_email(self, subject, body, recipient, html=False, attachment_path=None):
        """
        Gửi email

        Args:
            subject (str): Tiêu đề email
            body (str): Nội dung email
            recipient (str): Email người nhận
            html (bool, optional): Có sử dụng HTML hay không. Mặc định là False.
            attachment_path (str): Đường dẫn đến file đính kèm (tùy chọn)
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = recipient
            msg['Subject'] = subject

            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Thêm tệp đính kèm nếu có
            # Add attachment if any
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as file:
                    attachment = MIMEApplication(file.read(), _subtype=os.path.splitext(attachment_path)[1][1:])
                    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                    msg.attach(attachment)

            # Kết nối và gửi email
            # Connect and send email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
            server.quit()

            self.logger.info(f"Đã gửi email đến {recipient}")

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi email: {e}")


class SlackNotifier:
    """
    Lớp để gửi thông báo qua Slack
    """

    def __init__(self, webhook_url):
        """
        Khởi tạo đối tượng SlackNotifier

        Args:
            webhook_url (str): URL webhook Slack
        """
        self.logger = logging.getLogger(__name__)
        self.webhook_url = webhook_url

    def send_success_notification(self, item, drive_url):
        """
        Gửi thông báo thành công qua Slack

        Args:
            item (dict): Mục đã được xử lý
            drive_url (str): URL của tệp trên Google Drive
        """
        try:
            message = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"✅ Thành công tạo nội dung AI: {item['id']}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*ID:*\n{item['id']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Mô tả:*\n{item['description'][:100]}..."
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Định dạng:*\n{item['output_format']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Mô hình:*\n{item['model']}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Google Drive URL:*\n<{drive_url}|Xem nội dung trên Google Drive>"
                        }
                    }
                ]
            }

            self._send_slack_notification(message)

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi thông báo Slack thành công: {e}")

    def send_failure_notification(self, item, error_message):
        """
        Gửi thông báo lỗi qua Slack

        Args:
            item (dict): Mục đã được xử lý
            error_message (str): Thông báo lỗi
        """
        try:
            message = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"❌ Lỗi khi tạo nội dung AI: {item['id']}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*ID:*\n{item['id']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Mô tả:*\n{item['description'][:100]}..."
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Định dạng:*\n{item['output_format']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Mô hình:*\n{item['model']}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Lỗi:*\n```{error_message}```"
                        }
                    }
                ]
            }

            self._send_slack_notification(message)

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi thông báo Slack lỗi: {e}")

    def _send_slack_notification(self, message):
        """
        Gửi thông báo Slack

        Args:
            message (dict): Tin nhắn cần gửi
        """
        try:
            response = requests.post(
                self.webhook_url,
                json=message
            )

            if response.status_code != 200:
                self.logger.error(f"Lỗi khi gửi thông báo Slack: {response.status_code} - {response.text}")
            else:
                self.logger.info("Thông báo Slack đã được gửi thành công")

        except Exception as e:
            self.logger.error(f"Lỗi khi gửi thông báo Slack: {e}")
