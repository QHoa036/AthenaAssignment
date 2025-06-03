# Lịch Sử Lặp Lại Kỹ Thuật Prompt

Tài liệu này theo dõi sự phát triển của các prompt tài sản game của chúng tôi qua nhiều lần lặp lại, ghi lại các cải tiến, thách thức và kết quả học tập.

## Khung Lặp Lại

Mỗi lần lặp lại tuân theo cấu trúc tài liệu này:

1. **Mục Tiêu Lặp Lại**: Mục tiêu cải thiện cụ thể
2. **Sửa Đổi Prompt**: Thay đổi so với phiên bản trước
3. **Phân Tích Kết Quả**: Kết quả và quan sát
4. **Kết Quả Học Tập**: Những hiểu biết chính thu được
5. **Bước Tiếp Theo**: Các thay đổi dự kiến cho các lần lặp lại trong tương lai

## Các Lần Lặp Lại Mẫu

### Lặp Lại 1: Thiết Lập Cơ Sở

#### Mục Tiêu
Thiết lập hiệu suất cơ sở với các kỹ thuật prompt tiêu chuẩn cho nhân vật game 2D.

#### Prompt Đã Sử Dụng
```
Tạo một sprite nhân vật 2D cho game RPG fantasy. Nhân vật nên là một phù thủy với áo choàng màu xanh, cầm một cây gậy, và có bộ râu trắng dài. Làm theo phong cách pixel art.
```

#### Phân Tích Kết Quả
- Tạo ra nhân vật phù thủy cơ bản có thể nhận ra như mục tiêu
- Tỷ lệ không phù hợp với tiêu chuẩn nghệ thuật game
- Bảng màu thiếu sự gắn kết với phong cách game dự định
- Chi tiết hạn chế ở các đặc điểm nhân vật quan trọng

#### Kết Quả Học Tập
- Các prompt mô tả cơ bản tạo ra kết quả có thể nhận ra nhưng chung chung
- Cần các điểm tham chiếu phong cách nghệ thuật cụ thể hơn
- Yêu cầu thông số kỹ thuật cho tài sản game có thể sử dụng
- Cần hướng dẫn về tỷ lệ nhân vật

#### Bước Tiếp Theo
- Thêm kích thước pixel cụ thể
- Tham chiếu các ví dụ phong cách nghệ thuật hiện có
- Bao gồm hướng dẫn về đường viền
- Xác định góc nhìn

### Lặp Lại 2: Tích Hợp Thông Số Kỹ Thuật

#### Mục Tiêu
Cải thiện độ chính xác kỹ thuật và khả năng sử dụng của tài sản được tạo ra.

#### Sửa Đổi Prompt
```
Tạo một sprite nhân vật 2D cho game RPG fantasy theo phong cách của Final Fantasy VI. Nhân vật nên là:
- Một phù thủy với áo choàng màu xanh dương trung bình với viền vàng
- Cầm một cây gậy gỗ với đầu pha lê
- Có bộ râu trắng dài đến giữa ngực
- Góc nhìn chính diện
- Độ phân giải 32x32 pixel
- Đường viền rõ ràng có thể đọc được ở kích thước nhỏ
- Nền trong suốt
- Giới hạn ở bảng màu 16 màu
```

#### Phân Tích Kết Quả
- Cải thiện sự tuân thủ kỹ thuật với thông số game
- Tính nhất quán về tỷ lệ tốt hơn
- Mức độ chi tiết phù hợp hơn cho độ phân giải dự định
- Phong cách gần với tham chiếu hơn nhưng vẫn thiếu các yếu tố đặc trưng

#### Kết Quả Học Tập
- Thông số kỹ thuật cải thiện đáng kể khả năng sử dụng
- Tham chiếu đến phong cách game hiện có cung cấp hướng dẫn tốt hơn
- Các ràng buộc pixel giúp tập trung chi tiết một cách thích hợp
- Vẫn cần quản lý bảng màu tốt hơn

#### Bước Tiếp Theo
- Thêm mã màu hex cụ thể
- Cung cấp hướng dẫn tư thế chi tiết hơn
- Bao gồm các prompt tiêu cực cho các yếu tố không mong muốn

### Lặp Lại 3: Tích Hợp Tham Chiếu Trực Quan

#### Mục Tiêu
Đạt được sự phù hợp gần hơn với phong cách nghệ thuật game tham chiếu và cải thiện sự gắn kết nghệ thuật.

