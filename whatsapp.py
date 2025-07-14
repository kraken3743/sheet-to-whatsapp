import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def upload_image_to_imgbb(path):
    try:
        with open(path,"rb") as f:
            res = requests.post("https://api.imgbb.com/1/upload",
                                 data={"key":os.getenv("IMGBB_API_KEY")},
                                 files={"image":f})
        return res.json()["data"]["url"]
    except Exception as e:
        print(f"[ERROR] imgbb upload failed: {e}")
        return None

def send_whatsapp_image(to_num, img_path):
    if not to_num.startswith("whatsapp:"):
        to_num = "whatsapp:" + to_num

    url = upload_image_to_imgbb(img_path)
    if not url:
        print("[ERROR] upload failed — abort send")
        return

    try:
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
        msg = client.messages.create(from_=os.getenv("TWILIO_WHATSAPP"), to=to_num,
                                     body="Your scheduled Google Sheet screenshot.", media_url=[url])
        print(f"[WHATSAPP] Sent SID {msg.sid}")
    except Exception as e:
        print(f"[ERROR] Twilio failed: {e}")
