import schedule
import threading
import time
import os
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

def job(config):
    print(f"[INFO] Triggering job for {config['whatsapp_number']}")
    screenshot_path = take_screenshot(config["sheet_url"])

    if not screenshot_path or not os.path.exists(screenshot_path):
        print(f"[ERROR] Screenshot not created. Skipping WhatsApp send.")
        return

    send_whatsapp_image(config["whatsapp_number"], screenshot_path)

def schedule_user(sheet_url, number, times):
    config = {"sheet_url": sheet_url, "whatsapp_number": number}
    for t in times:
        print(f"[SCHEDULER] Scheduling {number} at {t.strip()}")
        try:
            schedule.every().day.at(t.strip()).do(job, config).tag(number)
        except Exception as e:
            print(f"[ERROR] Scheduling failed for {t}: {e}")

def run_loop():
    print("[SCHEDULER] Running scheduler loop...")
    while True:
        schedule.run_pending()
        time.sleep(1)
