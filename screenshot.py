from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url, crop_box=(30, 165, 1650, 1250)):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.add_argument("--force-device-scale-factor=0.75")
    options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

    driver.get(sheet_url)
