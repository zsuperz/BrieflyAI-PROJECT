# Licensed under AGPL-3.0 by zsuperz - Contact for commercial use

# bot.py
# Licensed under AGPL-3.0 by zsuperz
# Contact zsupercodez@gmail.com for commercial licensing options

import os
import time
import subprocess
import whisper
import matplotlib.pyplot as plt
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from pyannote.audio import Pipeline
from collections import defaultdict
import requests
import json
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Global paths
OUTPUT_AUDIO = "meeting_audio.wav"
OUTPUT_TRANSCRIPT = "meeting_transcript.txt"
SPEAKER_GRAPH_IMAGE = "speaker_chart.png"

# Load models once
print("🔄 Loading speaker diarization model...")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
print("✅ Speaker diarization model loaded.")

print("🔄 Loading Whisper transcription model...")
whisper_model = whisper.load_model("small")
print("✅ Whisper model loaded.")

def start_audio_recording():
    print("🎙️ Starting audio recording using FFmpeg...")
    audio_device = os.getenv("AUDIO_DEVICE_NAME", "Stereo Mix (Realtek(R) Audio)")
    return subprocess.Popen([
        "ffmpeg",
        "-y",
        "-f", "dshow",
        "-i", f"audio={audio_device}",
        OUTPUT_AUDIO
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_audio_recording(process):
    print("🛑 Stopping audio recording...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("✅ Audio recording complete and saved to:", OUTPUT_AUDIO)

def plot_speaker_durations(speaker_durations):
    print("📊 Generating speaker duration bar chart...")
    speakers = list(speaker_durations.keys())
    durations = [speaker_durations[s] for s in speakers]

    plt.figure(figsize=(8, 5))
    plt.bar(speakers, durations, color='skyblue')
    plt.xlabel("Speakers")
    plt.ylabel("Speaking Time (seconds)")
    plt.title("Speaking Time per Speaker")
    plt.tight_layout()
    plt.savefig(SPEAKER_GRAPH_IMAGE)
    plt.close()
    print(f"✅ Speaker duration graph saved to {SPEAKER_GRAPH_IMAGE}")

def diarize_and_transcribe(audio_path, participant_names=None):
    print("\n🔍 Starting speaker diarization...")
    diarization = pipeline(audio_path)
    print("✅ Diarization complete. Detected speaker segments:")

    segments_with_speakers = []
    speaker_durations = defaultdict(float)
    speaker_map = {}

    for segment, _, speaker in diarization.itertracks(yield_label=True):
        duration = segment.end - segment.start
        speaker_durations[speaker] += duration
        print(f"  ⏱️ {segment.start:.2f}s - {segment.end:.2f}s: {speaker}")
        segments_with_speakers.append((segment.start, segment.end, speaker))

    plot_speaker_durations(speaker_durations)

    # Assign names heuristically (if names are fewer than speakers, fallback to IDs)
    sorted_speakers = sorted(speaker_durations.items(), key=lambda x: -x[1])

    if participant_names:
        print("\n👤 Mapping speakers based on talking time:")
        for i, (speaker, _) in enumerate(sorted_speakers):
            assigned_name = participant_names[i] if i < len(participant_names) else speaker
            speaker_map[speaker] = assigned_name
            print(f"  {speaker} → {assigned_name}")
    else:
        speaker_map = {s: s for s, _ in sorted_speakers}    

    print("\n✍️ Starting Whisper transcription...")
    whisper_result = whisper_model.transcribe(audio_path, verbose=False)
    print("✅ Transcription complete. Matching segments to speakers...")

    def get_speaker_label(timestamp):
        for start, end, speaker in segments_with_speakers:
            if start - 0.5 <= timestamp <= end + 0.5:
                return speaker_map.get(speaker, speaker)
        return "Unknown"

    combined_output = []
    for segment in whisper_result['segments']:
        start = segment['start']
        speaker = get_speaker_label(start)
        timestamp = str(timedelta(seconds=int(start)))
        line = f"[{timestamp}] {speaker}: {segment['text']}"
        print(line)
        combined_output.append(line)

    with open(OUTPUT_TRANSCRIPT, "w", encoding="utf-8") as f:
        f.write("\n".join(combined_output))

    print(f"\n📄 Transcript with speaker labels saved to: {OUTPUT_TRANSCRIPT}")
    return "\n".join(combined_output)

def force_mute(driver):
    print("📵 Forcing mic and camera OFF using JavaScript...")
    try:
        driver.execute_script("""
            Array.from(document.querySelectorAll('[data-is-muted]')).forEach(el => {
                if (el.getAttribute('data-is-muted') === 'false') el.click();
            });
        """)
    except Exception as e:
        print("⚠️ JavaScript mute injection failed:", e)



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Or set directly for testing

def generate_summary_with_gemini(transcript):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # or hardcode for testing

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Summarize this meeting:\n\n{transcript}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        summary = (
            result.get("candidates", [{}])[0]
                  .get("content", {})
                  .get("parts", [{}])[0]
                  .get("text", "No summary available.")
        )
    except Exception as e:
        summary = f"⚠️ Error getting summary: {e}\nFull response:\n{response.text}"

    with open("summary_output.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    return summary







def run_meeting_bot(meeting_url):
    print(f"\n🚀 Joining meeting at: {meeting_url}")
    


def get_participant_names(driver):
    print("👥 Trying to open participant panel...")
    try:
        time.sleep(5)  # ensure we're fully in the meeting

        participants_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'People')]")
        driver.execute_script("arguments[0].click();", participants_button)

        # Wait until at least one participant shows up
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'notranslate')]"))
        )

        print("🔍 Looking for participant name elements...")
        fallback_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'notranslate')]")
        names = [el.text.strip() for el in fallback_elements if el.text.strip()]

        excluded_names = ["AI Agent", "Meeting Room", "Your presentation"]
        names = [name for name in names if name not in excluded_names]

        print(f"🧾 Found {len(names)} participant names:")
        for name in names:
            print(f" - {name}")

        return names
    except Exception as e:
        print("⚠️ Could not fetch participants:", e)
        return []





