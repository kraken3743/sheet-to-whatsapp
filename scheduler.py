import schedule
import time
import datetime
from screenshot import take_screenshot
from whatsapp import send_whatsapp_image

users = {}

def schedule_user(sheet_url, number, times, start_date, end_date, crop_box):
    users[number] = {
        "sheet_url": sheet_url,
        "times": times,
        "start_date": start_date,
        "end_date": end_date,
        "crop_box": crop_box
    }
    print(f"[SCHEDULE] Scheduled {number} at {times} daily.")

def cancel_user(number):
    if number in users:
        del users[number]
        print(f"[CANCEL] Schedule cancelled for {number}")

def run_loop():
    print("[SCHEDULER] Background loop starting...")

    while True:
        try:
            now = datetime.datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M")
            print(f"[SCHEDULER] Tick {now.strftime('%H:%M:%S')}")

            for number, user in list(users.items()):
                start = user["start_date"]
                end = user["end_date"]
                if today_str < start or today_str > end:
                    continue  # skip outside date range

                if current_time in user["times"]:
                    print(f"[SEND] Triggering for {number} at {current_time}")
                    try:
                        path = take_screenshot(user["sheet_url"], user["crop_box"])
                        send_whatsapp_image(number, path)
                    except Exception as e:
                        print(f"[ERROR] Sending failed for {number}: {e}")

            time.sleep(1)
        except Exception as e:
            print(f"[SCHEDULER ERROR] {e}")
            time.sleep(2)
