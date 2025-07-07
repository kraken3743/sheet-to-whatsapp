import schedule
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

tasks = {}

def schedule_user(sheet_url, number, times, crop_box, start_date, num_days):
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days)).strftime("%Y-%m-%d")

    def job():
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        print(f"[DEBUG] Start: {start_date} | End: {end_date} | Now: {today}")

        if start_date <= today <= end_date:
            print(f"[JOB] Triggered for {number}")
            screenshot_path = take_screenshot(sheet_url, crop_box)
            send_whatsapp_image(number, screenshot_path)
        elif today > end_date:
            print(f"[JOB] Auto-cancelling {number} after end date {end_date}")
            cancel_user(number)

    for t in times:
        job_instance = schedule.every().day.at(t.strip()).do(job)
        if number not in tasks:
            tasks[number] = []
        tasks[number].append(job_instance)

    print(f"[SCHEDULE] Scheduled {number} at {times} daily.")

def cancel_user(number):
    if number in tasks:
        for job in tasks[number]:
            schedule.cancel_job(job)
        del tasks[number]
        print(f"[CANCEL] Cancelled all jobs for {number}")
    else:
        print(f"[CANCEL] No active jobs found for {number}")

def run_loop():
    while True:
        schedule.run_pending()
        print(f"[SCHEDULER] Tick {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(1)
