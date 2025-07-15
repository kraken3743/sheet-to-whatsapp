from flask import Flask, request, render_template
from scheduler import schedule_user, run_scheduler
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    number = data['whatsapp_number']
    times = [t.strip() for t in data['times'].split(',') if t.strip()]
    crop_box = (
        int(data['crop_left']),
        int(data['crop_top']),
        int(data['crop_right']),
        int(data['crop_bottom'])
    )
    custom_url = data.get('custom_url', '').strip() or None

    print(f"[REGISTER] {number} at {times}, custom_url={custom_url}, crop={crop_box}")
    schedule_user(number, times, crop_box, custom_url)
    return "Scheduled successfully!"

@app.route('/cancel', methods=['POST'])
def cancel():
    number = request.form['whatsapp_number']
    from scheduler import cancel_user
    cancel_user(number)
    return "Schedule cancelled."

if __name__ == '__main__':
    threading.Thread(target=run_scheduler, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
