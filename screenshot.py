from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box=(30, 165, 1300, 1250)):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.binary_location = "/usr/bin/chromium"  # Adjust if needed
    service = Service("/usr/bin/chromedriver")     # Adjust if needed

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(sheet_url)
    time.sleep(7)
    driver.save_screenshot("full_sheet.png")
    driver.quit()

    image = Image.open("full_sheet.png")
    cropped = image.crop(crop_box)
    cropped_path = "sheet.png"
    cropped.save(cropped_path)
    return cropped_path
