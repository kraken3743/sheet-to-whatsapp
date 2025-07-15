from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time

def take_screenshot(sheet_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1600")
    options.binary_location = "/usr/bin/chromium"  # Update if needed

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(sheet_url)
    time.sleep(7)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    screenshot_path = "sheet.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    return screenshot_path
