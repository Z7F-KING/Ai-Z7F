import requests
import random
import string
import time

OUTPUT_FILE = "DiscordUserByZ7F.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9"
}

CHARS = string.ascii_lowercase + string.digits + "_"

def generate_random_username(length=4):
    return ''.join(random.choice(CHARS) for _ in range(length))

def main():
    print("=" * 50)
    print("  Discord Random 4-Char Checker - By Z7F  ")
    print("=" * 50)
    print(f"[+] التجميع شغال... سيتم حفظ المتاح في: {OUTPUT_FILE}\n")

    tested_count = 0
    available_count = 0

    # استخدام Session لإبقاء الاتصال مفتوح وتسريع الطلبات
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        while True:
            username = generate_random_username(4)
            tested_count += 1
            
            url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
            payload = {"username": username}
            
            try:
                response = session.post(url, json=payload, timeout=3)
                
                if response.status_code == 200:
                    data = response.json()
                    if not data.get("taken", True):
                        available_count += 1
                        print(f"[{tested_count}] [✓] متاح: {username}")
                        with open(OUTPUT_FILE, "a", encoding="utf-8") as f_out:
                            f_out.write(f"{username}\n")
                    else:
                        print(f"[{tested_count}] [X] غير متاح: {username}")
                elif response.status_code == 429:
                    print(f"[{tested_count}] [!] Rate Limit (حظر مؤقت) - جارٍ الانتظار 3 ثوانٍ...")
                    time.sleep(3)
                else:
                    print(f"[{tested_count}] [!] رمز استجابة: {response.status_code}")
            except Exception as e:
                print(f"[{tested_count}] [!] خطأ اتصال: {e}")

            # مهلة قصيرة جداً (0.3 ثانية) لتسريع الفحص بدون ضرب حظر سريع
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n\n[!] تم إيقاف الفحص.")
        print(f"[+] تم فحص {tested_count} يوزر | تم العثور على {available_count} متاح.")

if __name__ == "__main__":
    main()
