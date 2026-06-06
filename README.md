# 🩺 SehatSaathi — Smart Health Companion for Elders

> **SehatSaathi** (सेहत साथी) is an AI-powered desktop application designed to assist elderly individuals with medicine reminders, caretaker monitoring, voice guidance, and medicine verification through computer vision.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 About the Project

SehatSaathi is built with the elderly in mind — especially those who live alone or with limited support. The app provides:

- Voice-guided reminders in **Hindi & English**
- A **Caretaker Dashboard** to monitor medicine intake
- **Computer vision** to verify if the correct medicine was taken
- Smart **alert escalation** when doses are missed
- Analytics to track health patterns over time

---

## ✨ Features

| Feature | Description |
|---|---|
| 👵 Elder Mode | Simple, voice-guided UI for seniors |
| 🧑‍⚕️ Caretaker Dashboard | Monitor elder's medicine schedule and history |
| 🔔 Smart Reminders | Auto-repeating reminders with escalation |
| 🗣️ Voice Guidance | Hindi & English TTS using pyttsx3 / gTTS |
| 🎙️ Speech Input | Voice commands via SpeechRecognition |
| 📸 Medicine Verification | OpenCV-based image comparison to confirm correct medicine |
| 📊 Analytics | Graphs and patterns for missed/taken doses |
| 🌐 Multilingual | Supports English and Hindi interface |
| 🚨 Alert System | Caretaker gets notified after 3 missed doses |
| 🗄️ MySQL Database | Persistent storage for users, medicines, and logs |

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **GUI:** Tkinter (ttk)
- **Database:** MySQL (`mysql-connector-python`)
- **Computer Vision:** OpenCV (`opencv-python`), Pillow
- **Voice (TTS):** pyttsx3, gTTS
- **Voice (STT):** SpeechRecognition
- **Audio Playback:** Windows MCI / sounddevice
- **Data & Analytics:** pandas, matplotlib, numpy

---

## 📁 Project Structure

```
SehatSaathi/
│
├── main.py                  # App entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
│
├── ui/                      # All UI screens
│   ├── login.py             # Login & role selection
│   ├── elder_screen.py      # Elder-facing interface
│   ├── caretaker_dashboard.py  # Caretaker panel
│   ├── screens.py           # Screen helpers
│   ├── state.py             # Global app state
│   ├── theme.py             # UI theme & styling
│   ├── common.py            # Shared UI components
│   └── i18n.py              # Translations (EN/HI)
│
├── voice/
│   ├── tts.py               # Text-to-Speech (Hindi & English)
│   └── stt.py               # Speech-to-Text input
│
├── vision/
│   ├── camera.py            # Camera capture
│   ├── detection.py         # Medicine image comparison
│   └── verify_ui.py         # Verification UI
│
├── core/
│   └── reminder.py          # Reminder scheduling engine
│
├── database/
│   ├── db.py                # MySQL connection
│   └── models.py            # DB table operations
│
├── alerts/
│   └── notify.py            # Alert & escalation logic
│
├── analytics/
│   ├── graphs.py            # Matplotlib charts
│   └── patterns.py          # Dose pattern analysis
│
├── data/
│   └── logs.csv             # Local CSV activity logs
│
└── assets/
    ├── images/
    │   ├── medicines/       # Reference medicine images
    │   └── captures/        # Camera captured images
    └── sounds/              # Alert sounds
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- MySQL Server running locally
- Webcam (for medicine verification)
- Microphone (for voice input)

### 1. Clone the Repository

```bash
git clone https://github.com/Sharyu27/SehatSaathi.git
cd SehatSaathi
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE medicine_db;
```

Then update your credentials in `config.py`:

```python
MYSQL_HOST     = "localhost"
MYSQL_USER     = "root"
MYSQL_PASSWORD = "your_password_here"
MYSQL_DATABASE = "medicine_db"
```

### 4. Run the App

```bash
python main.py
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
LANGUAGE         = "english"   # "english" or "hindi"
USER_NAME        = "Aaji"      # Elder's name
REMINDER_INTERVAL = 5          # Minutes between reminders
MAX_REMINDERS    = 3           # Max reminders before escalation
ALERT_THRESHOLD  = 3           # Missed doses before caretaker alert
VOICE_TYPE       = "female"
SPEECH_SPEED     = 150
```

---

## 🖥️ Usage

### Login Screen
- **Elder Mode** → Simple voice-guided interface
- **Caretaker Login** → Admin panel (default: `admin` / `1234`)

### Caretaker Dashboard
- Add/remove medicines and schedules
- View dose history and analytics
- Monitor alerts and missed doses

### Elder Screen
- Receive voice reminders
- Confirm medicine intake
- Camera verification of correct medicine

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute with attribution.

---

## 👨‍💻 Authors

- **Sharyu27** — [GitHub](https://github.com/Sharyu27)

---

> Made with ❤️ for elderly care — *"Sehat ka Saathi, Har Pal Saath"*
