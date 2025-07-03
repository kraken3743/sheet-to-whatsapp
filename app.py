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
        times = data['times'].split(',')
        print(f"[REGISTER] Received: {sheet_url}, {number}, {times}")
        schedule_user(sheet_url, number, times)
        return "Scheduled successfully!"
    except Exception as e:
        print(f"[ERROR] in /register: {e}")
        return "Failed to schedule.", 500

# ✅ Start the scheduler thread immediately — no matter what
threading.Thread(target=run_loop, daemon=True).start()

# Start the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
