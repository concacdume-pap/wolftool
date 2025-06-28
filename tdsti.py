#Coded by Traodoisub.com (Modified with ADB option)
import os
from time import sleep
from datetime import datetime

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

try:
	import requests
except:
	os.system("pip3 install requests")
	import requests

try:
	from pystyle import Colors, Colorate, Write, Center, Add, Box
except:
	os.system("pip3 install pystyle")
	from pystyle import Colors, Colorate, Write, Center, Add, Box

headers = {
	'authority': 'traodoisub.com',
	'accept': '*/*',
	'accept-language': 'vi,en;q=0.9',
	'user-agent': 'traodoisub tiktok tool',
}

def login_tds(token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+token, headers=headers, timeout=5).json()
		if 'success' in r:
			os.system('clear')
			print(Colors.green + f"Đăng nhập thành công!\nUser: {Colors.yellow + r['data']['user'] + Colors.green} | Xu hiện tại: {Colors.yellow + r['data']['xu']}")
			return 'success'
		else:
			print(Colors.red + f"Token TDS không hợp lệ, hãy kiểm tra lại!\n")
			return 'error_token'
	except:
		return 'error'

def load_job(type_job, token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields='+type_job+'&access_token='+token, headers=headers, timeout=5).json()
		if 'data' in r:
			return r
		elif "countdown" in r:
			sleep(round(r['countdown']))
			print(Colors.red + f"{r['error']}\n")
			return 'error_countdown'
		else:
			print(Colors.red + f"{r['error']}\n")
			return 'error_error'
	except:
		return 'error'

def duyet_job(type_job, token, uid):
	try:
		r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={uid}&access_token={token}', headers=headers, timeout=5).json()
		if "cache" in r:
			return r['cache']
		elif "success" in r:
			print(f"{Colors.cyan}Nhận thành công {r['data']['job_success']} nhiệm vụ | {Colors.green}{r['data']['msg']} | {Colors.yellow}{r['data']['xu']}")
			return 'error'
		else:
			print(f"{Colors.red}{r['error']}")
			return 'error'
	except:
		return 'error'

def check_tiktok(id_tiktok, token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields=tiktok_run&id='+id_tiktok+'&access_token='+token, headers=headers, timeout=5).json()
		if 'success' in r:
			os.system('clear')
			print(Colors.green + f"{r['data']['msg']}|ID: {Colors.yellow + r['data']['id'] + Colors.green}")
			return 'success'
		else:
			print(Colors.red + f"{r['error']}\n")
			return 'error_token'
	except:
		return 'error'

# BANNER
os.system('clear')
banner = r'''
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
BÁN KEY GIÁ 1K/1 NGÀY
════════════════════════════════════════════════════════════

'''
gach  = '========================================='
option = f'''{gach}{Colors.green}
Danh sách nhiệm vu tool hỗ trợ: {Colors.red}
1.Job Follow
2.Job Tym
{Colors.yellow}{gach}
'''
option_acc = f'''{gach}{Colors.green}
Danh sách lựa chọn: {Colors.red}
1. Tiếp tục sử dụng acc TDS đã lưu
2. Sử dụng acc TDS mới
{Colors.yellow}{gach}
'''
print(Colorate.Horizontal(Colors.yellow_to_red, Center.XCenter(banner)))
print(Colors.red + Center.XCenter(Box.DoubleCube("Tool TDS TikTok Free Version 1.0")))

# LOGIN TOKEN
while True:
	try:
		f = open(f'TDS.txt','r')
		token_tds = f.read()
		f.close()
		cache = 'old'
	except FileNotFoundError:
		token_tds = Write.Input("Nhập token TDS:", Colors.green_to_yellow, interval=0.0025)
		cache = 'new'
	
	for _ in range(3):
		check_log = login_tds(token_tds)
		if check_log == 'success' or check_log == 'error_token':
			break
		else:
			sleep(2)

	if check_log == 'success':
		if cache == 'old':
			while True:
				print(option_acc)
				try:
					choice = int(Write.Input("Lựa chọn của bạn là (Ví dụ: sử dụng acc cũ nhập 1):", Colors.green_to_yellow, interval=0.0025))
					if choice in [1,2]:
						break
				except: pass
				os.system('clear')
				print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")
			
			os.system('clear')
			if choice == 1:
				break
			else:
				os.remove('TDS.txt')
		else:
			f = open(f'TDS.txt', 'w')
			f.write(f'{token_tds}')
			f.close()
			break
	else:
		sleep(1)
		os.system('clear')

# CẤU HÌNH JOB
if check_log == 'success':
	while True:
		id_tiktok = Write.Input("Nhập ID TikTok chạy (lấy ở cấu hình web TDS):", Colors.green_to_yellow, interval=0.0025)
		for _ in range(3):
			check_log = check_tiktok(id_tiktok, token_tds)
			if check_log == 'success' or check_log == 'error_token':
				break
			else:
				sleep(2)
		if check_log == 'success':
			break
		else:
			os.system('clear')
			print(Colors.red + f"ID chưa được cấu hình! Hãy cấu hình trên TDS rồi nhập lại.\n")

	while True:
		print(option)
		try:
			choice = int(Write.Input("Lựa chọn nhiệm vụ muốn làm (1 = Follow, 2 = Tym):", Colors.green_to_yellow, interval=0.0025))
			if choice in [1,2]:
				break
		except: pass
		os.system('clear')
		print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")

	while True:
		try:
			delay = int(Write.Input("Thời gian delay giữa các job (giây):", Colors.green_to_yellow, interval=0.0025))
			if delay > 1:
				break
		except: pass
		os.system('clear')
		print(Colors.red + f"Vui lòng nhập số > 2\n")

	# THÊM HỎI DÙNG ADB
	while True:
		try:
			use_adb = int(Write.Input("Bạn có muốn mở link TikTok bằng ADB không? (1 = Có, 2 = Không):", Colors.green_to_yellow, interval=0.0025))
			if use_adb in [1,2]:
				break
		except: pass
		os.system('clear')
		print(Colors.red + f"Chỉ được nhập 1 hoặc 2!\n")

	while True:
		try:
			max_job = int(Write.Input("Dừng lại sau bao nhiêu nhiệm vụ?:", Colors.green_to_yellow, interval=0.0025))
			if max_job > 9:
				break
		except: pass
		os.system('clear')
		print(Colors.red + f"Vui lòng nhập số > 9\n")

	os.system('clear')

	if choice == 1:
		type_load = 'tiktok_follow'
		type_duyet = 'TIKTOK_FOLLOW_CACHE'
		type_nhan = 'TIKTOK_FOLLOW'
		type_type = 'FOLLOW'
		api_type = 'TIKTOK_FOLLOW_API'
	else:
		type_load = 'tiktok_like'
		type_duyet = 'TIKTOK_LIKE_CACHE'
		type_nhan = 'TIKTOK_LIKE'
		type_type = 'TYM'
		api_type = 'TIKTOK_LIKE_API'

	dem_tong = 0

	while True:
		list_job = load_job(type_load, token_tds)
		sleep(2)
		if isinstance(list_job, dict):
			for job in list_job['data']:
				uid = job['id']
				link = job['link']

				if use_adb == 1:
					os.system(f'adb shell am start -a android.intent.action.VIEW -d "{link}"')
				else:
					os.system(f'termux-open-url "{link}"')

				check_duyet = duyet_job(type_duyet, token_tds, uid)

				if check_duyet != 'error':
					dem_tong += 1
					t_now = datetime.now().strftime("%H:%M:%S")
					print(f'{Colors.yellow}[{dem_tong}] {Colors.red}| {Colors.cyan}{t_now} {Colors.red}| {Colors.pink}{type_type} {Colors.red}| {Colors.light_gray}{uid}')

					if check_duyet > 9:
						sleep(3)
						duyet_job(type_nhan, token_tds, api_type)

				if dem_tong == max_job:
					break
				else:
					for i in range(delay,-1,-1):
						print(Colors.green + 'Vui lòng đợi: '+str(i)+' giây',end=('\r'))
						sleep(1)

		if dem_tong == max_job:
			print(f'{Colors.green}Hoàn thành {max_job} nhiệm vụ!')
			break
