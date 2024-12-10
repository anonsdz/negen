# Bước 1: Chọn base image cho Node.js phiên bản 20
FROM node:20

# Bước 2: Cài đặt các gói cần thiết bao gồm sudo, Python, pip, htop và speedtest-cli
RUN apt-get update -q && apt-get install -y --no-install-recommends \
    sudo \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    procps \
    htop \
    speedtest-cli \
    && rm -rf /var/lib/apt/lists/*

# Cập nhật pip nếu cần thiết (sử dụng curl để đảm bảo tải đúng phiên bản)
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Bước 3: Tạo một user không phải root (optional nhưng khuyến khích)
RUN useradd -ms /bin/bash nodeuser
USER nodeuser

# Cài đặt các phụ thuộc Node.js (nếu có)
WORKDIR /app
COPY package*.json ./
RUN npm install

# Bước 4: Copy ứng dụng của bạn vào container
COPY . .

# Bước 5: Mở port ứng dụng của bạn (ví dụ: 3000 cho Node.js app)
EXPOSE 3000

# Bước 6: Chạy ứng dụng của bạn
CMD ["npm", "start"]
