import socket
import requests
import os
import json
from datetime import datetime

# تهيئة الألوان
R, G, Y, B, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;36m', '\033[1;37m'

def logo():
    os.system('clear')
    print(f"""
{R}  _______ ______ ______      ___ _____ _  __
{R} |__   __|____  |  ____|    /   |__   __| |/ /
{R}    | |     / /| |__      / /| |  | |  | ' / 
{R}    | |    / / |  __|    / /_| |  | |  |  <  
{R}    | |   / /  | |      / ___  |  | |  | . \\ 
{R}    |_|  /_/   |_|     /_/   |_|  |_|  |_|\\_\\
{C}=================================================
{Y}  Z7F ATK ULTRA V3.0 | CYBER-INTELLIGENCE TOOL
{G}  PRECISION SCANNING & RECONNAISSANCE
{C}================================================={W}""")

def advanced_scan():
    logo()
    target = input(f"{G}Enter Target URL/IP: {W}").replace('http://','').replace('https://','').split('/')[0]
    
    try:
        print(f"\n{Y}[*] Starting Deep Analysis for: {target}...{W}")
        ip = socket.gethostbyname(target)
        
        # 1. معلومات السيرفر والشبكة بالتفصيل
        print(f"\n{B}[1] Network Intelligence:{W}")
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if res['status'] == 'success':
            print(f"  {C}IP Address:  {W}{ip}")
            print(f"  {C}ASN:         {W}{res.get('as')}")
            print(f"  {C}Provider:    {W}{res.get('isp')}")
            print(f"  {C}Location:    {W}{res.get('country')}, {res.get('city')} ({res.get('zip')})")
            print(f"  {C}Coordinates: {W}{res.get('lat')}, {res.get('lon')}")
            print(f"  {C}Timezone:    {W}{res.get('timezone')}")
            print(f"  {C}Mobile/VPN:  {W}{'Yes' if res.get('mobile') or res.get('proxy') else 'No'}")

        # 2. فحص الحماية والتقنيات (Web Headers)
        print(f"\n{B}[2] Security Headers & Tech:{W}")
        try:
            h = requests.get(f"http://{target}", timeout=3).headers
            print(f"  {C}Server:      {W}{h.get('Server', 'Hidden')}")
            print(f"  {C}Powered By:  {W}{h.get('X-Powered-By', 'Unknown')}")
            print(f"  {C}XSS Protect: {W}{h.get('X-XSS-Protection', 'Not Active')}")
            print(f"  {C}HSTS:        {W}{'Enabled' if h.get('Strict-Transport-Security') else 'Disabled'}")
        except: print(f"  {R}[-] Could not fetch headers.{W}")

        # 3. فحص البورتات الاحترافي
        print(f"\n{B}[3] Deep Port Scanning (Top 25):{W}")
        ports = [21,22,23,25,53,80,110,135,139,143,443,445,465,587,993,995,1723,3306,3389,5432,5900,8080,8443]
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.4)
            if s.connect_ex((ip, port)) == 0:
                try: service = socket.getservbyport(port)
                except: service = "Unknown"
                print(f"  {G}[OPEN]{W} Port {port} | Service: {service}")
            s.close()

    except Exception as e:
        print(f"{R}[-] Fatal Error: {e}{W}")
    
    input(f"\n{Y}Press Enter to return...")

def main():
    while True:
        logo()
        print(f"{G}[1] {W}Deep Target Recon (Full Power)")
        print(f"{G}[2] {W}Quick Port Scan")
        print(f"{G}[3] {W}Tool Credits")
        print(f"{R}[0] Exit")
        
        c = input(f"\n{Y}Z7F-ATK > {W}")
        if c == '1': advanced_scan()
        elif c == '2':
            logo()
            target = input("Target IP: ")
            print(f"{G}[*] Scanning {target}...")
            # فحص سريع
            for p in [80,443,21,22]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((target, p)) == 0: print(f"  - {p} Open")
                s.close()
            input("Done...")
        elif c == '0': break

if __name__ == "__main__":
    main()
