from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os

def take_screenshot(sheet_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.add_argument("--force-device-scale-factor=0.75")
    options.binary_location = "/usr/bin/chromium"  # Use Chromium path in Railway

    driver = webdriver.Chrome(
        executable_path="/usr/bin/chromedriver",  # Use preinstalled chromedriver
        options=options
    )

    driver.get(sheet_url)
    print("[SCREENSHOT] Waiting for sheet to load...")
    time.sleep(7)

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    screenshot_path = "full_sheet.png"
    driver.save_screenshot(screenshot_path)
    print(f"[SCREENSHOT] Full page saved to {screenshot_path}")
    driver.quit()

    # Crop only the area from A1 to J31
    image = Image.open(screenshot_path)
    crop_box = (20, 130, 1000, 900)
    cropped_image = image.crop(crop_box)
    cropped_image_path = "sheet.png"
    cropped_image.save(cropped_image_path)
    print(f"[SCREENSHOT] Cropped screenshot saved to {cropped_image_path}")

    return cropped_image_path
