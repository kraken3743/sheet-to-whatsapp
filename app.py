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
    try:
        data = request.form
        sheet_url = data['sheet_url']
        number = data['whatsapp_number']
        start_date = data['start_date']
        times = data['times'].split(',')
        num_days = int(data.get('num_days', 1))

        crop_box = (
            int(data.get("crop_left", 20)),
            int(data.get("crop_top", 130)),
            int(data.get("crop_right", 1000)),
            int(data.get("crop_bottom", 900))
        )

        print(f"[REGISTER] Received: sheet={sheet_url}, number={number}, date={start_date}, times={times}, days={num_days}, crop={crop_box}")

        # Pass everything to scheduler
        schedule_user(sheet_url, number, times, start_date, num_days, crop_box)

        return "Scheduled successfully!"

    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return f"Failed to schedule: {str(e)}", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    try:
        number = request.form.get("whatsapp_number")
        from scheduler import cancel_user
        cancel_user(number)
        return "Schedule cancelled!"
    except Exception as e:
        print(f"[ERROR] in /cancel: {e}")
        return f"Failed to cancel: {str(e)}", 500

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
