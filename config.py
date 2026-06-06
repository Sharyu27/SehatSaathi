# ===============================
# SehatSaathi - Configuration File
# ===============================

# -------- User Settings --------
LANGUAGE = "english"        # options: english / hindi
USER_NAME = "Aaji"          # respectful name for elder

# -------- Reminder Settings --------
REMINDER_INTERVAL = 5       # minutes between repeat reminders
MAX_REMINDERS = 3           # escalation limit

# -------- Voice Settings --------
VOICE_TYPE = "female"       # female voice for elderly
SPEECH_SPEED = 150          # speed of speaking

# -------- File Paths --------
DB_PATH = "data/medicine.db"
LOG_FILE = "data/logs.csv"
IMAGE_FOLDER = "assets/images/"

# -------- Database (MySQL) --------
# Make sure MySQL server is running and credentials are correct.
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "sharyu"
MYSQL_DATABASE = "medicine_db"

# -------- Alert Settings --------
ALERT_THRESHOLD = 3         # after 3 misses → alert caretaker

# -------- System Status --------
SYSTEM_STATUS = "active"    # active / stopped