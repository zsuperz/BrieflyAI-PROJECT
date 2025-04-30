from app import create_app
import os
from dotenv import load_dotenv

app = create_app()



load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if __name__ == "__main__":
    app.run(debug=True)