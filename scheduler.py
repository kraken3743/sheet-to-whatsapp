import threading
import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = []
lock = threading.Lock()

def schedule_user(sheet_url, number, time_str, crop_box):
    with lock:
        users.append({
            "sheet_url": sheet_url,
            "number": number,
            "time": time_str,
            "crop_box": crop_box,
            "sent": False
        })
        print(f"[SCHEDULE] Scheduled {number} at {time_str}")

def run_loop():
    while True:
        now = datetime.now().strftime("%H:%M")
        with lock:
            for user in users:
                if user["time"] == now and not user["sent"]:
                    print(f"[SEND] Triggering send for {user['number']} at {now}")
                    try:
                        img = take_screenshot(user["sheet_url"], user["crop_box"])
                        send_whatsapp_image(user["number"], img)
                        user["sent"] = True
                    except Exception as e:
                        print(f"[ERROR] Failed to send: {e}")
        time.sleep(1)
