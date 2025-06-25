import hashlib
import random
import requests
import time
from datetime import datetime
import json
import sys
import urllib3
import os
from base64 import b64encode

# Hiệu ứng màu sắc
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\x1b[38;2;0;255;127m"
RED = "\x1b[38;2;255;69;0m"
CYAN = "\x1b[38;2;0;255;255m"
YELLOW = "\x1b[38;2;255;215;0m"
PINK = "\x1b[38;2;255;105;180m"
WHITE = "\x1b[38;2;245;245;245m"
CHECK = f"{GREEN}✔{RESET}"
CROSS = f"{RED}✘{RESET}"
STAR = f"{YELLOW}★{RESET}"
INFO = f"{CYAN}ℹ{RESET}"
LINE = f"{CYAN}═{"═" * 48}═{RESET}"
HALF_LINE = f"{PINK}─{"─" * 20}─{RESET}"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cấu hình API
app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32'
}

email_prefix = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']

vietnamese_names = {
    'ho': ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Phan', 'Vũ', 'Đặng', 'Bùi', 'Đỗ', 'Hồ'],
    'dem': ['Văn', 'Thị', 'Hữu', 'Đức', 'Gia', 'Minh', 'Nhật', 'Ngọc', 'Thanh', 'Quốc'],
    'ten': ['Anh', 'Bảo', 'Châu', 'Duy', 'Hùng', 'Khoa', 'Linh', 'My', 'Nam', 'Phúc', 'Quang', 'Trang']
}

def random_vietnamese_name():
    ho = random.choice(vietnamese_names['ho'])
    dem = random.choice(vietnamese_names['dem'])
    ten = random.choice(vietnamese_names['ten'])
    return ho, dem, ten

def get_random_avatar_base64():
    try:
        avt_files = [f for f in os.listdir('avt') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not avt_files:
            return None
        with open(f"avt/{random.choice(avt_files)}", "rb") as f:
            return b64encode(f.read()).decode()
    except:
        return None

def get_random_proxy(proxy_list):
    if not proxy_list:
        return None
    return random.choice(proxy_list)

def format_proxy(proxy_str):
    if proxy_str.startswith('socks'):
        return {'http': proxy_str, 'https': proxy_str}
    else:
        return {'http': f"http://{proxy_str}", 'https': f"http://{proxy_str}"}

def create_account(proxy_list):
    birth = datetime.strftime(datetime.fromtimestamp(random.randint(
        int(time.mktime(datetime.strptime('1990-01-01', '%Y-%m-%d').timetuple())),
        int(time.mktime(datetime.strptime('2002-12-30', '%Y-%m-%d').timetuple()))
    )), '%Y-%m-%d')

    ho, dem, ten = random_vietnamese_name()
    full_name = f"{ho} {dem} {ten}"
    password = f'{ho}{random.randint(1000, 999999)}@NvĐ'
    email = f"{ho.lower()}{dem.lower()}{ten.lower()}{random.randint(1000,9999)}@{random.choice(email_prefix)}"
    gender = 'M' if dem != 'Thị' else 'F'
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()
    reg_instance = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"

    proxy = get_random_proxy(proxy_list)
    proxy_dict = format_proxy(proxy) if proxy else None
    avatar_base64 = get_random_avatar_base64()

    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': birth,
        'client_country_code': 'VN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': ho,
        'lastname': f"{dem} {ten}",
        'email': email,
        'gender': gender,
        'locale': 'vi_VN',
        'method': 'user.register',
        'password': password,
        'reg_instance': reg_instance,
        'format': 'json',
        'return_multiple_errors': True
    }

    if avatar_base64:
        req['profile_pic'] = avatar_base64

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    req['sig'] = hashlib.md5((sig + app['secret']).encode()).hexdigest()

    try:
        res = requests.post(
            'https://b-api.facebook.com/method/user.register',
            data=req,
            verify=False,
            headers={
                'User-Agent': 'FB4A; FBAV/350.0.0.48.273; FBBV/313055866',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            proxies=proxy_dict,
            timeout=30
        )
        reg_json = res.json()
    except Exception as e:
        print(f"{CROSS} {RED}Lỗi proxy: {e}{RESET}")
        return

    uid = reg_json.get('session_info', {}).get('uid')
    token = reg_json.get('session_info', {}).get('access_token')
    error = reg_json.get('error_msg')

    if uid and token:
        with open(file_name, 'a') as f:
            f.write(f"{birth}:{full_name}:{email}:{password}:{uid}:{token}\n")

        print(LINE)
        print(f"{CHECK} {GREEN}Đăng ký thành công!")
        print(f"{INFO} Họ: {RED}{ho}{RESET} | Đệm: {CYAN}{dem}{RESET} | Tên: {PINK}{ten}{RESET}")
        print(f"{INFO} Email: {YELLOW}{email}{RESET}")
        print(f"{INFO} UID: {WHITE}{uid}{RESET}")
        if proxy:
            print(f"{INFO} Proxy: {CYAN}{proxy}{RESET}")
        if avatar_base64:
            print(f"{INFO} Avatar: {GREEN}✔{RESET} Đã chèn avt")
        print(f"{INFO} Token: {WHITE}{token}{RESET}")
        print(LINE)
    else:
        print(LINE)
        print(f"{CROSS} {RED}Đăng ký thất bại!{RESET}")
        print(f"{INFO} Lỗi: {YELLOW}{error or 'Không rõ'}{RESET}")
        if proxy:
            print(f"{INFO} Proxy dùng: {proxy}")
        print(LINE)

# Nhập số lượng, tên file, và file proxy
while True:
    try:
        account_count = int(input(f"{STAR} {CYAN}Nhập số tài khoản muốn tạo: {RESET}"))
        if account_count > 0:
            break
        else:
            print(f"{CROSS} {RED}Phải > 0!{RESET}")
    except:
        print(f"{CROSS} {RED}Lỗi nhập!{RESET}")

while True:
    file_name = input(f"{STAR} {CYAN}Tên file lưu acc: {RESET}").strip()
    if file_name:
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        break
    else:
        print(f"{CROSS} {RED}Không được trống!{RESET}")

proxy_list = []
proxy_file = input(f"{STAR} {CYAN}Nhập tên file proxy (Enter nếu không dùng proxy): {RESET}").strip()
if proxy_file:
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            proxy_list = [line.strip() for line in f if line.strip()]
    else:
        print(f"{CROSS} {RED}File proxy không tồn tại! Tiếp tục không dùng proxy.{RESET}")

print(LINE)
print(f"{CHECK} {GREEN}Bắt đầu tạo {account_count} tài khoản...{RESET}")
print(LINE)
for i in range(account_count):
    print(f"{HALF_LINE} Tài khoản {i+1}/{account_count} {HALF_LINE}")
    create_account(proxy_list)

print(LINE)
print(f"{CHECK} {GREEN}Hoàn tất! Đã lưu vào: {WHITE}{file_name}{RESET}")
print(LINE)
sys.exit()
