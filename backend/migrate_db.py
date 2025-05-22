import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load cấu hình từ file .env
load_dotenv()

# Kiểm tra xem đã có tham số dòng lệnh chưa
if len(sys.argv) < 2:
    print("Usage: python migrate_db.py [path_to_env_file]")
    sys.exit(1)

# Load cấu hình từ file .env được chỉ định
env_file = sys.argv[1]
load_dotenv(env_file)

# Kết nối tới database nguồn (SQLite)
sqlite_url = "sqlite:///./app.db"
sqlite_engine = create_engine(sqlite_url)
SqliteSession = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
sqlite_session = SqliteSession()

# Kết nối tới database đích (PostgreSQL)
pg_url = os.getenv("DATABASE_URL")
if not pg_url:
    print("ERROR: DATABASE_URL not found in environment variables")
    sys.exit(1)

pg_engine = create_engine(pg_url)
PgSession = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
pg_session = PgSession()

# Danh sách các bảng cần di chuyển
tables = [
    "users",
    "models",
    "code_history",
    "payments",
    # Thêm các bảng khác nếu cần
]

print("Starting database migration from SQLite to PostgreSQL...")

try:
    # Di chuyển dữ liệu từng bảng
    for table in tables:
        print(f"Migrating table: {table}")
        
        # Lấy dữ liệu từ SQLite
        result = sqlite_session.execute(text(f"SELECT * FROM {table}"))
        rows = result.fetchall()
        
        if not rows:
            print(f"  - No data in table {table}")
            continue
            
        print(f"  - Found {len(rows)} rows")
        
        # Lấy tên cột
        columns = result.keys()
        
        # Tạo câu lệnh INSERT
        for row in rows:
            column_names = ", ".join(columns)
            placeholders = ", ".join([":"+c for c in columns])
            insert_query = text(f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})")
            
            # Tạo dictionary từ row
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i]
            
            # Thực hiện insert vào PostgreSQL
            pg_session.execute(insert_query, row_dict)
        
        pg_session.commit()
        print(f"  - Successfully migrated table {table}")
    
    print("Migration completed successfully!")
    
except Exception as e:
    pg_session.rollback()
    print(f"ERROR during migration: {str(e)}")
    sys.exit(1)
    
finally:
    sqlite_session.close()
    pg_session.close()