import datetime
import time
import threading

from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

schedules = {}

def schedule_user(sheet_url, number, times, crop_box, start_date, end_date):
    schedules[number] = {
        'sheet_url': sheet_url,
        'times': times,
        'crop_box': crop_box,
        'start_date': start_date,
        'end_date': end_date
    }
    print(f"[SCHEDULE] Scheduled {number} at {times} daily.")

def cancel_schedule(number):
    if number in schedules:
        del schedules[number]
        print(f"[CANCEL] Schedule for {number} cancelled.")

def run_loop():
    print("[SCHEDULER] Started loop.")
    while True:
        now = datetime.datetime.now()
        now_str = now.strftime("%H:%M")
        today_str = now.strftime("%Y-%m-%d")

        for number, info in list(schedules.items()):
            start = datetime.datetime.strptime(info['start_date'], "%Y-%m-%d").date()
            end = datetime.datetime.strptime(info['end_date'], "%Y-%m-%d").date()
            today = datetime.date.today()

            if today < start or today > end:
                if today > end:
                    print(f"[AUTO-DISABLE] End date passed. Removing {number}")
                    del schedules[number]
                continue

            if now_str in info['times']:
                print(f"[TRIGGER] Sending screenshot to {number}")
                image_path = take_screenshot(info['sheet_url'], info['crop_box'])
                send_whatsapp_image(number, image_path)

        time.sleep(1)
