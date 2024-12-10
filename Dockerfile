# Bước 1: Chọn base image cho Node.js phiên bản 20
FROM node:20

# Bước 2: Chỉ định thư mục làm việc
WORKDIR /app

# Bước 3: Copy toàn bộ mã nguồn vào container
COPY . .

# Bước 4: Mở port ứng dụng của bạn (ví dụ: 3000 cho Node.js app)
EXPOSE 3000

# Bước 5: Chạy ứng dụng Node.js
CMD ["node", "index.js"]  # Thay thế index.js bằng tên file bạn muốn chạy
