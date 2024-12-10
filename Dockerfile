# Bắt đầu từ một image nhẹ và tối giản
FROM python:3.9-slim

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc cho ứng dụng
WORKDIR /app

# Sao chép các tệp yêu cầu vào container
COPY requirements.txt /app/

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . /app/

# Tạo và cấu hình thư mục cho SSH nếu cần
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Cấu hình port cho SSH
EXPOSE 22

# Cấu hình cổng của ứng dụng (nếu cần)
EXPOSE 8080

# Tối ưu hóa việc chạy ứng dụng (ví dụ: bot Telegram)
CMD ["python", "bot.py"]
