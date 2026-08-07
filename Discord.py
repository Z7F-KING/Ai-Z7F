import asyncio
import aiohttp
import sys

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

checked_count = 0
total_count = 0

async def fetch_all_proxies(session):
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.splitlines():
                        line = line.strip()
                        if ":" in line and len(line.split(":")) == 2:
                            proxies.add(line)
        except Exception:
            continue
    return list(proxies)

async def check_proxy(session, proxy, working_list, semaphore):
    global checked_count, total_count
    async with semaphore:
        proxy_url = f"http://{proxy}"
        is_working = False
        try:
            # مهلة 2 ثانية لتناسب سرعة معالجة الهواتف
            async with session.get("http://httpbin.org/ip", proxy=proxy_url, timeout=aiohttp.ClientTimeout(total=2)) as response:
                if response.status == 200:
                    is_working = True
        except Exception:
            is_working = False

        checked_count += 1
        if is_working:
            working_list.append(proxy)
            print(f"\033[92m[{checked_count}/{total_count}] [+] شغال : {proxy}\033[0m")
        else:
            print(f"\033[91m[{checked_count}/{total_count}] [-] خربان : {proxy}\033[0m")
        
        sys.stdout.flush()

async def main():
    global total_count
    # تحديد حدود الاتصال لتفادي خنق النظام في iSH
    connector = aiohttp.TCPConnector(limit=100, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        print("[*] جاري سحب القوائم...")
        raw_proxies = await fetch_all_proxies(session)
        total_count = len(raw_proxies)
        
        if total_count == 0:
            print("[-] لم يتم العثور على بروكسيات، تحقق من الاتصال بالمطبوعات.")
            return

        print(f"[*] تم جلب {total_count} بروكسي.")
        print("[*] جاري الفحص...\n")

        working_proxies = []
        # 50 اتصال متزامن لتفادي تعليق تطبيق iSH
        semaphore = asyncio.Semaphore(50)

        tasks = [check_proxy(session, proxy, working_proxies, semaphore) for proxy in raw_proxies]
        await asyncio.gather(*tasks)

        print(f"\n\033[94m[✓] اكتمل الفحص! الشغال: {len(working_proxies)} / {total_count}\033[0m")
        
        with open("working_proxies.txt", "w") as f:
            for p in working_proxies:
                f.write(f"{p}\n")
        print("[*] تم الحفظ في working_proxies.txt")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[-] تم الإيقاف.")
