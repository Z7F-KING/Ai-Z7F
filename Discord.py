import random, asyncio

# اعدادات مضاد الرات ليميت
BASE_DELAY = 0.8
MAX_DELAY = 15
current_delay = BASE_DELAY
consecutive_429 = 0

async def check_username_smart(session, username):
    global checked, found, proxy_index, current_delay, consecutive_429

    # نحاول بنفس البروكسي لين ينجح
    for _ in range(2): # محاولتين بس لنفس اليوزر
        if proxy_index < len(PROXIES):
            proxy = format_proxy(PROXIES[proxy_index])
            proxy_display = PROXIES[proxy_index]
        else:
            proxy = None
            proxy_display = "بدون بروكسي"

        try:
            # تأخير ذكي + عشوائية عشان ما ننكشف
            await asyncio.sleep(current_delay + random.uniform(0.2, 0.8))

            async with session.post(URL, json={"username": username}, headers=HEADERS, proxy=proxy, timeout=10) as r:

                if r.status == 429:
                    data = await r.json()
                    retry_after = float(data.get("retry_after", 2.5))

                    consecutive_429 += 1
                    # كل ما ننبند نزيد التأخير
                    current_delay = min(MAX_DELAY, BASE_DELAY * (1.5 ** consecutive_429) + retry_after)

                    print(f"\n[!] 429 على {proxy_display} | نوم {current_delay:.1f}s | تأخيرنا الحين: {current_delay:.1f}s")
                    await asyncio.sleep(current_delay)

                    # اذا انبندنا 3 مرات ورا بعض نبدل البروكسي
                    if consecutive_429 >= 3:
                        proxy_index += 1
                        consecutive_429 = 0
                        print(f"[!] بدلنا البروكسي -> {PROXIES[proxy_index] if proxy_index < len(PROXIES) else 'بدون'}")
                    continue

                # اذا الطلب نجح نرجع نسرّع شوي
                consecutive_429 = 0
                current_delay = max(BASE_DELAY, current_delay * 0.95)

                data = await r.json()
                taken = data.get("taken", True)

                global checked, found
                checked += 1

                if taken is False:
                    found += 1
                    save_user(username)
                    print(f"\n[✓ متاح] {username} | {proxy_display} | فحصنا: {checked} | تأخير: {current_delay:.2f}s")
                    return True
                else:
                    print(f"[x] {username} | {proxy_display} | فحصنا: {checked} | تأخير: {current_delay:.2f}s", end="\r")
                    return False

        except Exception:
            print(f"[!] بروكسي مات {proxy_display} -> اللي بعده")
            proxy_index += 1
            consecutive_429 = 0
            current_delay = BASE_DELAY
            await asyncio.sleep(1)
            continue

    return False
