# speaker_identity.py
# Licensed under AGPL-3.0 by zsuperz
# Contact zsupercodez@gmail.com for commercial licensing options

import whisper
from pyannote.audio import Pipeline
from datetime import timedelta

# Load Whisper model
whisper_model = whisper.load_model("base")

# Load the updated pyannote pipeline (no token needed for 3.1)
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")

# Path to your audio file
AUDIO_FILE = "output.wav"

# 1. Run Speaker Diarization
diarization = pipeline(AUDIO_FILE)

# 2. Run Transcription with Whisper
whisper_result = whisper_model.transcribe(AUDIO_FILE, verbose=False)

# 3. Build a timeline of who spoke when
segments_with_speakers = []
for segment, _, speaker in diarization.itertracks(yield_label=True):
    segments_with_speakers.append((segment.start, segment.end, speaker))

# 4. Function to get the speaker label based on the timestamp
def get_speaker_label(timestamp):
    for start, end, speaker in segments_with_speakers:
        if start <= timestamp <= end:
            return speaker
    return "Unknown"

# 5. Combine Whisper transcription with speaker labels
transcription_with_speaker = []
for segment in whisper_result['segments']:
    start = segment['start']
    speaker = get_speaker_label(start)
    transcription_with_speaker.append({
        "timestamp": str(timedelta(seconds=int(start))),
        "speaker": speaker,
        "text": segment['text']
    })

# 6. Print the result
for entry in transcription_with_speaker:
    print(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}")
