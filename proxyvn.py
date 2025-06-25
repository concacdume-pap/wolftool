import requests, re,os,sys 
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate

# ========== Cài đặt ==========
TIMEOUT = 2
THREADS = 300
MAX_PROXY = 50000

# ========== Nguồn proxy Việt Nam ==========
proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1000&country=VN",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=VN",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=1000&country=VN",
    "https://proxylist.geonode.com/api/proxy-list?limit=300&country=VN&protocols=http",
    "https://www.proxy-list.download/api/v1/get?type=http&country=vn",
    "https://www.proxy-list.download/api/v1/get?type=https&country=vn",
    "https://www.proxy-list.download/api/v1/get?type=socks4&country=vn",
    "https://www.proxy-list.download/api/v1/get?type=socks5&country=vn",
    "https://www.proxy-list.download/api/v1/get?type=http&country=vn"
]

# ========== Hàm hỗ trợ ==========
def extract_proxies(text):
    return re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", text)

def fetch_proxy_source(url):
    try:
        res = requests.get(url, timeout=10)
        proxies = extract_proxies(res.text)
        return (url, proxies)
    except:
        return (url, [])

def check_proxy(proxy):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        res = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=TIMEOUT)
        if res.ok:
            print(f"\033[32m✓ Sống:\033[0m {proxy}")
            return proxy
    except:
        print(f"\033[31m✗ Chết:\033[0m {proxy}")
    return None

# ========== Chạy chính ==========
def main():
    os.system("clear")
    print("🚀 ĐANG ĐÀO PROXY...\n")
    all_proxy = []
    stats_table = []

    with ThreadPoolExecutor(max_workers=50) as pool:
        results = pool.map(fetch_proxy_source, proxy_sources)
        for url, proxies in results:
            all_proxy.extend(proxies)
            stats_table.append([url[:60] + ("..." if len(url) > 60 else ""), len(proxies)])

    print(tabulate(stats_table, headers=["Nguồn", "Số lượng proxy"], tablefmt="fancy_grid"))
    all_proxy = list(set(all_proxy))[:MAX_PROXY]

    with open("proxy_raw.txt", "w") as f:
        f.write("\n".join(all_proxy))
    print(f"\n📦 Tổng proxy thu được: {len(all_proxy)} (lưu proxy_raw.txt)")

    print("\n🧪 BẮT ĐẦU LỌC PROXY...\n")
    sleep(2)
    alive = []
    with ThreadPoolExecutor(max_workers=THREADS) as pool:
        futures = [pool.submit(check_proxy, p) for p in all_proxy]
        for f in as_completed(futures):
            result = f.result()
            if result: alive.append(result)

    with open("proxy_live.txt", "w") as f:
        f.write("\n".join(alive))

    print(f"\n🎯 Proxy sống: \033[32m{len(alive)}\033[0m / {len(all_proxy)} (lưu proxy_live.txt)")
    print("🎉 HOÀN TẤT!")

if __name__ == "__main__":
    main()
