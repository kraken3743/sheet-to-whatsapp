from flask import Flask, request, render_template
from scheduler import schedule_user, cancel_user, run_loop
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

        crop_box = (
            int(data.get("crop_left", 20)),
            int(data.get("crop_top", 130)),
            int(data.get("crop_right", 1000)),
            int(data.get("crop_bottom", 900))
        )

        num_days = int(data.get("num_days", 30))
        print(f"[REGISTER] {sheet_url}, {number}, {times}, crop: {crop_box}, days: {num_days}")

        schedule_user(sheet_url, number, times, num_days, crop_box)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    try:
        number = request.form['whatsapp_number']
        cancel_user(number)
        return "Cancelled successfully!"
    except Exception as e:
        print(f"[ERROR] in /cancel: {e}")
        return "Failed to cancel.", 500

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
