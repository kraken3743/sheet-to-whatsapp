from flask import Flask, request, render_template
from scheduler import schedule_user, cancel_schedule, run_loop
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
        times = data['times'].split(',')
        start_date = data['start_date']
        end_date = data['end_date']
        crop_left = int(data['crop_left'])
        crop_top = int(data['crop_top'])
        crop_right = int(data['crop_right'])
        crop_bottom = int(data['crop_bottom'])

        crop_box = (crop_left, crop_top, crop_right, crop_bottom)

        print(f"[REGISTER] Scheduled for {number} at {times}")
        schedule_user(sheet_url, number, times, crop_box, start_date, end_date)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    try:
        number = request.form['whatsapp_number']
        cancel_schedule(number)
        return "Schedule cancelled."
    except Exception as e:
        print(f"[ERROR] in /cancel: {e}")
        return "Failed to cancel.", 500


# Always run scheduler thread, even in Railway
scheduler_thread = threading.Thread(target=run_loop, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
