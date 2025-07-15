import threading
import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

lock = threading.Lock()
users = {}

DEFAULT_SHEET_URLS = [
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit#gid=909429816",
    "https://docs.google.com/spreadsheets/d/1_QSvPyOCCP43AZ6eZqNIm4OmJb8ds9EB4UD88C2-Sb4/edit?gid=862699111#gid=862699111"
]

def schedule_user(number, times, crop_box, custom_url):
    with lock:
        all_urls = DEFAULT_SHEET_URLS.copy()
        if custom_url:
            all_urls.append(custom_url)

        users[number] = {
            "times": times,
            "crop_box": crop_box,
            "sheet_urls": all_urls
        }
        print(f"[SCHEDULE] {number} at {times} for {len(all_urls)} URLs")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        with lock:
            for number, config in users.items():
                if current_time in config["times"]:
                    for url in config["sheet_urls"]:
                        try:
                            print(f"[SEND] Sending to {number} - {url}")
                            img_path = take_screenshot(url, config["crop_box"])
                            send_whatsapp_image(number, img_path)
                        except Exception as e:
                            print(f"[ERROR] Sending to {number}: {e}")

        time.sleep(60)
