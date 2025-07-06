import undetected_chromedriver as uc
from PIL import Image
import time
import os

def take_screenshot(sheet_url):
    print("[SCREENSHOT] Launching Chrome headless browser...")
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1600")

        #Correct binary path for Railway
        options.binary_location = "/usr/bin/chromium"

        driver = uc.Chrome(options=options)
        driver.get(sheet_url)
        time.sleep(7)

        full = "full_sheet.png"
        driver.save_screenshot(full)
        driver.quit()
        print(f"[SCREENSHOT] Full page saved to {full}")

        image = Image.open(full)
        crop_box = (20, 130, 1000, 900)  # Adjusted crop box
        cropped = image.crop(crop_box)
        cropped.save("sheet.png")
        print(f"[SCREENSHOT] Cropped screenshot saved to sheet.png")
        return "sheet.png"
    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
