import asyncio
import aiohttp
import random
import string
import time
from collections import deque

# ===== الإعدادات =====
CHARSET = string.ascii_lowercase + string.digits
LENGTH = 4
CONCURRENT_WORKERS = 20 # هذا هو السر، 20-25 آمن جدا اذا تحترم الـ 429
MIN_DELAY = 0.12
MAX_DELAY = 0.28

AVAILABLE_FILE = "available.txt"
URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Discord-Locale": "en-US"
}

checked = 0
available_count = 0
seen_usernames = set()
file_buffer = []

async def worker(queue, session, lock):
    global checked, available_count
    while True:
        username = await queue.get()
        try:
            await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

            async with session.post(URL, json={"username": username}, headers=HEADERS) as r:
                if r.status == 429:
                    data = await r.json()
                    retry_after = data.get('retry_after', 2.5)
                    print(f"\n[!] Rate Limit - نهدي شوي {retry_after:.2f}s")
                    await asyncio.sleep(retry_after)
                    # رجع اليوزر للطابور مرة ثانية
                    await queue.put(username)
                    continue

                data = await r.json()
                taken = data.get("taken")

                async with lock:
                    checked += 1
                    if taken is False:
                        available_count += 1
                        file_buffer.append(username)
                        print(f"\n[✓ متاح] {username} | فحصنا: {checked} | لقينا: {available_count}")
                        # كل 5 يوزرات احفظ
                        if len(file_buffer) >= 5:
                            with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
                                f.write("\n".join(file_buffer) + "\n")
                            file_buffer.clear()
                    else:
                        # عشان لا يزحم الكونسول
                        if checked % 20 == 0:
                            print(f"[x] نفحص... اخر واحد: {username} | فحصنا: {checked} | لقينا: {available_count}", end="\r")

        except Exception as e:
            # لو صار خطأ رجعه للطابور
            await queue.put(username)
        finally:
            queue.task_done()

async def producer(queue):
    print(f"نولد يوزرات {LENGTH} عشوائية بدون تكرار...")
    while True:
        username = ''.join(random.choices(CHARSET, k=LENGTH))
        if username[0] in "._" or username[-1] in "._": continue
        if "__" in username or ".." in username: continue
        if username in seen_usernames: continue

        seen_usernames.add(username)
        await queue.put(username)
        # لو الطابور فل لا نولد زيادة
        if queue.qsize() > 5000:
            await asyncio.sleep(0.5)

async def main():
    print(f"""
    ===== Discord Checker V2 - TURBO =====
    Workers: {CONCURRENT_WORKERS}
    Delay: {MIN_DELAY} - {MAX_DELAY}s
    """)

    queue = asyncio.Queue(maxsize=10000)
    lock = asyncio.Lock()

    connector = aiohttp.TCPConnector(limit=CONCURRENT_WORKERS, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # شغل العمال
        workers = [asyncio.create_task(worker(queue, session, lock)) for _ in range(CONCURRENT_WORKERS)]
        prod = asyncio.create_task(producer(queue))

        try:
            await asyncio.gather(prod, *workers)
        except KeyboardInterrupt:
            print("\n\nتم الايقاف... جاري حفظ الباقي...")
            if file_buffer:
                with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
                    f.write("\n".join(file_buffer) + "\n")
            print(f"انتهى! فحصنا {checked} ولقينا {available_count} متاح")

if __name__ == "__main__":
    asyncio.run(main())
