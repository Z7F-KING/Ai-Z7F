import random
import string
import requests
import threading
import os
import sys

# ألوان احترافية
G = '\033[1;32m' # أخضر
W = '\033[1;37m' # أبيض
C = '\033[1;36m' # سماوي
Y = '\033[1;33m' # أصفر

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print(f"""
{C}══════════════════════════════════════
{Y}     ULTRA USER GEN & CHECKER
{C}══════════════════════════════════════
{W}  1 - TikTok    {W}  2 - Instagram
{W}  3 - Telegram  {W}  4 - Roblox
{C}══════════════════════════════════════{W}""")

class Checker:
    def __init__(self):
        self.total_checked = 0

    def generate_user(self, length):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def check_platform(self, platform, user):
        try:
            if platform == "1": # TikTok
                r = requests.get(f"https://www.tiktok.com/@{user}", headers={"User-Agent": "Mozilla/5.0"})
                return r.status_code == 404
            elif platform == "2": # Instagram
                r = requests.get(f"https://www.instagram.com/{user}/")
                return r.status_code == 404
            elif platform == "3": # Telegram
                r = requests.get(f"https://t.me/{user}")
                return "tgme_page_extra" not in r.text and r.status_code == 200
            elif platform == "4": # Roblox
                r = requests.get(f"https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=2000-01-01")
                return r.json().get("code") == 0
        except:
            return False
        return False

    def start(self, platform, length):
        while True:
            user = self.generate_user(length)
            # تحديث السطر الحالي في الكونسول (بدون النزول لسطر جديد)
            sys.stdout.write(f"\r{W}Check | {Y}{user} {W}| Total: {C}{self.total_checked}")
            sys.stdout.flush()
            
            if self.check_platform(platform, user):
                print(f"\n{G}✅ Found | {W}{user}") # النزول لسطر جديد عند الإيجاد
                with open("found.txt", "a") as f:
                    f.write(f"{user}\n")
            
            self.total_checked += 1

def main():
    clear()
    logo()
    choice = input(f"{Y}Choose Platform: {W}")
    length = int(input(f"{Y}User Length (3, 4, 5): {W}"))
    
    # السرعة: 0.0 تعني أعلى سرعة ممكنة باستخدام Threads مكثفة
    speed = input(f"{Y}Speed (Type 0.0 for Max): {W}")
    threads_num = 25 if speed == "0.0" else 5
    
    print(f"\n{C}[!] Searching... (Results saved to found.txt){W}\n")
    
    app = Checker()
    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=app.start, args=(choice, length))
        t.start()
        threads.append(t)

if __name__ == "__main__":
    main()
