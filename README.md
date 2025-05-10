

---

# BrieflyAI

**BrieflyAI** is your intelligent meeting assistant — perfect for busy users who can’t attend online meetings in real-time. It sends a bot to join the meeting, records it, transcribes the audio using Whisper, and summarizes the discussion using Gemini AI, so you can catch up at your convenience.

---

## 🚀 Features

* Automatically joins online meetings via a bot
* Records audio from the meeting
* Generates transcripts using **OpenAI Whisper**
* Summarizes content using **Gemini AI**
* Full stack solution with Python backend and React.js frontend

---

## 🧠 Tech Stack

### Backend

* Python
* Flask
* Whisper (for transcription)
* Pyannote.audio (for speaker diarization)
* FFmpeg (for audio/video processing)
* Selenium (for meeting automation)
* Gemini AI (for summarization)

### Frontend

* React.js
* Axios (for API communication)
* Tailwind CSS (optional, for styling)

---

## 🛠️ Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zsuperz/BrieflyAI-PROJECT.git
   cd BrieflyAI-PROJECT
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Configure Python interpreter in VSCode:**

   Make sure VSCode is using the virtualenv as your Python interpreter. Click the Python version in the bottom bar and select the appropriate environment.

4. **Install dependencies:**

   ```bash
   pip install flask flask-cors
   pip install pyannote.audio
   pip install openai-whisper
   pip install selenium
   pip install torch torchaudio
   pip install matplotlib
   pip install python-dotenv
   ```

5. **Start the Flask development server:**

   ```bash
   flask run
   ```

---

## 🌐 Frontend Setup (React.js)

1. **Create a new React project:**

   ```bash
   npm create vite@latest my-react-app --template react
   cd my-react-app
   npm install
   ```

2. **Install necessary dependencies:**

   ```bash
   npm install axios
   npm install tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Configure Tailwind CSS:**

   * Update `tailwind.config.js`:

     ```js
     module.exports = {
       content: ["./src/**/*.{js,jsx,ts,tsx}"],
       theme: {
         extend: {},
       },
       plugins: [],
     }
     ```

   * Add Tailwind directives to `src/index.css`:

     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

4. **Build your UI components to interact with the Flask backend.**

5. **Start the React development server:**

   ```bash
   npm run dev
   ```

---

## 📝 Example Workflow

1. User is unavailable for a scheduled online meeting
2. User schedules the bot via the frontend UI
3. Backend launches an automated browser session (via Selenium) to join the meeting
4. Audio is recorded using FFmpeg
5. Transcription is handled by Whisper
6. Gemini AI generates a meeting summary
7. Transcript and summary are displayed in the user's dashboard

---

## ⚠️ Notes

* Ensure FFmpeg is installed and added to your system PATH
* Whisper and Pyannote may require model downloads on the first run
* Selenium may need a compatible WebDriver — we recommend using **Microsoft Edge WebDriver**

### 🧩 Edge Browser Setup

To automate meetings via Selenium, our system uses **Microsoft Edge**. Make sure:

* Microsoft Edge is installed
* You're logged into the Edge browser with the account that will join meetings
* The Edge WebDriver path is correctly configured

Example usage in your Python script:

```python
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium import webdriver

options = Options()
options.add_argument("user-data-dir=C:/Users/yourname/AppData/Local/Microsoft/Edge/User Data")
options.add_argument("profile-directory=Profile 1")

service = Service(executable_path="C:/Users/yourname/Drivers/msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)
```

> The bot will use your logged-in Edge browser session to access and join the meeting.

---

## 🔐 Environment Variables

Create a `.env` file in the root of your project and include the following keys:

```env
GEMINI_API_KEY=your_api_key_here
EDGE_DRIVER_PATH=C:/Users/yourname/Drivers/msedgedriver.exe
EDGE_USER_DATA_DIR=C:/Users/yourname/AppData/Local/Microsoft/Edge/User Data
EDGE_PROFILE=Profile 1
AUDIO_DEVICE_NAME=Stereo Mix (Realtek(R) Audio)
```

Then in your Python backend, load the environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH")
EDGE_USER_DATA_DIR = os.getenv("EDGE_USER_DATA_DIR")
EDGE_PROFILE = os.getenv("EDGE_PROFILE")
AUDIO_DEVICE_NAME = os.getenv("AUDIO_DEVICE_NAME")
```

---

## 📄 License

This project is licensed under the **GNU Affero General Public License (AGPL)**.

---


