import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def upload_image_to_imgbb(image_path):
    with open(image_path, "rb") as f:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": os.getenv("IMGBB_API_KEY")},
            files={"image": f}
        )
    return res.json()["data"]["url"]

def send_whatsapp_image(to_number, image_path):
    if not to_number.startswith("whatsapp:"):
        to_number = "whatsapp:" + to_number
    try:
        image_url = upload_image_to_imgbb(image_path)
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
        message = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP"),
            to=to_number,
            body="📊 Your scheduled sheet update.",
            media_url=[image_url]
        )
        print(f"[WHATSAPP] Sent to {to_number} | SID: {message.sid}")
    except Exception as e:
        print(f"[ERROR] Twilio failed: {e}")
