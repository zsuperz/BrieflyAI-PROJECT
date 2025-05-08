# whisper.py
# Licensed under AGPL-3.0 by zsuperz
# Contact zsupercodez@gmail.com for commercial licensing options
import whisper

# Load Whisper model (you can change this to "base", "small", "medium", or "large")
model = whisper.load_model("medium")

# Path to your test audio file
audio_path = "meeting_audio.wav"

# Transcribe the audio
print("Transcribing...")
result = model.transcribe(audio_path)

# Print full transcription
print("\n--- Transcription Result ---\n")
print(result["text"])
