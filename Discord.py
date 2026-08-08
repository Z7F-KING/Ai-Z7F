import requests
import time

# إعدادات الأداة
INPUT_FILE = "users.txt"  # ملف يحتوي على قائمة اليوزرات المراد فحصها (كل يوزر في سطر)
OUTPUT_FILE = "DiscordUserByZ7F.txt"  # الملف الذي سيتم حفظ اليوزرات المتاحة فيه

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

def check_username(username):
    """
    إرسال طلب لمكتبة الديسكورد للتحقق من إمكانية استخدام اسم المستخدم.
    """
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    payload = {"username": username.strip()}
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=5)
        
        # التأكد من حالة الاستجابة
        if response.status_code == 200:
            data = response.json()
            # إذا كانت القيمة taken تساوي False يعني اليوزر غير مأخوذ (متاح)
            if not data.get("taken", True):
                return True, "متاح"
            else:
                return False, "غير متاح"
        elif response.status_code == 429:
            return None, "Rate Limit (حظر مؤقت للطلبات)"
        else:
            return False, f"حالة غير متوقعة: {response.status_code}"
            
    except Exception as e:
        return None, f"خطأ في الاتصال: {str(e)}"

def main():
    print("=" * 45)
    print("      Discord Username Checker - By Z7F      ")
    print("=" * 45)
    
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] خطأ: لم يتم العثور على الملف '{INPUT_FILE}'. قم بإنشائه وأضف فيه اليوزرات.")
        return

    print(f"[+] تم تحميل {len(usernames)} يوزر لبدء الفحص...\n")

    for username in usernames:
        status, message = check_username(username)
        
        if status is True:
            print(f"[✓] متاح: {username}")
            # حفظ اليوزر فوراً في الملف المطلوب
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f_out:
                f_out.write(f"{username}\n")
        elif status is False:
            print(f"[X] غير متاح: {username}")
        else:
            print(f"[!] تنبيه ({username}): {message}")
            # انتظار إضافي عند مواجهة حظر مؤقت (Rate Limit)
            time.sleep(5)
            
        # مهلة زمنية قصيرة بين الطلبات تجنباً للحظر
        time.sleep(1.5)

    print("\n[+] اكتمل الفحص. تم حفظ جميع اليوزرات المتاحة في:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
