import pandas as pd
from database.db import get_logs

def detect_pattern():
    data = get_logs()

    if not data:
        return "No data"

    df = pd.DataFrame(data)

    missed = df[df['status'] == "missed"]

    if len(missed) > len(df) * 0.3:
        return "Misses medicines frequently"

    return "Good adherence"