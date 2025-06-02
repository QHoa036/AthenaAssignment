#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kiểm thử cho module database
Unit tests for database module
"""

import os
import sys
import unittest
import tempfile
from datetime import datetime, date

# Thêm thư mục gốc vào sys.path để có thể import các module
# Add root directory to sys.path to be able to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """
    Lớp kiểm thử cho DatabaseManager
    Test class for DatabaseManager
    """

    def setUp(self):
        """
        Chuẩn bị trước mỗi kiểm thử
        Setup before each test
        """
        # Tạo cơ sở dữ liệu tạm cho kiểm thử
        # Create temporary database for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        self.db_manager = DatabaseManager(self.test_db_path)

    def tearDown(self):
        """
        Dọn dẹp sau mỗi kiểm thử
        Clean up after each test
        """
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)

    def test_log_success(self):
        """
        Kiểm thử ghi log thành công
        Test logging success
        """
        # Ghi log thành công
        # Log success
        self.db_manager.log_success(
            item_id="test_id",
            description="Test description",
            output_format="png",
            model="openai",
            drive_url="https://drive.google.com/test"
        )

        # Lấy logs
        # Get logs
        today = datetime.now().date()
        logs = self.db_manager._fetch_daily_logs(today)

        # Kiểm tra
        # Check
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['item_id'], "test_id")
        self.assertEqual(logs[0]['status'], "success")
        self.assertEqual(logs[0]['drive_url'], "https://drive.google.com/test")

    def test_log_failure(self):
        """
        Kiểm thử ghi log thất bại
        Test logging failure
        """
        # Ghi log thất bại
        # Log failure
        self.db_manager.log_failure(
            item_id="test_id",
            description="Test description",
            output_format="png",
            model="openai",
            error_message="Test error"
        )

        # Lấy logs
        # Get logs
        today = datetime.now().date()
        logs = self.db_manager._fetch_daily_logs(today)

        # Kiểm tra
        # Check
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['item_id'], "test_id")
        self.assertEqual(logs[0]['status'], "failure")
        self.assertEqual(logs[0]['error_message'], "Test error")

    def test_get_stats(self):
        """
        Kiểm thử lấy thống kê
        Test getting statistics
        """
        # Ghi log thành công và thất bại
        # Log success and failure
        self.db_manager.log_success(
            item_id="test_success_1",
            description="Test success 1",
            output_format="png",
            model="openai",
            drive_url="https://drive.google.com/test1"
        )

        self.db_manager.log_success(
            item_id="test_success_2",
            description="Test success 2",
            output_format="jpg",
            model="claude",
            drive_url="https://drive.google.com/test2"
        )

        self.db_manager.log_failure(
            item_id="test_failure_1",
            description="Test failure 1",
            output_format="gif",
            model="openai",
            error_message="Test error 1"
        )

        # Lấy thống kê
        # Get statistics
        today = datetime.now().date()
        stats = self.db_manager._fetch_daily_stats(today)

        # Kiểm tra
        # Check
        self.assertIsNotNone(stats)
        self.assertEqual(stats['total_count'], 3)
        self.assertEqual(stats['success_count'], 2)
        self.assertEqual(stats['failure_count'], 1)
        self.assertAlmostEqual(stats['success_rate'], 66.67, delta=0.01)


if __name__ == "__main__":
    unittest.main()
