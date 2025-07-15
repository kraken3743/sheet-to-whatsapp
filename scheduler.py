import threading
import time
from datetime import datetime
import pytz
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def schedule_user(sheet_url, number, times):
    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "times": times
        }
        print(f"[SCHEDULE] {number} at times {times}")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Removed {number}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M")
        with lock:
            for number, config in users.items():
                if now in config["times"]:
                    print(f"[SEND] Triggering send for {number} at {now}")
                    try:
                        img_path = take_screenshot(config["sheet_url"])
                        send_whatsapp_image(number, img_path)
                    except Exception as e:
                        print(f"[ERROR] while sending to {number}: {e}")
        time.sleep(60)  # Check every minute
