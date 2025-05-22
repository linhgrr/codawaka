# Triển khai Backend lên AWS Free Tier

Hướng dẫn triển khai backend FastAPI lên AWS Elastic Beanstalk với RDS.

## Các bước triển khai

### 1. Chuẩn bị trước khi triển khai

1. Cài đặt AWS CLI và EB CLI:
   ```
   pip install awscli awsebcli
   ```

2. Cấu hình AWS CLI:
   ```
   aws configure
   ```
   Nhập AWS Access Key, Secret Key, Region (ví dụ: ap-southeast-1) và output format (json).

3. Tạo cơ sở dữ liệu RDS PostgreSQL trên AWS:
   - Đăng nhập AWS Console
   - Tạo database PostgreSQL (db.t3.micro cho free tier)
   - Bật public access hoặc cấu hình VPC phù hợp
   - Ghi nhớ thông tin kết nối

4. Cập nhật `.env.production` với thông tin kết nối PostgreSQL:
   ```
   DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/your-database-name
   ```

5. Di chuyển dữ liệu từ SQLite sang PostgreSQL (nếu cần):
   ```
   python migrate_db.py .env.production
   ```

### 2. Triển khai lên Elastic Beanstalk

1. Khởi tạo Elastic Beanstalk application:
   ```
   cd /path/to/backend
   eb init -p python-3.11 your-app-name
   ```

2. Tạo environment mới:
   ```
   eb create your-environment-name
   ```

3. Cấu hình biến môi trường (từ file .env.production) trong EB Console hoặc sử dụng lệnh:
   ```
   eb setenv DATABASE_URL=postgresql://... SECRET_KEY=... [và các biến khác]
   ```

4. Triển khai ứng dụng:
   ```
   eb deploy
   ```

5. Mở ứng dụng:
   ```
   eb open
   ```

### 3. Kiểm tra và gỡ lỗi

1. Xem logs:
   ```
   eb logs
   ```

2. SSH vào instance:
   ```
   eb ssh
   ```

3. Kiểm tra endpoints:
   - Truy cập `/docs` để xem Swagger UI

### 4. Cấu hình CORS

Đảm bảo cập nhật `ALLOW_ORIGINS` trong biến môi trường để chấp nhận domain của frontend của bạn.

### 5. Cập nhật frontend

Cập nhật file `apiConfig.js` trong frontend để trỏ đến URL của backend trên Elastic Beanstalk.

## Chi phí ước tính (Free Tier)

- Elastic Beanstalk: Miễn phí (sử dụng EC2 t2.micro trong free tier)
- RDS: Miễn phí cho db.t3.micro (750 giờ/tháng)
- S3: Miễn phí cho 5GB lưu trữ
- Chú ý: Free tier chỉ áp dụng trong 12 tháng đầu tiên sau khi đăng ký AWS

## Giới hạn Free Tier

- EC2: 750 giờ/tháng với t2.micro
- RDS: 750 giờ/tháng với db.t3.micro
- 20GB lưu trữ cho RDS
- 5GB lưu trữ cho S3
- 15GB băng thông ra cho data transfer