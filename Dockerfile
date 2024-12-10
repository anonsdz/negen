# Bước 1: Chọn base image cho Node.js (phiên bản mới nhất)
FROM node:latest

# Bước 2: Cài đặt các gói cần thiết bao gồm sudo, Python, pip, htop và speedtest-cli
RUN apt-get update && apt-get install -y \
    sudo \
    python3 \
    python3-pip \
    procps \
    htop \
    speedtest-cli \
    && rm -rf /var/lib/apt/lists/*

# Bước 3: Sao chép script start.sh vào container
COPY start.sh /start.sh

# Bước 4: Cấp quyền thực thi cho script
RUN chmod +x /start.sh

# Bước 5: Chạy script start.sh khi container khởi động
CMD ["/start.sh"]
