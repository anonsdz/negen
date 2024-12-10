# Bước 1: Chọn base image từ Alpine
FROM node:alpine

# Bước 2: Cài đặt các gói cần thiết
RUN apk add --no-cache \
    sudo \
    python3 \
    python3-pip \
    procps \
    htop \
    speedtest-cli

# Bước 3: Sao chép và cấp quyền thực thi cho script start.sh
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Bước 4: Chạy script khi container khởi động
CMD ["/start.sh"]
