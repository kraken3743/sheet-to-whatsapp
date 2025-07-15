import threading
import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = []
lock = threading.Lock()

def schedule_user(sheet_urls, number, times, crop_box):
    with lock:
        users.append({
            "sheet_urls": sheet_urls,
            "number": number,
            "times": times,
            "crop_box": crop_box
        })
        print(f"[SCHEDULE] Added {number} at {times} for sheets: {sheet_urls}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        with lock:
            for user in users:
                if current_time in user["times"]:
                    print(f"[SEND] Triggering for {user['number']} at {current_time}")
                    for url in user["sheet_urls"]:
                        try:
                            image_path = take_screenshot(url, user["crop_box"])
                            send_whatsapp_image(user["number"], image_path)
                        except Exception as e:
                            print(f"[ERROR] {user['number']} | {e}")
        time.sleep(60)
