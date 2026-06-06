from __future__ import annotations

from contextlib import closing

import mysql.connector

from config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

def normalize_hhmm(value: str) -> str:
    """
    Normalize time input to strict HH:MM (24h).
    Accepts 'H:M', 'HH:MM', 'HHMM', 'HMM' etc.
    Raises ValueError if invalid.
    """
    raw = (value or "").strip()
    if not raw:
        raise ValueError("Time is required")

    if ":" in raw:
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid time format")
        h_s, m_s = parts[0].strip(), parts[1].strip()
    else:
        digits = "".join(ch for ch in raw if ch.isdigit())
        if len(digits) not in (3, 4):
            raise ValueError("Invalid time format")
        if len(digits) == 3:
            h_s, m_s = digits[0], digits[1:]
        else:
            h_s, m_s = digits[:2], digits[2:]

    h, m = int(h_s), int(m_s)
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError("Time must be between 00:00 and 23:59")
    return f"{h:02d}:{m:02d}"


# ---------- CONNECTION ----------
def connect():
    # Ensure DB exists then connect to it.
    _ensure_database()
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )
    _init_db(conn)
    return conn


def _ensure_database() -> None:
    conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
    with closing(conn.cursor()) as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.close()


def _init_db(conn) -> None:
    with closing(conn.cursor()) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS medicines (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              time VARCHAR(5) NOT NULL,
              image TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
              id INT AUTO_INCREMENT PRIMARY KEY,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              medicine_id INT NULL,
              medicine_name VARCHAR(255) NULL,
              scheduled_time VARCHAR(5) NULL,
              status VARCHAR(32) NOT NULL,
              image TEXT NULL,
              notes TEXT NULL
            )
            """
        )
    conn.commit()

# ---------- SAVE LOG ----------
def save_log(status, image=None, medicine_id=None, medicine_name=None, scheduled_time=None, notes=None):
    conn = connect()
    with closing(conn.cursor()) as cursor:
        cursor.execute(
            "INSERT INTO logs (status, image, medicine_id, medicine_name, scheduled_time, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            (status, image, medicine_id, medicine_name, scheduled_time, notes),
        )
        conn.commit()
    conn.close()

# ---------- GET LOGS ----------
def get_logs():
    conn = connect()
    with closing(conn.cursor(dictionary=True)) as cursor:
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC, id DESC")
        data = cursor.fetchall()
    conn.close()
    return data

# ---------- GET MEDICINES ----------
def get_medicines():
    conn = connect()
    with closing(conn.cursor(dictionary=True)) as cursor:
        cursor.execute("SELECT * FROM medicines ORDER BY time ASC, id ASC")
        data = cursor.fetchall()
    conn.close()
    return data


def get_next_medicine(now_hhmm: str):
    """
    Returns the next medicine at/after now_hhmm (24h string "HH:MM").
    If none remaining today, returns the first medicine of the day.
    """
    meds = get_medicines() or []
    if not meds:
        return None
    for m in meds:
        if str(m.get("time", "")) >= now_hhmm:
            return m
    return meds[0]

# ---------- ADD MEDICINE ----------
def add_medicine(name, time, image):
    conn = connect()
    t = normalize_hhmm(time)
    with closing(conn.cursor()) as cursor:
        cursor.execute("INSERT INTO medicines (name, time, image) VALUES (%s, %s, %s)", (name, t, image))
        conn.commit()
    conn.close()