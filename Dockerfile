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

# Bước 3: Tạo một user không phải root (optional nhưng khuyến khích)
RUN useradd -ms /bin/bash nodeuser
USER nodeuser

# Bước 4: Chỉ định thư mục làm việc
WORKDIR /app

# Bước 5: Copy toàn bộ mã nguồn vào container (trừ những gì được ignore trong .dockerignore)
COPY . .

# Bước 6: Mở port ứng dụng của bạn (ví dụ: 3000 cho Node.js app)
EXPOSE 3000

# Bước 7: Chạy ứng dụng của bạn
CMD ["node", "index.js"]  # Hoặc lệnh tương ứng để chạy ứng dụng của bạn
