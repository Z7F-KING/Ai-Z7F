import asyncio
import aiohttp
import sys

# مصادر متجددة وسريعة لجلب البروكسيات
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

async def fetch_all_proxies(session):
    proxies = set()
    for url in PROXY_SOURCES:
        try:
            async with session.get(url, timeout=4) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.splitlines():
                        line = line.strip()
                        if ":" in line and len(line.split(":")) == 2:
                            proxies.add(line)
        except Exception:
            continue
    return list(proxies)

async def check_proxy_fast(session, proxy, working_list, semaphore):
    async with semaphore:
        proxy_url = f"http://{proxy}"
        try:
            # مهلة 1.5 ثانية لضمان أقصى سرعة
            async with session.get("https://httpbin.org/ip", proxy=proxy_url, timeout=aiohttp.ClientTimeout(total=1.5)) as response:
                if response.status == 200:
                    working_list.append(proxy)
                    print(f"\033[92m[+] شغال : {proxy}\033[0m")
                    sys.stdout.flush()
                    return
        except Exception:
            pass
        
        # طباعة البروكسي غير المتاح / الخربان
        print(f"\033[91m[-] خربان : {proxy}\033[0m")
        sys.stdout.flush()

async def main():
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        print("[*] جاري جلب آلاف البروكسيات...")
        raw_proxies = await fetch_all_proxies(session)
        total_count = len(raw_proxies)
        
        print(f"[*] تم جلب {total_count} بروكسي.")
        print("[*] جاري الفحص السريع (عرض الشغال والخربان)...\n")

        working_proxies = []
        # فحص 500 بروكسي بالتوازي للحفاظ على السرعة العالية
        semaphore = asyncio.Semaphore(500)

        tasks = [check_proxy_fast(session, proxy, working_proxies, semaphore) for proxy in raw_proxies]
        await asyncio.gather(*tasks)

        print(f"\n\033[94m[✓] انتهى الفحص! البروكسيات الشغالة والسريعة: {len(working_proxies)} / {total_count}\033[0m")
        
        with open("working_proxies.txt", "w") as f:
            for p in working_proxies:
                f.write(f"{p}\n")
        print("[*] تم حفظ البروكسيات الشغالة فقط في working_proxies.txt")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[-] تم إيقاف الفحص.")
