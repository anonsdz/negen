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

# Bước 3: Chạy một shell (bash hoặc sh) khi container khởi động
CMD ["/bin/sh"]
