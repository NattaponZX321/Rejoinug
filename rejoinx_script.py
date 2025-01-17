import os
import time
import psutil
import requests

# สีสำหรับแบนเนอร์และข้อความ
CYAN = "\033[96m"
MAGENTA = "\033[95m"
DARK_BLUE = "\033[94m"
RESET = "\033[0m"

def print_banner():
    banner = [
        "██████╗ ██╗   ██╗██████╗  █████╗ ███████╗███████╗██╗  ██╗    ██████╗ ███████╗     ██╗ ██████╗ ██╗███╗   ██╗",
        "██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝╚██╗██╔╝    ██╔══██╗██╔════╝     ██║██╔═══██╗██║████╗  ██║",
        "██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗███████╗ ╚███╔╝     ██████╔╝█████╗       ██║██║   ██║██║██╔██╗ ██║",
        "██╔══██╗  ╚██╔╝  ██╔═══╝ ██╔══██║╚════██║╚════██║ ██╔██╗     ██╔══██╗██╔══╝  ██   ██║██║   ██║██║██║╚██╗██║",
        "██████╔╝   ██║   ██║     ██║  ██║███████║███████║██╔╝ ██╗    ██║  ██║███████╗╚█████╔╝╚██████╔╝██║██║ ╚████║",
        "╚═════╝    ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝ ╚════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝"
    ]

    print(CYAN)
    for line in banner:
        print(line)
    print(RESET)

def display_cpu_info():
    cpu_temp = psutil.sensors_temperatures().get("coretemp", [])
    if cpu_temp:
        temp_value = cpu_temp[0].current  # อุณหภูมิ CPU (CoreTemp ตัวแรก)
    else:
        temp_value = "Unknown"

    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage, temp_value

def display_cpu_frame():
    print(MAGENTA + "-" * 80 + RESET)
    cpu_usage, temp_value = display_cpu_info()
    print(f"{CYAN}CPU Usage: {cpu_usage}% | CPU Temperature: {temp_value}°C{RESET}")
    print(MAGENTA + "-" * 80 + RESET)

def send_to_webhook(webhook_url, cpu_usage, temp_value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    payload = {
        "content": f"**CPU Status Update**\n> Time: {timestamp}\n> Usage: {cpu_usage}%\n> Temp: {temp_value}°C"
    }
    try:
        requests.post(webhook_url, json=payload)
        print(f"{DARK_BLUE}Sent update to webhook.{RESET}")
    except Exception as e:
        print(f"{MAGENTA}Failed to send webhook: {e}{RESET}")

def manage_roblox_clients(selected_game_url, selected_client_count, roblox_clients, webhook_url):
    for client in roblox_clients[:selected_client_count]:
        print(f"{CYAN}Opening Roblox Client: {client}{RESET}")
        os.system(f"am start -n {client}/com.roblox.client")
        time.sleep(3)
        os.system(f"am start -a android.intent.action.VIEW -d 'roblox://placeID={selected_game_url}'")
        print(f"{MAGENTA}Client {client} is joining the game...{RESET}")
        time.sleep(5)  # หน่วงเวลาเปิด Client

# Main
roblox_clients = [
    "com.roblox.client",
    "com.roblox.clienu",
    "com.roblox.clienv",
    "com.roblox.clienw",
    "com.roblox.clienx",
    "com.roblox.clieny"
]

print_banner()

# รับข้อมูลเกมและ Webhook URL
selected_game_url = input("Enter the Game ID or Private Server Link: ")
webhook_url = input("Enter the Webhook URL: ")

# เลือกจำนวน Client Roblox
selected_client_count = int(input("Select the number of clients to open (1-10): "))

# เริ่มเปิด Roblox Clients
manage_roblox_clients(selected_game_url, selected_client_count, roblox_clients, webhook_url)

# กำหนดเวลาส่ง Webhook
webhook_interval = int(input("Enter the interval for webhook updates (in seconds): "))

# เริ่มแสดงข้อมูล CPU และส่ง Webhook
try:
    last_webhook_time = 0
    while True:
        display_cpu_frame()
        cpu_usage, temp_value = display_cpu_info()

        # ส่งข้อมูลไป Webhook ตาม interval
        if time.time() - last_webhook_time >= webhook_interval:
            send_to_webhook(webhook_url, cpu_usage, temp_value)
            last_webhook_time = time.time()

        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")
    