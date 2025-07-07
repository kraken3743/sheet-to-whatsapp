import schedule
import time
from datetime import datetime, timedelta
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

schedules = {}

def schedule_user(data):
    try:
        number = data["whatsapp_number"]
        url = data["sheet_url"]
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        times = [t.strip() for t in data["times"].split(",")]
        num_days = int(data.get("num_days", 1))
        end_date = start_date + timedelta(days=num_days - 1)

        crop = (
            int(data.get("crop_left", 20)),
            int(data.get("crop_top", 130)),
            int(data.get("crop_right", 1000)),
            int(data.get("crop_bottom", 900)),
        )

        schedules[number] = {
            "sheet_url": url,
            "times": times,
            "crop": crop,
            "start_date": start_date,
            "end_date": end_date,
        }

        for t in times:
            schedule.every().day.at(t).do(run_job, number=number).tag(number)
        print(f"[SCHEDULE] Scheduled {number} at {times} daily.")
    except Exception as e:
        print(f"[ERROR] schedule_user: {e}")

def cancel_user(number):
    schedule.clear(number)
    if number in schedules:
        del schedules[number]
    print(f"[CANCEL] Cleared schedule for {number}")

def run_job(number):
    try:
        now = datetime.now()
        if number not in schedules:
            print(f"[SKIP] No config for {number}")
            return

        config = schedules[number]
        start, end = config["start_date"], config["end_date"]
        print(f"[JOB-CHECK] {number} | Now: {now.date()} | Start: {start}, End: {end}")

        if not (start <= now.date() <= end):
            print(f"[SKIP] {number}: Outside date range.")
            return

        print(f"[JOB-EXECUTE] {number} at {now.strftime('%H:%M')}")
        path = take_screenshot(config["sheet_url"], config["crop"])
        send_whatsapp_image(number, path)
        print(f"[JOB-RUNNER] Success for {number}")

        # Auto-remove schedule after last day
        if now.date() == end:
            cancel_user(number)
    except Exception as e:
        print(f"[ERROR] run_job: {e}")

def run_loop():
    print("[SCHEDULER] Loop started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
