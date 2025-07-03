from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os

def take_screenshot(sheet_url):
    try:
        print("[SCREENSHOT] Launching Chrome headless browser...")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1600")

        driver = webdriver.Chrome(options=options)
        print(f"[SCREENSHOT] Navigating to: {sheet_url}")
        driver.get(sheet_url)
        time.sleep(7)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        full = "full_sheet.png"
        driver.save_screenshot(full)
        print(f"[SCREENSHOT] Full page saved to {full}")
        driver.quit()

        image = Image.open(full)
        crop_box = (70, 150, 1000, 900)  # A1:J31 (adjust if needed)
        cropped = image.crop(crop_box)
        cropped_path = "sheet.png"
        cropped.save(cropped_path)
        print(f"[SCREENSHOT] Cropped screenshot saved to {cropped_path}")

        return cropped_path

    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
