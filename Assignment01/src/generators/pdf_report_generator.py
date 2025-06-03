#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module tạo báo cáo PDF sử dụng ReportLab
"""

import os
import logging
import json
from datetime import datetime
import jinja2
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFReportGenerator:
    """
    Lớp tạo báo cáo PDF từ dữ liệu sử dụng ReportLab
    """

    def __init__(self):
        """
        Khởi tạo đối tượng PDFReportGenerator
        """
        self.logger = logging.getLogger(__name__)

        # Cấu hình styles cho ReportLab
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'Title', 
            parent=self.styles['Heading1'],
            fontSize=18,
            alignment=1,  # Center alignment
            spaceAfter=12
        )
        self.heading_style = ParagraphStyle(
            'Heading', 
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        )
        self.normal_style = self.styles['Normal']
        
        # Tạo môi trường Jinja2 sử dụng thư mục templates (vẫn giữ lại để truy xuất dữ liệu templates)
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )

    def generate_daily_report(self, data, output_path, chart_path=None):
        """
        Tạo báo cáo hàng ngày và lưu vào file PDF

        Args:
            data (dict): Dữ liệu cho báo cáo
            output_path (str): Đường dẫn đến file đầu ra (PDF)
            chart_path (str, optional): Đường dẫn đến biểu đồ

        Returns:
            str: Đường dẫn đến file báo cáo PDF
        """
        try:
            # Đảm bảo đường dẫn có đuôi .pdf
            if not output_path.lower().endswith('.pdf'):
                output_path = f"{os.path.splitext(output_path)[0]}.pdf"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Thêm dữ liệu ngày và thời gian
            if 'date' not in data:
                data['date'] = datetime.now().strftime('%d/%m/%Y')
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

            # Tạo tài liệu PDF
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            elements = []
            
            # Tiêu đề báo cáo
            elements.append(Paragraph(f"Báo cáo hàng ngày - {data['date']}", self.title_style))
            elements.append(Spacer(1, 20))
            
            # Thông tin tổng quan
            elements.append(Paragraph("Thông tin tổng quan", self.heading_style))
            
            # Bảng thống kê
            stats_data = [
                ["Thông số", "Giá trị"],
                ["Tổng số lượng", str(data.get('total_count', 0))],
                ["Số lượng thành công", str(data.get('success_count', 0))],
                ["Số lượng thất bại", str(data.get('failure_count', 0))],
                ["Tỉ lệ thành công", f"{data.get('success_rate', 0):.1f}%"],
                ["Tỉ lệ thất bại", f"{data.get('failure_rate', 0):.1f}%"]
            ]
            
            stats_table = Table(stats_data, colWidths=[200, 200])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 20))
            
            # Thêm biểu đồ nếu có
            if chart_path and os.path.exists(chart_path):
                chart_image = Image(chart_path, width=400, height=300)
                elements.append(Paragraph("Biểu đồ phân tích", self.heading_style))
                elements.append(chart_image)
                elements.append(Spacer(1, 20))
            
            # Chi tiết logs
            if 'logs' in data and data['logs']:
                elements.append(Paragraph("Chi tiết logs", self.heading_style))
                logs_data = [["Thời gian", "ID", "Trạng thái", "Mô hình", "Định dạng"]]
                
                for log in data['logs']:
                    logs_data.append([
                        log.get('timestamp', ''),
                        log.get('id', ''),
                        log.get('status', ''),
                        log.get('model', ''),
                        log.get('output_format', '')
                    ])
                
                logs_table = Table(logs_data, colWidths=[100, 50, 80, 80, 80])
                logs_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(logs_table)
            
            # Thông tin thời gian tạo báo cáo
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(f"Báo cáo được tạo vào: {data['timestamp']}", self.normal_style))
            
            # Tạo file PDF
            doc.build(elements)
            self.logger.info(f"Báo cáo PDF hàng ngày đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo PDF hàng ngày: {str(e)}")
            return None

    def generate_weekly_report(self, data, output_path, chart_path=None):
        """
        Tạo báo cáo hàng tuần và lưu vào file PDF

        Args:
            data (dict): Dữ liệu cho báo cáo
            output_path (str): Đường dẫn đến file đầu ra (PDF)
            chart_path (str, optional): Đường dẫn đến biểu đồ

        Returns:
            str: Đường dẫn đến file báo cáo PDF
        """
        try:
            # Đảm bảo đường dẫn có đuôi .pdf
            if not output_path.lower().endswith('.pdf'):
                output_path = f"{os.path.splitext(output_path)[0]}.pdf"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Kiểm tra dữ liệu ngày
            if 'start_date' not in data or 'end_date' not in data:
                self.logger.error("Thiếu dữ liệu ngày bắt đầu hoặc ngày kết thúc cho báo cáo tuần")
                return None
            
            # Thêm dữ liệu thời gian
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

            # Tạo tài liệu PDF
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            elements = []
            
            # Tiêu đề báo cáo
            elements.append(Paragraph(
                f"Báo cáo tuần - {data['start_date']} đến {data['end_date']}", 
                self.title_style
            ))
            elements.append(Spacer(1, 20))
            
            # Thông tin tổng quan
            elements.append(Paragraph("Thông tin tổng quan", self.heading_style))
            
            # Bảng tổng hợp
            if 'summary' in data:
                summary_data = [
                    ["Thông số", "Giá trị"],
                    ["Tổng số lượng", str(data['summary'].get('total_count', 0))],
                    ["Số lượng thành công", str(data['summary'].get('success_count', 0))],
                    ["Số lượng thất bại", str(data['summary'].get('failure_count', 0))],
                    ["Tỉ lệ thành công", f"{data['summary'].get('success_rate', 0):.1f}%"],
                    ["Tỉ lệ thất bại", f"{data['summary'].get('failure_rate', 0):.1f}%"]
                ]
                
                summary_table = Table(summary_data, colWidths=[200, 200])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(summary_table)
                elements.append(Spacer(1, 20))
            
            # Thêm biểu đồ nếu có
            if chart_path and os.path.exists(chart_path):
                chart_image = Image(chart_path, width=400, height=300)
                elements.append(Paragraph("Biểu đồ phân tích theo ngày", self.heading_style))
                elements.append(chart_image)
                elements.append(Spacer(1, 20))
            
            # Bảng dữ liệu theo ngày
            if 'days' in data and data['days']:
                elements.append(Paragraph("Thống kê theo ngày", self.heading_style))
                days_data = [["Ngày", "Tổng số", "Thành công", "Thất bại", "Tỉ lệ thành công"]]
                
                for day in data['days']:
                    days_data.append([
                        day.get('date', ''),
                        str(day.get('total_count', 0)),
                        str(day.get('success_count', 0)),
                        str(day.get('failure_count', 0)),
                        f"{day.get('success_rate', 0):.1f}%"
                    ])
                
                days_table = Table(days_data, colWidths=[80, 80, 80, 80, 100])
                days_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(days_table)
            
            # Thông tin thời gian tạo báo cáo
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(f"Báo cáo được tạo vào: {data['timestamp']}", self.normal_style))
            
            # Tạo file PDF
            doc.build(elements)
            self.logger.info(f"Báo cáo PDF hàng tuần đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo PDF hàng tuần: {str(e)}")
            return None

    def generate_custom_report(self, title, data, output_path):
        """
        Tạo báo cáo tùy chỉnh và lưu vào file PDF

        Args:
            title (str): Tiêu đề báo cáo
            data (dict): Dữ liệu cho báo cáo
            output_path (str): Đường dẫn đến file đầu ra (PDF)

        Returns:
            str: Đường dẫn đến file báo cáo PDF
        """
        try:
            # Đảm bảo đường dẫn có đuôi .pdf
            if not output_path.lower().endswith('.pdf'):
                output_path = f"{os.path.splitext(output_path)[0]}.pdf"
            
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Thêm dữ liệu thời gian nếu chưa có
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

            # Tạo tài liệu PDF
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            elements = []
            
            # Tiêu đề báo cáo
            report_title = data.get('title', title)
            elements.append(Paragraph(report_title, self.title_style))
            elements.append(Spacer(1, 20))
            
            # Nội dung báo cáo
            if 'content' in data:
                if isinstance(data['content'], str):
                    # Nếu nội dung là chuỗi văn bản
                    elements.append(Paragraph(data['content'], self.normal_style))
                elif isinstance(data['content'], list):
                    # Nếu nội dung là danh sách
                    for item in data['content']:
                        if isinstance(item, dict) and 'heading' in item:
                            # Tiêu đề phần
                            elements.append(Paragraph(item['heading'], self.heading_style))
                            elements.append(Spacer(1, 10))
                            
                            # Nội dung phần
                            if 'text' in item:
                                elements.append(Paragraph(item['text'], self.normal_style))
                            
                            # Bảng dữ liệu nếu có
                            if 'table' in item and len(item['table']) > 0:
                                table = Table(item['table'])
                                table.setStyle(TableStyle([
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                                ]))
                                elements.append(table)
                            
                            # Hình ảnh nếu có
                            if 'image_path' in item and os.path.exists(item['image_path']):
                                img = Image(item['image_path'], width=400, height=300)
                                elements.append(img)
                            
                            elements.append(Spacer(1, 15))
            
            # Thông tin thời gian tạo báo cáo
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(f"Báo cáo được tạo vào: {data['timestamp']}", self.normal_style))
            
            # Tạo file PDF
            doc.build(elements)
            self.logger.info(f"Báo cáo PDF tùy chỉnh đã được tạo: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo báo cáo PDF tùy chỉnh: {str(e)}")
            return None

    def export_data_to_file(self, data, output_path, format='json'):
        """
        Xuất dữ liệu báo cáo ra file (JSON hoặc XML)

        Args:
            data (dict): Dữ liệu cần xuất
            output_path (str): Đường dẫn đến file đầu ra
            format (str): Định dạng file ('json' hoặc 'xml')

        Returns:
            str: Đường dẫn đến file đã tạo, None nếu có lỗi
        """
        try:
            # Đảm bảo thư mục đầu ra tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if format.lower() == 'json':
                # Đảm bảo đường dẫn có đuôi .json
                if not output_path.lower().endswith('.json'):
                    output_path = f"{os.path.splitext(output_path)[0]}.json"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
            elif format.lower() == 'xml':
                # Đảm bảo đường dẫn có đuôi .xml
                if not output_path.lower().endswith('.xml'):
                    output_path = f"{os.path.splitext(output_path)[0]}.xml"
                
                try:
                    import dicttoxml
                    from xml.dom.minidom import parseString
                    xml = dicttoxml.dicttoxml(data)
                    dom = parseString(xml)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(dom.toprettyxml())
                except ImportError:
                    self.logger.error("Không thể xuất file XML. Thư viện 'dicttoxml' chưa được cài đặt.")
                    return None
            else:
                self.logger.error(f"Không hỗ trợ định dạng: {format}. Sử dụng 'json' hoặc 'xml'.")
                return None
            
            self.logger.info(f"Đã xuất dữ liệu ra file {format}: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Lỗi khi xuất dữ liệu ra file {format}: {str(e)}")
            return None
