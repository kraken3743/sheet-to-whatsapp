import schedule
import threading
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

all_jobs = {}

def job_runner(sheet_url, number, crop_box):
    try:
        print(f"[JOB-RUNNER] Taking screenshot for {number}")
        path = take_screenshot(sheet_url, crop_box=crop_box)
        print(f"[JOB-RUNNER] Screenshot path: {path}")
        send_whatsapp_image(number, path)
    except Exception as e:
        print(f"[ERROR] in job_runner: {e}")

def schedule_user(sheet_url, number, times, start_date_str, num_days, crop_box, auto_disable):
    cancel_user(number)  # avoid duplicates
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = start_date + timedelta(days=num_days)

    jobs = []

    for t in times:
        def make_job(time_slot):
            def job():
                now = datetime.now()
                print(f"[JOB-CHECK] Checking for {number} at {now.strftime('%H:%M:%S')}")

                if start_date.date() <= now.date() < end_date.date():
                    print(f"[JOB-EXECUTE] Running job for {number} at {time_slot}")
                    job_runner(sheet_url, number, crop_box)
                elif auto_disable and now.date() >= end_date.date():
                    print(f"[JOB-EXPIRE] Auto-cancelling expired job for {number}")
                    cancel_user(number)
            return job

        job_obj = schedule.every().day.at(t).do(make_job(t))
        jobs.append(job_obj)
        print(f"[SCHEDULE] Scheduled {number} at {t} daily.")

    all_jobs[number] = jobs
    print(f"[DEBUG] Start: {start_date.date()} | End: {end_date.date()} | Now: {datetime.now().date()}")

def cancel_user(number):
    if number in all_jobs:
        for j in all_jobs[number]:
            schedule.cancel_job(j)
        del all_jobs[number]
        print(f"[CANCEL] Cancelled all jobs for {number}")

def run_loop():
    print("[SCHEDULER] Starting loop...")
    while True:
        schedule.run_pending()
        print("[SCHEDULER] Tick", datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)
