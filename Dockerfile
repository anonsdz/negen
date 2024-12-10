# Sử dụng một image chính thức của Ubuntu làm base image
FROM ubuntu:20.04

# Cập nhật danh sách các package và cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y \
    curl \
    git \
    nano \
    htop \
    ca-certificates \
    lsb-release \
    wget \
    unzip \
    sudo \
    software-properties-common \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    speedtest-cli \
  && rm -rf /var/lib/apt/lists/*

# Kiểm tra phiên bản của các công cụ cài đặt
RUN python3 --version && pip3 --version && node --version && npm --version && git --version && speedtest-cli --version

# Đặt working directory
WORKDIR /app

# Thêm một command mặc định để chạy khi container chạy
CMD [ "bash" ]
