import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

def parse_time_12h(t_str):
    return datetime.strptime(t_str, "%I:%M %p").strftime("%H:%M")

def schedule_user(sheet_url, number, start_date_str, end_date_str, times_12, crop_box):
    times_24 = [parse_time_12h(t) for t in times_12]
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    with lock:
        users[number] = {
            "sheet_url": sheet_url,
            "start": start_date,
            "end": end_date,
            "times": times_24,
            "crop_box": crop_box
        }
    print(f"[SCHEDULE] {number}: {start_date} – {end_date} at {times_24}")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Canceled schedule for {number}")

def run_loop():
    while True:
        now = datetime.now()
        current = now.strftime("%H:%M")
        today = now.date()

        with lock:
            for num, cfg in list(users.items()):
                if today > cfg["end"]:
                    print(f"[AUTO-REMOVE] {num} expired on {cfg['end']}")
                    users.pop(num)
                    continue
                if cfg["start"] <= today <= cfg["end"] and current in cfg["times"]:
                    print(f"[SEND] {num} at {current}")
                    try:
                        img = take_screenshot(cfg["sheet_url"], cfg["crop_box"])
                        send_whatsapp_image(num, img)
                    except Exception as e:
                        print(f"[ERROR] send failed for {num}: {e}")

        time.sleep(60)
