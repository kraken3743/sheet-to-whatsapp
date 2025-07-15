import threading
import time
from datetime import datetime
import pytz
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

IST = pytz.timezone('Asia/Kolkata')

DEFAULT_SHEET_URLS = [
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit#gid=909429816",
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit?gid=862699111"
]

users = {}
lock = threading.Lock()

def schedule_user(number, times, crop_box, custom_url=None):
    with lock:
        users[number] = {
            "times": times,
            "crop_box": crop_box,
            "custom_url": custom_url if custom_url else None
        }
        print(f"[SCHEDULE] {number} at {times} IST")

def cancel_user(number):
    with lock:
        if number in users:
            del users[number]
            print(f"[CANCEL] Schedule canceled for {number}")

def run_loop():
    while True:
        now = datetime.now(IST)
        current_time = now.strftime("%H:%M")
        with lock:
            for number, config in list(users.items()):
                if current_time in config['times']:
                    print(f"[SEND] Triggering send to {number} at {current_time}")
                    try:
                        urls = DEFAULT_SHEET_URLS.copy()
                        if config['custom_url']:
                            urls.append(config['custom_url'])
                        for url in urls:
                            img = take_screenshot(url, config['crop_box'])
                            send_whatsapp_image(number, img)
                    except Exception as e:
                        print(f"[ERROR] sending to {number}: {e}")
        time.sleep(30)
