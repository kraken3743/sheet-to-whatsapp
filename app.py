from flask import Flask, render_template, request
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
    time_str = data['time']  # format HH:MM
    crop_box = (
        int(data['crop_left']),
        int(data['crop_top']),
        int(data['crop_right']),
        int(data['crop_bottom']),
    )
    schedule_user(sheet_url, number, time_str, crop_box)
    return "Scheduled successfully!"

if __name__ == "__main__":
    threading.Thread(target=run_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
