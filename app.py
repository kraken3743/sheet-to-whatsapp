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
        schedule_user(data)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] /register: {e}")
        return "Failed to schedule.", 500

@app.route('/cancel', methods=['POST'])
def cancel():
    try:
        number = request.form["whatsapp_number"]
        cancel_user(number)
        return "Cancelled successfully!"
    except Exception as e:
        print(f"[ERROR] /cancel: {e}")
        return "Failed to cancel.", 500

if __name__ == '__main__':
    threading.Thread(target=run_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
