import time
from datetime import datetime
from pytz import timezone
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = {}

def schedule_user(sheet_url, number, times, crop_box):
    users[number] = {
        "sheet_url": sheet_url,
        "times": times,
        "crop_box": crop_box
    }

def run_loop():
    print("[SCHEDULER] Loop started")
    ist = timezone("Asia/Kolkata")
    while True:
        now = datetime.now(ist).strftime("%H:%M")
        for number, config in users.items():
            if now in config["times"]:
                print(f"[SEND] Triggering for {number} at {now}")
                try:
                    img_path = take_screenshot(config["sheet_url"], config["crop_box"])
                    send_whatsapp_image(number, img_path)
                except Exception as e:
                    print(f"[ERROR] Failed to send to {number}: {e}")
        time.sleep(60)
