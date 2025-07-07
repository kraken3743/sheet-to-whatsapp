# scheduler.py
import schedule
import time
import threading
import json
import os
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

jobs = {}
PERSIST_FILE = "schedules.json"

def job_wrapper(number, job_data):
    today = datetime.now().date()
    start = datetime.strptime(job_data['start_date'], "%Y-%m-%d").date()
    end = start + timedelta(days=job_data['num_days'])

    print(f"[DEBUG] Start: {start} | End: {end} | Now: {today}")
    if start <= today < end:
        screenshot_path = take_screenshot(job_data['sheet_url'], tuple(job_data['crop_box']))
        send_whatsapp_image(number, screenshot_path)
    elif today >= end:
        print(f"[AUTO-DISABLE] Removing schedule for {number} (expired)")
        cancel_user(number)

def persist_jobs():
    with open(PERSIST_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)

def load_persisted_jobs():
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, 'r') as f:
            persisted = json.load(f)
            for number, job_data in persisted.items():
                schedule_user(**job_data, from_load=True)

def schedule_user(sheet_url, number, times, start_date, num_days, crop_box, from_load=False):
    print(f"  Sheet URL: {sheet_url}\n  Start Date: {start_date}\n  Times: {times}")
    jobs[number] = {
        "sheet_url": sheet_url,
        "times": times,
        "start_date": start_date,
        "num_days": num_days,
        "crop_box": crop_box
    }

    for t in times:
        schedule.every().day.at(t).do(job_wrapper, number=number, job_data=jobs[number])

    if not from_load:
        persist_jobs()

    print(f"[SCHEDULE] Scheduled {number} at {times} daily.")

def cancel_user(number):
    jobs.pop(number, None)
    persist_jobs()
    schedule.clear()  # Remove all jobs
    for num, job_data in jobs.items():
        for t in job_data['times']:
            schedule.every().day.at(t).do(job_wrapper, number=num, job_data=job_data)
    print(f"[CANCEL] Cancelled schedule for {number}.")

def run_loop():
    print("[SCHEDULER] Running loop...")
    while True:
        schedule.run_pending()
        time.sleep(1)