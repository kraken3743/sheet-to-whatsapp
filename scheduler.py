import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = {}

def schedule_user(sheet_url, number, time_str, crop_box):
    users[number] = {
        "sheet_url": sheet_url,
        "time": time_str,
        "crop_box": crop_box,
        "sent": False
    }

def cancel_user(number):
    if number in users:
        del users[number]
        print(f"[CANCEL] Canceled schedule for {number}")

def run_scheduler_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now().strftime("%H:%M")
        for number, config in list(users.items()):
            if not config["sent"] and now == config["time"]:
                print(f"[SCHEDULER] Sending to {number} at {now}")
                try:
                    path = take_screenshot(config["sheet_url"], config["crop_box"])
                    send_whatsapp_image(number, path)
                    config["sent"] = True
                except Exception as e:
                    print(f"[ERROR] Failed for {number}: {e}")
        time.sleep(1)
