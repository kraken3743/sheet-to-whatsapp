from screenshot import take_screenshot
from whatsapp import send_whatsapp_image
from datetime import datetime
import time
import pytz
import threading

lock = threading.Lock()
users = {}

DEFAULT_SHEETS = [
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit#gid=909429816",
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit?gid=862699111#gid=862699111"
]

def schedule_user(optional_sheet_url, number, times, crop_box):
    with lock:
        users[number] = {
            "extra_url": optional_sheet_url.strip() if optional_sheet_url else None,
            "times": times,
            "crop_box": crop_box
        }
        print(f"[SCHEDULE] {number} scheduled for {times} with crop {crop_box}")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Canceled for {number}")

def run_loop():
    tz = pytz.timezone("Asia/Kolkata")
    while True:
        now = datetime.now(tz)
        current_time = now.strftime("%H:%M")

        with lock:
            for number, config in list(users.items()):
                if current_time in config['times']:
                    print(f"[SEND] Triggering {number} at {current_time}")
                    try:
                        crop_box = config["crop_box"]
                        for url in DEFAULT_SHEETS:
                            path = take_screenshot(url, crop_box)
                            send_whatsapp_image(number, path)
                        if config["extra_url"]:
                            path = take_screenshot(config["extra_url"], crop_box)
                            send_whatsapp_image(number, path)
                    except Exception as e:
                        print(f"[ERROR] Failed to send to {number}: {e}")
        time.sleep(30)
