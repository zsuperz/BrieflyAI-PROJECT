# metting_join_record_bot.py
# Licensed under AGPL-3.0 by zsuperz
# Contact zsupercodez@gmail.com for commercial licensing options



import subprocess
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

MEETING_URL = "https://meet.google.com/jei-asbk-omq"

def start_audio_recording():
    print("Starting FFmpeg audio recording...")
    return subprocess.Popen([
        "ffmpeg",
        "-y",  # Overwrite output file if exists
        "-f", "dshow",
        "-i", 'audio=Stereo Mix (Realtek(R) Audio)',
        "meeting_audio.wav"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_audio_recording(process):
    print("Stopping audio recording...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("Audio recording saved.")

def join_meeting_logged_in():
    options = Options()

    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    options.add_argument("user-data-dir=C:/Users/super/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Profile 3")

    service = Service(executable_path="C:/Users/super/AppData/Local/Microsoft/Microsoft Edge Developer/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)
    driver.get(MEETING_URL)

    print("Opening meeting...")
    time.sleep(5)

    try:
        mic_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='microphone']")
        cam_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='camera']")

        if mic_button.get_attribute("aria-pressed") == "false":
            print("Mic is already muted.")
        else:
            mic_button.click()
            print("Mic turned off.")

        if cam_button.get_attribute("aria-pressed") == "false":
            print("Camera is already off.")
        else:
            cam_button.click()
            print("Camera turned off.")
    except Exception as e:
        print(f"Error with mic/camera toggle: {str(e)}")

    time.sleep(2)

    try:
        join_now_button = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_now_button.click()
        print("Joined meeting!")
    except Exception as e:
        print(f"Could not find 'Join now' button. Error: {str(e)}")

    # Start audio recording now
    recording_process = start_audio_recording()

    try:
        time.sleep(60)  # Stay in meeting
    finally:
        stop_audio_recording(recording_process)
        print("Leaving meeting...")
        driver.quit()

if __name__ == "__main__":
    join_meeting_logged_in()
