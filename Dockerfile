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

# Bước 5: Sao chép mã nguồn vào container
COPY . /app

# Bước 6: Thiết lập thư mục làm việc trong container
WORKDIR /app

# Bước 7: Đổi sang người dùng không phải root (nếu bạn muốn sử dụng quyền người dùng này)
USER myuser

# Bước 8: Cài đặt các module Node.js từ package.json
RUN npm install

# Bước 9: Cài đặt các thư viện Python từ requirements.txt
RUN pip install -r requirements.txt

# Bước 10: Dừng bất kỳ tiến trình nào của botv3.py đang chạy (nếu có)
RUN pkill -f botv3.py || echo "No process with botv3.py found"

# Bước 11: Mở cổng cần thiết nếu cần (optional)
# EXPOSE 8080
