import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def schedule_user(sheet_url, number, start_date, num_days, times, crop_box):
    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "start_date": datetime.strptime(start_date, "%Y-%m-%d").date(),
            "end_date": datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=num_days - 1),
            "times": times,
            "crop_box": crop_box
        }
        print(f"[SCHEDULE] Scheduled {number} at {times} from {start_date} for {num_days} days.")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Canceled schedule for {number}")

def run_loop():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today = now.date()

        with lock:
            for number, config in list(users.items()):
                if today > config["end_date"]:
                    print(f"[AUTO REMOVE] {number} expired on {config['end_date']}")
                    del users[number]
                    continue

                if today >= config["start_date"] and current_time in config["times"]:
                    print(f"[SEND] Triggering send for {number} at {current_time}")
                    try:
                        img_path = take_screenshot(config["sheet_url"], config["crop_box"])
                        send_whatsapp_image(number, img_path)
                    except Exception as e:
                        print(f"[ERROR] Failed to send screenshot to {number}: {e}")

        time.sleep(1)
