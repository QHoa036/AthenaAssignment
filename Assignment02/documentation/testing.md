# Phương Pháp Xác Thực Tài Sản Game

Tài liệu này trình bày cách tiếp cận có hệ thống của chúng tôi để kiểm tra và xác thực các tài sản game được tạo ra bằng AI so với các tài liệu tham chiếu.

## Khung Xác Thực

### 1. Đánh Giá Độ Trung Thực Hình Ảnh

#### Các Chỉ Số Khách Quan
- **Chỉ Số Tương Đồng Cấu Trúc (SSIM)**
  - Đo lường sự tương đồng giữa hình ảnh tham chiếu và hình ảnh được tạo ra
  - Mục tiêu: điểm SSIM >0.7 cho tài sản chấp nhận được

- **Phân Tích Biểu Đồ Màu**
  - So sánh phân bố màu giữa tài sản tham chiếu và tài sản được tạo ra
  - Mục tiêu: sai lệch <15% so với bảng màu tham chiếu

- **So Sánh Phát Hiện Cạnh**
  - Đánh giá độ chính xác của đường viền và cấu trúc
  - Mục tiêu: tương đồng cạnh >80%

#### Tiêu Chí Đánh Giá Chủ Quan
- Sự gắn kết trực quan với phong cách nghệ thuật game
- Độ rõ ràng trong nhận diện nhân vật/đối tượng
- Giá trị nghệ thuật và sự hấp dẫn
- Tính nhất quán với thương hiệu/IP (nếu áp dụng)

### 2. Xác Thực Sự Tuân Thủ Kỹ Thuật

- **Xác Minh Độ Phân Giải**
  - Khớp chính xác với kích thước đã yêu cầu

- **Tuân Thủ Định Dạng**
  - Định dạng tệp, tính trong suốt, không gian màu

- **Tương Thích Với Game Engine**
  - Kiểm tra nhập vào engine mục tiêu
  - Đánh giá tác động hiệu suất

- **Kiểm Tra Quy Mô**
  - Hiển thị ở các độ phân giải màn hình khác nhau
  - Khả năng đọc ở khoảng cách camera game dự định

### 3. Phương Pháp Phân Tích So Sánh

#### Giao Thức Kiểm Tra A/B
1. Trình bày cả tài sản tham chiếu và tài sản được tạo ra cho nhóm kiểm tra
2. Thu thập dữ liệu và lý do ưu tiên mù
3. Xác định các mô hình ưu tiên và các khu vực cần cải thiện

#### Quy Trình Đánh Giá Chuyên Gia
1. Gửi đến giám đốc nghệ thuật/nghệ sĩ chính
2. Phản hồi có cấu trúc sử dụng bảng đánh giá
3. Các khuyến nghị cải tiến cụ thể

#### Đánh Giá Trong Ngữ Cảnh
1. Đặt tài sản trong mô hình môi trường game
2. Đánh giá sự tích hợp trực quan với các tài sản khác
3. Đánh giá sự rõ ràng về chức năng trong ngữ cảnh gameplay

## Công Cụ Xác Thực

### Giao Thức Kiểm Tra Layer.ai

1. **Tải Lên Tài Sản Tham Chiếu và Tài Sản Được Tạo Ra**
   - Duy trì quy ước đặt tên nhất quán
   - Gắn thẻ với loại tài sản và số lần lặp lại

2. **Phân Tích So Sánh**
   - Sử dụng công cụ so sánh cạnh nhau
   - Chạy phân tích tương đồng tự động
   - Tạo bản đồ nhiệt sự khác biệt

3. **Kiểm Tra Ưu Tiên A/B**
   - Cấu hình các kịch bản kiểm tra mù
   - Thu thập và tổng hợp phản hồi
   - Xuất kết quả tổng hợp

### Script Xác Thực Tùy Chỉnh

Script `validation.py` của chúng tôi thực hiện các kiểm tra tự động này:
- Tính toán điểm SSIM
- So sánh biểu đồ màu
- Phát hiện và so sánh cạnh
- Xác minh độ phân giải và định dạng
- Ghi nhật ký kết quả và trực quan hóa

### Mẫu Báo Cáo Xác Thực

Mỗi xác thực tài sản tạo ra một báo cáo chuẩn hóa bao gồm:
- Các chỉ số khách quan với trạng thái đạt/không đạt
- Hình ảnh so sánh trực quan
- Tổng hợp phản hồi của chuyên gia
- Các khuyến nghị lặp lại
- Theo dõi hiệu suất lịch sử

## Ngưỡng Xác Thực

| Chỉ số | Loại bỏ | Chấp nhận được | Xuất sắc |
|--------|--------|------------|-----------|
| Điểm SSIM | <0.6 | 0.6-0.8 | >0.8 |
| Phù hợp màu | <70% | 70%-90% | >90% |
| Độ chính xác cạnh | <75% | 75%-90% | >90% |
| Đánh giá chuyên gia | <6/10 | 6-8/10 | >8/10 |
| Ưu tiên A/B | <40% | 40%-60% | >60% |

## Vòng Lặp Cải Tiến Liên Tục

Kết quả xác thực được phản hồi trực tiếp vào:
1. Tinh chỉnh prompt
2. Điều chỉnh tham số
3. Lựa chọn mô hình
4. Làm rõ tài sản tham chiếu

Điều này tạo ra một chu kỳ cải tiến liên tục trong đó mỗi lần lặp lại được xây dựng trên kiến thức đã được xác thực từ các lần thử trước.
