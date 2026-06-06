from __future__ import annotations

from dataclasses import dataclass


LanguageCode = str


STRINGS: dict[str, dict[LanguageCode, str]] = {
    "app_name": {"en": "SehatSaathi", "hi": "सेहतसाथी"},
    "language": {"en": "Language", "hi": "भाषा"},
    "english": {"en": "English", "hi": "अंग्रेज़ी"},
    "hindi": {"en": "Hindi", "hi": "हिन्दी"},
    "back": {"en": "Back", "hi": "वापस"},
    "logout": {"en": "Logout", "hi": "लॉगआउट"},
    "save": {"en": "Save", "hi": "सेव करें"},
    "close": {"en": "Close", "hi": "बंद करें"},
    "headline": {"en": "Medicine Assistant", "hi": "दवाई सहायक"},
    "choose_role": {"en": "Choose your role", "hi": "अपनी भूमिका चुनें"},
    "caretaker_login": {"en": "Caretaker Login", "hi": "केयरटेकर लॉगिन"},
    "elder_mode": {"en": "Elder Mode", "hi": "वरिष्ठ मोड"},
    "login_title": {"en": "Login", "hi": "लॉगिन"},
    "username": {"en": "Username", "hi": "यूज़रनेम"},
    "password": {"en": "Password", "hi": "पासवर्ड"},
    "login": {"en": "Login", "hi": "लॉगिन"},
    "invalid_login": {"en": "Invalid username or password", "hi": "गलत यूज़रनेम या पासवर्ड"},
    "dashboard": {"en": "Dashboard", "hi": "डैशबोर्ड"},
    "taken": {"en": "Taken", "hi": "ली गई"},
    "missed": {"en": "Missed", "hi": "छूटी"},
    "adherence": {"en": "Adherence", "hi": "अनुपालन"},
    "next_dose": {"en": "Next dose", "hi": "अगली खुराक"},
    "tip": {"en": "Tip", "hi": "सुझाव"},
    "add_medicine": {"en": "Add Medicine", "hi": "दवा जोड़ें"},
    "reports": {"en": "Reports", "hi": "रिपोर्ट"},
    "alerts": {"en": "Alerts", "hi": "अलर्ट"},
    "medicine_name": {"en": "Medicine name", "hi": "दवा का नाम"},
    "medicine_time": {"en": "Time (e.g. 10:00)", "hi": "समय (जैसे 10:00)"},
    "medicine_image": {"en": "Image (optional)", "hi": "तस्वीर (वैकल्पिक)"},
    "browse": {"en": "Browse", "hi": "चुनें"},
    "saved": {"en": "Saved", "hi": "सेव हो गया"},
    "save_failed": {"en": "Save failed", "hi": "सेव नहीं हुआ"},
    "reports_title": {"en": "Reports", "hi": "रिपोर्ट"},
    "open_graph": {"en": "Open adherence graph", "hi": "अनुपालन ग्राफ़ खोलें"},
    "pattern": {"en": "Pattern", "hi": "पैटर्न"},
    "alerts_title": {"en": "Alerts", "hi": "अलर्ट"},
    "alert_ok": {"en": "No alert threshold reached.", "hi": "अलर्ट सीमा पूरी नहीं हुई।"},
    "alert_triggered": {"en": "Alert threshold reached!", "hi": "अलर्ट सीमा पूरी हो गई!"},
    "db_not_connected": {"en": "Database not connected yet - showing empty stats", "hi": "डेटाबेस कनेक्ट नहीं है - खाली आँकड़े दिख रहे हैं"},
    "elder_greeting": {"en": "Namaskar", "hi": "नमस्कार"},
    "demo_screen": {"en": "demo screen", "hi": "डेमो स्क्रीन"},
    "repeat": {"en": "Repeat", "hi": "दोहराएँ"},
    "snooze": {"en": "Snooze", "hi": "स्नूज़"},
    "listening": {"en": "Listening...", "hi": "सुन रहे हैं..."},
    "yes": {"en": "Yes", "hi": "हाँ"},
    "no": {"en": "No", "hi": "नहीं"},
    "skip": {"en": "Skip", "hi": "स्किप"},
    "reminder_stage": {"en": "Reminder Stage", "hi": "रिमाइंडर स्टेज"},
    "one_way_mode": {"en": "One-way mode: app speaks, user taps buttons.", "hi": "एक तरफ़ा मोड: ऐप बोलता है, यूज़र बटन दबाता है।"},
    "add_medicine_first": {"en": "Add a medicine first in caretaker mode.", "hi": "पहले केयरटेकर मोड में दवा जोड़ें।"},
    "speaking_status": {"en": "Speaking...", "hi": "ऐप बोल रहा है..."},
}


def t(lang: LanguageCode, key: str) -> str:
    entry = STRINGS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("en") or key


@dataclass(slots=True)
class I18n:
    lang: LanguageCode = "en"

    def tr(self, key: str) -> str:
        return t(self.lang, key)
