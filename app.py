from flask import Flask, render_template, request
from scheduler import schedule_user, run_loop
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        number = request.form['whatsapp_number']
        times = [t.strip() for t in request.form['times'].split(',')]
        custom_url = request.form.get('custom_sheet_url', '').strip()

        crop_box = (
            int(request.form['crop_left']),
            int(request.form['crop_top']),
            int(request.form['crop_right']),
            int(request.form['crop_bottom'])
        )

        schedule_user(number, times, crop_box, custom_url)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] register: {e}")
        return "Failed to schedule.", 500

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
