import os
import sys
import threading
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import LANGUAGE, REMINDER_INTERVAL, USER_NAME
from database.db import get_medicines, save_log
from ui.state import AppState, ReminderPrompt
from vision.camera import capture_image
from vision.detection import compare_images
from voice.tts import speak


def _say(text_en: str, text_hi: str) -> None:
    if str(LANGUAGE).lower().startswith("hi"):
        speak(text_hi, lang="hi")
    else:
        speak(text_en, lang="en")


def _prompt_for_button_response(
    state: AppState | None,
    medicine: dict,
    stage: int,
    text_en: str,
    text_hi: str,
    timeout_seconds: float,
) -> tuple[str, str]:
    if state is None:
        time.sleep(timeout_seconds)
        return "Timeout", "No app state available"

    prompt = ReminderPrompt(
        medicine_name=str(medicine.get("name", "Medicine")),
        scheduled_time=str(medicine.get("time", "")),
        stage=stage,
        text_en=text_en,
        text_hi=text_hi,
    )
    return state.request_reminder_response(prompt, timeout_seconds)


def start_reminder_procedure(
    state: AppState | None,
    medicine: dict,
    snooze_minutes: int = 5,
    *,
    skip_camera: bool = False,
    captured_image_path: str | None = None,
) -> str:
    med_name = str(medicine.get("name", "Medicine"))
    med_time = str(medicine.get("time", ""))
    med_id = medicine.get("id")
    expected_image = (medicine.get("image") or "").strip()
    response_window = max(1, REMINDER_INTERVAL) * 60

    _say(
        f"{USER_NAME}, it's time for {med_name}. Please tap Yes, No, or Skip.",
        f"{USER_NAME}, {med_name} à¤²à¥‡à¤¨à¥‡ à¤•à¤¾ à¤¸à¤®à¤¯ à¤¹à¥ˆà¥¤ à¤•à¥ƒà¤ªà¤¯à¤¾ à¤¹à¤¾à¤, à¤¨à¤¹à¥€à¤‚, à¤¯à¤¾ à¤¸à¥à¤•à¤¿à¤ª à¤¦à¤¬à¤¾à¤à¤à¥¤",
    )

    captured = captured_image_path
    verified = False
    if expected_image and not skip_camera:
        try:
            captured = capture_image(output_dir="assets/images/captures")
            if captured:
                verified = compare_images(expected_image, captured)
        except Exception:
            verified = False

    if verified:
        save_log("taken", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes="camera_verified")
        _say("Confirmed. Good job.", "à¤ à¥€à¤• à¤¹à¥ˆ, à¤¦à¤µà¤¾ à¤²à¥€ à¤—à¤ˆà¥¤")
        return "taken"

    print(f"Waiting for Stage 1 button response for up to {max(1, REMINDER_INTERVAL)} minute(s)...")
    status, raw = _prompt_for_button_response(
        state,
        medicine,
        1,
        f"{USER_NAME}, it's time for {med_name}. Please tap Yes, No, or Skip.",
        f"{USER_NAME}, {med_name} à¤²à¥‡à¤¨à¥‡ à¤•à¤¾ à¤¸à¤®à¤¯ à¤¹à¥ˆà¥¤ à¤•à¥ƒà¤ªà¤¯à¤¾ à¤¹à¤¾à¤, à¤¨à¤¹à¥€à¤‚, à¤¯à¤¾ à¤¸à¥à¤•à¤¿à¤ª à¤¦à¤¬à¤¾à¤à¤à¥¤",
        response_window,
    )
    if status == "Yes":
        save_log("taken", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
        _say("Great. Thank you.", "à¤¬à¤¹à¥à¤¤ à¤…à¤šà¥à¤›à¥‡à¥¤")
        return "taken"
    if status == "Skip":
        save_log("delayed", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
        _say(f"Okay. Snoozing for {snooze_minutes} minutes.", f"à¤ à¥€à¤• à¤¹à¥ˆà¥¤ {snooze_minutes} à¤®à¤¿à¤¨à¤Ÿ à¤¬à¤¾à¤¦ à¤«à¤¿à¤° à¤¯à¤¾à¤¦ à¤¦à¤¿à¤²à¤¾à¤Šà¤à¤—à¥€à¥¤")
        time.sleep(max(1, snooze_minutes) * 60)
    elif status == "No":
        save_log("not_taken", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
        _say("Okay. I will remind you again soon.", "à¤ à¥€à¤• à¤¹à¥ˆà¥¤ à¤®à¥ˆà¤‚ à¤«à¤¿à¤° à¤¯à¤¾à¤¦ à¤¦à¤¿à¤²à¤¾à¤Šà¤à¤—à¥€à¥¤")
    else:
        save_log("no_response", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw or status)

    print("No confirmed response. Starting Stage 2...")
    _say(
        f"Reminder: Please take {med_name} now and tap Yes, No, or Skip.",
        f"à¤•à¥ƒà¤ªà¤¯à¤¾ {med_name} à¤…à¤­à¥€ à¤²à¥‡à¤‚ à¤”à¤° à¤¹à¤¾à¤, à¤¨à¤¹à¥€à¤‚, à¤¯à¤¾ à¤¸à¥à¤•à¤¿à¤ª à¤¦à¤¬à¤¾à¤à¤à¥¤",
    )
    print(f"Waiting for Stage 2 button response for up to {max(1, REMINDER_INTERVAL)} minute(s)...")
    status, raw = _prompt_for_button_response(
        state,
        medicine,
        2,
        f"Reminder: Please take {med_name} now and tap Yes, No, or Skip.",
        f"à¤•à¥ƒà¤ªà¤¯à¤¾ {med_name} à¤…à¤­à¥€ à¤²à¥‡à¤‚ à¤”à¤° à¤¹à¤¾à¤, à¤¨à¤¹à¥€à¤‚, à¤¯à¤¾ à¤¸à¥à¤•à¤¿à¤ª à¤¦à¤¬à¤¾à¤à¤à¥¤",
        response_window,
    )
    if status == "Yes":
        save_log("taken_late", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
        _say("Thank you.", "à¤¶à¥à¤•à¥à¤°à¤¿à¤¯à¤¾à¥¤")
        return "taken_late"
    if status == "Skip":
        save_log("delayed", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
        _say(f"Okay. Snoozing for {snooze_minutes} minutes.", f"à¤ à¥€à¤• à¤¹à¥ˆà¥¤ {snooze_minutes} à¤®à¤¿à¤¨à¤Ÿ à¤¬à¤¾à¤¦ à¤«à¤¿à¤° à¤¯à¤¾à¤¦ à¤¦à¤¿à¤²à¤¾à¤Šà¤à¤—à¥€à¥¤")
        time.sleep(max(1, snooze_minutes) * 60)
    elif status == "No":
        save_log("not_taken", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw)
    else:
        save_log("no_response", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes=raw or status)

    print("No confirmed response after Stage 2. Escalating to Stage 3: ALERTING CARETAKER")
    save_log("missed", captured, medicine_id=med_id, medicine_name=med_name, scheduled_time=med_time, notes="escalated_alert")
    _say(
        "Medicine was missed. Alerting caretaker.",
        "à¤¦à¤µà¤¾ à¤¨à¤¹à¥€à¤‚ à¤²à¥€ à¤—à¤ˆ à¤¹à¥ˆà¥¤ à¤®à¥ˆà¤‚ à¤…à¤²à¤°à¥à¤Ÿ à¤•à¤° à¤°à¤¹à¥€ à¤¹à¥‚à¤à¥¤",
    )
    return "missed"


def run_scheduler_loop(state: AppState | None, schedule_dict):
    print("Reminder Engine Active...")
    triggered_today: set[str] = set()

    while True:
        now = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%Y-%m-%d")

        if not schedule_dict:
            try:
                meds = get_medicines() or []
            except Exception:
                meds = []

            for m in meds:
                t = str(m.get("time", ""))
                key = f"{today}:{m.get('id')}:{t}"
                if t == now and key not in triggered_today:
                    print(f"[SCHEDULER] Triggering: {m.get('name')} @ {t}")
                    proc_thread = threading.Thread(target=start_reminder_procedure, args=(state, m), daemon=True)
                    proc_thread.start()
                    triggered_today.add(key)
        else:
            if now in schedule_dict:
                key = f"{today}:{now}"
                if key not in triggered_today:
                    med_name = schedule_dict[now]
                    proc_thread = threading.Thread(
                        target=start_reminder_procedure,
                        args=(state, {"name": med_name, "time": now}),
                        daemon=True,
                    )
                    proc_thread.start()
                    triggered_today.add(key)

        if now == "00:00":
            triggered_today = set()

        time.sleep(10)


if __name__ == "__main__":
    print("--- Testing Escalation Brain ---")
    demo_medicine = {"id": 0, "name": "Crocin", "time": "10:00", "image": ""}
    result = start_reminder_procedure(None, demo_medicine, skip_camera=True)
    print(f"Final Outcome: {result}")
