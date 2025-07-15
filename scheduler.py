import time
from datetime import datetime
import pytz
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = {}
lock = None

DEFAULT_URLS = [
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit#gid=909429816",
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit?gid=862699111#gid=862699111"
]

def schedule_user(number, times, crop_box, custom_url=None):
    users[number] = {
        "times": times,
        "crop_box": crop_box,
        "custom_url": custom_url
    }

def cancel_user(number):
    if number in users:
        del users[number]

def run_scheduler():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = now.strftime("%H:%M")
        for number, config in list(users.items()):
            if current_time in config["times"]:
                urls = DEFAULT_URLS.copy()
                if config["custom_url"]:
                    urls.append(config["custom_url"])
                for url in urls:
                    try:
                        img_path = take_screenshot(url, config["crop_box"])
                        send_whatsapp_image(number, img_path)
                    except Exception as e:
                        print(f"[ERROR] sending image to {number}: {e}")
