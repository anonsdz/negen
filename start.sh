#!/bin/bash
# Dừng tất cả các dịch vụ không cần thiết
sudo systemctl stop apache2
sudo systemctl stop nginx
sudo systemctl stop mysql
sudo systemctl stop postgresql

# Chạy một lệnh không làm gì
sleep infinity
