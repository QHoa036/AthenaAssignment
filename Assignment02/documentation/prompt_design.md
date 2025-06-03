# Phương Pháp Kỹ Thuật Prompt Cho Tài Sản Game

Tài liệu này trình bày cách tiếp cận có cấu trúc của chúng tôi để thiết kế prompt nhằm tạo ra tài sản game chất lượng cao bằng các mô hình AI.

## Khung Cấu Trúc Prompt

### 1. Định Nghĩa Tài Sản Cốt Lõi

```
{loại_tài_sản} cho {thể_loại_game} với phong cách {mô_tả_phong_cách}
```

Ví dụ: "Sprite nhân vật cho game nền tảng 2D với phong cách pixel art"

### 2. Lớp Thuộc Tính Trực Quan

```
Thuộc Tính Trực Quan:
- Màu sắc chính: {bảng_màu}
- Ánh sáng: {điều_kiện_ánh_sáng}
- Góc nhìn: {điểm_nhìn}
- Mức độ chi tiết: {mức_độ_chi_tiết}
- Phong cách nghệ thuật: {tham_chiếu_phong_cách_cụ_thể}
```

Ví dụ:
```
Thuộc Tính Trực Quan:
- Màu sắc chính: xanh dương và cam rực rỡ với điểm nhấn tím đậm
- Ánh sáng: ánh sáng bên hông kịch tính với độ tương phản cao
- Góc nhìn: góc nhìn đẳng thước từ phía trước
- Mức độ chi tiết: trung bình-cao với đường viền rõ ràng
- Phong cách nghệ thuật: tương tự như Hollow Knight với đường nét sạch sẽ
```

### 3. Thông Số Kỹ Thuật

```
Thông Số Kỹ Thuật:
- Độ phân giải: {chiều_rộng}x{chiều_cao}
- Định dạng: {định_dạng_tệp}
- Nền: {loại_nền}
- Khung hình hoạt ảnh: {số_lượng_khung} [nếu áp dụng]
- Trong suốt: {có/không}
```

Ví dụ:
```
Thông Số Kỹ Thuật:
- Độ phân giải: 512x512
- Định dạng: PNG
- Nền: trong suốt
- Khung hình hoạt ảnh: tư thế tĩnh
- Trong suốt: có
```

### 4. Tích Hợp Tham Chiếu Ngữ Cảnh

```
Tích Hợp Tham Chiếu:
- Tham chiếu tương tự như: {mô_tả_tham_chiếu hoặc URL}
- Các yếu tố quan trọng cần duy trì: {các_yếu_tố_cụ_thể}
- Tránh các khía cạnh này: {các_yếu_tố_cần_tránh}
```

Ví dụ:
```
Tích Hợp Tham Chiếu:
- Tham chiếu tương tự như: thiết kế nhân vật của nhân vật chính trong Hollow Knight
- Các yếu tố quan trọng cần duy trì: độ rõ ràng của đường viền, tỷ lệ chi tiết, khuôn mặt giống mặt nạ
- Tránh các khía cạnh này: chi tiết quá mức ở các khu vực nhỏ, kết cấu thực tế
```

### 5. Hướng Dẫn Định Hướng Thẩm Mỹ

```
Định Hướng Thẩm Mỹ:
- Tâm trạng: {mô_tả_tâm_trạng}
- Chủ đề: {yếu_tố_chủ_đề}
- Ảnh hưởng văn hóa: {tham_chiếu_văn_hóa}
- Đối tượng mục tiêu: {nhân_khẩu_học_đối_tượng}
```

Ví dụ:
```
Định Hướng Thẩm Mỹ:
- Tâm trạng: bí ẩn và hơi buồn bã
- Chủ đề: nền văn minh cổ đại được thiên nhiên chiếm lại
- Ảnh hưởng văn hóa: kết hợp các yếu tố trang trí Art Nouveau
- Đối tượng mục tiêu: người chơi từ thanh thiếu niên đến người lớn đánh giá cao các trò chơi indie nghệ thuật
```

### 6. Chỉ Thị Tối Ưu Hóa Kỹ Thuật

```
Chỉ Thị Tối Ưu Hóa:
- Ưu tiên: {khía_cạnh_ưu_tiên}
- Đảm bảo tương thích với: {môi_trường}
- Duy trì sự nhất quán với: {tài_sản_liên_quan}
```

Ví dụ:
```
Chỉ Thị Tối Ưu Hóa:
- Ưu tiên: khả năng đọc rõ ràng ở quy mô nhỏ hơn
- Đảm bảo tương thích với: môi trường game tối
- Duy trì sự nhất quán với: ngôn ngữ thiết kế nhân vật đã được thiết lập trước đó
```

## Tối Ưu Hóa Thông Số

Đối với mỗi mô hình AI, chúng tôi tinh chỉnh các thông số sau:

1. **Cài Đặt Nhiệt Độ**: Kiểm soát tính ngẫu nhiên
   - Thấp (0.2-0.4): Kết quả dễ dự đoán hơn
   - Trung bình (0.5-0.7): Sáng tạo cân bằng
   - Cao (0.8-1.0): Biến thể tối đa

2. **Mức Độ Chi Tiết**: Điều chỉnh dựa trên độ phức tạp của tài sản
   - Thấp: Biểu diễn biểu tượng, tượng trưng
   - Trung bình: Tài sản game tiêu chuẩn với chi tiết rõ ràng
   - Cao: Các tác phẩm trưng bày với chi tiết phức tạp

3. **Nhấn Mạnh Phong Cách**: Trọng số giữa các khía cạnh phong cách khác nhau
   - Thông số kỹ thuật (trọng số cao hơn cho tài sản kỹ thuật)
   - Biểu hiện nghệ thuật (trọng số cao hơn cho nghệ thuật chính)
   - Thiết kế chức năng (trọng số cao hơn cho các yếu tố tương tác)

4. **Prompting Tiêu Cực**: Các yếu tố cần tránh rõ ràng
   - Vấn đề kỹ thuật: mờ, nhiễu ảnh, ánh sáng không nhất quán
   - Vấn đề thiết kế: bố cục lộn xộn, khả năng đọc kém
   - Không phù hợp về phong cách: phong cách nghệ thuật không phù hợp với thể loại game

## Cân Nhắc Đặc Thù Cho Từng Mô Hình

### Stable Diffusion

- Điểm mạnh: Kết cấu chi tiết, nhất quán về phong cách
- Tối ưu hóa: Nhấn mạnh các từ khóa về bố cục, sử dụng mô hình LoRA cho phong cách

### Midjourney

- Điểm mạnh: Sự hài hòa thẩm mỹ, diễn giải sáng tạo
- Tối ưu hóa: Sử dụng tham số phiên bản, cài đặt kiểu dáng

### DALL-E

- Điểm mạnh: Tuân theo hướng dẫn cụ thể, độ chính xác bố cục
- Tối ưu hóa: Mô tả cấu trúc rõ ràng, hướng dẫn vị trí cụ thể

### ComfyUI/Automatic1111

- Điểm mạnh: Kiểm soát kỹ thuật, kết quả nhất quán với cài đặt đã lưu
- Tối ưu hóa: Phát triển và lưu quy trình làm việc cụ thể cho từng loại tài sản
