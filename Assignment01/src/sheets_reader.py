#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module đọc dữ liệu từ Google Sheets
Module for reading data from Google Sheets
"""

import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GoogleSheetsReader:
    """
    Lớp để đọc dữ liệu từ Google Sheets
    Class to read data from Google Sheets
    """

    def __init__(self, credentials_file):
        """
        Khởi tạo đối tượng GoogleSheetsReader
        Initialize GoogleSheetsReader object

        Args:
            credentials_file (str): Đường dẫn đến file credentials Google API
                                   Path to Google API credentials file
        """
        self.logger = logging.getLogger(__name__)
        self.credentials_file = credentials_file

    def _get_service(self):
        """
        Tạo dịch vụ Google Sheets API
        Create Google Sheets API service

        Returns:
            service: Dịch vụ Google Sheets API hoặc None nếu có lỗi
                    Google Sheets API service or None if error
        """
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            credentials = Credentials.from_service_account_file(
                self.credentials_file, scopes=scopes)
            service = build('sheets', 'v4', credentials=credentials)
            return service
        except Exception as e:
            self.logger.error(f"Lỗi khi kết nối với Google Sheets API: {e}")
            self.logger.error(f"Error connecting to Google Sheets API: {e}")
            return None

    def read_sheet(self, sheet_id, range_name="Sheet1!A1:Z1000"):
        """
        Đọc dữ liệu từ Google Sheet
        Read data from Google Sheet

        Args:
            sheet_id (str): ID của Google Sheet
                           ID of the Google Sheet
            range_name (str): Phạm vi đọc (mặc định: Sheet1!A1:Z1000)
                             Range to read (default: Sheet1!A1:Z1000)

        Returns:
            list: Danh sách các mục dữ liệu, mỗi mục là một từ điển
                 List of data items, each item is a dictionary
        """
        try:
            service = self._get_service()
            if not service:
                return []

            result = service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=range_name).execute()
            rows = result.get('values', [])

            if not rows:
                self.logger.warning("Không tìm thấy dữ liệu trong Google Sheet")
                self.logger.warning("No data found in Google Sheet")
                return []

            headers = rows[0]
            items = []

            for row in rows[1:]:
                # Đảm bảo mỗi hàng có đủ cột
                # Ensure each row has enough columns
                if len(row) < len(headers):
                    row.extend([''] * (len(headers) - len(row)))

                # Tạo từ điển từ header và dữ liệu hàng
                # Create dictionary from header and row data
                item = {headers[i].lower(): row[i] for i in range(len(headers))}

                # Đảm bảo các trường bắt buộc có trong mục
                # Ensure required fields are in the item
                required_fields = ['id', 'description', 'output_format', 'model']
                if all(field in item for field in required_fields):
                    items.append(item)
                else:
                    self.logger.warning(f"Bỏ qua hàng thiếu trường bắt buộc: {row}")
                    self.logger.warning(f"Skipping row with missing required fields: {row}")

            self.logger.info(f"Đã đọc {len(items)} mục từ Google Sheet")
            self.logger.info(f"Read {len(items)} items from Google Sheet")
            return items

        except Exception as e:
            self.logger.error(f"Lỗi khi đọc Google Sheet: {e}")
            self.logger.error(f"Error reading Google Sheet: {e}")
            return []
