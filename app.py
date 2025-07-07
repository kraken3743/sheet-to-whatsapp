import threading
from flask import Flask, request, render_template
from scheduler import schedule_user, cancel_user, run_loop
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
        end_date = data['end_date']
        times = [t.strip() for t in data['times'].split(',') if t.strip()]
        crop_box = (
            int(data.get('crop_left', 20)),
            int(data.get('crop_top', 130)),
            int(data.get('crop_right', 1000)),
            int(data.get('crop_bottom', 900))
        )

        schedule_user(sheet_url, number, times, start_date, end_date, crop_box)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    number = request.form['whatsapp_number']
    cancel_user(number)
    return f"Cancelled all schedules for {number}"

if __name__ == '__main__':
    print("[MAIN] Starting scheduler thread...")
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
