# Chọn image Python chính thức làm nền tảng
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện phụ thuộc từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Cấu hình lệnh để chạy bot
CMD ["python", "bot.py"]
