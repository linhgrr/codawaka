import aiohttp
import asyncio
import time
import random
from tqdm import tqdm  # <- Import thư viện tqdm để tạo progress bar

# Cấu hình
BASE_URL = "http://localhost:8000"  # Thay đổi URL nếu cần
USERNAME = "admin123"
MODEL = "gemini-2.0-flash"
TOTAL_REQUESTS = 100
MAX_CONCURRENT = 10  # Số lượng request đồng thời tối đa

# Danh sách các prompt mẫu để tạo sự đa dạng
SAMPLE_PROMPTS = [
    "Viết hàm tính giai thừa",
    "Viết chương trình sắp xếp mảng",
    "Viết hàm kiểm tra số nguyên tố",
    "Tạo class quản lý sinh viên",
    "Viết chương trình đọc file CSV",
    "Viết hàm tìm kiếm nhị phân",
    "Tạo REST API đơn giản với Flask",
    "Viết hàm đệ quy tính dãy Fibonacci",
    "Lập trình game đoán số",
    "Tạo chương trình quản lý thư viện",
]

# Biến đếm toàn cục
successful_requests = 0
failed_requests = 0

# Hàm gửi một request
async def send_code_request(session, index, pbar, lock):
    global successful_requests, failed_requests

    prompt = random.choice(SAMPLE_PROMPTS)
    language = random.choice(["Python", "C++", "JavaScript", "Java"])
    
    data = {
        "username": USERNAME,
        "model_name": MODEL,
        "prompt": f"{prompt} sử dụng {language}",
        "language": language
    }
    
    start_time = time.time()
    try:
        async with session.post(f"{BASE_URL}/code/completion", json=data) as response:
            elapsed = time.time() - start_time
            status = response.status

            async with lock:
                if status == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                update_progress(pbar)
            return (status == 200), elapsed
    except Exception:
        elapsed = time.time() - start_time
        async with lock:
            failed_requests += 1
            update_progress(pbar)
        return False, elapsed

# Hàm cập nhật progress bar
def update_progress(pbar):
    total_done = successful_requests + failed_requests
    success_rate = (successful_requests / total_done) * 100 if total_done else 0
    pbar.update(1)
    pbar.set_description(f"Đã hoàn thành: {total_done}/{TOTAL_REQUESTS} | Thành công: {success_rate:.2f}%")

# Hàm chính chạy stress test
async def run_stress_test():
    global successful_requests, failed_requests

    total_time = 0
    response_times = []

    start_time = time.time()
    lock = asyncio.Lock()
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT)

    async with aiohttp.ClientSession(connector=connector) as session:
        with tqdm(total=TOTAL_REQUESTS, ncols=100) as pbar:
            tasks = []
            for i in range(TOTAL_REQUESTS):
                task = asyncio.create_task(send_code_request(session, i, pbar, lock))
                tasks.append(task)
                await asyncio.sleep(0.05)

            results = await asyncio.gather(*tasks)

            for success, elapsed in results:
                response_times.append(elapsed)
                total_time += elapsed

    end_time = time.time()
    test_duration = end_time - start_time

    avg_response_time = total_time / len(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0

    print("\n--- Kết quả Stress Test ---")
    print(f"Tổng số request: {TOTAL_REQUESTS}")
    print(f"Request thành công: {successful_requests}")
    print(f"Request thất bại: {failed_requests}")
    print(f"Tỷ lệ thành công: {successful_requests/TOTAL_REQUESTS*100:.2f}%")
    print(f"Thời gian test: {test_duration:.2f} giây")
    print(f"Requests/giây: {TOTAL_REQUESTS/test_duration:.2f}")
    print(f"Thời gian phản hồi trung bình: {avg_response_time:.2f} giây")
    print(f"Thời gian phản hồi tối thiểu: {min_response_time:.2f} giây")
    print(f"Thời gian phản hồi tối đa: {max_response_time:.2f} giây")

# Chạy stress test
if __name__ == "__main__":
    print(f"Bắt đầu stress test với {TOTAL_REQUESTS} requests sử dụng {USERNAME} và model {MODEL}")
    asyncio.run(run_stress_test())
