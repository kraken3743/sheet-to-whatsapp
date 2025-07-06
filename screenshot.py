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
        options.add_argument("--window-size=1920,3000")  # ↑ Taller window
        options.add_argument("--force-device-scale-factor=0.67")  # Zoom out slightly

        driver = uc.Chrome(
            options=options,
            browser_executable_path="/usr/bin/chromium"  # Required in Railway/Render
        )

        driver.get(sheet_url)
        time.sleep(7)

        # Hide sheet tabs before screenshot
        try:
            driver.execute_script("""
                const tabs = document.querySelector('[aria-label="Sheet Tabs"]');
                if (tabs) tabs.style.display = "none";
            """)
            print("[SCREENSHOT] Sheet tabs hidden.")
        except Exception as e:
            print(f"[WARN] Couldn't hide sheet tabs: {e}")

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        full = "full_sheet.png"
        driver.save_screenshot(full)
        driver.quit()
        print(f"[SCREENSHOT] Full page saved to {full}")

        # Crop to match A1:J32
        image = Image.open(full)

        # Adjust values after checking visually
        crop_box = (20, 130, 1180, 1350)  # left, top, right, bottom
        cropped = image.crop(crop_box)
        cropped.save("sheet.png")
        print("[SCREENSHOT] Cropped screenshot saved to sheet.png")

        return "sheet.png"

    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None
