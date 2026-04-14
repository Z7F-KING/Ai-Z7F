import random
import string
import requests
import threading
import os
import sys
import time

# ألوان التنسيق
G = '\033[1;32m' # أخضر
W = '\033[1;37m' # أبيض
C = '\033[1;36m' # سماوي
Y = '\033[1;33m' # أصفر
R = '\033[1;31m' # أحمر

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(f"""
{C}══════════════════════════════════════
{Y}     ELITE STATUS-LINE CHECKER V7
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class FinalChecker:
    def __init__(self, delay):
        self.total = 0
        self.delay = delay
        self.current_user = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/json"
        }

    def generate_smart_user(self, length):
        main_chars = string.ascii_lowercase + string.digits
        symbol = random.choice(['.', '_', ''])
        if symbol and length > 3:
            pos = random.randint(1, length - 2)
            part1 = ''.join(random.choice(main_chars) for _ in range(pos))
            part2 = ''.join(random.choice(main_chars) for _ in range(length - pos - 1))
            user = part1 + symbol + part2
        else:
            user = ''.join(random.choice(main_chars) for _ in range(length))
        return user

    def check_platform(self, platform, user):
        try:
            if platform == "1": # TikTok
                r = requests.get(f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}", timeout=3)
                return r.json().get("status_code") == 0
            elif platform == "2": # Instagram
                r = requests.get(f"https://www.instagram.com/{user}/", timeout=3)
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = requests.get(f"https://t.me/{user}", timeout=3)
                return "tgme_icon_user" not in r.text and "tgme_page_extra" in r.text
            elif platform == "4": # Roblox
                r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01", timeout=3)
                return r.json().get("code") == 0
            elif platform == "5": # Discord (Precise API Check)
                # فحص ديسكورد عبر API محاولة إنشاء اسم مستخدم
                payload = {"username": user}
                r = requests.post("https://discord.com/api/v9/users/@me/pomelo-attempt", json=payload, headers=self.headers, timeout=3)
                return r.json().get("taken") == False
            elif platform == "6": # YouTube
                r = requests.get(f"https://www.youtube.com/@{user}", timeout=3)
                return r.status_code == 404
        except:
            return False
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_smart_user(length)
            self.total += 1
            self.current_user = user
            
            # تحديث السطر الأول فقط باستمرار
            # الرمز \r يعيد المؤشر لبداية السطر، و \033[K يمسح ما تبقى من السطر القديم
            sys.stdout.write(f"\r\033[K{W}Check | {C}{user} {W}| Total: {Y}{self.total}")
            sys.stdout.flush()
            
            if self.check_platform(platform, user):
                # إذا وجد يوزر، يطبعه في سطر جديد "تحت" العداد
                print(f"\n{G}✅ Found | {W}{user} {G}كامل")
                with open("hits.txt", "a") as f:
                    f.write(f"{user}\n")
            
            if self.delay > 0:
                time.sleep(self.delay)

def main():
    clear()
    logo()
    plat = input(f"{Y}Select Platform (1-6): {W}")
    size = int(input(f"{Y}User Length (3, 4, 5): {W}"))
    speed = input(f"{Y}Speed (0-10): {W}")
    
    try:
        delay = float(speed)
    except:
        delay = 0.0
        
    print(f"\n{R}[!] Scanning... Results will appear below status line.{W}\n")
    
    bot = FinalChecker(delay)
    
    # استخدام Thread واحد للتوليد والطباعة لضمان بقاء السطر ثابتاً تماماً كما طلبت
    # ولو تبي سرعة أعلى ممكن نرفع الخيوط بس كذا بتضمن الشكل اللي طلبته
    bot.start(plat, size)

if __name__ == "__main__":
    main()
