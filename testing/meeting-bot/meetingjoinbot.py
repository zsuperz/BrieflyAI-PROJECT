from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

MEETING_URL = "https://meet.google.com/jei-asbk-omq"

def join_meeting_logged_in():
    options = Options()

    # Add arguments to disable camera/mic prompts
    options.add_argument("--use-fake-ui-for-media-stream")  # Disable camera/mic prompts
    options.add_argument("--disable-infobars")  # Disable "Chrome is being controlled" message
    options.add_argument("--start-maximized")  # Start in maximized window (not necessary for headless mode)
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--no-sandbox")  # Run in a sandboxed environment
    options.add_argument("--disable-dev-shm-usage")  # Prevents crash due to limited resources in certain environments
    
    # Headless mode (without GUI)
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional)

    # Path to your Edge user data directory
    options.add_argument("user-data-dir=C:/Users/super/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Profile 3")  # Use the desired profile

    # Set path to the msedgedriver executable using Service
    service = Service(executable_path="C:/Users/super/AppData/Local/Microsoft/Microsoft Edge Developer/msedgedriver.exe")

    # Create a new Edge driver instance with the Service and options
    driver = webdriver.Edge(service=service, options=options)
    driver.get(MEETING_URL)

    print("Opening meeting...")
    time.sleep(5)  # Increased sleep time for loading page and meeting UI

    try:
        # Wait for the mic and camera buttons to load, and mute them
        mic_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='microphone']")
        cam_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='camera']")

        # Mute mic before joining the meeting
        if mic_button.get_attribute("aria-pressed") == "false":
            print("Mic is already muted.")
        else:
            mic_button.click()
            print("Mic turned off.")

        # Mute camera before joining the meeting
        if cam_button.get_attribute("aria-pressed") == "false":
            print("Camera is already off.")
        else:
            cam_button.click()
            print("Camera turned off.")
    except Exception as e:
        print(f"Error with mic/camera toggle: {str(e)}")

    time.sleep(2)  # Allow the mute actions to take effect

    try:
        # Click "Join now"
        join_now_button = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_now_button.click()
        print("Joined meeting!")
    except Exception as e:
        print(f"Could not find 'Join now' button. Error: {str(e)}")

    time.sleep(60)  # Stay in the meeting for 60 seconds

    print("Leaving meeting...")
    driver.quit()

if __name__ == "__main__":
    join_meeting_logged_in()
