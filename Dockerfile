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

# Bước 6: Sao chép file package.json và cài đặt dependencies
COPY package*.json ./
RUN npm install

# Bước 7: Sao chép mã nguồn vào container
COPY . /app

# Bước 8: Thiết lập thư mục làm việc trong container
WORKDIR /app

# Bước 9: Đổi sang người dùng không phải root (nếu bạn muốn sử dụng quyền người dùng này)
USER myuser

# Bước 10: Chạy ứng dụng
CMD ["npm", "start"]
