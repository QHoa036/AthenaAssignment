# Dự án Tự Động Hóa Tạo Nội Dung Bằng AI

## Giới thiệu

Dự án này được phát triển để giải quyết Assignment 1 của bài tập Athena, tập trung vào việc tự động hóa quy trình tạo nội dung bằng AI. Hệ thống lấy dữ liệu từ Google Sheets, tạo nội dung sử dụng các mô hình AI (như OpenAI hoặc Claude), lưu trữ kết quả vào Google Drive, và cung cấp thông báo và báo cáo phân tích.

## Cấu trúc dự án

```
Assignment01/
├── src/                     # Mã nguồn chính
│   ├── main.py              # Điểm vào chính của ứng dụng
│   ├── sheets_reader.py     # Đọc dữ liệu từ Google Sheets
│   ├── ai_generator.py      # Tạo nội dung bằng AI
│   ├── drive_uploader.py    # Tải lên Google Drive
│   ├── notifier.py          # Gửi thông báo qua email và Slack
│   ├── database.py          # Quản lý cơ sở dữ liệu
│   ├── report_generator.py  # Tạo báo cáo từ dữ liệu
│   ├── chart_generator.py   # Tạo biểu đồ phân tích
│   └── html_report_generator.py # Tạo báo cáo HTML
├── config.py                # Cấu hình ứng dụng
├── data/                    # Dữ liệu ứng dụng và cơ sở dữ liệu
├── logs/                    # Tệp nhật ký
├── reports/                 # Báo cáo đầu ra
│   └── charts/              # Biểu đồ phân tích
├── docs/                    # Tài liệu
└── tests/                   # Kiểm thử đơn vị
```

## Cách hoạt động

1. **Đọc dữ liệu đầu vào**: Hệ thống đọc dữ liệu từ Google Sheets chứa các mô tả nội dung, URL tài sản tham chiếu, định dạng đầu ra và thông số mô hình AI.

2. **Tạo nội dung bằng AI**: Với mỗi hàng, hệ thống sử dụng OpenAI hoặc Claude để tạo nội dung (hình ảnh hoặc âm thanh) dựa trên mô tả và tài sản tham chiếu.

3. **Lưu trữ kết quả**: Nội dung được tạo sẽ được tải lên Google Drive với cấu trúc tổ chức hợp lý.

4. **Thông báo**: Hệ thống gửi thông báo qua email và Slack về tình trạng thành công hoặc thất bại.

5. **Ghi Log**: Tất cả các hoạt động và kết quả được lưu trữ trong cơ sở dữ liệu SQLite.

6. **Báo cáo phân tích**: Mỗi ngày, hệ thống tạo báo cáo phân tích với biểu đồ thống kê và gửi qua email cho quản trị viên.

## Cài đặt

1. Cài đặt các thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

2. Cấu hình thông số trong `config.py`:
   - Thêm thông tin API Google (Google Sheets, Google Drive)
   - Cấu hình API key cho OpenAI hoặc Claude
   - Cấu hình thông tin email và webhook Slack

3. Đảm bảo bạn có file Google API credentials (`google_credentials.json`) trong thư mục `data`.

## Sử dụng

### Chạy quy trình tự động hóa:

```bash
python src/main.py
```

### Chạy với tệp Google Sheet cụ thể:

```bash
python src/main.py --sheet-id YOUR_SHEET_ID
```

### Chạy với tệp cấu hình khác:

```bash
python src/main.py --config path/to/custom_config.py
```

## Google Sheets Format

Tệp Google Sheets cần có các cột sau:

- `id`: ID duy nhất cho mỗi mục
- `description`: Mô tả nội dung cần tạo
- `example_asset_url`: URL tham chiếu (tùy chọn)
- `output_format`: Định dạng đầu ra (png, jpg, gif, mp3)
- `model`: Mô hình AI sử dụng (openai, claude)

## Báo cáo

Báo cáo hàng ngày bao gồm:
- Tổng số mục được xử lý
- Tỷ lệ thành công và thất bại
- Biểu đồ phân tích
- Chi tiết về từng mục

## Yêu cầu hệ thống

- Python 3.8+
- Kết nối internet để truy cập Google API và API AI
- Quyền truy cập vào Google Sheets và Google Drive
- Tài khoản email và webhook Slack (cho thông báo)
