from flask import Flask, request, render_template
from scheduler import schedule_user, run_loop, cancel_user
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
        start_date = data['start_date']
        times = [t.strip() for t in data['times'].split(',')]
        num_days = int(data['num_days'])
        crop_left = int(data.get('crop_left', 20))
        crop_top = int(data.get('crop_top', 130))
        crop_right = int(data.get('crop_right', 1000))
        crop_bottom = int(data.get('crop_bottom', 900))
        auto_disable = data.get('auto_disable') == 'on'

        crop_box = (crop_left, crop_top, crop_right, crop_bottom)
        print(f"[REGISTER] {number}, Times: {times}, Start: {start_date}, Days: {num_days}, Crop: {crop_box}, Auto-disable: {auto_disable}")

        schedule_user(sheet_url, number, times, start_date, num_days, crop_box, auto_disable)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    number = request.form.get("whatsapp_number")
    if number:
        cancel_user(number)
        return f"Schedule cancelled for {number}"
    else:
        return "Missing number", 400

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
