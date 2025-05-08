# cromebottest.py
# Licensed under AGPL-3.0 by zsuperz
# Contact zsupercodez@gmail.com for commercial licensing options




# this is for crome brower but the all the crome browser needs to be closed to make it work

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

MEETING_URL = "https://meet.google.com/syr-dnro-shq"

def join_meeting_logged_in():
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")   # 👈 Add this line

    # ✅ Correct paths
    options.add_argument("user-data-dir=C:/Users/super/AppData/Local/Google/Chrome/User Data")
    options.add_argument("profile-directory=Profile 18")

    driver = webdriver.Chrome(options=options)
    driver.get(MEETING_URL)

    print("Opening meeting...")
    time.sleep(10)

    try:
        mic_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='microphone']")
        cam_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='camera']")
        mic_button.click()
        cam_button.click()
        print("Mic and camera turned off.")
    except:
        print("Mic/Cam toggle not found (may already be off).")

    time.sleep(2)

    try:
        join_now_button = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_now_button.click()
        print("Joined meeting!")
    except:
        print("Could not find 'Join now' button. Maybe already in?")

    time.sleep(60)

    print("Leaving meeting...")
    driver.quit()

if __name__ == "__main__":
    join_meeting_logged_in()
