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
        start_date = data['start_date']
        end_date = data['end_date']
        times_raw = data['times'].split(',')
        times = []

        for t in times_raw:
            t = t.strip().upper()
            dt_obj = datetime.strptime(t, "%I:%M %p")
            times.append(dt_obj.strftime("%H:%M"))

        crop_box = (
            int(data['crop_left']),
            int(data['crop_top']),
            int(data['crop_right']),
            int(data['crop_bottom'])
        )

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

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
