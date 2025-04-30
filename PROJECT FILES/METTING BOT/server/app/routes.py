from flask import Blueprint, request, jsonify
import logging
from flask_cors import CORS  # Importing CORS
from .logic.bot import run_meeting_bot

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Blueprint
main = Blueprint("main", __name__)

# Enable CORS for this blueprint
CORS(main)  # This will enable CORS for this blueprint, you can configure it for specific domains if needed.

@main.route("/transcribe", methods=["POST"])
def transcribe_meeting():
    data = request.get_json()
    meeting_url = data.get("meeting_url")

    if not meeting_url:
        logging.error("Missing meeting URL")
        return jsonify({"error": "Missing meeting URL"}), 400

    try:
        logging.info(f"Starting transcription for meeting URL: {meeting_url}")
        transcript = run_meeting_bot(meeting_url)
        logging.info("Transcription successful.")
        return jsonify({"transcript": transcript}), 200
    except Exception as e:
        logging.error(f"Error during transcription: {str(e)}")
        return jsonify({"error": str(e)}), 500