def run_meeting_bot(meeting_url):
    print(f"\n🚀 Joining meeting at: {meeting_url}")



    # Set up Edge options
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-data-dir=C:/Users/super/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Profile 3")
    
    service = Service(executable_path="C:/Users/super/AppData/Local/Microsoft/Microsoft Edge Developer/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)
    driver.get(meeting_url)

    time.sleep(5)

    # Mute mic and camera
    try:
        mic = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='microphone']")
        cam = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label*='camera']")
        if mic.get_attribute("aria-pressed") != "false":
            mic.click()
            print("🔇 Microphone muted.")
        if cam.get_attribute("aria-pressed") != "false":
            cam.click()
            print("🎥 Camera turned off.")
    except Exception as e:
        print("⚠️ Could not toggle mic/camera:", str(e))

    force_mute(driver)
    time.sleep(2)

    # ✅ Click "Join now"
    try:
        join_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Join now')]/..")
        join_btn.click()
        print("✅ Joined the meeting!")
    except Exception as e:
        print("⚠️ Could not click 'Join now':", str(e))

    # ✅ Wait and open the participant panel before recording starts
    time.sleep(5)
    participant_names = get_participant_names(driver)  # <-- Now we open panel inside this

    # ✅ Start recording AFTER participant names are loaded
    recorder = start_audio_recording()

    try:
        print("🕒 Staying in the meeting for 65 seconds...")
        time.sleep(65)  # or however long you want to record
    except Exception as e:
        print("❌ Error during meeting wait:", e)
    finally:
        stop_audio_recording(recorder)
        driver.quit()
        print("👋 Left the meeting.")


    # Transcribe & diarize with speaker name mapping
    transcript_text = diarize_and_transcribe(OUTPUT_AUDIO, participant_names)  # ✅ Pass names

    # Generate summary with Gemini
    summary = generate_summary_with_gemini(transcript_text)

    # Return result to frontend
    return {
        "transcript": transcript_text,
        "chart_url": "/chart",
        "summary": summary
    }



