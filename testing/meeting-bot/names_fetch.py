from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

MEETING_URL = "https://meet.google.com/xof-ezmk-cpy"  # Replace with your test meeting

def join_meeting_and_get_participants():
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Disable headless for debugging
    options.add_argument("--disable-gpu")

    # Use your Edge profile (must be logged in to Google account)
    options.add_argument("user-data-dir=C:/Users/super/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Profile 3")

    service = Service("C:/Users/super/AppData/Local/Microsoft/Microsoft Edge Developer/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    driver.get(MEETING_URL)
    print("🔗 Opening meeting...")
    time.sleep(7)

    try:
        mic_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='microphone']")
        cam_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='camera']")
        if mic_button.get_attribute("aria-pressed") != "false":
            mic_button.click()
            print("🎙️ Mic turned off.")
        if cam_button.get_attribute("aria-pressed") != "false":
            cam_button.click()
            print("📷 Camera turned off.")
    except Exception as e:
        print("⚠️ Could not toggle mic/camera:", e)

    time.sleep(2)

    try:
        join_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_btn.click()
        print("✅ Joined the meeting!")
    except Exception as e:
        print("⚠️ Could not click 'Join now':", e)

    time.sleep(8)

    try:
        print("👥 Trying to open participant panel...")

        participants_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'People')]")
        driver.execute_script("arguments[0].click();", participants_button)

        # Wait for participant list to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'notranslate')]"))
        )

        print("🔍 Looking for participant name elements...")

        fallback_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'notranslate')]")
        names = [el.text.strip() for el in fallback_elements if el.text.strip()]

        # Optional filtering
        names = [name for name in names if name.lower() not in ["meeting room", "your presentation"]]

        print(f"🧾 Found {len(names)} participant names:")
        for name in names:
            print(f" - {name}")

        return names

    except Exception as e:
        print("⚠️ Could not fetch participants:", e)
        return []

    finally:
        time.sleep(5)
        driver.quit()
        print("👋 Meeting ended.")

if __name__ == "__main__":
    join_meeting_and_get_participants()
