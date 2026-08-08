import asyncio
import aiohttp
import itertools
import string
import random
from datetime import datetime

# ===== الإعدادات =====
CHARSET = string.ascii_lowercase + string.digits # تقدر تغيرها لـ string.ascii_lowercase فقط عشان حروف
LENGTH = 4
CONCURRENT_REQUESTS = 5 # لا ترفعه فوق 10 عشان لا يتبند الـ IP حقك
DELAY = 0.3 # تأخير بين كل طلب

# تخزين المتاح
AVAILABLE_FILE = "available.txt"

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Discord-Locale": "en-US"
}

checked = 0
available_count = 0

async def check_username(session, username, sem):
    global checked, available_count
    async with sem:
        try:
            await asyncio.sleep(DELAY + random.uniform(0, 0.3))
            async with session.post(URL, json={"username": username}, headers=HEADERS) as r:

                if r.status == 429:
                    data = await r.json()
                    retry_after = data.get('retry_after', 5)
                    print(f"[!] Rate Limit - ننتظر {retry_after}s")
                    await asyncio.sleep(retry_after)
                    return await check_username(session, username, sem)

                data = await r.json()

                # هذا هو الرد الرسمي من الديسكورد
                taken = data.get("taken")

                checked += 1

                if taken is False:
                    available_count += 1
                    print(f"[✓ متاح] {username} | فحصنا: {checked}")
                    with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{username}\n")
                    return True
                else:
                    print(f"[x] مستخدم: {username} | فحصنا: {checked}", end="\r")
                    return False

        except Exception as e:
            print(f"\n[!] خطأ مع {username}: {e}")
            return False

async def main():
    print(f"""
    ===== Discord 4-Letter Username Checker =====
    Charset: {CHARSET}
    Length: {LENGTH}
    المجموع التقريبي: {len(CHARSET)**LENGTH:,}

    """)

    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)

    # لو تبي تفحص عشوائي مو بالترتيب (افضل لليوزرات الرباعية)
    RANDOM_MODE = True

    async with aiohttp.ClientSession() as session:
        if RANDOM_MODE:
            # يفحص بشكل عشوائي الى ما لا نهاية - افضل طريقة
            while True:
                username = ''.join(random.choices(CHARSET, k=LENGTH))

                # قوانين الديسكورد: ما يبدأ او ينتهي بنقطة او اندرسكور
                if username[0] in "._" or username[-1] in "._":
                    continue
                if "__" in username or ".." in username:
                    continue

                await check_username(session, username, sem)
        else:
            # يفحص بالترتيب aaaa, aaab...
            tasks = []
            for combo in itertools.product(CHARSET, repeat=LENGTH):
                username = ''.join(combo)
                if username[0] in "._" or username[-1] in "._":
                    continue
                tasks.append(check_username(session, username, sem))

                if len(tasks) >= 1000: # يشغلهم دفعات
                    await asyncio.gather(*tasks)
                    tasks = []

            if tasks:
                await asyncio.gather(*tasks)

    print(f"\nانتهى! لقينا {available_count} يوزر متاح وحفظناها في {AVAILABLE_FILE}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nتم الايقاف يدوياً")
