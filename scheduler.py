import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def schedule_user(sheet_url, number, num_days, times, crop_box):
    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "start": datetime.now().date(),
            "end": datetime.now().date() + timedelta(days=num_days - 1),
            "times": times,
            "crop_box": crop_box
        }
    print(f"[SCHEDULE] {number} scheduled from {users[number]['start']} to {users[number]['end']} at {times}")

def cancel_user(number):
    with lock:
        removed = users.pop(number, None)
    print(f"[CANCEL] {'Removed' if removed else 'No schedule for'} {number}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now()
        now_str = now.strftime("%H:%M")
        today = now.date()

        with lock:
            for number, cfg in list(users.items()):
                if today > cfg["end"]:
                    print(f"[AUTO-REMOVE] {number} expired on {cfg['end']}")
                    users.pop(number)
                    continue

                if today >= cfg["start"] and now_str in cfg["times"]:
                    print(f"[SEND] Trigger for {number} at {now_str}")
                    try:
                        path = take_screenshot(cfg["sheet_url"], cfg["crop_box"])
                        send_whatsapp_image(number, path)
                    except Exception as e:
                        print(f"[ERROR] during send for {number}: {e}")

        time.sleep(30)
