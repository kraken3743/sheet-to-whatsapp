from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box=(20,130,1000,900)):
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
    time.sleep(7)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    full = "full.png"
    driver.save_screenshot(full)
    driver.quit()

    img = Image.open(full)
    cropped = img.crop(crop_box)
    cropped.save("sheet.png")
    print("[SCREENSHOT] Cropped saved")
    return "sheet.png"
