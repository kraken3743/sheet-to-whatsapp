import schedule
import time
import threading
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

jobs = {}

def schedule_user(sheet_url, whatsapp_number, times, crop_box, start_date, num_days):
    def job_runner():
        today = datetime.now().date()
        if today >= datetime.strptime(start_date, "%Y-%m-%d").date():
            screenshot_path = take_screenshot(sheet_url, crop_box)
            send_whatsapp_image(whatsapp_number, screenshot_path)

    key = whatsapp_number

    for t in times:
        job = schedule.every().day.at(t).do(job_runner)
        jobs.setdefault(key, []).append(job)

    print(f"[SCHEDULER] Jobs scheduled for {key}")

def cancel_schedule(whatsapp_number):
    key = whatsapp_number
    if key in jobs:
        for job in jobs[key]:
            schedule.cancel_job(job)
        del jobs[key]
        print(f"[CANCEL] All jobs for {key} cancelled.")

def run_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)
