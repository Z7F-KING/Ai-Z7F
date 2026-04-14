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
{Y}     PREMIUM MULTI-CHECKER V4
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class Checker:
    def __init__(self, delay):
        self.total_checked = 0
        self.delay = delay
        self.current_user = "..."

    def generate_user(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def check_platform(self, platform, user):
        try:
            # مهلة الرد (timeout) خليتها قصيرة جداً عشان لا يعلق الفحص
            if platform == "1": # TikTok
                r = requests.get(f"https://www.tiktok.com/@{user}", timeout=2)
                return r.status_code == 404
            elif platform == "2": # Instagram
                r = requests.get(f"https://www.instagram.com/{user}/", timeout=2)
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = requests.get(f"https://t.me/{user}", timeout=2)
                return "tgme_page_extra" not in r.text and r.status_code == 200
            elif platform == "4": # Roblox
                r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01", timeout=2)
                return r.json().get("code") == 0
            elif platform == "5": # Discord
                r = requests.get(f"https://discordapp.com/api/v6/invite/{user}", timeout=2)
                return r.status_code == 404
            elif platform == "6": # YouTube
                r = requests.get(f"https://www.youtube.com/@{user}", timeout=2)
                return r.status_code == 404
        except:
            return False
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_user(length)
            self.current_user = user
            self.total_checked += 1
            
            # تحديث اليوزر في مكانه فوق بدون تكرار الأسطر
            sys.stdout.write(f"\r{W}Check | {C}{self.current_user} {W}| Total: {Y}{self.total_checked}")
            sys.stdout.flush()
            
            if self.check_platform(platform, user):
                # عند الإيجاد ينزل سطر جديد عشان يثبت اليوزر الشغال
                sys.stdout.write(f"\n{G}✅ Found | {W}{user}\n")
                sys.stdout.flush()
                with open("hits.txt", "a") as f:
                    f.write(f"{user}\n")
            
            if self.delay > 0:
                time.sleep(self.delay)

def main():
    clear()
    logo()
    choice = input(f"{Y}Select Platform (1-6): {W}")
    length = int(input(f"{Y}User Length (3, 4, 5): {W}"))
    
    # السرعة أصبحت مرنة (0-10)
    try:
        speed_val = input(f"{Y}Speed (0-10): {W}")
        delay = float(speed_val)
    except:
        delay = 0.0
    
    print(f"\n{R}[!] Scanning Started...{W}\n")
    
    app = Checker(delay)
    
    # زيادة عدد الـ Threads لسرعة جبارة عند اختيار 0
    num_threads = 30 if delay == 0 else 10
    
    for _ in range(num_threads):
        threading.Thread(target=app.start, args=(choice, length), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
