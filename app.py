from flask import Flask, request, render_template
from scheduler import schedule_user, cancel_user, run_scheduler_loop
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        sheet_url = data['sheet_url']
        number = data['whatsapp_number']
        schedule_time = data['time']
        crop_box = (
            int(data['crop_left']),
            int(data['crop_top']),
            int(data['crop_right']),
            int(data['crop_bottom'])
        )

        print(f"[REGISTER] Scheduling {number} at {schedule_time}")
        schedule_user(sheet_url, number, schedule_time, crop_box)
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

if __name__ == '__main__':
    threading.Thread(target=run_scheduler_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
