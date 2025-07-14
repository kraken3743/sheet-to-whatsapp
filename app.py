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
        time_str = data['time'].strip()

        crop_box = (
            int(data['crop_left']),
            int(data['crop_top']),
            int(data['crop_right']),
            int(data['crop_bottom'])
        )

        print(f"[REGISTER] {number} for {time_str} | Crop: {crop_box}")
        schedule_user(sheet_url, number, time_str, crop_box)
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
