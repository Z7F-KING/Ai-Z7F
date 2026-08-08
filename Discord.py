import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

OUTPUT_FILE = "DiscordUserByZ7F.txt"
# عدد الخيوط (Threads) - زد الرقم لتسريع أكبر (مثال: 10 أو 15)
MAX_WORKERS = 10 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

CHARS = string.ascii_lowercase + string.digits + "_"
file_lock = Lock()
print_lock = Lock()

tested_count = 0
available_count = 0

def generate_random_username(length=4):
    return ''.join(random.choice(CHARS) for _ in range(length))

def check_username(username):
    global tested_count, available_count
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    payload = {"username": username}
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=3)
        
        with print_lock:
            tested_count += 1
            current_test = tested_count
            
        if response.status_code == 200:
            data = response.json()
            if not data.get("taken", True):
                with print_lock:
                    available_count += 1
                    print(f"[{current_test}] [✓] متاح: {username}")
                
                # حفظ آمن وسريع في الملف
                with file_lock:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f_out:
                        f_out.write(f"{username}\n")
            else:
                with print_lock:
                    print(f"[{current_test}] [X] غير متاح: {username}")
                    
        elif response.status_code == 429:
            with print_lock:
                print(f"[{current_test}] [!] Rate Limit (حظر مؤقت) - جارٍ الانتظار...")
            time.sleep(3)
        else:
            with print_lock:
                print(f"[{current_test}] [!] رمز استجابة: {response.status_code}")
                
    except Exception as e:
        pass

def worker():
    while True:
        username = generate_random_username(4)
        check_username(username)
        # مهلة قصيرة جداً لتفادي حجب الـ IP السريع
        time.sleep(0.2)

def main():
    print("=" * 50)
    print("  Discord FAST 4-Char Checker - By Z7F  ")
    print(f"  [+] عدد الخيوط الشغالة: {MAX_WORKERS}")
    print(f"  [+] الحفظ المباشر في: {OUTPUT_FILE}")
    print("=" * 50 + "\n")

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(worker) for _ in range(MAX_WORKERS)]
            for future in as_completed(futures):
                future.result()
    except KeyboardInterrupt:
        print("\n\n[!] تم إيقاف الفحص.")
        print(f"[+] إجمالي الفحص: {tested_count} | المتاح: {available_count}")

if __name__ == "__main__":
    main()
