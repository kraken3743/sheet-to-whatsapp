import schedule
import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

all_jobs = {}

def job_runner(sheet_url, number, crop_box):
    try:
        print(f"[JOB] Running for {number}...")
        path = take_screenshot(sheet_url, crop_box=crop_box)
        send_whatsapp_image(number, path)
    except Exception as e:
        print(f"[ERROR] in job_runner: {e}")

def schedule_user(sheet_url, number, times, start_date_str, num_days, crop_box, auto_disable):
    cancel_user(number)  # prevent duplicates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = start_date + timedelta(days=num_days)

    jobs = []

    for t in times:
        def make_job(time_slot):
            def job():
                now = datetime.now()
                if start_date.date() <= now.date() < end_date.date():
                    job_runner(sheet_url, number, crop_box)
                elif auto_disable and now.date() >= end_date.date():
                    print(f"[EXPIRE] Job for {number} at {time_slot} expired. Auto-cancelling.")
                    cancel_user(number)
            return job

        job_obj = schedule.every().day.at(t).do(make_job(t))
        jobs.append(job_obj)

    all_jobs[number] = jobs
    print(f"[SCHEDULED] {number} from {start_date_str} for {num_days} days at {times}")

def cancel_user(number):
    if number in all_jobs:
        for j in all_jobs[number]:
            schedule.cancel_job(j)
        del all_jobs[number]
        print(f"[CANCEL] Cancelled schedule for {number}")

def run_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)
