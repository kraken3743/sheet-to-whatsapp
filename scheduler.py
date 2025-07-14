import threading
import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def schedule_user(sheet_url, number, start_date, end_date, times, crop_box):
    from datetime import datetime
    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "start_date": datetime.strptime(start_date, "%Y-%m-%d").date(),
            "end_date": datetime.strptime(end_date, "%Y-%m-%d").date(),
            "times": times,
            "crop_box": crop_box
        }
        print(f"[SCHEDULE] Scheduled {number} from {start_date} to {end_date} at {times}")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Canceled {number}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today = now.date()

        with lock:
            for number, cfg in list(users.items()):
                if today > cfg["end_date"]:
                    print(f"[AUTO REMOVE] {number} expired on {cfg['end_date']}")
                    del users[number]
                    continue

                if cfg["start_date"] <= today <= cfg["end_date"]:
                    if current_time in cfg["times"]:
                        print(f"[SEND] Sending for {number} at {current_time}")
                        try:
                            path = take_screenshot(cfg["sheet_url"], cfg["crop_box"])
                            send_whatsapp_image(number, path)
                        except Exception as e:
                            print(f"[ERROR] {number}: {e}")

        time.sleep(60)
