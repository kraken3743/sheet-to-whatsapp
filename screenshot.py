import undetected_chromedriver as uc
from PIL import Image
import time

def take_screenshot(sheet_url):
    print("[SCREENSHOT] Launching Chrome headless browser...")
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1600")  # Match old working height
        options.add_argument("--force-device-scale-factor=0.75")  # Match zoom of old version

        driver = uc.Chrome(
            options=options,
            browser_executable_path="/usr/bin/chromium"
        )

        driver.get(sheet_url)
        print("[SCREENSHOT] Waiting for sheet to load...")
        time.sleep(7)

        # Scroll and try to hide tabs if needed
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Try to hide sheet tabs
        try:
            driver.execute_script("""
                const tabs = document.querySelector('[aria-label="Sheet Tabs"]');
                if (tabs) tabs.style.display = 'none';
            """)
            print("[SCREENSHOT] Attempted to hide sheet tabs.")
        except Exception as e:
            print(f"[WARN] Could not hide tabs: {e}")

        # Save screenshot
        screenshot_path = "full_sheet.png"
        driver.save_screenshot(screenshot_path)
        print(f"[SCREENSHOT] Full page saved to {screenshot_path}")
        driver.quit()

        # Crop using the working crop box from your first code
        image = Image.open(screenshot_path)
        crop_box = (20, 130, 1000, 900)  # same as old working setup
        cropped_image = image.crop(crop_box)

        cropped_image_path = "sheet.png"
        cropped_image.save(cropped_image_path)
        print(f"[SCREENSHOT] Cropped screenshot saved to {cropped_image_path}")

        return cropped_image_path

    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
