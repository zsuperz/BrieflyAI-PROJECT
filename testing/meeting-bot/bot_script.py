import subprocess
import time
import whisper
import sys
import os
import matplotlib.pyplot as plt
from collections import Counter
import re

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

MEETING_URL = "https://meet.google.com/jei-asbk-omq"
OUTPUT_AUDIO = "meeting_audio.wav"
OUTPUT_TRANSCRIPT = "meeting_transcript.txt"

def start_audio_recording():
    print("Starting FFmpeg audio recording...")
    return subprocess.Popen([
        "ffmpeg",
        "-y",  # Overwrite output file
        "-f", "dshow",
        "-i", 'audio=Stereo Mix (Realtek(R) Audio)',  # Use virtual audio cable
        OUTPUT_AUDIO
    ])

def stop_audio_recording(process):
    print("Stopping audio recording...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("Audio recording saved.")

def transcribe_audio(file_path):
    print("Transcribing audio with Whisper...")
    model = whisper.load_model("medium")  # Can be changed to "small" or "large"
    result = model.transcribe(file_path)

    text = result["text"]

    with open(OUTPUT_TRANSCRIPT, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Transcript saved to {OUTPUT_TRANSCRIPT}")

    # ---- 📊 WORD FREQUENCY VISUALIZATION ----
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    most_common = word_counts.most_common(10)

    if most_common:
        labels, counts = zip(*most_common)
        plt.figure(figsize=(10, 6))
        plt.bar(labels, counts, color='skyblue')
        plt.title("Top 10 Most Frequent Words in Meeting Transcript")
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("word_frequency.png")
        plt.show()
        print("Word frequency chart saved as word_frequency.png")
    else:
        print("No words found in transcription.")

    return text

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

        if mic_button.get_attribute("aria-pressed") != "false":
            mic_button.click()
            print("Mic turned off.")

        if cam_button.get_attribute("aria-pressed") != "false":
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

    recording_process = start_audio_recording()

    try:
        time.sleep(60)  # Stay in the meeting for 60 seconds
    finally:
        stop_audio_recording(recording_process)
        driver.quit()
        print("Left meeting.")
        transcribe_audio(OUTPUT_AUDIO)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        manual_audio_path = sys.argv[1]
        if os.path.exists(manual_audio_path):
            print(f"Transcribing file: {manual_audio_path}")
            transcribe_audio(manual_audio_path)
        else:
            print(f"File not found: {manual_audio_path}")
    else:
        join_meeting_logged_in()
