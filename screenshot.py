from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box=(20, 130, 1000, 900)):
    print(f"[SCREENSHOT] Starting capture for: {sheet_url}")
    print(f"[SCREENSHOT] Crop area: {crop_box}")

    # Set Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.add_argument("--force-device-scale-factor=0.75")
    options.binary_location = "/usr/bin/chromium"

    # Launch Chrome
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(sheet_url)
        print("[SCREENSHOT] Waiting for Google Sheet to load...")
        time.sleep(7)  # Wait for Google Sheet to render

        # Scroll to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Capture full screenshot
        full_path = "full_sheet.png"
        driver.save_screenshot(full_path)
        print(f"[SCREENSHOT] Full page saved to {full_path}")

    except Exception as e:
        print(f"[ERROR] Failed to capture screenshot: {e}")
        driver.quit()
        return None

    driver.quit()

    # Crop the screenshot
    try:
        image = Image.open(full_path)
        cropped = image.crop(crop_box)
        cropped_path = "sheet.png"
        cropped.save(cropped_path)
        print(f"[SCREENSHOT] Cropped screenshot saved to {cropped_path}")
        return cropped_path
    except Exception as e:
        print(f"[ERROR] Cropping failed: {e}")
        return None
