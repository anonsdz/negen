# Chọn base image cho Node.js
FROM node:20

# Cài đặt các gói cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
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

# Tạo user không phải root (optional)
RUN useradd -ms /bin/bash nodeuser
USER nodeuser

# Chỉ định thư mục làm việc
WORKDIR /app

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Kiểm tra nội dung thư mục /app (optional)
RUN ls -l /app

# Mở port nếu cần thiết
EXPOSE 3000

# Không chỉ định file chính, chỉ chạy Node.js mà không có file
CMD ["node"]
