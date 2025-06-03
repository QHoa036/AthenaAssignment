#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo báo cáo từ dữ liệu trong cơ sở dữ liệu
"""

import os
import logging
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

from .chart_generator import ChartGenerator
from .html_report_generator import HTMLReportGenerator

class ReportGenerator:
    """
    Lớp tạo báo cáo từ dữ liệu trong cơ sở dữ liệu
    """

    def __init__(self, db_path, output_dir):
        """
        Khởi tạo đối tượng ReportGenerator

        Args:
            db_path (str): Đường dẫn đến file cơ sở dữ liệu
            output_dir (str): Thư mục lưu báo cáo đầu ra
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path
        self.output_dir = output_dir

        # Đảm bảo thư mục đầu ra tồn tại
        os.makedirs(output_dir, exist_ok=True)

        # Khởi tạo các đối tượng tạo biểu đồ và HTML
        self.chart_generator = ChartGenerator(output_dir)
        self.html_generator = HTMLReportGenerator()

    def generate_daily_report(self, date=None):
        """
        Tạo báo cáo hàng ngày

        Args:
            date (datetime.date, optional): Ngày tạo báo cáo. Mặc định là hôm nay.

        Returns:
            str: Đường dẫn đến file báo cáo
        """
        try:
            # Nếu không có ngày được chỉ định, sử dụng ngày hôm nay
            if date is None:
                date = datetime.now().date()

            self.logger.info(f"Tạo báo cáo hàng ngày cho {date}")

            # Lấy dữ liệu từ cơ sở dữ liệu
            daily_logs = self._fetch_daily_logs(date)
            daily_stats = self._fetch_daily_stats(date)

            if not daily_stats:
                self.logger.warning(f"Không có dữ liệu để tạo báo cáo cho {date}")
                self.logger.warning(f"No data to generate report for {date}")
                return None

            # Tạo biểu đồ thống kê
            chart_path = self.chart_generator.generate_daily_chart(
                date,
                daily_stats['success_count'],
                daily_stats['failure_count']
            )

            # Tạo báo cáo HTML
            report_filename = f"report_{date.strftime('%Y%m%d')}.html"
            report_path = os.path.join(self.output_dir, report_filename)

            self.html_generator.generate_daily_report(
                report_path,
                date,
                daily_stats,
                daily_logs,
                os.path.basename(chart_path)
            )

            self.logger.info(f"Đã tạo báo cáo hàng ngày: {report_path}")
            self.logger.info(f"Daily report generated: {report_path}")

            return report_path

        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo hàng ngày: {e}")
            return None

    def generate_weekly_report(self, end_date=None):
        """
        Tạo báo cáo hàng tuần

        Args:
            end_date (datetime.date, optional): Ngày kết thúc của tuần. Mặc định là hôm nay.

        Returns:
            str: Đường dẫn đến file báo cáo
        """
        try:
            # Nếu không có ngày kết thúc được chỉ định, sử dụng ngày hôm nay
            if end_date is None:
                end_date = datetime.now().date()

            # Tính ngày bắt đầu (7 ngày trước ngày kết thúc)
            start_date = end_date - timedelta(days=6)

            self.logger.info(f"Tạo báo cáo hàng tuần từ {start_date} đến {end_date}")

            # Lấy dữ liệu từ cơ sở dữ liệu
            weekly_stats = self._fetch_date_range_stats(start_date, end_date)

            if not weekly_stats:
                self.logger.warning(f"Không có dữ liệu để tạo báo cáo từ {start_date} đến {end_date}")
                return None

            # Tạo biểu đồ thống kê
            chart_path = self.chart_generator.generate_weekly_chart(
                start_date,
                end_date,
                weekly_stats
            )

            # Tạo báo cáo HTML
            report_filename = f"weekly_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.html"
            report_path = os.path.join(self.output_dir, report_filename)

            self.html_generator.generate_weekly_report(
                report_path,
                start_date,
                end_date,
                weekly_stats,
                os.path.basename(chart_path)
            )

            self.logger.info(f"Đã tạo báo cáo hàng tuần: {report_path}")

            return report_path

        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo hàng tuần: {e}")
            return None

    def _fetch_daily_logs(self, date):
        """
        Lấy logs hàng ngày từ cơ sở dữ liệu

        Args:
            date (datetime.date): Ngày cần lấy logs

        Returns:
            list: Danh sách logs
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
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
            self.logger.error(f"Lỗi khi lấy logs hàng ngày: {e}")
            return []

    def _fetch_daily_stats(self, date):
        """
        Lấy thống kê hàng ngày từ cơ sở dữ liệu

        Args:
            date (datetime.date): Ngày cần lấy thống kê

        Returns:
            dict: Từ điển chứa thông tin thống kê
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Chuyển đổi date thành chuỗi ngày
            date_str = date.strftime('%Y-%m-%d')

            # Đếm tổng số mục
            # Count total items
            cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE date(timestamp) = date(?)
            ''', (date_str,))
            total_count = cursor.fetchone()[0]

            # Nếu không có dữ liệu, trả về None
            # If no data, return None
            if total_count == 0:
                conn.close()
                return None

            # Đếm số lượng thành công
            # Count successes
            cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE date(timestamp) = date(?) AND status = 'success'
            ''', (date_str,))
            success_count = cursor.fetchone()[0]

            # Đếm số lượng thất bại
            # Count failures
            cursor.execute('''
            SELECT COUNT(*) FROM logs
            WHERE date(timestamp) = date(?) AND status = 'failure'
            ''', (date_str,))
            failure_count = cursor.fetchone()[0]

            # Thống kê theo định dạng
            cursor.execute('''
            SELECT output_format, COUNT(*) as count
            FROM logs
            WHERE date(timestamp) = date(?)
            GROUP BY output_format
            ''', (date_str,))
            format_stats = {row[0]: row[1] for row in cursor.fetchall()}

            # Thống kê theo mô hình
            cursor.execute('''
            SELECT model, COUNT(*) as count
            FROM logs
            WHERE date(timestamp) = date(?)
            GROUP BY model
            ''', (date_str,))
            model_stats = {row[0]: row[1] for row in cursor.fetchall()}

            conn.close()

            stats = {
                'date': date_str,
                'total_count': total_count,
                'success_count': success_count,
                'failure_count': failure_count,
                'success_rate': (success_count / total_count) * 100 if total_count > 0 else 0,
                'failure_rate': (failure_count / total_count) * 100 if total_count > 0 else 0,
                'format_stats': format_stats,
                'model_stats': model_stats
            }

            return stats

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thống kê hàng ngày: {e}")
            return None

    def _fetch_date_range_stats(self, start_date, end_date):
        """
        Lấy thống kê theo khoảng ngày từ cơ sở dữ liệu

        Args:
            start_date (datetime.date): Ngày bắt đầu
            end_date (datetime.date): Ngày kết thúc

        Returns:
            list: Danh sách từ điển chứa thông tin thống kê theo ngày
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Chuyển đổi ngày thành chuỗi
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # Lấy thống kê theo ngày
            cursor.execute('''
            SELECT
                date(timestamp) as date,
                COUNT(*) as total_count,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) as failure_count
            FROM logs
            WHERE date(timestamp) BETWEEN date(?) AND date(?)
            GROUP BY date(timestamp)
            ORDER BY date(timestamp)
            ''', (start_date_str, end_date_str))

            rows = cursor.fetchall()

            if not rows:
                conn.close()
                return []

            stats = []
            for row in rows:
                date_str, total_count, success_count, failure_count = row

                stats.append({
                    'date': date_str,
                    'total_count': total_count,
                    'success_count': success_count,
                    'failure_count': failure_count,
                    'success_rate': (success_count / total_count) * 100 if total_count > 0 else 0,
                    'failure_rate': (failure_count / total_count) * 100 if total_count > 0 else 0
                })

            conn.close()
            return stats

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thống kê theo khoảng ngày: {e}")
            return []
