import schedule
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

scheduled_tasks = {}

def job_wrapper(config):
    now = datetime.now()
    end_date = config["start_date"] + timedelta(days=config["num_days"])
    print(f"[DEBUG] Start: {config['start_date']} | End: {end_date} | Now: {now}")

    if now.date() >= end_date.date():
        print(f"[DISABLE] Auto-cancelling job for {config['number']} after {config['num_days']} days.")
        cancel_schedule(config['number'])
        return

    screenshot_path = take_screenshot(config["sheet_url"], config["crop_box"])
    send_whatsapp_image(config["number"], screenshot_path)

def schedule_user(sheet_url, number, times, crop_box, num_days):
    start_date = datetime.now()
    config = {
        "sheet_url": sheet_url,
        "number": number,
        "times": times,
        "crop_box": crop_box,
        "start_date": start_date,
        "num_days": num_days
    }

    print(f"[SCHEDULE] Scheduled {number} at {times} daily.")

    if number in scheduled_tasks:
        cancel_schedule(number)

    jobs = []
    for t in times:
        job = schedule.every().day.at(t).do(job_wrapper, config)
        jobs.append(job)

    scheduled_tasks[number] = jobs

def cancel_schedule(number):
    if number in scheduled_tasks:
        for job in scheduled_tasks[number]:
            schedule.cancel_job(job)
        del scheduled_tasks[number]
        print(f"[CANCEL] Schedule cancelled for {number}")
    else:
        print(f"[CANCEL] No schedule found for {number}")

def run_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)
