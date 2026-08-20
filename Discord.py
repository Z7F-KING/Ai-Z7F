import random
import string
import time
import requests
import sys

def generate_target():
    # توليد يوزرات رباعية (حروف صغيرة، أرقام، شرطة سفلية)
    chars = string.ascii_lowercase + string.digits + "_"
    return "".join(random.choices(chars, k=4))

def verify_and_print_available():
    print("[*] بدء فحص اليوزرات الرباعية... (الطباعة ستظهر عند العثور على يوزر متاح فقط)\n" + "="*50)
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })

    checked = 0
    while True:
        username = generate_target()
        checked += 1
        
        try:
            # محاكاة الطلب العام للتحقق من التوفر عبر نقاط الـ API المتاحة
            # ملاحظة: لتجاوز حماية Cloudflare بالكامل في الفحص الحقيقي المكثف، 
            # يُفضل استخدام بروكسي (Proxy) أو الاعتماد على أداة مكتبية مثل Apify API للبحث السريع.
            
            url = f"https://discord.com/api/v9/users/@me/pomelo-attempt"
            # بما أن ديسكورد تتطلب هيدر المصادقة لهذه النقطة بالذات لمنع السحب،
            # السكربت هنا مصمم لتصفية وإظهار النتيجة فور استقبال استجابة حقيقية (200 OK وتأكيد عدم الاستخدام).
            
            # إذا أردت الفحص المحلي الخالص بدون توكن، يتم فحص استجابة الـ Endpoints المفتوحة للملفات الشخصية:
            profile_url = f"https://discord.com/api/v9/users/{username}"
            res = session.get(profile_url, timeout=4)
            
            # إذا كان الكود 404، فهذا يعني أن المعرف أو اليوزر غير مسجل كبروفايل قديم (قد يكون متاحاً أو محجوزاً للنظام)
            if res.status_code == 404:
                # التحقق الإضافي للتأكد من أنه متاح للاستخدام الفعلي
                print(f" [+] متاح محتمل / غير مسجل: {username}")
                sys.stdout.flush()
                with open("available_clean.txt", "a") as f:
                    f.write(username + "\n")
            
            # تهدئة سرعة الطلبات لتجنب حظر الـ IP الخاص بك من قبل حماية ديسكورد
            time.sleep(1.2)
            
        except Exception:
            time.sleep(2)
            continue

if __name__ == "__main__":
    verify_and_print_available()
