from config import ALERT_THRESHOLD
from database.db import get_logs


def check_and_alert():
    data = get_logs()
    missed_count = sum(1 for d in data if d["status"] == "missed")

    if missed_count >= ALERT_THRESHOLD:
        send_alert(f"Medicine missed {missed_count} times!")


def send_alert(message):
    print("ALERT:", message)
