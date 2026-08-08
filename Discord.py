import requests
import random
import string
import time

OUTPUT_FILE = "DiscordUserByZ7F.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

# الحروف والأرقام المستخدمة لتوليد يوزر من 4 خانات
CHARS = string.ascii_lowercase + string.digits + "_"

def generate_random_username(length=4):
    """توليد يوزر عشوائي مكون من 4 خانات"""
    return ''.join(random.choice(CHARS) for _ in range(length))

def check_username(username):
    """إرسال طلب لنقطة فحص اليوزرات في ديسكورد"""
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    payload = {"username": username}
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("taken", True):
                return True, "متاح"
            else:
                return False, "غير متاح"
        elif response.status_code == 429:
            return None, "Rate Limit (حظر مؤقت)"
        else:
            return False, f"رمز الاستجابة: {response.status_code}"
            
    except Exception as e:
        return None, f"خطأ في الاتصال: {str(e)}"

def main():
    print("=" * 50)
    print("  Discord Random 4-Char Checker - By Z7F  ")
    print("=" * 50)
    print(f"[+] التجميع شغال... سيتم حفظ المتاح في: {OUTPUT_FILE}\n")

    tested_count = 0
    available_count = 0

    try:
        while True:
            username = generate_random_username(4)
            tested_count += 1
            
            status, message = check_username(username)
            
            if status is True:
                available_count += 1
                print(f"[{tested_count}] [✓] متاح: {username}")
                # حفظ اليوزر المتاح فوراً في الملف
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f_out:
                    f_out.write(f"{username}\n")
            elif status is False:
                print(f"[{tested_count}] [X] غير متاح: {username}")
            else:
                print(f"[{tested_count}] [!] تنبيه ({username}): {message}")
                # انتظار 10 ثوانٍ في حال مواجهة Rate Limit لتفادي حظر الـ IP
                time.sleep(10)

            # مهلة زمنية قصيرة بين كل فحص لتقليل احتمالية الحظر المؤقت
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n\n[!] تم إيقاف الفحص بواسطة المستخدم.")
        print(f"[+] إجمالي المجهود: تم فحص {tested_count} يوزر | تم العثور على {available_count} متاح.")

if __name__ == "__main__":
    main()
