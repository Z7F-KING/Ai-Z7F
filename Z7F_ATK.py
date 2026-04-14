import socket
import requests
import os
import sys
from datetime import datetime

# الألوان
R = '\033[1;31m' # أحمر
G = '\033[1;32m' # أخضر
Y = '\033[1;33m' # أصفر
B = '\033[1;34m' # أزرق
W = '\033[1;37m' # أبيض
C = '\033[1;36m' # سماوي

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
{Y}  Z7F ATK ULTIMATE SCANNER | V 2.0 PROFESSIONAL
{G}  STAY ETHICAL - POWERED BY Z7F ATK TEAM
{C}================================================={W}""")

def web_scanner():
    logo()
    print(f"{Y}[!] Example: google.com or 1.1.1.1")
    target = input(f"{G}Z7F-ATK > {W}Enter Target URL/IP: ").replace('http://','').replace('https://','').split('/')[0]
    
    try:
        ip = socket.gethostbyname(target)
        print(f"\n{C}[+] Target: {W}{target}")
        print(f"{C}[+] IP Address: {W}{ip}")
        print(f"{Y}{'-'*40}")

        # 1. Port Scanning
        print(f"{G}[*] Scanning Critical Ports...{W}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((ip, port)) == 0:
                try: service = socket.getservbyport(port)
                except: service = "Unknown"
                print(f"  {G}[OPEN] {W}Port {port} ({service})")
            s.close()

        # 2. IP Info
        print(f"\n{G}[*] Fetching Server Info...{W}")
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        if res['status'] == 'success':
            print(f"  {C}Location: {W}{res['country']}, {res['city']}")
            print(f"  {C}ISP:      {W}{res['isp']}")
            print(f"  {C}Org:      {W}{res['org']}")

        # 3. Admin Page Finder (Basic)
        print(f"\n{G}[*] Checking Admin Panels...{W}")
        admin_list = ['/admin/', '/login/', '/config/', '/cp/', '/wp-admin/']
        for path in admin_list:
            try:
                r = requests.get(f"http://{target}{path}", timeout=1)
                if r.status_code == 200:
                    print(f"  {G}[FOUND] {W}Possible Admin Page: {path}")
            except: pass

    except Exception as e:
        print(f"{R}[-] Error: {e}")
    
    input(f"\n{Y}Press Enter to return to Menu...")

def main_menu():
    while True:
        logo()
        print(f"{G}[1] {W}Full Website Scanner (Ports/IP/Admin)")
        print(f"{G}[2] {W}Domain Whois Lookup")
        print(f"{G}[3] {W}Show My IP")
        print(f"{G}[4] {W}Credits / Info")
        print(f"{R}[0] Exit Tool")
        
        choice = input(f"\n{Y}Z7F-ATK > {W}")
        
        if choice == '1':
            web_scanner()
        elif choice == '2':
            # Whois simple demo
            logo()
            target = input(f"{G}Enter Domain: {W}")
            os.system(f"whois {target} | head -n 20")
            input("\nEnter to back...")
        elif choice == '3':
            my_ip = requests.get('https://api.ipify.org').text
            print(f"\n{G}[+] Your Public IP: {W}{my_ip}")
            input("\nEnter to back...")
        elif choice == '4':
            print(f"\n{C}Tool Name: {W}Z7F ATK PRO")
            print(f"{C}Dev: {W}Z7F ATK TEAM")
            print(f"{C}Description: {W}Advanced reconnaissance tool for iSH.")
            input("\nEnter to back...")
        elif choice == '0':
            print(f"{R}Shutting down Z7F ATK...{W}")
            break
        else:
            print(f"{R}[!] Invalid selection")

if __name__ == "__main__":
    main_menu()
