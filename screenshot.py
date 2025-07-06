import undetected_chromedriver as uc
from PIL import Image
import time
import os

def take_screenshot(sheet_url):
    print("[SCREENSHOT] Launching Chrome headless browser...")
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,3000")
        options.add_argument("--force-device-scale-factor=0.67")

        # Do NOT use options.binary_location here
        # Instead, pass it explicitly below ↓↓↓
        driver = uc.Chrome(
            options=options,
            browser_executable_path="/usr/bin/chromium"  # ✅ Required on Railway
        )

        driver.get(sheet_url)
        time.sleep(8)

        # Hide sheet tabs
        driver.execute_script("""
            const tabs = document.querySelector('[aria-label="Sheet Tabs"]');
            if (tabs) tabs.style.display = "none";
        """)

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        full = "full_sheet.png"
        driver.save_screenshot(full)
        driver.quit()
        print(f"[SCREENSHOT] Full page saved to {full}")

        image = Image.open(full)
        crop_box = (20, 130, 1150, 1520)  # Adjust as needed
        cropped = image.crop(crop_box)
        cropped.save("sheet.png")
        print("[SCREENSHOT] Cropped screenshot saved to sheet.png")

        return "sheet.png"

    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
