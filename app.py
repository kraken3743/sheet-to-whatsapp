from flask import Flask, request, render_template
import threading
import os
from scheduler import schedule_user, run_loop
from whatsapp import send_whatsapp_image
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", current_date=datetime.utcnow().date())

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.form
        sheet_url = data['sheet_url']
        number = data['whatsapp_number']
        time_str = data['time']
        crop_box = (
            int(data['crop_left']),
            int(data['crop_top']),
            int(data['crop_right']),
            int(data['crop_bottom'])
        )

        schedule_user(sheet_url, number, time_str, crop_box)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] /register failed: {e}")
        return "Failed to schedule.", 500

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
