# Kỹ Thuật Prompt AI Cho Tài Sản Game

Dự án này thực hiện Nhiệm Vụ Athena 2: Kỹ Thuật Prompt AI để tạo ra tài sản game chất lượng cao bằng cách sử dụng các kỹ thuật prompt nâng cao với các mô hình AI.

## Tổng Quan Dự Án

Hệ thống này cung cấp cách tiếp cận có cấu trúc cho việc tạo tài sản game sử dụng các mô hình AI:

1. **Khung Thiết Kế Prompt** - Phương pháp có hệ thống để tạo prompt hiệu quả
2. **Tạo Tài Sản** - Các script để tạo tài sản sử dụng các mô hình AI khác nhau
3. **Quy Trình Xác Thực** - Các phương pháp để kiểm tra và so sánh tài sản được tạo ra với tài liệu tham chiếu
4. **Tài Liệu** - Tài liệu toàn diện về toàn bộ quy trình

## Cấu Trúc Dự Án

```
Assignment02/
├── src/                     # Mã nguồn
│   ├── prompt_generator.py  # Tiện ích tạo prompt
│   ├── asset_generator.py   # Tạo tài sản sử dụng các mô hình AI
│   ├── validation.py        # Công cụ xác thực và so sánh
│   └── config.py            # Cài đặt cấu hình
├── prompts/                 # Mẫu và ví dụ prompt
├── assets/                  # Tài sản được tạo ra và tham chiếu
│   ├── reference/           # Tài sản game tham chiếu
│   └── generated/           # Tài sản được tạo bằng AI
├── validation/              # Kết quả xác thực
└── documentation/           # Tài liệu quy trình
    ├── prompt_design.md     # Phương pháp thiết kế prompt
    ├── testing.md           # Tài liệu quy trình kiểm tra
    └── iterations.md        # Lịch sử lặp lại và cải tiến
```

## Quy Trình Kỹ Thuật Prompt

Cách tiếp cận của chúng tôi đối với kỹ thuật prompt tuân theo các bước chính sau:

1. **Phân Tích**: Nghiên cứu tài sản game tham chiếu để hiểu đặc điểm trực quan của chúng
2. **Thiết Kế Cấu Trúc**: Tạo cấu trúc prompt với các phần cụ thể
3. **Tinh Chỉnh Tham Số**: Thử nghiệm với các tham số mô hình để có kết quả tối ưu
4. **Lặp Lại**: Tinh chỉnh prompt dựa trên kết quả kiểm tra
5. **Xác Thực**: So sánh tài sản được tạo ra với tài liệu tham chiếu
6. **Tài Liệu**: Ghi lại từng giai đoạn của quy trình

## Cài Đặt và Sử Dụng

1. Cài đặt các gói phụ thuộc:
   ```
   pip install -r requirements.txt
   ```

2. Cấu hình cài đặt trong `src/config.py`

3. Tạo prompt và tài sản:
   ```
   python src/asset_generator.py
   ```

4. Xác thực kết quả:
   ```
   python src/validation.py
   ```

Để xem tài liệu chi tiết về từng bước của quy trình, hãy xem các tệp trong thư mục `documentation`.
