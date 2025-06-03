# Dự án Tự Động Hóa Tạo Nội Dung Bằng AI

## Giới thiệu

Dự án này được phát triển để giải quyết Assignment 1 của bài tập Athena, tập trung vào việc tự động hóa quy trình tạo nội dung bằng AI. Hệ thống lấy dữ liệu từ Google Sheets, tạo nội dung sử dụng các mô hình AI (như OpenAI hoặc Claude), lưu trữ kết quả vào Google Drive, và cung cấp thông báo và báo cáo phân tích.

> **Lưu ý**: Mã nguồn này đã được địa phương hóa hoàn toàn với chú thích, docstring, và thông báo logger bằng tiếng Việt để hỗ trợ nhóm phát triển người Việt.

## Cấu trúc dự án

```
Assignment01/
├── src/                     # Mã nguồn chính (đã địa phương hóa tiếng Việt)
│   ├── integrations/         # Các module tích hợp
│   │   ├── drive_uploader.py  # Tải lên Google Drive
│   │   └── sheets_reader.py   # Đọc dữ liệu từ Google Sheets
│   ├── generators/           # Các bộ tạo nội dung
│   │   ├── ai_generator.py    # Tạo nội dung bằng AI
│   │   ├── chart_generator.py # Tạo biểu đồ phân tích
│   │   ├── report_generator.py # Tạo báo cáo từ dữ liệu
│   │   └── html_report_generator.py # Tạo báo cáo HTML
│   ├── notifications/        # Dịch vụ thông báo
│   │   └── notifier.py        # Gửi thông báo qua email và Slack
│   ├── persistence/          # Lưu trữ dữ liệu
│   │   └── database.py        # Quản lý cơ sở dữ liệu
│   └── main.py                # Điểm vào chính của ứng dụng
├── .env                     # Biến môi trường
├── data/                    # Dữ liệu ứng dụng và cơ sở dữ liệu
│   └── google_credentials.json # Thông tin xác thực Google API
├── logs/                    # Tệp nhật ký
├── reports/                 # Báo cáo đầu ra
│   └── charts/              # Biểu đồ phân tích
├── docs/                    # Tài liệu
│   ├── README_en.md         # Tài liệu tiếng Anh
│   └── README_vi.md         # Tài liệu tiếng Việt
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

2. Thiết lập các biến môi trường trong tệp `.env`:
   ```
   # Thông tin xác thực Google API
   GOOGLE_APPLICATION_CREDENTIALS=./data/google_credentials.json
   GOOGLE_SHEETS_ID=your_sheet_id

   # Khóa API cho các dịch vụ AI
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key

   # Cấu hình thông báo email
   EMAIL_SENDER=your_email@example.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECIPIENT=admin@example.com

   # Cấu hình Slack
   SLACK_WEBHOOK_URL=your_slack_webhook_url

   # Cài đặt lưu trữ
   GOOGLE_DRIVE_FOLDER_ID=your_folder_id
   ```

3. Đảm bảo bạn có file Google API credentials (`google_credentials.json`) trong thư mục `data`.

## Sử dụng

### Chạy quy trình tự động hóa:

```bash
python src/main.py
```

### Chạy với các tham số dòng lệnh cụ thể (ghi đè cài đặt trong .env):

```bash
python src/main.py --sheet-id YOUR_SHEET_ID --openai-key YOUR_OPENAI_KEY --drive-folder YOUR_FOLDER_ID
```

### Chạy với tệp .env tùy chỉnh:

```bash
python src/main.py --env-file path/to/.env.custom
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
