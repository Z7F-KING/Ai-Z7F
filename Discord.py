import asyncio
import aiohttp
import random
import string
from pathlib import Path

FILE_SAVE = "DiscordUserByZ7F.txt"
LENGTH = 4
CHARSET = string.ascii_lowercase + string.digits

# بروكسياتك كلها
PROXIES = [
    "183.110.216.159:8090",
    "47.103.30.64:8080",
    "87.120.216.231:65000",
    "8.215.25.3:2081",
    "216.106.182.177:3128",
    "130.110.103.245:3128",
    "195.191.158.128:8080",
    "219.249.37.107:8382",
    "78.189.92.15:1953",
    "112.74.101.87:9999",
    "66.163.127.204:10006",
    "204.76.203.9:3128",
    "122.246.4.6:17981",
    "219.65.73.81:80",
    "39.106.165.196:8080",
    "5.39.218.113:3128",
    "58.254.153.147:17981",
    "218.252.100.222:80",
    "185.105.118.110:8080",
    "16.163.88.228:80",
    "8.215.25.3:2080",
    "219.93.101.60:80",
    "197.221.249.198:80",
    "38.76.9.0:999",
    "41.220.22.7:80",
    "116.0.53.37:8080",
    "212.127.95.235:8081",
    "91.239.211.19:10808",
    "41.220.16.214:80",
    "8.215.112.34:7777",
    "163.181.207.213:9999",
    "218.252.192.228:80",
    "97.74.87.226:80",
    "120.232.115.170:17981",
    "12.50.107.217:80",
    "185.235.16.12:80",
    "89.167.124.218:8888",
    "213.14.182.148:3310",
    "37.59.125.131:8888",
    "219.93.101.62:80",
    "112.64.135.45:8080",
    "92.169.21.156:80",
    "40.160.27.66:1080",
]

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

checked = 0
found = 0
proxy_index = 0

def format_proxy(p):
    if not p: return None
    if not p.startswith("http"): return f"http://{p}"
    return p

def save_user(username):
    Path(FILE_SAVE).touch(exist_ok=True)
    with open(FILE_SAVE, "r", encoding="utf-8") as f:
        existing = set(l.strip() for l in f)
    if username in existing:
        return
    with open(FILE_SAVE, "a", encoding="utf-8") as f:
        f.write(username + "\n")
    # ترتيب
    with open(FILE_SAVE, "r", encoding="utf-8") as f:
        lines = sorted(set(l.strip() for l in f if l.strip()))
    with open(FILE_SAVE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

async def check_username(session, username):
    global checked, found, proxy_index

    # نجرب كل البروكسيات واحد واحد لليوزر نفسه
    for i in range(len(PROXIES) + 1):
        if proxy_index < len(PROXIES):
            proxy_raw = PROXIES[proxy_index]
            proxy = format_proxy(proxy_raw)
            proxy_display = proxy_raw
        else:
            proxy = None
            proxy_display = "بدون بروكسي"

        try:
            async with session.post(URL, json={"username": username}, headers=HEADERS, proxy=proxy, timeout=8) as r:
                if r.status == 429:
                    data = await r.json()
                    wait = data.get("retry_after", 2)
                    print(f"[!] Rate Limit {wait}s على {proxy_display} - نبدل")
                    proxy_index += 1
                    await asyncio.sleep(wait)
                    continue

                data = await r.json()
                taken = data.get("taken", True)
                checked += 1

                if taken is False:
                    found += 1
                    save_user(username)
                    print(f"\n[✓ متاح] {username} | بروكسي: {proxy_display} | فحصنا: {checked} | لقينا: {found}")
                    return True
                else:
                    print(f"[x] {username} مستخدم | {proxy_display} | فحصنا: {checked} | متاح: {found}", end="\r")
                    return False

        except Exception as e:
            # البروكسي ميت نروح للي بعده فوراً
            print(f"[!] البروكسي مات {proxy_display} -> نجرب اللي بعده")
            proxy_index += 1
            if proxy_index > len(PROXIES):
                proxy_index = len(PROXIES) # نثبت على بدون بروكسي
            continue

    # اذا خلصو كلهم
    print(f"\n[!] خلصو البروكسيات كلها، بنكمل بدون بروكسي من الحين")
    return False

async def main():
    global proxy_index
    Path(FILE_SAVE).touch(exist_ok=True)
    print(f"""

Z7F Discord Checker - By Z7F
البروكسيات: {len(PROXIES)}
الحفظ في: {FILE_SAVE}
يفحط لانهائي لين تقفل بـ CTRL+C

""")
    async with aiohttp.ClientSession() as session:
        while True:
            username = ''.join(random.choices(CHARSET, k=LENGTH))
            if username[0] in "._" or username[-1] in "._": continue
            if "__" in username or ".." in username: continue

            await check_username(session, username)
            await asyncio.sleep(0.6 + random.uniform(0, 0.7))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\nوقفنا - كل شي محفوظ في {FILE_SAVE}")
