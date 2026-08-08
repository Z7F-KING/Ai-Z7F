import requests
import random
import string
import time

OUTPUT_FILE = "DiscordUserByZ7F.txt"

# ترويسات متصفح عادية بدون أي Token
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://discord.com",
    "Referer": "https://discord.com/register"
}

CHARS = string.ascii_lowercase + string.digits + "_"

def generate_random_username(length=4):
    return ''.join(random.choice(CHARS) for _ in range(length))

def check_username_no_token(session, username):
    # استخدام نقطة فحص اليوزر العامة الخاصة بصفحة التسجيل
    url = "https://discord.com/api/v9/auth/register"
    payload = {
        "fingerprint": None,
        "username": username,
        "invite": None,
        "consent": True,
        "gift_code_sku_id": None,
        "captcha_key": None
    }
    
    try:
        response = session.post(url, json=payload, timeout=5)
        
        # إذا رجع 400، نفحص تفاصيل الخطأ المرجعة من ديسكورد
        if response.status_code == 400:
            data = response.json()
            errors = data.get("errors", {})
            
            # إذا كانت مشكلة اليوزر أنه مأخوذ مسبقاً
            if "username" in errors:
                return False, "غير متاح"
            else:
                # إذا لم يظهر خطأ خاص باليوزر، فالاسم متاح وقبله النظام
                return True, "متاح"
                
        elif response.status_code == 429:
            return None, "Rate Limit (حظر مؤقت)"
        else:
            # أي رمز استجابة آخر (مثل فتح الكابتشا) يحدد تواجد اليوزر
            return True, "متاح"
            
    except Exception as e:
        return None, f"خطأ اتصال: {str(e)}"

def main():
    print("=" * 50)
    print("  Discord No-Token 4-Char Checker - By Z7F  ")
    print(f"  [+] الحفظ المباشر في: {OUTPUT_FILE}")
    print("=" * 50 + "\n")

    tested_count = 0
    available_count = 0

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        while True:
            username = generate_random_username(4)
            tested_count += 1
            
            status, message = check_username_no_token(session, username)
            
            if status is True:
                available_count += 1
                print(f"[{tested_count}] [✓] متاح: {username}")
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f_out:
                    f_out.write(f"{username}\n")
            elif status is False:
                print(f"[{tested_count}] [X] غير متاح: {username}")
            else:
                print(f"[{tested_count}] [!] تنبيه ({username}): {message}")
                time.sleep(4)

            # مهلة زمنية بسيطة لحماية الـ IP من حظر الـ Rate Limit
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n[!] تم إيقاف الفحص.")
        print(f"[+] إجمالي الفحص: {tested_count} | المتاح: {available_count}")

if __name__ == "__main__":
    main()
