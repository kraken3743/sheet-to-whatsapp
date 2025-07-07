import schedule
import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

scheduled_jobs = {}

def job_runner(sheet_url, whatsapp_number, crop_box):
    print(f"[JOB] Running for {whatsapp_number}")
    screenshot_path = take_screenshot(sheet_url, crop_box)
    if screenshot_path:
        send_whatsapp_image(whatsapp_number, screenshot_path)

def schedule_user(sheet_url, whatsapp_number, times, num_days=30, crop_box=(20, 130, 1000, 900)):
    today = datetime.today().date()

    for day_offset in range(num_days):
        job_date = today + timedelta(days=day_offset)
        for t in times:
            hour, minute = map(int, t.strip().split(":"))

            def make_job():
                return lambda: job_runner(sheet_url, whatsapp_number, crop_box)

            job = schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(make_job())
            job.tag(whatsapp_number)
            scheduled_jobs.setdefault(whatsapp_number, []).append(job)

    print(f"[SCHEDULE] {whatsapp_number} scheduled for {num_days} days at {times}")

def cancel_user(whatsapp_number):
    jobs = schedule.get_jobs(tag=whatsapp_number)
    for job in jobs:
        schedule.cancel_job(job)
    scheduled_jobs.pop(whatsapp_number, None)
    print(f"[CANCEL] Jobs cancelled for {whatsapp_number}")

def run_loop():
    print("[SCHEDULER] Starting loop...")
    while True:
        schedule.run_pending()
        time.sleep(1)
