#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo báo cáo HTML
Module for generating HTML reports
"""

import os
import logging
from datetime import datetime
import jinja2

class HTMLReportGenerator:
    """
    Lớp tạo báo cáo HTML từ dữ liệu
    Class for generating HTML reports from data
    """
    
    def __init__(self):
        """
        Khởi tạo đối tượng HTMLReportGenerator
        Initialize HTMLReportGenerator object
        """
        self.logger = logging.getLogger(__name__)
        
        # Tạo môi trường Jinja2
        # Create Jinja2 environment
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__))),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Tạo các template mặc định
        # Create default templates
        self._create_default_templates()
    
    def _create_default_templates(self):
        """
        Tạo các template mặc định
        Create default templates
        """
        # Template cho báo cáo hàng ngày
        # Template for daily report
        daily_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Báo cáo hàng ngày - {{ date }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        .stats-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }
        .stats-box {
            flex: 1;
            margin: 0 10px;
            padding: 15px;
            background: #fff;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
            text-align: center;
        }
        .success {
            border-top: 4px solid #2ecc71;
        }
        .failure {
            border-top: 4px solid #e74c3c;
        }
        .total {
            border-top: 4px solid #3498db;
        }
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .status-success {
            color: #2ecc71;
            font-weight: bold;
        }
        .status-failure {
            color: #e74c3c;
            font-weight: bold;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Báo cáo hàng ngày / Daily Report</h1>
            <h2>{{ date }}</h2>
        </div>
        
        <div class="stats-container">
            <div class="stats-box total">
                <h3>Tổng số / Total</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ stats.total_count }}</p>
            </div>
            <div class="stats-box success">
                <h3>Thành công / Success</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ stats.success_count }} ({{ "%.1f"|format(stats.success_rate) }}%)</p>
            </div>
            <div class="stats-box failure">
                <h3>Thất bại / Failure</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ stats.failure_count }} ({{ "%.1f"|format(stats.failure_rate) }}%)</p>
            </div>
        </div>
        
        <div class="chart-container">
            <h2>Biểu đồ phân tích / Analytics Chart</h2>
            <img src="charts/{{ chart_filename }}" alt="Biểu đồ phân tích">
        </div>
        
        <h2>Chi tiết các mục / Item Details</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Mô tả / Description</th>
                    <th>Định dạng / Format</th>
                    <th>Mô hình / Model</th>
                    <th>Trạng thái / Status</th>
                    <th>Liên kết / Link</th>
                </tr>
            </thead>
            <tbody>
                {% for item in logs %}
                <tr>
                    <td>{{ item.item_id }}</td>
                    <td>{{ item.description }}</td>
                    <td>{{ item.output_format }}</td>
                    <td>{{ item.model }}</td>
                    <td class="status-{{ item.status }}">{{ item.status|upper }}</td>
                    <td>
                        {% if item.drive_url %}
                        <a href="{{ item.drive_url }}" target="_blank">Google Drive</a>
                        {% elif item.error_message %}
                        {{ item.error_message|truncate(50) }}
                        {% else %}
                        -
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <footer>
            <p>Báo cáo được tạo tự động vào {{ timestamp }}</p>
            <p>Report automatically generated at {{ timestamp }}</p>
        </footer>
    </div>
</body>
</html>"""
        
        # Template cho báo cáo hàng tuần
        # Template for weekly report
        weekly_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Báo cáo hàng tuần - {{ start_date }} - {{ end_date }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .progress-container {
            background-color: #e0e0e0;
            border-radius: 8px;
            height: 20px;
            margin: 10px 0;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background-color: #2ecc71;
            border-radius: 8px;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Báo cáo hàng tuần / Weekly Report</h1>
            <h2>{{ start_date }} đến / to {{ end_date }}</h2>
        </div>
        
        <div class="chart-container">
            <h2>Biểu đồ phân tích / Analytics Chart</h2>
            <img src="charts/{{ chart_filename }}" alt="Biểu đồ phân tích tuần">
        </div>
        
        <h2>Tóm tắt theo ngày / Daily Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Ngày / Date</th>
                    <th>Tổng số / Total</th>
                    <th>Thành công / Success</th>
                    <th>Thất bại / Failure</th>
                    <th>Tỷ lệ / Rate</th>
                </tr>
            </thead>
            <tbody>
                {% for day in daily_stats %}
                <tr>
                    <td>{{ day.date }}</td>
                    <td>{{ day.total_count }}</td>
                    <td>{{ day.success_count }}</td>
                    <td>{{ day.failure_count }}</td>
                    <td>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {{ day.success_rate }}%"></div>
                        </div>
                        {{ "%.1f"|format(day.success_rate) }}%
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <footer>
            <p>Báo cáo được tạo tự động vào {{ timestamp }}</p>
            <p>Report automatically generated at {{ timestamp }}</p>
        </footer>
    </div>
</body>
</html>"""
        
        # Lưu các template mặc định
        # Save default templates
        template_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            with open(os.path.join(template_dir, "daily_report_template.html"), "w") as f:
                f.write(daily_template)
                
            with open(os.path.join(template_dir, "weekly_report_template.html"), "w") as f:
                f.write(weekly_template)
                
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo template mặc định: {e}")
            self.logger.error(f"Error creating default templates: {e}")
    
    def generate_daily_report(self, output_path, date, stats, logs, chart_filename):
        """
        Tạo báo cáo HTML hàng ngày
        Generate daily HTML report
        
        Args:
            output_path (str): Đường dẫn đến file báo cáo đầu ra
                             Path to output report file
            date (datetime.date): Ngày tạo báo cáo
                                 Date to create report for
            stats (dict): Dữ liệu thống kê
                        Statistics data
            logs (list): Danh sách logs
                      List of logs
            chart_filename (str): Tên file biểu đồ
                                Chart filename
        """
        try:
            template = self.template_env.get_template("daily_report_template.html")
            
            # Tạo dữ liệu ngữ cảnh cho template
            # Create context data for template
            context = {
                "date": date.strftime("%Y-%m-%d"),
                "stats": stats,
                "logs": logs,
                "chart_filename": chart_filename,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Render template
            html_content = template.render(**context)
            
            # Lưu file báo cáo
            # Save report file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            self.logger.info(f"Đã tạo báo cáo HTML hàng ngày: {output_path}")
            self.logger.info(f"Daily HTML report generated: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo HTML hàng ngày: {e}")
            self.logger.error(f"Error generating daily HTML report: {e}")
    
    def generate_weekly_report(self, output_path, start_date, end_date, daily_stats, chart_filename):
        """
        Tạo báo cáo HTML hàng tuần
        Generate weekly HTML report
        
        Args:
            output_path (str): Đường dẫn đến file báo cáo đầu ra
                             Path to output report file
            start_date (datetime.date): Ngày bắt đầu
                                      Start date
            end_date (datetime.date): Ngày kết thúc
                                    End date
            daily_stats (list): Danh sách thống kê theo ngày
                              List of daily statistics
            chart_filename (str): Tên file biểu đồ
                                Chart filename
        """
        try:
            template = self.template_env.get_template("weekly_report_template.html")
            
            # Tạo dữ liệu ngữ cảnh cho template
            # Create context data for template
            context = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "daily_stats": daily_stats,
                "chart_filename": chart_filename,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Render template
            html_content = template.render(**context)
            
            # Lưu file báo cáo
            # Save report file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            self.logger.info(f"Đã tạo báo cáo HTML hàng tuần: {output_path}")
            self.logger.info(f"Weekly HTML report generated: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo HTML hàng tuần: {e}")
            self.logger.error(f"Error generating weekly HTML report: {e}")
