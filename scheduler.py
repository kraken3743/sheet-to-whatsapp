import time
from datetime import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

scheduled_jobs = {}

def schedule_user(sheet_url, number, send_time, crop_box):
    scheduled_jobs[number] = {
        "sheet_url": sheet_url,
        "send_time": send_time,
        "crop_box": crop_box,
        "sent": False
    }
    print(f"[SCHEDULE] Scheduled {number} at {send_time}")

def run_loop():
    print("[SCHEDULER] Loop started")
    while True:
        now = datetime.now().strftime("%H:%M")
        for number, job in list(scheduled_jobs.items()):
            if not job["sent"] and now == job["send_time"]:
                print(f"[SEND] Sending to {number}")
                try:
                    img_path = take_screenshot(job["sheet_url"], job["crop_box"])
                    send_whatsapp_image(number, img_path)
                    job["sent"] = True
                except Exception as e:
                    print(f"[ERROR] Sending failed: {e}")
        time.sleep(1)
