#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo báo cáo HTML
"""

import os
import logging
import shutil
from datetime import datetime
import jinja2

class HTMLReportGenerator:
    """
    Lớp tạo báo cáo HTML từ dữ liệu
    """

    def __init__(self):
        """
        Khởi tạo đối tượng HTMLReportGenerator
        """
        self.logger = logging.getLogger(__name__)

        # Tạo môi trường Jinja2 sử dụng thư mục templates
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    def generate_custom_report(self, title, sections, output_path, chart_path=None):
        """
        Tạo báo cáo HTML tùy chỉnh với các phần được cung cấp

        Args:
            title (str): Tiêu đề báo cáo
            sections (list): Danh sách các phần, mỗi phần là một dict với:
                - title: tiêu đề phần
                - content: nội dung phần (text hoặc HTML)
                - data_table: (tùy chọn) dữ liệu bảng dạng dict với keys 'headers' và 'rows'
            output_path (str): Đường dẫn đến file đầu ra
            chart_path (str, optional): Đường dẫn đến biểu đồ

        Returns:
            str: Đường dẫn đến file báo cáo HTML đã tạo hoặc None nếu có lỗi
        """
        try:
            # Đảm bảo đường dẫn có đuôi .html
            if not output_path.lower().endswith('.html'):
                output_path = f"{os.path.splitext(output_path)[0]}.html"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Chuẩn bị dữ liệu cho template
            data = {
                'title': title,
                'sections': sections,
                'timestamp': datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            }
            
            # Xử lý biểu đồ nếu có
            if chart_path:
                # Copy biểu đồ vào thư mục charts (tạo nếu chưa có)
                charts_dir = os.path.join(os.path.dirname(output_path), 'charts')
                os.makedirs(charts_dir, exist_ok=True)
                
                chart_filename = os.path.basename(chart_path)
                chart_dest = os.path.join(charts_dir, chart_filename)
                
                # Copy file nếu cần
                if os.path.exists(chart_path) and chart_path != chart_dest:
                    shutil.copy2(chart_path, chart_dest)
                
                data['chart_path'] = f"charts/{chart_filename}"
            
            # Tạo template tùy chỉnh cho báo cáo
            custom_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{{ title }}</title>
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
                    .section {
                        margin-bottom: 30px;
                        padding: 15px;
                        background: #fff;
                        border-radius: 5px;
                        box-shadow: 0 0 5px rgba(0,0,0,0.05);
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
                        <h1>{{ title }}</h1>
                    </div>
                    
                    {% if chart_path is defined %}
                    <div class="chart-container">
                        <h2>Biểu đồ phân tích / Analytics Chart</h2>
                        <img src="{{ chart_path }}" alt="Biểu đồ phân tích">
                    </div>
                    {% endif %}
                    
                    {% for section in sections %}
                    <div class="section">
                        <h2>{{ section.title }}</h2>
                        
                        {% if section.content %}
                        <div class="content">
                            {{ section.content|safe }}
                        </div>
                        {% endif %}
                        
                        {% if section.data_table %}
                        <table>
                            <thead>
                                <tr>
                                {% for header in section.data_table.headers %}
                                    <th>{{ header }}</th>
                                {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in section.data_table.rows %}
                                <tr>
                                    {% for cell in row %}
                                    <td>{{ cell }}</td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        {% endif %}
                    </div>
                    {% endfor %}
                    
                    <footer>
                        <p>Báo cáo được tạo tự động vào {{ timestamp }}</p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            template = jinja2.Template(custom_template)
            html_content = template.render(**data)
            
            # Ghi file HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Báo cáo HTML tùy chỉnh đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo HTML tùy chỉnh: {str(e)}")
            return None


    def generate_daily_report(self, data, output_path, chart_path=None):
        """
        Tạo báo cáo hàng ngày và lưu vào file HTML

        Args:
            data (dict): Dữ liệu cho báo cáo
            output_path (str): Đường dẫn đến file đầu ra (HTML)
            chart_path (str, optional): Đường dẫn đến biểu đồ

        Returns:
            str: Đường dẫn đến file báo cáo HTML
        """
        try:
            # Đảm bảo đường dẫn có đuôi .html
            if not output_path.lower().endswith('.html'):
                output_path = f"{os.path.splitext(output_path)[0]}.html"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Thêm dữ liệu ngày và thời gian
            if 'date' not in data:
                data['date'] = datetime.now().strftime('%d/%m/%Y')
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            
            # Xử lý biểu đồ nếu có
            if chart_path:
                # Copy biểu đồ vào thư mục charts (tạo nếu chưa có)
                charts_dir = os.path.join(os.path.dirname(output_path), 'charts')
                os.makedirs(charts_dir, exist_ok=True)
                
                chart_filename = os.path.basename(chart_path)
                chart_dest = os.path.join(charts_dir, chart_filename)
                
                # Copy file nếu cần
                if os.path.exists(chart_path) and chart_path != chart_dest:
                    shutil.copy2(chart_path, chart_dest)
                
                data['chart_path'] = f"charts/{chart_filename}"
            
            # Render template
            template = self.template_env.get_template('daily_report.html')
            html_content = template.render(**data)
            
            # Ghi file HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Báo cáo HTML hàng ngày đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo HTML hàng ngày: {str(e)}")
            return None

    def generate_weekly_report(self, data, output_path, chart_path=None):
        """
        Tạo báo cáo hàng tuần và lưu vào file HTML

        Args:
            data (dict): Dữ liệu cho báo cáo
            output_path (str): Đường dẫn đến file đầu ra (HTML)
            chart_path (str, optional): Đường dẫn đến biểu đồ

        Returns:
            str: Đường dẫn đến file báo cáo HTML
        """
        try:
            # Đảm bảo đường dẫn có đuôi .html
            if not output_path.lower().endswith('.html'):
                output_path = f"{os.path.splitext(output_path)[0]}.html"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Kiểm tra dữ liệu ngày
            if 'start_date' not in data or 'end_date' not in data:
                self.logger.error("Thiếu dữ liệu ngày bắt đầu hoặc ngày kết thúc cho báo cáo tuần")
                return None
            
            # Thêm dữ liệu thời gian
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            
            # Xử lý biểu đồ nếu có
            if chart_path:
                # Copy biểu đồ vào thư mục charts (tạo nếu chưa có)
                charts_dir = os.path.join(os.path.dirname(output_path), 'charts')
                os.makedirs(charts_dir, exist_ok=True)
                
                chart_filename = os.path.basename(chart_path)
                chart_dest = os.path.join(charts_dir, chart_filename)
                
                # Copy file nếu cần
                if os.path.exists(chart_path) and chart_path != chart_dest:
                    shutil.copy2(chart_path, chart_dest)
                
                data['chart_filename'] = chart_filename
            
            # Mặc định trường daily_stats nếu chưa có
            data.setdefault('daily_stats', [])
            
            # Render template
            template = self.template_env.get_template('weekly_report.html')
            html_content = template.render(**data)
            
            # Ghi file HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Báo cáo HTML hàng tuần đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo HTML hàng tuần: {str(e)}")
            return None
            
    def export_data_to_file(self, data, output_path, format_type='json'):
        """
        Xuất dữ liệu báo cáo ra file

        Args:
            data (dict): Dữ liệu cần xuất
            output_path (str): Đường dẫn đến file đầu ra
            format_type (str, optional): Định dạng file (json hoặc xml). Mặc định là 'json'

        Returns:
            str: Đường dẫn đến file đã tạo hoặc None nếu có lỗi
        """
        try:
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Đặt đuôi file phù hợp
            format_type = format_type.lower()
            if format_type == 'json':
                if not output_path.lower().endswith('.json'):
                    output_path = f"{os.path.splitext(output_path)[0]}.json"
                    
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
            elif format_type == 'xml':
                if not output_path.lower().endswith('.xml'):
                    output_path = f"{os.path.splitext(output_path)[0]}.xml"
                
                try:
                    from dicttoxml import dicttoxml
                    xml_data = dicttoxml(data, custom_root='report', attr_type=False)
                    
                    with open(output_path, 'wb') as f:
                        f.write(xml_data)
                except ImportError:
                    self.logger.error("Lỗi: Thư viện dicttoxml chưa được cài đặt. Sử dụng 'pip install dicttoxml'")
                    return None
            else:
                self.logger.error(f"Định dạng không được hỗ trợ: {format_type}. Hỗ trợ: json, xml")
                return None
                
            self.logger.info(f"Dữ liệu đã được xuất ra file {format_type}: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xuất dữ liệu ra file: {str(e)}")
            return None
