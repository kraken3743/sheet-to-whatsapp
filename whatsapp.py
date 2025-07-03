import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def upload_image_to_imgbb(image_path):
    try:
        with open(image_path, "rb") as f:
            res = requests.post(
                "https://api.imgbb.com/1/upload",
                data={"key": os.getenv("IMGBB_API_KEY")},
                files={"image": f}
            )
        image_url = res.json()["data"]["url"]
        print(f"[UPLOAD] Uploaded to imgbb: {image_url}")
        return image_url
    except Exception as e:
        print(f"[ERROR] Upload to imgbb failed: {e}")
        return None

def send_whatsapp_image(to_number, image_path):
    if not to_number.startswith("whatsapp:"):
        to_number = "whatsapp:" + to_number

    image_url = upload_image_to_imgbb(image_path)
    if not image_url:
        print("[ERROR] No image URL. Aborting send.")
        return

    try:
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
        message = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP"),
            to=to_number,
            body="Here is your updated Google Sheet 📊",
            media_url=[image_url]
        )
        print(f"[WHATSAPP] Sent to {to_number} | SID: {message.sid}")
    except Exception as e:
        print(f"[ERROR] Twilio send failed: {e}")
