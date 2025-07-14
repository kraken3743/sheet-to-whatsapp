import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests

load_dotenv()

def upload_image_to_imgbb(image_path):
    try:
        with open(image_path, "rb") as file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                data={"key": os.getenv("IMGBB_API_KEY")},
                files={"image": file}
            )
        return response.json()["data"]["url"]
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

def send_whatsapp_image(to_number, image_path):
    if not to_number.startswith("whatsapp:"):
        to_number = "whatsapp:" + to_number

    image_url = upload_image_to_imgbb(image_path)
    if not image_url:
        print("[ERROR] Upload failed. No image sent.")
        return

    try:
        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH"))
        message = client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP"),
            to=to_number,
            body="📊 Here is your Google Sheet update!",
            media_url=[image_url]
        )
        print(f"[WHATSAPP] Sent to {to_number}")
    except Exception as e:
        print(f"[ERROR] Twilio failed: {e}")
