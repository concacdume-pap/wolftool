import requests, json, os ,sys
from time import sleep
from threading import Thread
from tqdm import tqdm
from pystyle import Colors,Colorate 
from rich.console import Console
from colorama import Fore,init
import random

# Màu terminal ANSI
red = '\033[1;31m'
luc = '\033[1;32m'
vang = '\033[1;33m'
trang = '\033[1;37m'
thanh_xau = trang + '~' + red + '[' + vang + '⟨⟩' + red + '] ' + trang + '➩ ' + luc

console = Console()
init(autoreset=True)

SET_FILE = 'setting.json'
CRED_FILE = 'creds.json'

def dong_ke(n=14):
    for _ in range(n):
        print(red + '────', end='')
    print('')

def slow_type(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Diagonal(Colors.red_to_yellow, """
                      © Bản Quyền Thuộc PhuocAn 

 ██████╗ ██╗  ██╗██╗   ██╗ ██████╗  ██████╗                                            
 ██████╔╝███████║██║   ██║██║   ██║██║                         
 ██╔═══╝ ██╔══██║██║   ██║██║   ██║██║                           
 ██║     ██║  ██║╚██████╔╝╚██████╔╝╚██████╗                      
 ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ 
╠═══════════════════════════════════════════════╣
║▶ Nhóm   :  https://zalo.me/g/mprgxe166        ║
║▶ FaceBook : facebook.com/phuocan.9999         ║
║▶ Youtube : youtube.com/@phuocan.9999          ║
║▶ Zalo : 0915.948.201                          ║
╚═══════════════════════════════════════════════╝
════════════════════════════════════════════════════════════
BÁN KEY GIÁ 500Đ/1 NGÀY
════════════════════════════════════════════════════════════
"""))

def delay_progress(seconds):
    for _ in tqdm(range(seconds), desc="⏳ Đợi", ncols=70, colour='cyan'):
        sleep(1)

def login(self):
        try:
            res = requests.post('https://tuongtaccheo.com/logintoken.php', data={'access_token': self.token})
            data = res.json()
            self.cookie = 'PHPSESSID=' + res.cookies['PHPSESSID']
            return data['data']['user'], data['data']['sodu']
        except:
            return False


def mo_trinh_duyet(link):
    if not link.startswith('http://') and not link.startswith('https://'):
        link = 'https://www.tiktok.com/@' + link.strip('@')
    os.system(f'termux-open-url "{link}"')

def tap_vao(x, y, ip_port):
    os.system(f'adb connect {ip_port}')
    os.system(f'adb -s {ip_port} shell input tap {x} {y}')

def save_settings(data):
    with open(SET_FILE, 'w') as f:
        json.dump(data, f)

