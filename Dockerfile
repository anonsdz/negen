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
    && rm -rf /var/lib/apt/lists/* # Dọn dẹp các file không cần thiết để giảm kích thước image

# Bước 3: Tạo thư mục làm việc trong container
WORKDIR /app

# Bước 4: Sao chép package.json và package-lock.json vào container
COPY package*.json ./

# Bước 5: Cài đặt các dependencies từ package.json
RUN npm install

# Bước 6: Sao chép toàn bộ mã nguồn vào container
COPY . .

# Bước 7: Mở cổng cho ứng dụng (ví dụ 3000 cho ứng dụng Node.js)
EXPOSE 3000

# Bước 8: Lệnh khởi động ứng dụng
CMD ["npm", "start"]
