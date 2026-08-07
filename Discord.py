import requests

def get_free_proxies():
    # سحب قائمة بروكسيات متجددة من مصدر مفتوح
    url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
    except Exception as e:
        print(f"خطأ في جلب القائمة: {e}")
    return []

def check_proxy(proxy):
    # فحص هل البروكسي يعمل ويسجيب أم لا
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        res = requests.get("https://httpbin.org/ip", proxies=proxy_dict, timeout=3)
        if res.status_code == 200:
            return True
    except:
        return False
    return False

# تجربة السكربت
raw_proxies = get_free_proxies()
print(f"تم جلب {len(raw_proxies)} بروكسي، جاري الفحص...")

working_proxies = []
for p in raw_proxies[:20]:  # فحص أول 20 بروكسي كعينّة
    if check_proxy(p):
        print(f"[+] شغّال: {p}")
        working_proxies.append(p)
    else:
        print(f"[-] غير شغال: {p}")

print(f"\nالبروكسيات الشغالة حالياً: {len(working_proxies)}")
