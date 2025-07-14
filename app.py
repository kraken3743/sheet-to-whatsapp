from flask import Flask, request, render_template
from scheduler import schedule_user, cancel_user, run_loop
import threading
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", datetime=datetime)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        sheet_url = data['sheet_url']
        number = data['whatsapp_number']

        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

        times = [convert_to_24hr_format(t.strip()) for t in data['times'].split(',')]

        crop_box = (
            int(data['crop_left']),
            int(data['crop_top']),
            int(data['crop_right']),
            int(data['crop_bottom'])
        )

        print(f"[REGISTER] {number} from {start_date} to {end_date} at {times} crop={crop_box}")
        schedule_user(sheet_url, number, start_date, end_date, times, crop_box)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    try:
        number = request.form['whatsapp_number']
        cancel_user(number)
        return "Schedule canceled."
    except Exception as e:
        print(f"[ERROR] in /cancel: {e}")
        return "Failed to cancel.", 500

def convert_to_24hr_format(time_str):
    in_time = datetime.strptime(time_str, "%I:%M %p")
    return in_time.strftime("%H:%M")

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    print("[SCHEDULER] Loop started")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
