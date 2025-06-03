#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tải lên Google Drive
"""

import os
import logging
import mimetypes
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleDriveUploader:
    """
    Lớp để tải tệp lên Google Drive
    """

    def __init__(self, credentials_file, folder_id):
        """
        Khởi tạo đối tượng GoogleDriveUploader

        Args:
            credentials_file (str): Đường dẫn đến file credentials Google API
            folder_id (str): ID thư mục Google Drive để lưu tệp
        """
        self.logger = logging.getLogger(__name__)
        self.credentials_file = credentials_file
        self.folder_id = folder_id

    def _get_service(self):
        """
        Tạo dịch vụ Google Drive API

        Returns:
            service: Dịch vụ Google Drive API hoặc None nếu có lỗi
        """
        try:
            scopes = ['https://www.googleapis.com/auth/drive.file']
            credentials = Credentials.from_service_account_file(
                self.credentials_file, scopes=scopes)
            service = build('drive', 'v3', credentials=credentials)
            return service
        except Exception as e:
            self.logger.error(f"Lỗi khi kết nối với Google Drive API: {e}")
            return None

    def upload(self, file_path, description):
        """
        Tải tệp lên Google Drive

        Args:
            file_path (str): Đường dẫn đến tệp cần tải lên
            description (str): Mô tả tệp

        Returns:
            str: URL của tệp trên Google Drive hoặc None nếu có lỗi
        """
        try:
            service = self._get_service()
            if not service:
                return None

            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type is None:
                # Nếu không thể đoán mime_type, sử dụng loại mặc định dựa trên phần mở rộng
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.png':
                    mime_type = 'image/png'
                elif ext == '.jpg' or ext == '.jpeg':
                    mime_type = 'image/jpeg'
                elif ext == '.gif':
                    mime_type = 'image/gif'
                elif ext == '.mp3':
                    mime_type = 'audio/mpeg'
                else:
                    mime_type = 'application/octet-stream'

            file_metadata = {
                'name': file_name,
                'description': description,
                'parents': [self.folder_id]
            }

            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                resumable=True
            )

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()

            # Thiết lập quyền để mọi người có thể xem
            service.permissions().create(
                fileId=file.get('id'),
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()

            self.logger.info(f"Tệp đã được tải lên Google Drive: {file.get('webViewLink')}")

            return file.get('webViewLink')

        except Exception as e:
            self.logger.error(f"Lỗi khi tải lên Google Drive: {e}")
            self.logger.error(f"Error uploading to Google Drive: {e}")
            return None
