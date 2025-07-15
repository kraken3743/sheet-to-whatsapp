from datetime import datetime
import time
import pytz
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = []

def schedule_user(sheet_url, number, time_str, crop_box):
    users.append({
        "sheet_url": sheet_url,
        "number": number,
        "time_str": time_str,
        "crop_box": crop_box,
        "sent": False
    })
    print(f"[SCHEDULED] {number} at {time_str} IST")

def run_loop():
    print("[SCHEDULER] Loop started")
    ist = pytz.timezone("Asia/Kolkata")
    while True:
        now = datetime.now(ist)
        current_time = now.strftime("%H:%M")
        for user in users:
            if not user['sent'] and current_time == user['time_str']:
                print(f"[SEND] Triggering for {user['number']} at {current_time}")
                try:
                    path = take_screenshot(user['sheet_url'], user['crop_box'])
                    send_whatsapp_image(user['number'], path)
                    user['sent'] = True
                except Exception as e:
                    print(f"[ERROR] Failed: {e}")
        time.sleep(1)
