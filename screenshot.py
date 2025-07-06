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
        options.add_argument("--window-size=1920,2200")  # Increase height
        options.add_argument("--force-device-scale-factor=0.75")  # Zoom out
        options.binary_location = "/usr/bin/chromium"  # For Railway or Linux

        driver = uc.Chrome(options=options)
        driver.get(sheet_url)
        time.sleep(5)

        # Scroll to bottom so row 32 is visible
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

        # Take full screenshot
        full = "full_sheet.png"
        driver.save_screenshot(full)
        driver.quit()
        print(f"[SCREENSHOT] Full page saved to {full}")

        # Crop only A1 to J32 from screenshot
        image = Image.open(full)
        
        # Manually tuned crop box (Left, Top, Right, Bottom) — adjust if needed
        crop_box = (40, 130, 1150, 1550)  # Slightly larger bottom
        cropped = image.crop(crop_box)
        cropped.save("sheet.png")
        print("[SCREENSHOT] Cropped screenshot saved to sheet.png")
        return "sheet.png"

    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
