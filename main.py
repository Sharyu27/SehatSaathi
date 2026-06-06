# ==========================================
# SehatSaathi - Final Integrated Main File
# ==========================================

import tkinter as tk
import threading

# UI
from ui.i18n import I18n
from ui.login import show_login
from ui.state import AppState

# Core (Reminder Engine)
from core.reminder import run_scheduler_loop

# Database
from database.db import connect

# Alerts
from alerts.notify import check_and_alert

# ------------------------------------------
# Initialize System
# ------------------------------------------
def initialize_system(state: AppState):
    print("Starting SehatSaathi System...")

    # Test database connection
    try:
        conn = connect()
        conn.close()
        print("Database Connected")
    except Exception as e:
        print("Database Error:", e)

    # Start background reminder scheduler
    scheduler_thread = threading.Thread(
        target=run_scheduler_loop,
        args=(state, None),
        daemon=True   # runs in background
    )
    scheduler_thread.start()

    # Start alert monitoring (optional loop later)
    try:
        check_and_alert()
    except:
        print("Alert system not ready")


# ------------------------------------------
# Main Application (GUI)
# ------------------------------------------
def main():
    # Step 1: Create GUI window
    root = tk.Tk()
    root.title("SehatSaathi")
    root.geometry("400x500")

    # Step 2: Create shared UI state
    state = AppState(root=root, i18n=I18n(lang="en"), lang_var=tk.StringVar(master=root, value="English"))

    # Step 3: Initialize backend systems
    initialize_system(state)

    # Step 4: Load UI
    state.navigate(show_login)

    # Step 5: Run application
    root.mainloop()


# ------------------------------------------
# Run Program
# ------------------------------------------
if __name__ == "__main__":
    main()
