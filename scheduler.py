import schedule
import threading
import time
import os
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

def job(config):
    print(f"[INFO] Triggering job for {config['whatsapp_number']}")
    screenshot_path = take_screenshot(config["sheet_url"])

    if not screenshot_path or not os.path.exists(screenshot_path):
        print(f"[ERROR] Screenshot not created. Skipping WhatsApp send.")
        return

    send_whatsapp_image(config["whatsapp_number"], screenshot_path)

def convert_ist_to_utc(time_str):
    """Converts IST time (HH:MM) to UTC for scheduling."""
    try:
        ist_time = datetime.strptime(time_str.strip(), "%H:%M")
        utc_time = ist_time - timedelta(hours=5, minutes=30)
        return utc_time.strftime("%H:%M")
    except Exception as e:
        print(f"[ERROR] Time conversion failed for {time_str}: {e}")
        return None

def schedule_user(sheet_url, number, times):
    config = {"sheet_url": sheet_url, "whatsapp_number": number}
    for t in times:
        utc_time = convert_ist_to_utc(t)
        if utc_time:
            print(f"[SCHEDULER] Scheduling {number} at {t.strip()} IST → {utc_time} UTC")
            try:
                schedule.every().day.at(utc_time).do(job, config).tag(number)
            except Exception as e:
                print(f"[ERROR] Scheduling failed for {t}: {e}")

def run_loop():
    print("[SCHEDULER] Running scheduler loop...")
    while True:
        # Show current time in both UTC and IST for debug clarity
        now_utc = datetime.utcnow().strftime("%H:%M")
        now_ist = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%H:%M")
        print(f"[TIME] UTC: {now_utc}, IST: {now_ist}")
        schedule.run_pending()
        time.sleep(60)  # Check once every minute