def load_settings():
    if os.path.exists(SET_FILE):
        with open(SET_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_creds(token, cookie):
    with open(CRED_FILE, 'w') as f:
        json.dump({"token": token, "cookie": cookie}, f)

def load_creds():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r') as f:
            return json.load(f)
    return {}

class TTC:
    def __init__(self, token, cookie):
        self.token = token
        self.cookie = cookie

     
    def get_job(self, endpoint):
        try:
            headers = {'cookie': self.cookie, 'user-agent': 'Mozilla/5.0', 'x-requested-with': 'XMLHttpRequest'}
            res = requests.post(f'https://tuongtaccheo.com/tiktok/kiemtien/{endpoint}', headers=headers)
            return res.json()
        except:
            return False

    def nhantien(self, ids, endpoint):
        try:
            headers = {
                'cookie': self.cookie,
                'user-agent': 'Mozilla/5.0',
                'x-requested-with': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            data = {'id': ids}
            res = requests.post(endpoint, headers=headers, data=data)
            res_json = res.json()
            if 'mess' in res_json:
                return res_json.get('sodu', 'Không rõ'), res_json.get('xu', 0)
            return False, 0
        except:
            return False, 0

    def dat_cau_hinh(self, uid):
        try:
            headers = {'cookie': self.cookie, 'user-agent': 'Mozilla/5.0'}
            res = requests.post('https://tuongtaccheo.com/cauhinh/datnick.php',
                                headers=headers, data={'iddat[]': uid, 'loai': 'tt'})
            return res.json() if res.text.startswith('{') else {"status": int(res.text.strip())}
        except:
            return {}

def run_tool():
    banner()
    dong_ke()
    print(f'{luc}1. Dùng token + cookie đã lưu')
    print(f'{luc}2. Nhập mới token + cookie TTC')
    choice = input(f'{thanh_xau}Chọn: {vang}').strip()

    if choice == '1':
        creds = load_creds()
        token = creds.get("token", "")
        cookie = creds.get("cookie", "")
        if not token or not cookie:
            print(red + "❌ Không tìm thấy token/cookie đã lưu. Vui lòng chọn nhập mới.")
            return
    else:
        token = input(f'{thanh_xau}Nhập Access_Token TTC: {vang}')
        cookie = input(f'{thanh_xau}Nhập Cookie TTC: {vang}')
        save_creds(token, cookie)

    client = TTC(token, cookie)
    dong_ke()
    use_adb = input(f'{thanh_xau}Bạn có muốn dùng ADB tự động? (1 = Có / 2 = Không): {vang}').strip()
    adb_mode = (use_adb == '1')

    settings = load_settings() if adb_mode else {}
    if adb_mode:
        if settings:
            ip_port = settings['ip_port']
            x_follow, y_follow = settings['follow']
            x_tym, y_tym = settings['tym']
        else:
            ip_port = input(f'{thanh_xau}Nhập IP và cổng ADB (vd: 192.168.1.8:5555): {vang}')
            x_follow = int(input(f'{thanh_xau}Toạ độ FOLLOW - nhập X: {vang}'))
            y_follow = int(input(f'{thanh_xau}Toạ độ FOLLOW - nhập Y: {vang}'))
            x_tym = int(input(f'{thanh_xau}Toạ độ TYM - nhập X: {vang}'))
            y_tym = int(input(f'{thanh_xau}Toạ độ TYM - nhập Y: {vang}'))
            save_settings({
                'ip_port': ip_port,
                'follow': [x_follow, y_follow],
                'tym': [x_tym, y_tym]
            })
            print(f'{luc}✅ Đã lưu setting vào file {SET_FILE}')

    uid = input(f'{thanh_xau}{luc}Nhập UID TikTok Cấu Hình : {vang}')
    if uid:
        result = client.dat_cau_hinh(uid)
        if result and result.get('status') == 1:
            print(f'{luc}✅ Cấu hình thành công UID: {vang}{uid}')
        else:
            print(red + '❌ Cấu hình thất bại hoặc UID không hợp lệ.')
            sys.exit("")
        dong_ke()

    job_type = input(f'{thanh_xau}{luc}Loại nhiệm vụ [tim/follow]: {vang}')
    endpoint = 'getpost.php' if job_type == 'tim' else 'subcheo/getpost.php'
    nhan_endpoint = 'https://tuongtaccheo.com/tiktok/kiemtien/subcheo/nhantien.php'
    if adb_mode:
        x, y = (x_tym, y_tym) if job_type == 'tim' else (x_follow, y_follow)

    while True:
        try:
            delay = int(input(f'{thanh_xau}{luc}Delay mỗi job (lớn hơn 10s): {vang}'))
            if delay < 10:
                print(red + '❌ Delay phải trên 10 giây')
                continue
            per_xu = int(input(f'{thanh_xau}{luc}Số nhiệm vụ để nhận xu (10-40): {vang}'))
            if per_xu < 10 or per_xu > 40:
                print(red + '❌ Chỉ chấp nhận từ 10 đến 40 nhiệm vụ!')
                continue
            break
        except:
            print(red + '❌ Nhập số không hợp lệ.')

    done, ids = 0, ''
    while True:
        jobs = client.get_job(endpoint)
        if not jobs:
            print(red + '⚠️ Không lấy được nhiệm vụ.')
            sleep(2)
            continue

        for job in jobs:
            if isinstance(job, str):
                try:
                    job = json.loads(job)
                except:
                    continue

            try:
                link = job['link']
                idpost = job['idpost']
            except:
                continue

            Thread(target=mo_trinh_duyet, args=(link,)).start()
            print(f'{luc} JOB {done} : {vang}{idpost}')
            done += 1
            ids += str(idpost) + ','

            if adb_mode:
                tap_vao(x, y, ip_port)
            delay_progress(delay)

            if done % per_xu == 0:
                print(f'{luc}→ Nhận xu...')
                sodu, xu_cong = client.nhantien(ids.strip(','), nhan_endpoint)
                ids = ''
                if not sodu:
                    print(red + '❌ Nhận xu thất bại')
                else:
                    print(f'{luc}✅ Nhận thành công ({done})... {vang}+{xu_cong} {luc}xu | Xu hiện tại: {vang}{sodu}')
                dong_ke()

run_tool()
