#!/bin/bash

# Script khởi động tự động cho hệ thống tạo tài sản AI
# Tác giả: QHoa036
# Ngày: 03/06/2025

# Màu sắc cho terminal
XANH='\033[0;32m'
DO='\033[0;31m'
VANG='\033[0;33m'
XANH_DUONG='\033[0;34m'
KHONG_MAU='\033[0m'

# Đường dẫn thư mục gốc dự án
THU_MUC_GOC="$(dirname "$(realpath "$0")")"
cd "$THU_MUC_GOC" || exit 1

echo -e "${XANH_DUONG}=== HỆ THỐNG TỰ ĐỘNG HÓA TẠO TÀI SẢN AI ===${KHONG_MAU}"
echo -e "${XANH_DUONG}=== Phiên bản 1.0 ===${KHONG_MAU}"
echo ""

# Kiểm tra môi trường Python
if ! command -v python3 &>/dev/null; then
    echo -e "${DO}Lỗi: Python3 không được cài đặt trên hệ thống.${KHONG_MAU}"
    exit 1
fi

# Kiểm tra và tạo môi trường ảo nếu cần
if [ ! -d "venv" ]; then
    echo -e "${VANG}Không tìm thấy môi trường ảo. Tạo môi trường ảo mới...${KHONG_MAU}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Kiểm tra file .env
if [ ! -f ".env.local" ]; then
    echo -e "${VANG}Cảnh báo: Không tìm thấy file .env.local${KHONG_MAU}"
    echo -e "${VANG}Tạo file .env.local...${KHONG_MAU}"

    cat >.env.local <<EOF
# Google API credentials
GOOGLE_SHEETS_ID=your_sheet_id
GOOGLE_DRIVE_FOLDER_ID=your_folder_id

# AI API keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Notification settings
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENTS=admin@example.com,manager@example.com

# Slack settings
SLACK_WEBHOOK_URL=your_slack_webhook_url
EOF

    echo -e "${VANG}Vui lòng cập nhật file .env với thông tin của bạn trước khi chạy lại script.${KHONG_MAU}"
    exit 1
fi

# Kiểm tra tệp xác thực Google
if [ ! -f "data/google_credentials.json" ] && [ "$1" != "--debug" ] && [ "$1" != "--skip-google-auth" ]; then
    echo -e "${VANG}Cảnh báo: Không tìm thấy file xác thực Google (data/google_credentials.json)${KHONG_MAU}"
    echo -e "${VANG}Bạn cần tạo Service Account và tải xuống file credentials.${KHONG_MAU}"
    echo -e "${VANG}Hoặc chạy với tham số --debug hoặc --skip-google-auth để bỏ qua.${KHONG_MAU}"

    mkdir -p data

    # Chạy chế độ debug nếu người dùng đồng ý
    read -p "Bạn có muốn chạy ở chế độ debug không? (y/n): " chon_debug
    if [ "$chon_debug" = "y" ] || [ "$chon_debug" = "Y" ]; then
        echo -e "${XANH}Chạy ở chế độ debug...${KHONG_MAU}"
        set -- "--debug"
    else
        exit 1
    fi
fi

# Hiển thị menu tùy chọn
echo -e "${XANH}Chọn một tùy chọn:${KHONG_MAU}"
echo "1) Chạy với cấu hình mặc định"
echo "2) Chạy ở chế độ debug"
echo "3) Sử dụng file .env tùy chỉnh"
echo "4) Chỉ định Google Sheet ID"
echo "5) Chỉ định cả Google Sheet ID và file .env"
echo "6) Thoát"

read -p "Nhập lựa chọn của bạn (1-6): " lua_chon

case $lua_chon in
1)
    echo -e "${XANH}Chạy với cấu hình mặc định...${KHONG_MAU}"
    python src/main.py
    ;;
2)
    echo -e "${XANH}Chạy ở chế độ debug...${KHONG_MAU}"
    python src/main.py --debug
    ;;
3)
    read -p "Nhập đường dẫn đến file .env tùy chỉnh: " env_file
    echo -e "${XANH}Chạy với file .env tùy chỉnh: $env_file${KHONG_MAU}"
    python src/main.py --env "$env_file"
    ;;
4)
    read -p "Nhập Google Sheet ID: " sheet_id
    echo -e "${XANH}Chạy với Google Sheet ID: $sheet_id${KHONG_MAU}"
    python src/main.py --sheet-id "$sheet_id"
    ;;
5)
    read -p "Nhập Google Sheet ID: " sheet_id
    read -p "Nhập đường dẫn đến file .env tùy chỉnh: " env_file
    echo -e "${XANH}Chạy với Google Sheet ID: $sheet_id và file .env: $env_file${KHONG_MAU}"
    python src/main.py --sheet-id "$sheet_id" --env "$env_file"
    ;;
6)
    echo -e "${XANH_DUONG}Thoát chương trình. Tạm biệt!${KHONG_MAU}"
    exit 0
    ;;
*)
    echo -e "${DO}Lựa chọn không hợp lệ. Thoát.${KHONG_MAU}"
    exit 1
    ;;
esac

# Kết thúc script
echo -e "${XANH}Hoàn thành quá trình xử lý.${KHONG_MAU}"
deactivate
