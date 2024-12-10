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

# Bước 5: Cập nhật npm lên phiên bản mới nhất
RUN npm install -g npm@latest

# Bước 6: Xóa cache npm để tránh lỗi cũ
RUN npm cache clean --force

# Bước 7: Sao chép file package.json và package-lock.json (nếu có) và cài đặt các phụ thuộc
COPY package*.json ./

# Bước 8: Chạy npm install
RUN npm install --legacy-peer-deps

# Bước 9: Sao chép toàn bộ mã nguồn vào thư mục /app trong container
COPY . /app

# Bước 10: Thiết lập thư mục làm việc trong container
WORKDIR /app

# Bước 11: Đổi sang người dùng không phải root (nếu bạn muốn sử dụng quyền người dùng này)
USER myuser

# Bước 12: Mở cổng 3000 (hoặc cổng mà ứng dụng của bạn sử dụng) nếu cần
EXPOSE 3000

# Bước 13: Chạy ứng dụng Node.js
CMD ["npm", "start"]
