from flask import Blueprint, request, jsonify
import logging
from flask_cors import CORS
from .logic.bot import run_meeting_bot, generate_summary_with_gemini  # Import the new summary function

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Blueprint
main = Blueprint("main", __name__)

# Enable CORS for this blueprint
CORS(main)

@main.route("/transcribe", methods=["POST"])
def transcribe_meeting():
    data = request.get_json()
    meeting_url = data.get("meeting_url")

    if not meeting_url:
        logging.error("Missing meeting URL")
        return jsonify({"error": "Missing meeting URL"}), 400

    try:
        logging.info(f"Starting transcription for meeting URL: {meeting_url}")
        
        # Run the bot to get the transcript and summary
        result = run_meeting_bot(meeting_url)
        
        # Extract the transcript and summary from the result
        transcript = result["transcript"]
        summary = result["summary"]
        chart_url = result["chart_url"]  # Assuming this is returned as well
        
        logging.info("Transcription and summary generation successful.")
        
        # Return the transcript and summary
        return jsonify({
            "transcript": transcript,
            "summary": summary,
            "chart_url": chart_url
        }), 200

    except Exception as e:
        logging.error(f"Error during transcription or summary generation: {str(e)}")
        return jsonify({"error": str(e)}), 500
