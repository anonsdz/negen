# Sử dụng image chính thức của Node.js phiên bản mới nhất
FROM node:latest

# Cài đặt các công cụ bổ sung như git, speedtest-cli và htop
RUN apt-get update && apt-get install -y \
    git \
    speedtest-cli \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục cho ứng dụng
WORKDIR /usr/src/app

# Copy package.json và package-lock.json vào container
COPY package*.json ./

# Cài đặt các dependency, đảm bảo npm mới nhất được cài
RUN npm install -g npm@latest && npm install

# Nếu bạn xây dựng ứng dụng cho môi trường sản xuất, dùng lệnh sau:
# RUN npm ci --only=production

# Clone repository từ GitHub
RUN git clone https://github.com/anonsdz/negen/ && cd negen

# Copy mã nguồn vào container
COPY . .

# Mở cổng 8080
EXPOSE 8080

# Tăng bộ nhớ heap lên 64GB
ENV NODE_OPTIONS="--max-old-space-size=65536"

# Lệnh để chạy ứng dụng khi container khởi động
CMD ["npm", "start"]
