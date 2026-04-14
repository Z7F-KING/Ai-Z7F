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

# قفل لمنع تداخل الطباعة
print_lock = threading.Lock()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(f"""
{C}══════════════════════════════════════
{Y}     NO-COOLDOWN TURBO CHECKER V9
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class TurboChecker:
    def __init__(self, delay):
        self.total = 0
        self.delay = delay
        # استخدام Session لسرعة خرافية في الاتصال
        self.session = requests.Session()
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
            return part1 + symbol + part2
        return ''.join(random.choice(main_chars) for _ in range(length))

    def check_platform(self, platform, user):
        try:
            # الفحص الآن عبر الـ Session المفتوح لسرعة أعلى
            if platform == "1": # TikTok
                r = self.session.get(f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}", timeout=2)
                return r.json().get("status_code") == 0
            elif platform == "2": # Instagram
                r = self.session.get(f"https://www.instagram.com/{user}/", timeout=2)
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = self.session.get(f"https://t.me/{user}", timeout=2)
                return "tgme_icon_user" not in r.text and "tgme_page_extra" in r.text
            elif platform == "4": # Roblox
                r = self.session.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01", timeout=2)
                return r.json().get("code") == 0
            elif platform == "5": # Discord
                payload = {"username": user}
                r = self.session.post("https://discord.com/api/v9/users/@me/pomelo-attempt", json=payload, headers=self.headers, timeout=2)
                return r.json().get("taken") == False
            elif platform == "6": # YouTube
                r = self.session.get(f"https://www.youtube.com/@{user}", timeout=2)
                return r.status_code == 404
        except:
            return False

    def start_worker(self, platform, length):
        while True:
            user = self.generate_smart_user(length)
            
            # تحديث العداد واليوزر فوراً
            with print_lock:
                self.total += 1
                sys.stdout.write(f"\r\033[K{W}Check | {C}{user} {W}| Total: {Y}{self.total}")
                sys.stdout.flush()
            
            if self.check_platform(platform, user):
                with print_lock:
                    print(f"\n{G}✅ Found | {W}{user}")
            
            # إذا السرعة 0، لا يوجد أي انتظار ميكرو ثانية حتى
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
        
    print(f"\n{R}[!] Turbo Mode On. No Cooldown.{W}\n")
    
    bot = TurboChecker(delay)
    
    # رفع عدد الخيوط لـ 25 خيط عند اختيار السرعة 0
    num_threads = 25 if delay == 0 else 5
    
    for _ in range(num_threads):
        t = threading.Thread(target=bot.start_worker, args=(plat, size))
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
