import random
import string
import requests
import threading
import os
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
{Y}     ELITE API CHECKER - V6
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class ProChecker:
    def __init__(self, delay):
        self.total = 0
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }

    def generate_smart_user(self, length):
        # توليد يوزر يحتوي على حروف وأرقام
        main_chars = string.ascii_lowercase + string.digits
        
        # اختيار رمز واحد فقط (إما نقطة أو شرطة أو بدون)
        symbol = random.choice(['.', '_', ''])
        
        if symbol and length > 3:
            # وضع الرمز في مكان عشوائي ليس الأول ولا الأخير
            pos = random.randint(1, length - 2)
            part1 = ''.join(random.choice(main_chars) for _ in range(pos))
            part2 = ''.join(random.choice(main_chars) for _ in range(length - pos - 1))
            user = part1 + symbol + part2
        else:
            user = ''.join(random.choice(main_chars) for _ in range(length))
        return user

    def check(self, platform, user):
        try:
            if platform == "1": # TikTok
                r = requests.get(f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}", headers=self.headers, timeout=5)
                return r.json().get("status_code") == 0
            elif platform == "2": # Instagram
                r = requests.get(f"https://www.instagram.com/{user}/", headers=self.headers, timeout=5)
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = requests.get(f"https://t.me/{user}", headers=self.headers, timeout=5)
                return "tgme_icon_user" not in r.text and "tgme_page_extra" in r.text
            elif platform == "4": # Roblox
                r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01", timeout=5)
                return r.json().get("code") == 0
            elif platform == "5": # Discord
                r = requests.get(f"https://discordapp.com/api/v6/invite/{user}", timeout=5)
                return r.status_code == 404
            elif platform == "6": # YouTube
                r = requests.get(f"https://www.youtube.com/@{user}", headers=self.headers, timeout=5)
                return r.status_code == 404
        except:
            return False

    def work(self, platform, length):
        while True:
            user = self.generate_smart_user(length)
            self.total += 1
            
            # طباعة كل فحص في سطر جديد عشان ما يعلق
            print(f"{W}Check | {C}{user} {W}| Total: {Y}{self.total}")
            
            if self.check(platform, user):
                print(f"{G}✅ Found | {W}{user} {G}完全")
                with open("found_v6.txt", "a") as f:
                    f.write(f"{user}\n")
            
            # الالتزام بالسرعة المحددة من المستخدم
            if self.delay > 0:
                time.sleep(self.delay)

def main():
    clear()
    logo()
    plat = input(f"{Y}Select Platform (1-6): {W}")
    size = int(input(f"{Y}User Length (3, 4, 5): {W}"))
    speed = input(f"{Y}Speed (0 to 10): {W}")
    
    try:
        delay = float(speed)
    except:
        delay = 0.5
        
    print(f"\n{R}[!] Scanning with precision...{W}\n")
    
    bot = ProChecker(delay)
    
    # عدد الخيوط قليل لضمان دقة السرعة وعدم تداخل الأسطر
    threads = 5 if delay > 0 else 15
    
    for _ in range(threads):
        threading.Thread(target=bot.work, args=(plat, size), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
