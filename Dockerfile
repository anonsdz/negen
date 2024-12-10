# Bước 1: Chọn base image cho Node.js
FROM node:18-slim

# Bước 2: Cài đặt Python và pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Bước 3: Sao chép mã nguồn vào container
COPY . /app

# Bước 4: Thiết lập thư mục làm việc trong container
WORKDIR /app

# Bước 5: Cài đặt các module Node.js từ package.json
RUN npm install

# Bước 6: Cài đặt các thư viện Python từ requirements.txt
RUN pip install -r requirements.txt

# Bước 8: Chạy ứng dụng của bạn (ví dụ Python hoặc Node.js)
CMD ["python3", "botv3.py"]
