# Bước 1: Sử dụng image từ Alpine Linux
FROM alpine:latest

# Bước 2: Cài đặt các gói cần thiết
RUN apk update && apk add --no-cache \
    sudo \
    python3 \
    python3-dev \
    py3-pip \
    procps \
    htop \
    speedtest-cli

# Bước 3: Sao chép script start.sh vào container
COPY start.sh /start.sh

# Bước 4: Cấp quyền thực thi cho script
RUN chmod +x /start.sh

# Bước 5: Chạy script start.sh khi container khởi động
CMD ["/start.sh"]
