import asyncio
import aiohttp
import itertools
import string
import random

# ===== الإعدادات =====
CHARSET = string.ascii_lowercase + string.digits
LENGTH = 4
CONCURRENT_REQUESTS = 8
DELAY = 0.2
BATCH_SIZE = 100

AVAILABLE_FILE = "available.txt"

URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "X-Discord-Locale": "en-US"
}

checked = 0
available_count = 0

sem = asyncio.Semaphore(CONCURRENT_REQUESTS)


async def check_username(session, username):
    global checked, available_count

    async with sem:
        await asyncio.sleep(DELAY + random.uniform(0, 0.2))

        try:
            async with session.post(URL, json={"username": username}, headers=HEADERS) as r:

                if r.status == 429:
                    # تجاهل وإعادة المحاولة لاحقًا (بدون recursion)
                    return None

                data = await r.json()
                taken = data.get("taken")

                checked += 1

                if taken is False:
                    available_count += 1
                    print(f"[✓] {username} | checked: {checked}")

                    # كتابة سريعة
                    with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
                        f.write(username + "\n")

                else:
                    print(f"[x] {username} | checked: {checked}", end="\r")

        except:
            return None


async def generate_usernames():
    while True:
        username = ''.join(random.choices(CHARSET, k=LENGTH))

        if username[0] in "._" or username[-1] in "._":
            continue
        if "__" in username or ".." in username:
            continue

        yield username


async def worker(session, queue):
    while True:
        username = await queue.get()
        await check_username(session, username)
        queue.task_done()


async def producer(queue):
    async for username in generate_usernames():
        await queue.put(username)


async def main():
    print(f"""
    ===== FAST Discord Username Checker =====
    Charset: {CHARSET}
    Length: {LENGTH}
    Batch: {BATCH_SIZE}
    """)

    queue = asyncio.Queue(maxsize=CONCURRENT_REQUESTS * 2)

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        # workers
        workers = [
            asyncio.create_task(worker(session, queue))
            for _ in range(CONCURRENT_REQUESTS)
        ]

        # producer
        prod = asyncio.create_task(producer(queue))

        await asyncio.gather(prod)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nتم الإيقاف")
