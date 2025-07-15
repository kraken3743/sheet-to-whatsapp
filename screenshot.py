from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.add_argument("--force-device-scale-factor=0.75")
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(sheet_url)
    time.sleep(8)  # wait for page to fully load
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    full_path = "full.png"
    driver.save_screenshot(full_path)
    driver.quit()

    image = Image.open(full_path)
    cropped = image.crop(crop_box)
    out_path = "sheet.png"
    cropped.save(out_path)
    return out_path
