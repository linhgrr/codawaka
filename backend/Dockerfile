FROM python:3.11-slim

WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Tạo thư mục data
RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite:///./data/app.db

# Mở cổng 8000
EXPOSE 8000

# Khởi động ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]