#### Sửa Đổi Prompt
```
Tạo một sprite nhân vật 2D cho game RPG fantasy theo đúng phong cách pixel art của Final Fantasy VI (thời đại SNES).

Thông Số Kỹ Thuật:
- Độ phân giải 32x32 pixel
- Nền trong suốt
- Bảng màu giới hạn sử dụng chính xác các màu này: #3A66A7 (áo choàng chính), #C9D9FB (điểm nhấn áo choàng), #FCFCE0 (râu), #8F563B (gậy)

Mô Tả Nhân Vật:
- Phù thủy già với tỷ lệ phù hợp với sprite nhân vật FFVI (cao 2.5 đầu)
- Áo choàng màu xanh dương trung bình với điểm nhấn xanh nhạt ở các cạnh
- Đứng ở tư thế đứng yên chính diện tiêu chuẩn của FFVI
- Râu trắng dài đến giữa ngực, được định nghĩa rõ ràng so với áo choàng
- Cầm một cây gậy gỗ với đầu pha lê phát sáng hơi lệch tâm

KHÔNG bao gồm:
- Kỹ thuật pixel art hiện đại như dithering
- Đường viền đen dày hơn 1px
- Chi tiết khuôn mặt ngoài mắt và các đặc điểm cơ bản
- Tỷ lệ hoặc bóng đổ thực tế
```

#### Phân Tích Kết Quả
- Cải thiện đáng kể trong việc phù hợp phong cách
- Độ chính xác màu sắc gần với tham chiếu hơn nhiều
- Tỷ lệ và đường viền phù hợp với ngữ cảnh game
- Đáp ứng đầy đủ thông số kỹ thuật

#### Kết Quả Học Tập
- Mã màu rõ ràng tạo ra kết quả chính xác hơn nhiều
- Prompt tiêu cực ngăn chặn hiệu quả các vấn đề phổ biến
- Tham chiếu đến tiêu đề game cụ thể giúp AI hiểu phong cách
- Hướng dẫn kỹ thuật và nghệ thuật phải cân bằng

#### Bước Tiếp Theo
- Tạo cấu trúc mẫu cho các loại tài sản khác nhau
- Kiểm tra với các mô hình AI khác nhau
- Thêm hướng dẫn khung hình hoạt ảnh cho bộ sprite

## Các Lần Lặp Lại Nâng Cao

### Lặp Lại 4: Tối Ưu Hóa Đặc Thù Cho Mô Hình

#### Mục Tiêu
Tối ưu hóa prompt cho đặc điểm của mô hình AI cụ thể để tối đa hóa chất lượng.

#### Sửa Đổi Prompt
```
[Chỉ thị đặc thù cho mô hình dựa trên kết quả kiểm tra]
```

### Lặp Lại 5: Tính Nhất Quán Phong Cách Giữa Các Bộ Tài Sản

#### Mục Tiêu
Đảm bảo sự gắn kết trực quan giữa nhiều tài sản trong cùng một thế giới game.

#### Sửa Đổi Prompt
```
[Chỉ thị về tính nhất quán tài sản]
```

## Khung Lặp Lại Cuối Cùng

Khung lặp lại cuối cùng của chúng tôi sử dụng cấu trúc mẫu này:

```
[LOẠI TÀI SẢN] cho [THỂ LOẠI GAME] trong [THAM CHIẾU PHONG CÁCH]

THÔNG SỐ KỸ THUẬT:
- Độ phân giải: [KÍCH THƯỚC CHÍNH XÁC]
- Định dạng: [ĐỊNH DẠNG TỆP]
- Bảng màu: [MÃ MÀU CỤ THỂ]
- [CÁC YÊU CẦU KỸ THUẬT KHÁC]

THUỘC TÍNH TRỰC QUAN:
- [ĐẶC ĐIỂM TRỰC QUAN CHÍNH]
- [HƯỚNG DẪN TỶ LỆ]
- [THÔNG TIN GÓC NHÌN]
- [YẾU TỐ ĐẶC TRƯNG]

THAM CHIẾU NGỮ CẢNH:
- Phù hợp phong cách: [THAM CHIẾU CỤ THỂ]
- Yêu cầu chức năng: [NHU CẦU GAMEPLAY]
- Ngữ cảnh bối cảnh: [THẾ GIỚI/MÔI TRƯỜNG]

KHÔNG BAO GỒM:
- [YẾU TỐ KHÔNG MONG MUỐN]
- [KHÔNG PHÙ HỢP VỀ PHONG CÁCH]
- [VẤN ĐỀ KỸ THUẬT]

[THAM SỐ ĐẶC THÙ CHO MÔ HÌNH]
```
