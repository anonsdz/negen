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

# Bước 3: Tạo một người dùng mới (optional, nếu bạn muốn không sử dụng root)
RUN useradd -ms /bin/bash myuser

# Bước 4: Cài đặt quyền sudo cho người dùng
RUN echo "myuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Bước 5: Sao chép toàn bộ mã nguồn vào thư mục /app trong container
COPY . /app

# Bước 6: Thiết lập thư mục làm việc trong container
WORKDIR /app

# Bước 7: Đổi sang người dùng không phải root (nếu bạn muốn sử dụng quyền người dùng này)
USER myuser

