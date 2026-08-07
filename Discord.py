import asyncio
import aiohttp
import random
import string
import os
from pathlib import Path

# ===== اعداداتك =====
FILE_SAVE = "DiscordUserByZ7F.txt" # اسم الملف اللي تبيه
PROXY_FILE = "proxies.txt"
CHARSET = string.ascii_lowercase + string.digits # حروف وارقام عشان تلاقي متاح، لو تبي حروف فقط شل string.digits
LENGTH = 4
CONCURRENT = 3 # خله قليل عشان ما تتبند
DELAY = 0.8

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

checked = 0
available = 0
seen = set()

def load_proxies():
    if not Path(PROXY_FILE).exists():
        return []
    proxies = []
    with open(PROXY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("http"):
                line = "http://" + line
            proxies.append(line)
    print(f"[+] لقيت {len(proxies)} بروكسي في {PROXY_FILE}")
    return proxies

def save_user(username):
    # يحفظ بدون تكرار وبالترتيب
    if not Path(FILE_SAVE).exists():
        Path(FILE_SAVE).write_text("", encoding="utf-8")

    with open(FILE_SAVE, "r", encoding="utf-8") as f:
        existing = set(x.strip() for x in f)

    if username not in existing:
        with open(FILE_SAVE, "a", encoding="utf-8") as f:
            f.write(username + "\n")
        # ترتيب الملف بعد كل اضافة
        with open(FILE_SAVE, "r", encoding="utf-8") as f:
            lines = sorted(set(x.strip() for x in f if x.strip()))
        with open(FILE_SAVE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

async def check_one(session, username, proxy_list):
    global checked, available
    proxy = random.choice(proxy_list) if proxy_list else None

    try:
        async with session.post(URL, json={"username": username}, headers=HEADERS, proxy=proxy, timeout=10) as r:
            if r.status == 429:
                data = await r.json()
                wait = data.get("retry_after", 3)
                print(f"[!] Rate limit {wait}s - نغير بروكسي")
                await asyncio.sleep(wait)
                return False

            data = await r.json()
            taken = data.get("taken", True)
            checked += 1

            if taken is False:
                available += 1
                save_user(username)
                print(f"\n[✓ متاح] {username} | فحصنا: {checked} | متاح: {available} | حفظ في {FILE_SAVE}")
                return True
            else:
                print(f"[x] {username} مستخدم | فحصنا: {checked} | متاح: {available}", end="\r")
                return False

    except Exception as e:
        # بروكسي ميت او خطأ شبكة - نكمل
        return False

async def main():
    proxies = load_proxies()
    if not proxies:
        print("[!] ما لقيت proxies.txt - بشتغل بدون بروكسي وبشكل آمن")

    Path(FILE_SAVE).touch(exist_ok=True)
    print(f"""

    Discord 4-Letter Checker By Z7F
    يحفظ في: {FILE_SAVE}
    يفحط لانهائي - اضغط CTRL+C للايقاف

    """)

    sem = asyncio.Semaphore(CONCURRENT)

    async with aiohttp.ClientSession() as session:
        while True:
            # يولد يوزر عشوائي رباعي
            while True:
                username = ''.join(random.choices(CHARSET, k=LENGTH))
                if username in seen: continue
                if username[0] in "._" or username[-1] in "._": continue
                if "__" in username or ".." in username: continue
                seen.add(username)
                break

            async with sem:
                await asyncio.sleep(DELAY + random.uniform(0, 0.5))
                await check_one(session, username, proxies)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\nتم الايقاف. اليوزرات المتاحة محفوظة في {FILE_SAVE}")
