import random
import string
import requests
import threading
import os
import sys
import time

# ألوان التصميم
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
{Y}     PREMIUM MULTI-CHECKER V3
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class Checker:
    def __init__(self, delay):
        self.total_checked = 0
        self.delay = delay

    def generate_user(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def check_platform(self, platform, user):
        try:
            if platform == "1": # TikTok
                r = requests.get(f"https://www.tiktok.com/@{user}", timeout=5)
                return r.status_code == 404
            elif platform == "2": # Instagram
                r = requests.get(f"https://www.instagram.com/{user}/", timeout=5)
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = requests.get(f"https://t.me/{user}", timeout=5)
                return "tgme_page_extra" not in r.text and r.status_code == 200
            elif platform == "4": # Roblox
                r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01", timeout=5)
                return r.json().get("code") == 0
            elif platform == "5": # Discord (Endpoint check)
                r = requests.get(f"https://discord.com/api/v9/users/@me/outbound-promotions/codes", timeout=5) # Example check
                # ملاحظة: ديسكورد يتطلب توكن للفحص الدقيق، هنا يتم الفحص عبر الروابط العامة
                r = requests.get(f"https://discordapp.com/api/v6/invite/{user}", timeout=5)
                return r.status_code == 404
            elif platform == "6": # YouTube
                r = requests.get(f"https://www.youtube.com/@{user}", timeout=5)
                return r.status_code == 404
        except:
            return False
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_user(length)
            self.total_checked += 1
            
            # إظهار اليوزر المولد حالياً في سطر متجدد
            sys.stdout.write(f"\r{W}Check | {C}{user} {W}| Total: {Y}{self.total_checked}")
            sys.stdout.flush()
            
            if self.check_platform(platform, user):
                print(f"\n{G}✅ Found | {W}{user}{W}") 
                with open("hits.txt", "a") as f:
                    f.write(f"{user}\n")
            
            if self.delay > 0:
                time.sleep(self.delay)

def main():
    clear()
    logo()
    choice = input(f"{Y}Select Platform (1-6): {W}")
    length = int(input(f"{Y}User Length: {W}"))
    
    # تحديد السرعة
    try:
        speed_input = input(f"{Y}Speed (0.0 for No Delay / 0.1): {W}")
        delay = float(speed_input)
    except:
        delay = 0.0
    
    print(f"\n{R}[!] Scanning Started...{W}\n")
    
    app = Checker(delay)
    
    # استخدام 20 خيط (Thread) لضمان السرعة العالية جداً
    for _ in range(20):
        threading.Thread(target=app.start, args=(choice, length), daemon=True).start()

    # لإبقاء السكربت يعمل
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
