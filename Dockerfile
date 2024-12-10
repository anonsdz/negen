# Sử dụng image chính thức của Node.js phiên bản mới nhất
FROM node:latest

# Cài đặt các công cụ bổ sung như git, speedtest-cli và htop
RUN apt-get update && apt-get install -y \
    git \
    speedtest-cli \
    htop \
    && rm -rf /var/lib/apt/lists/*
