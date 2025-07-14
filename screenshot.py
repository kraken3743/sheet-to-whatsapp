from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box=(20, 130, 1000, 900)):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(sheet_url)
    time.sleep(7)
    driver.save_screenshot("full.png")
    driver.quit()

    image = Image.open("full.png")
    cropped = image.crop(crop_box)
    cropped_path = "cropped.png"
    cropped.save(cropped_path)
    return cropped_path
