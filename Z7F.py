import random
import string
import requests
import threading
import os
from time import sleep

# ألوان لتنسيق الواجهة
G = '\033[1;32m' # أخضر
R = '\033[1;31m' # أحمر
W = '\033[1;37m' # أبيض
C = '\033[1;36m' # سماوي
Y = '\033[1;33m' # أصفر

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(f"""
{C}══════════════════════════════════════
{Y}      USER GENERATOR & CHECKER
{C}══════════════════════════════════════
{W}  1 - TikTok    {W}  2 - Instagram
{W}  3 - Telegram  {W}  4 - Roblox
{C}══════════════════════════════════════{W}""")

class Checker:
    def __init__(self):
        self.found = 0

    def generate_user(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def check_tiktok(self, user):
        url = f"https://www.tiktok.com/@{user}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        if r.status_code == 404: return True
        return False

    def check_instagram(self, user):
        url = f"https://www.instagram.com/{user}/"
        r = requests.get(url)
        if r.status_code == 404: return True
        return False

    def check_telegram(self, user):
        url = f"https://t.me/{user}"
        r = requests.get(url)
        if "tgme_page_extra" not in r.text and r.status_code == 200:
            return False # مأخوذ
        return True # متاح غالباً

    def check_roblox(self, user):
        url = f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01"
        r = requests.get(url)
        if r.json().get("code") == 0: return True
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_user(length)
            is_available = False
            
            try:
                if platform == "1": is_available = self.check_tiktok(user)
                elif platform == "2": is_available = self.check_instagram(user)
                elif platform == "3": is_available = self.check_telegram(user)
                elif platform == "4": is_available = self.check_roblox(user)
                
                if is_available:
                    print(f"{G}✅ Found | {W}{user}")
                    with open("found_users.txt", "a") as f:
                        f.write(f"{user}\n")
            except:
                pass

# تشغيل الأداة
def main():
    clear()
    logo()
    choice = input(f"{Y}Choose Platform (1-4): {W}")
    length = int(input(f"{Y}Enter Username Length (3, 4, 5): {W}"))
    threads_num = int(input(f"{Y}Threads (Speed - e.g. 10): {W}"))
    
    print(f"\n{C}[!] Starting Fatch...{W}\n")
    
    app = Checker()
    for _ in range(threads_num):
        threading.Thread(target=app.start, args=(choice, length)).start()

if __name__ == "__main__":
    main()
