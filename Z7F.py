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
{Y}     ULTRA API CHECKER - PRO V5
{C}══════════════════════════════════════
{W}  1 - TikTok     {W}  2 - Instagram
{W}  3 - Telegram   {W}  4 - Roblox
{W}  5 - Discord    {W}  6 - YouTube
{C}══════════════════════════════════════{W}""")

class API_Checker:
    def __init__(self, delay):
        self.total_checked = 0
        self.delay = delay
        # الهيدرز لمحاكاة متصفح حقيقي وتجنب الحظر
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

    def generate_user(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def check_logic(self, platform, user):
        try:
            if platform == "1": # TikTok API Check
                url = f"https://www.tiktok.com/api/uniqueid/check/?unique_id={user}"
                r = requests.get(url, headers=self.headers, timeout=3)
                return r.json().get("status_code") == 0 # 0 يعني متاح
                
            elif platform == "2": # Instagram Check
                url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user}"
                r = requests.get(url, headers=self.headers, timeout=3)
                return r.status_code == 404

            elif platform == "3": # Telegram Check
                url = f"https://t.me/{user}"
                r = requests.get(url, headers=self.headers, timeout=3)
                if "If you have <strong>Telegram</strong>, you can contact" in r.text:
                    return False # مستخدم
                return "tgme_icon_user" not in r.text

            elif platform == "4": # Roblox Official API
                url = f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01"
                r = requests.get(url, timeout=3)
                return r.json().get("code") == 0

            elif platform == "5": # Discord Webhook/Invite Check
                url = f"https://discord.com/api/v9/invites/{user}"
                r = requests.get(url, timeout=3)
                return r.status_code == 404 # إذا الرابط غير صالح اليوزر متاح كـ يوزر أو سيرفر

            elif platform == "6": # YouTube Handle Check
                url = f"https://www.youtube.com/@{user}"
                r = requests.get(url, headers=self.headers, timeout=3)
                return "404 Not Found" in r.text or r.status_code == 404

        except Exception:
            return False
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_user(length)
            self.total_checked += 1
            
            # تحديث اليوزر المولد فوق (ثابت)
            sys.stdout.write(f"\r{W}Check | {C}{user} {W}| Total: {Y}{self.total_checked}")
            sys.stdout.flush()
            
            if self.check_logic(platform, user):
                # طباعة اليوزر الموجود تحت العداد الثابت
                sys.stdout.write(f"\n{G}✅ Found | {W}{user}\n")
                sys.stdout.flush()
                with open("found.txt", "a") as f:
                    f.write(f"{user}\n")
            
            if self.delay > 0:
                time.sleep(self.delay)

def main():
    clear()
    logo()
    choice = input(f"{Y}Select Platform (1-6): {W}")
    length = int(input(f"{Y}User Length (3, 4, 5): {W}"))
    speed_val = input(f"{Y}Speed (0-10): {W}")
    
    try:
        delay = float(speed_val)
    except:
        delay = 0.0
    
    print(f"\n{R}[!] High-Accuracy Scan Started...{W}\n")
    
    app = API_Checker(delay)
    
    # عدد الخيوط لزيادة السرعة
    threads_count = 15 if delay > 0 else 40
    
    for _ in range(threads_count):
        threading.Thread(target=app.start, args=(choice, length), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
