from flask import Flask, request, render_template
from scheduler import schedule_user, run_loop
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    sheet_url = data['sheet_url']
    number = data['whatsapp_number']
    times = [t.strip() for t in data['times'].split(',')]

    crop_box = (
        int(data.get('crop_left', 30)),
        int(data.get('crop_top', 150)),
        int(data.get('crop_right', 1300)),
        int(data.get('crop_bottom', 1250))
    )

    print(f"[REGISTER] Scheduling for {number} at {times} with crop {crop_box}")
    schedule_user(sheet_url, number, times, crop_box)
    return "Scheduled successfully!"

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
