import asyncio
import aiohttp

# جلب قائمة بروكسيات متجددة من مصادر مفتوحة
async def fetch_proxies(session):
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
    ]
    proxies = set()
    for url in urls:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.splitlines():
                        if ":" in line and len(line.split(":")) == 2:
                            proxies.add(line.strip())
        except Exception:
            continue
    return list(proxies)

# فحص البروكسي بسرعة عالية
async def check_proxy(session, proxy, working_list, semaphore):
    async with semaphore:  # تحديد عدد الفحوصات المتزامنة لمنع الضغط المحلي
        proxy_url = f"http://{proxy}"
        try:
            # استخدام مهلة قصيرة جداً (2 ثوانٍ) لضمان السرعة
            async with session.get("https://httpbin.org/ip", proxy=proxy_url, timeout=2) as response:
                if response.status == 200:
                    working_list.append(proxy)
                    print(f"[+] شغال وسريع: {proxy}")
        except Exception:
            pass

async def main():
    connector = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=connector) as session:
        print("[*] جاري جلب قوائم البروكسيات...")
        raw_proxies = await fetch_proxies(session)
        print(f"[*] تم جلب {len(raw_proxies)} بروكسي. جاري الفحص السريع...")

        working_proxies = []
        semaphore = asyncio.Semaphore(100)  # فحص 100 بروكسي في نفس اللحظة

        tasks = [check_proxy(session, proxy, working_proxies, semaphore) for proxy in raw_proxies]
        await asyncio.gather(*tasks)

        print(f"\n[✓] اكتمل الفحص! عدد البروكسيات الشغالة والسريعة: {len(working_proxies)}")
        
        # حفظ الشغال في ملف نصي للاستخدام المباشر
        with open("working_proxies.txt", "w") as f:
            for p in working_proxies:
                f.write(f"{p}\n")
        print("[*] تم حفظ البروكسيات الشغالة في working_proxies.txt")

if __name__ == "__main__":
    # تشغيل السكربت
    asyncio.run(main())
