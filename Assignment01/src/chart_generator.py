#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo biểu đồ cho báo cáo
Module for generating charts for reports
"""

import os
import logging
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Đảm bảo không cần GUI / Ensure no GUI needed
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import numpy as np

class ChartGenerator:
    """
    Lớp tạo biểu đồ cho báo cáo
    Class for generating charts for reports
    """
    
    def __init__(self, output_dir):
        """
        Khởi tạo đối tượng ChartGenerator
        Initialize ChartGenerator object
        
        Args:
            output_dir (str): Thư mục lưu biểu đồ đầu ra
                             Output directory for charts
        """
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        
        # Đảm bảo thư mục đầu ra tồn tại
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Thư mục lưu biểu đồ
        # Directory to store charts
        self.charts_dir = os.path.join(output_dir, "charts")
        os.makedirs(self.charts_dir, exist_ok=True)
        
        # Thiết lập style cho biểu đồ
        # Set chart style
        plt.style.use('ggplot')
    
    def generate_daily_chart(self, date, success_count, failure_count):
        """
        Tạo biểu đồ thống kê hàng ngày
        Generate daily statistics chart
        
        Args:
            date (datetime.date): Ngày tạo biểu đồ
                                 Date to create chart for
            success_count (int): Số lượng thành công
                               Number of successes
            failure_count (int): Số lượng thất bại
                               Number of failures
        
        Returns:
            str: Đường dẫn đến file biểu đồ
                Path to chart file
        """
        try:
            # Tạo dữ liệu
            # Create data
            categories = ['Thành công / Success', 'Thất bại / Failure']
            counts = [success_count, failure_count]
            colors = ['#2ecc71', '#e74c3c']
            
            # Tạo biểu đồ
            # Create chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
            
            # Biểu đồ cột
            # Bar chart
            ax1.bar(categories, counts, color=colors)
            ax1.set_title(f'Thống kê ngày / Daily Statistics: {date.strftime("%Y-%m-%d")}', fontsize=14)
            ax1.set_ylabel('Số lượng / Count', fontsize=12)
            
            # Thêm số liệu lên biểu đồ cột
            # Add numbers to bar chart
            for i, v in enumerate(counts):
                ax1.text(i, v + 0.1, str(v), ha='center', fontsize=12, fontweight='bold')
            
            # Biểu đồ tròn
            # Pie chart
            if sum(counts) > 0:  # Tránh chia cho 0 / Avoid dividing by zero
                ax2.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors, shadow=True)
                ax2.set_title(f'Tỷ lệ % / Percentage: {date.strftime("%Y-%m-%d")}', fontsize=14)
            else:
                ax2.text(0.5, 0.5, "Không có dữ liệu / No data", ha='center', va='center', fontsize=14)
                ax2.axis('off')
            
            plt.tight_layout()
            
            # Lưu biểu đồ
            # Save chart
            chart_filename = f"daily_chart_{date.strftime('%Y%m%d')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100)
            plt.close(fig)
            
            self.logger.info(f"Đã tạo biểu đồ hàng ngày: {chart_path}")
            self.logger.info(f"Daily chart generated: {chart_path}")
            
            return chart_path
            
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo biểu đồ hàng ngày: {e}")
            self.logger.error(f"Error generating daily chart: {e}")
            return None
    
    def generate_weekly_chart(self, start_date, end_date, stats_data):
        """
        Tạo biểu đồ thống kê hàng tuần
        Generate weekly statistics chart
        
        Args:
            start_date (datetime.date): Ngày bắt đầu
                                      Start date
            end_date (datetime.date): Ngày kết thúc
                                    End date
            stats_data (list): Danh sách thống kê theo ngày
                             List of daily statistics
        
        Returns:
            str: Đường dẫn đến file biểu đồ
                Path to chart file
        """
        try:
            if not stats_data:
                self.logger.warning(f"Không có dữ liệu để tạo biểu đồ từ {start_date} đến {end_date}")
                self.logger.warning(f"No data to generate chart from {start_date} to {end_date}")
                return None
            
            # Chuẩn bị dữ liệu
            # Prepare data
            dates = []
            success_counts = []
            failure_counts = []
            
            for stat in stats_data:
                dates.append(datetime.strptime(stat['date'], '%Y-%m-%d').date())
                success_counts.append(stat['success_count'])
                failure_counts.append(stat['failure_count'])
            
            # Tạo biểu đồ
            # Create charts
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # Biểu đồ cột chồng lên nhau
            # Stacked bar chart
            width = 0.35
            ax1.bar(dates, success_counts, width, label='Thành công / Success', color='#2ecc71')
            ax1.bar(dates, failure_counts, width, bottom=success_counts, label='Thất bại / Failure', color='#e74c3c')
            
            # Định dạng trục x
            # Format x-axis
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")
            
            # Đặt tiêu đề và nhãn
            # Set titles and labels
            title_period = f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}"
            ax1.set_title(f'Số lượng theo ngày / Daily Counts: {title_period}', fontsize=14)
            ax1.set_ylabel('Số lượng / Count', fontsize=12)
            ax1.legend()
            
            # Biểu đồ đường cho tỷ lệ thành công
            # Line chart for success rates
            success_rates = [stat['success_rate'] for stat in stats_data]
            ax2.plot(dates, success_rates, marker='o', linestyle='-', color='#3498db', linewidth=2, markersize=8)
            
            # Định dạng trục x
            # Format x-axis
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
            
            # Đặt tiêu đề và nhãn
            # Set titles and labels
            ax2.set_title(f'Tỷ lệ thành công theo ngày / Daily Success Rate: {title_period}', fontsize=14)
            ax2.set_ylabel('Tỷ lệ % / Rate %', fontsize=12)
            ax2.set_ylim(0, 100)
            
            # Thêm grid
            # Add grid
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax2.grid(True, linestyle='--', alpha=0.7)
            
            plt.tight_layout()
            
            # Lưu biểu đồ
            # Save chart
            chart_filename = f"weekly_chart_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100)
            plt.close(fig)
            
            self.logger.info(f"Đã tạo biểu đồ hàng tuần: {chart_path}")
            self.logger.info(f"Weekly chart generated: {chart_path}")
            
            return chart_path
            
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo biểu đồ hàng tuần: {e}")
            self.logger.error(f"Error generating weekly chart: {e}")
            return None
            
    def generate_format_distribution_chart(self, stats_data):
        """
        Tạo biểu đồ phân phối theo định dạng đầu ra
        Generate output format distribution chart
        
        Args:
            stats_data (dict): Dữ liệu thống kê theo định dạng
                             Statistics data by format
        
        Returns:
            str: Đường dẫn đến file biểu đồ
                Path to chart file
        """
        try:
            if not stats_data or not stats_data.get('format_stats'):
                self.logger.warning("Không có dữ liệu định dạng để tạo biểu đồ")
                self.logger.warning("No format data to generate chart")
                return None
            
            format_stats = stats_data['format_stats']
            
            # Chuẩn bị dữ liệu
            # Prepare data
            formats = list(format_stats.keys())
            counts = list(format_stats.values())
            
            # Màu sắc theo định dạng
            # Colors by format
            format_colors = {
                'png': '#3498db',   # Xanh dương / Blue
                'jpg': '#2ecc71',   # Xanh lá / Green
                'gif': '#e67e22',   # Cam / Orange
                'mp3': '#9b59b6',   # Tím / Purple
            }
            
            colors = [format_colors.get(fmt, '#95a5a6') for fmt in formats]
            
            # Tạo biểu đồ
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 7))
            
            ax.pie(counts, labels=formats, autopct='%1.1f%%', startangle=90, colors=colors, shadow=True)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            plt.title('Phân phối định dạng đầu ra / Output Format Distribution', fontsize=14)
            
            # Lưu biểu đồ
            # Save chart
            date_str = datetime.now().strftime('%Y%m%d')
            chart_filename = f"format_distribution_{date_str}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100)
            plt.close(fig)
            
            self.logger.info(f"Đã tạo biểu đồ phân phối định dạng: {chart_path}")
            self.logger.info(f"Format distribution chart generated: {chart_path}")
            
            return chart_path
            
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo biểu đồ phân phối định dạng: {e}")
            self.logger.error(f"Error generating format distribution chart: {e}")
            return None
