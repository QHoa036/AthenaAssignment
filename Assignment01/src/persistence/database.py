#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module quản lý cơ sở dữ liệu
"""

import sqlite3
import logging
import os
from datetime import datetime

class DatabaseManager:
    """
    Lớp quản lý cơ sở dữ liệu để ghi log các tác vụ
    """

    def __init__(self, db_path):
        """
        Khởi tạo đối tượng DatabaseManager

        Args:
            db_path (str): Đường dẫn đến file cơ sở dữ liệu
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path

        # Đảm bảo thư mục chứa cơ sở dữ liệu tồn tại
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Khởi tạo cơ sở dữ liệu nếu chưa tồn tại
        self._init_db()

    def _init_db(self):
        """
        Khởi tạo cơ sở dữ liệu với các bảng cần thiết
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tạo bảng logs nếu chưa tồn tại
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                description TEXT NOT NULL,
                output_format TEXT NOT NULL,
                model TEXT NOT NULL,
                status TEXT NOT NULL,
                drive_url TEXT,
                error_message TEXT,
                timestamp DATETIME NOT NULL
            )
            ''')

            conn.commit()
            conn.close()
            self.logger.info("Đã khởi tạo cơ sở dữ liệu")

        except Exception as e:
            self.logger.error(f"Lỗi khi khởi tạo cơ sở dữ liệu: {e}")

    def log_success(self, item_id, description, output_format, model, drive_url):
        """
        Ghi log thành công

        Args:
            item_id (str): ID của mục
            description (str): Mô tả mục
            output_format (str): Định dạng đầu ra
            model (str): Mô hình AI sử dụng
            drive_url (str): URL của tệp trên Google Drive
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO logs (item_id, description, output_format, model, status, drive_url, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, description, output_format, model, 'success', drive_url, datetime.now()))

            conn.commit()
            conn.close()
            self.logger.info(f"Đã ghi log thành công cho mục {item_id}")

        except Exception as e:
            self.logger.error(f"Lỗi khi ghi log thành công: {e}")

    def log_failure(self, item_id, description, output_format, model, error_message):
        """
        Ghi log thất bại

        Args:
            item_id (str): ID của mục
            description (str): Mô tả mục
            output_format (str): Định dạng đầu ra
            model (str): Mô hình AI sử dụng
            error_message (str): Thông báo lỗi
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO logs (item_id, description, output_format, model, status, error_message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, description, output_format, model, 'failure', error_message, datetime.now()))

            conn.commit()
            conn.close()
            self.logger.info(f"Đã ghi log thất bại cho mục {item_id}")

        except Exception as e:
            self.logger.error(f"Lỗi khi ghi log thất bại: {e}")

    def get_logs_by_date(self, date):
        """
        Lấy logs theo ngày

        Args:
            date (datetime.date): Ngày cần lấy logs

        Returns:
            list: Danh sách logs
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Để kết quả trả về dạng dict
            cursor = conn.cursor()

            # Chuyển đổi date thành chuỗi ngày
            date_str = date.strftime('%Y-%m-%d')

            cursor.execute('''
            SELECT * FROM logs
            WHERE date(timestamp) = date(?)
            ORDER BY timestamp
            ''', (date_str,))

            rows = cursor.fetchall()
            logs = [dict(row) for row in rows]

            conn.close()
            return logs

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy logs theo ngày: {e}")
            return []

    def get_success_failure_count_by_date(self, date):
        """
        Lấy số lượng thành công và thất bại theo ngày

        Args:
            date (datetime.date): Ngày cần lấy thống kê

        Returns:
            tuple: (success_count, failure_count)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Chuyển đổi date thành chuỗi ngày
            date_str = date.strftime('%Y-%m-%d')

            # Đếm số lượng thành công
            cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE date(timestamp) = date(?) AND status = 'success'
            ''', (date_str,))
            success_count = cursor.fetchone()[0]

            # Đếm số lượng thất bại
            cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE date(timestamp) = date(?) AND status = 'failure'
            ''', (date_str,))
            failure_count = cursor.fetchone()[0]

            conn.close()
            return (success_count, failure_count)

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thống kê theo ngày: {e}")
            return (0, 0)

    def get_success_failure_count_by_date_range(self, start_date, end_date):
        """
        Lấy số lượng thành công và thất bại theo khoảng ngày

        Args:
            start_date (datetime.date): Ngày bắt đầu
            end_date (datetime.date): Ngày kết thúc

        Returns:
            list: Danh sách tuple (date_str, success_count, failure_count)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Chuyển đổi ngày thành chuỗi
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            cursor.execute('''
            SELECT date(timestamp) as date,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) as failure_count
            FROM logs
            WHERE date(timestamp) BETWEEN date(?) AND date(?)
            GROUP BY date(timestamp)
            ORDER BY date(timestamp)
            ''', (start_date_str, end_date_str))

            stats = cursor.fetchall()
            conn.close()

            return [(row[0], row[1], row[2]) for row in stats]

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thống kê theo khoảng ngày: {e}")
            return []
