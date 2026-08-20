import random
import string
import urllib.request
import urllib.error
import sys
import time

def get_random_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"
    ]
    return random.choice(agents)

def generate_username():
    # الحروف والأرقام والشرطة السفلية المتاحة لليوزرات
    chars = string.ascii_lowercase + string.digits + "_"
    return "".join(random.choices(chars, k=4))

def check_discord_usernames():
    print("[*] بدء الفحص الفوري لليوزرات الرباعية... (النتائج ستظهر هنا مباشرة)\n" + "="*50)
    
    checked = 0
    while True:
        username = generate_username()
        checked += 1
        
        # فحص عبر رابط البحث العام أو التحقق المباشر
        url = f"https://discord.com/api/v9/users/{username}"
        
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": get_random_agent(),
                "Accept": "application/json"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                # إذا رد بـ 200 معناه اليوزر مستخدم ومحجوز لشخص ما
                pass
        except urllib.error.HTTPError as e:
            # إذا كان الرد 404 (غير موجود) فهذا يعني أن اليوزر غير مستخدم بالصيغة التقليدية وقد يكون متاحاً
            if e.code == 404:
                print(f"[+] [متاح / غير مسجل]: {username}")
                sys.stdout.flush()
                with open("available_found.txt", "a") as f:
                    f.write(username + "\n")
            elif e.code == 429:
                print("[-] تم رصد ضغط حماية (Rate Limit)، جاري التهدئة...")
                time.sleep(5)
        except Exception:
            # تجاهل أخطاء الاتصال المؤقتة لكي لا يتوقف السكربت
            pass
        
        # طباعة مؤشر الحركة لتعرف أن السكربت شغال وغير متوقف
        sys.stdout.write(f"\r[-] جاري الفحص... (الرقم المحسوب: {checked})")
        sys.stdout.flush()
        
        # مهلة قصيرة جداً لتسريع الفحص
        time.sleep(0.3)

if __name__ == "__main__":
    check_discord_usernames()
