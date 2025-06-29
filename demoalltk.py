import os, sys, time, json, random
from datetime import datetime, date
from time import sleep
from rich.console import Console
from rich.table import Table
from tqdm import tqdm
import cloudscraper

# Hiệu ứng gõ chữ
def type_print(text, delay=0.01):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Banner
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    type_print("\033[1;36m═══════════════════════════════════════════════", 0.002)
    type_print("     🍉 TOOL GOLIKE THREADS AUTO BY PHUOCAN 🍉", 0.004)
    type_print("═══════════════════════════════════════════════\033[0m", 0.002)

# Hiển thị banner và hỏi tên
banner()
user_name = input("👤 Nhập tên của bạn để bắt đầu: ").strip()

# Đọc auth/token
with open("Authorization.txt", "r") as f:
    author = f.read().strip()
with open("token.txt", "r") as f:
    token = f.read().strip()

# Headers và scraper
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': author,
    't': token,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
    'Referer': 'https://app.golike.net/account/manager/threads',
}
scraper = cloudscraper.create_scraper()

# Các hàm gọi API
def chonacc():
    try:
        return scraper.get('https://gateway.golike.net/api/threads-account', headers=headers).json()
    except: return None

def nhannv(account_id):
    try:
        return scraper.get('https://gateway.golike.net/api/advertising/publishers/threads/jobs',
                           headers=headers, params={'account_id': account_id, 'data': 'null'}).json()
    except: return None

def hoanthanh(ads_id, account_id):
    try:
        return scraper.post('https://gateway.golike.net/api/advertising/publishers/threads/complete-jobs',
                            headers=headers, json={'ads_id': ads_id, 'account_id': account_id, 'async': True, 'data': None}).json()
    except: return None

def baoloi(ads_id, object_id, account_id, loai):
    try:
        scraper.post('https://gateway.golike.net/api/report/send', headers=headers, json={
            'description': 'Tôi đã làm Job này rồi',
            'users_advertising_id': ads_id,
            'type': 'ads',
            'provider': 'tiktok',
            'fb_id': account_id,
            'error_type': 6,
        })
        scraper.post('https://gateway.golike.net/api/advertising/publishers/threads/skip-jobs',
                     headers=headers, json={'ads_id': ads_id, 'object_id': object_id,
                                            'account_id': account_id, 'type': loai})
    except: pass

# Cấu hình tool
print("\n\033[1;33mChọn loại nhiệm vụ:")
print("1. Chỉ Follow")
print("2. Chỉ Like")
print("3. Cả Follow và Like")
while True:
    try:
        loai_nv = int(input("👉 Nhập số: "))
        if loai_nv in [1, 2, 3]: break
    except: pass

so_job_moi_acc = int(input("🍉 Nhập số job mỗi acc: "))
delay = int(input("⏱️  Nhập delay giữa các job (giây): "))
so_job_loi_doi_acc = int(input("💥 Nếu gặp bao nhiêu job lỗi thì đổi acc?: "))

dsacc = chonacc()
if not dsacc or dsacc.get("status") != 200:
    print("⛔ Lỗi khi lấy danh sách tài khoản."); sys.exit()

ads_ids_done = set()
tong, dem = 0, 0
user_log = []
today = str(date.today())

# Reset BXH nếu qua ngày
log_file = "golike_stats.json"
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        try: all_data = json.load(f)
        except: all_data = []
else:
    all_data = []

# Lọc log hôm nay
all_data = [item for item in all_data if item.get("date") == today]

# Vòng chạy
while True:
    for acc in dsacc["data"]:
        account_id, account_name = acc["id"], acc["name"]
        print(f"➡️ Đang chạy acc: {account_name}")
        job_done = job_loi = 0

        while job_done < so_job_moi_acc:
            if job_loi >= so_job_loi_doi_acc:
                print("🚫 Quá số job lỗi, đổi acc..."); break

            job = nhannv(account_id)
            if not job or job.get("status") != 200 or not job["data"].get("link"):
                print("⛔ Không có job hoặc lỗi."); job_loi += 1; sleep(2); continue

            ads_id = job["data"]["id"]
            object_id = job["data"]["object_id"]
            job_type = job["data"]["type"]

            if (loai_nv == 1 and job_type != "follow") or (loai_nv == 2 and job_type != "like"):
                baoloi(ads_id, object_id, account_id, job_type); continue

            if ads_id in ads_ids_done:
                print("⛔ Job trùng, bỏ qua..."); baoloi(ads_id, object_id, account_id, job_type); sleep(1); continue
            ads_ids_done.add(ads_id)

            for _ in tqdm(range(delay), desc="⏳ Delay", bar_format="{desc}: {n_fmt}/{total_fmt}s"):
                sleep(1)

            nhantien = hoanthanh(ads_id, account_id)
            if nhantien and nhantien.get("status") == 200:
                tien = nhantien["data"]["prices"]
                tong += tien; dem += 1
                thoigian = time.strftime("%H:%M:%S", time.localtime())

                table = Table(show_header=True, header_style="bold magenta", title="🍉 GOLIKE THREADS TRACKER 🍉")
                table.add_column("STT", style="bold yellow", justify="center")
                table.add_column("Tên", style="cyan", justify="center")
                table.add_column("Thời gian", style="green", justify="center")
                table.add_column("Xu cộng", style="bold green", justify="center")
                table.add_column("Tổng", style="bold white", justify="center")
                table.add_row(str(dem), account_name, thoigian,
                              f"[bold green]+{tien}", f"[bold yellow]{tong:,} vnđ")

                os.system('cls' if os.name == 'nt' else 'clear'); banner()
                Console().print(table)

                user_log.append({"name": user_name, "xu": tien, "date": today})
                job_done += 1
            else:
                print("❌ Job lỗi."); baoloi(ads_id, object_id, account_id, job_type)
                job_loi += 1; sleep(2)

    # Ghi log và BXH
    all_data.extend(user_log)
    with open(log_file, "w") as f:
        json.dump(all_data, f, indent=2)

    bxh = {}
    for item in all_data:
        if item["date"] == today:
            bxh[item["name"]] = bxh.get(item["name"], 0) + item["xu"]

    top = sorted(bxh.items(), key=lambda x: x[1], reverse=True)
    bxh_table = Table(title=f"🏆 BẢNG XẾP HẠNG NGÀY {today}", header_style="bold blue")
    bxh_table.add_column("Hạng", style="bold yellow")
    bxh_table.add_column("Tên", style="cyan")
    bxh_table.add_column("Tổng xu", style="green")

    for i, (name, total) in enumerate(top[:5], start=1):
        bxh_table.add_row(str(i), name, f"{total:,} đ")

    Console().print(bxh_table)
    user_log = []
    sleep(5)
