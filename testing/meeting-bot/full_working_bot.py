import subprocess
import time
import whisper
import sys
import os
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from pyannote.audio import Pipeline

# CONFIG
MEETING_URL = "https://meet.google.com/wxw-jhmd-qse"
OUTPUT_AUDIO = "meeting_audio.wav"
OUTPUT_TRANSCRIPT = "meeting_transcript.txt"

# Initialize speaker diarization pipeline (no token needed for v3.1)
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")

def start_audio_recording():
    print("Starting FFmpeg audio recording...")
    return subprocess.Popen([
        "ffmpeg",
        "-y",  # Overwrite output file
        "-f", "dshow",
        "-i", 'audio=Stereo Mix (Realtek(R) Audio)',
        OUTPUT_AUDIO
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_audio_recording(process):
    print("Stopping audio recording...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("Audio recording saved.")

def diarize_and_transcribe(file_path):
    print("Running speaker diarization...")
    diarization = pipeline(file_path)

    print("Running Whisper transcription...")
    model = whisper.load_model("medium")
    whisper_result = model.transcribe(file_path, verbose=False)

    # Build speaker timeline
    segments_with_speakers = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        segments_with_speakers.append((segment.start, segment.end, speaker))

    # Function to find speaker
    def get_speaker_label(timestamp):
        for start, end, speaker in segments_with_speakers:
            if start <= timestamp <= end:
                return speaker
        return "Unknown"

    # Match Whisper segments with speaker labels
    combined_output = []
    for segment in whisper_result['segments']:
        start = segment['start']
        speaker = get_speaker_label(start)
        combined_output.append({
            "timestamp": str(timedelta(seconds=int(start))),
            "speaker": speaker,
            "text": segment['text']
        })

    # Save and print transcript
    with open(OUTPUT_TRANSCRIPT, "w", encoding="utf-8") as f:
        for entry in combined_output:
            line = f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\n"
            f.write(line)
            print(line, end="")

    print(f"\nTranscript with speaker labels saved to {OUTPUT_TRANSCRIPT}")

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

    # Start recording
    recording_process = start_audio_recording()

    try:
        time.sleep(100)  # Stay in the meeting for 60 seconds
    finally:
        stop_audio_recording(recording_process)
        driver.quit()
        print("Left meeting.")
        diarize_and_transcribe(OUTPUT_AUDIO)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        manual_audio_path = sys.argv[1]
        if os.path.exists(manual_audio_path):
            print(f"Processing file: {manual_audio_path}")
            diarize_and_transcribe(manual_audio_path)
        else:
            print(f"File not found: {manual_audio_path}")
    else:
        join_meeting_logged_in()
