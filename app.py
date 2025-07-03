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

if __name__ == '__main__':
    # START scheduler loop as background thread inside web server
    threading.Thread(target=run_loop, daemon=True).start()
    
    # Start Flask server on correct port for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
