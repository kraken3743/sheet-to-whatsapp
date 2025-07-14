import threading
import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def schedule_user(sheet_url, number, time_str, crop_box):
    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "time": time_str,
            "crop_box": crop_box,
            "sent": False
        }
        print(f"[SCHEDULE] {number} at {time_str}")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Schedule cancelled for {number}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now().strftime("%H:%M")
        with lock:
            for number, config in list(users.items()):
                if not config["sent"] and now == config["time"]:
                    print(f"[SEND] Sending to {number} at {now}")
                    try:
                        img_path = take_screenshot(config["sheet_url"], config["crop_box"])
                        send_whatsapp_image(number, img_path)
                        config["sent"] = True
                    except Exception as e:
                        print(f"[ERROR] Failed for {number}: {e}")
        time.sleep(1)
