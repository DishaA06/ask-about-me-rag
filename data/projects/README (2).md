# 🤖 ZBOT - Your Personal AI Sidekick

ZBOT is a smart, voice-activated AI assistant designed to simplify your digital tasks and provide conversational responses. It's lightweight, customizable, and powered by Python and NLP models.

---

## 🚀 Features

- 🗣️ Voice command recognition
- 💬 AI-powered conversations using OpenAI or local models
- 🔍 Google/web search integration
- 🗂️ Launches apps and executes system tasks
- 📰 Real-time news and weather updates
- 🎵 Media control and entertainment commands

---

## 🧰 Tech Stack

- **Language:** Python 3
- **Libraries:**
  - `speech_recognition`
  - `pyttsx3`
  - `openai` / `transformers`
  - `webbrowser`, `os`, `requests`, `datetime`
  - `wikipedia`, `newsapi-python`, etc.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/zBOT.git
cd zBOT
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python zbot.py
```

Say commands like:
- "zBot, open Chrome"
- "What’s the capital of Japan?"
- "Play chill music"
- "Who is Elon Musk?"

---

## Project Structure 📁

```text
ZBOT/
├── Main.py                    # Main execution file with threading logic
├── Requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .env                       # Environment variables (not in repo)
│
├── Frontend/                  # User Interface Components
│   ├── GUI.py                # PyQt5-based graphical interface
│   ├── Files/                # Temporary data files
│   │   ├── Mic.data         # Microphone status
│   │   ├── Status.data      # Assistant status
│   │   ├── Responses.data   # Chat responses
│   │   ├── Database.data    # Processed chat logs
│   │   └── ImageGeneration.data
|   |   
│   └── Graphics/             # UI assets and images
│       ├── final.gif        # Main animation
│       ├── Mic_on.png       # Microphone icons
│       ├── Mic_off.png
│       ├── Home.png         # Navigation icons
│       ├── Chats.png
│       ├── Close.png
│       ├── Minimize.png
│       └── Maximize.png
│
├── Backend/                   # Core AI Logic
│   ├── key.env               # API keys and config
│   ├── Model.py              # Decision-making model (FirstLayerDMM)
│   ├── Chatbot.py            # Conversational AI logic
│   ├── SpeechToText.py       # Voice recognition
│   ├── TextToSpeech.py       # Voice synthesis
│   ├── RealtimeSearchEngine.py # Web search integration
│   ├── Automation.py         # System task automation
│   └── ImageGeneration.py    # AI image generation
│
└── Data/                     # Application Data
    ├── ChatLog.json          # Conversation history
    ├── Voice.html            # Web-based speech recognition
    ├── Lata_Mangeshkar4.jpg  # Sample media files
    └── applicationforasickleave.txt # Generated content samples
```

---

## 🛠 Future Enhancements

- Support for multiple languages
- Contextual memory
- Integration with smart home devices
- Offline command processing

---

## 📬 Contact

- GitHub: [DishaA06](https://github.com/DishaA06)
- LinkedIn: [disha-oza-bba48928](https://linkedin.com/in/disha-oza-bba48928a)
- Email: doza57524@gmail.com
