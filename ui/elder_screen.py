from __future__ import annotations

import threading
from datetime import datetime
from tkinter import ttk

from database.db import get_next_medicine
from ui.common import center_card, screen, topbar
from ui.state import AppState
from ui.theme import apply_theme, card


def show_elder_screen(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)

    from ui.login import show_login

    topbar(container, state, title=f"👵 {state.i18n.tr('elder_mode')}", on_back=lambda: state.navigate(show_login))

    c = center_card(container, width=520)
    ttk.Label(c, text=f"🙏 {state.i18n.tr('elder_greeting')} Aaji", style="Title.TLabel").pack(anchor="w")
    ttk.Label(c, text=f"({state.i18n.tr('demo_screen')})", style="Muted.TLabel").pack(anchor="w", pady=(4, 14))

    info = card(c)
    info.pack(fill="x", pady=(0, 14))
    med_name = ttk.Label(info, text="—", style="H2.TLabel")
    med_time = ttk.Label(info, text="—", style="Muted.TLabel")
    med_name.pack(anchor="w")
    med_time.pack(anchor="w", pady=(4, 0))

    actions = ttk.Frame(c, style="Card.TFrame")
    actions.pack(fill="x")

    status_lbl = ttk.Label(c, text=state.i18n.tr("one_way_mode"), style="Muted.TLabel")
    status_lbl.pack(anchor="w", pady=(14, 0))

    if state.pending_reminder is not None:
        prompt = card(c)
        prompt.pack(fill="x", pady=(14, 0))
        prompt_text = state.pending_reminder.text_hi if state.i18n.lang == "hi" else state.pending_reminder.text_en
        ttk.Label(prompt, text=f"{state.i18n.tr('reminder_stage')} {state.pending_reminder.stage}", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(prompt, text=prompt_text, wraplength=420, style="H2.TLabel").pack(anchor="w", pady=(4, 12))
        ttk.Button(prompt, text=state.i18n.tr("yes"), style="Primary.TButton", command=lambda: state.submit_reminder_response("Yes")).pack(fill="x", pady=(0, 8))
        ttk.Button(prompt, text=state.i18n.tr("no"), style="Ghost.TButton", command=lambda: state.submit_reminder_response("No")).pack(fill="x", pady=(0, 8))
        ttk.Button(prompt, text=state.i18n.tr("skip"), style="Ghost.TButton", command=lambda: state.submit_reminder_response("Skip")).pack(fill="x")

    current_med: dict | None = None

    def refresh() -> None:
        nonlocal current_med

        try:
            if not med_name.winfo_exists():
                return
        except Exception:
            return

        now = datetime.now().strftime("%H:%M")
        try:
            current_med = get_next_medicine(now)
        except Exception:
            current_med = None

        if not current_med:
            med_name.configure(text="💊 (No medicines added yet)")
            med_time.configure(text="⏰ —")
        else:
            med_name.configure(text=f"💊 {current_med.get('name', '')}")
            med_time.configure(text=f"⏰ {current_med.get('time', '')}")

        state.root.after(4000, refresh)

    def run_reminder_flow(snooze_minutes: int = 5) -> None:
        if not current_med:
            status_lbl.configure(text=state.i18n.tr("add_medicine_first"))
            return

        def worker() -> None:
            from core.reminder import start_reminder_procedure
            from vision.verify_ui import verify_medicine_with_camera_ui

            def safe_status(text: str) -> None:
                try:
                    if status_lbl.winfo_exists():
                        status_lbl.configure(text=text)
                except Exception:
                    pass

            med = current_med
            expected = str(med.get("image") or "").strip()
            captured_path = None
            skip_camera = False

            if expected:
                done = threading.Event()
                holder: dict[str, object] = {"verified": False, "captured": None, "reason": "not_run"}

                def run_ui() -> None:
                    res = verify_medicine_with_camera_ui(state.root, expected, medicine_name=str(med.get("name", "")))
                    holder["verified"] = res.verified
                    holder["captured"] = res.captured_path
                    holder["reason"] = res.reason
                    done.set()

                state.root.after(0, lambda: safe_status("📷 Show medicine to camera..."))
                state.root.after(0, run_ui)
                done.wait()

                captured_path = holder["captured"] if isinstance(holder["captured"], str) else None
                if bool(holder["verified"]):
                    state.root.after(0, lambda: safe_status("✅ Verified by camera"))
                    result = start_reminder_procedure(state, med, snooze_minutes=snooze_minutes, skip_camera=True, captured_image_path=captured_path)
                    state.root.after(0, lambda: safe_status(f"Result: {result}"))
                    return
                skip_camera = True

            state.root.after(0, lambda: safe_status(state.i18n.tr("speaking_status")))
            result = start_reminder_procedure(state, med, snooze_minutes=snooze_minutes, skip_camera=skip_camera, captured_image_path=captured_path)
            state.root.after(0, lambda: safe_status(f"Result: {result}"))

        threading.Thread(target=worker, daemon=True).start()

    ttk.Button(actions, text=f"🔊 {state.i18n.tr('repeat')}", style="Primary.TButton", command=lambda: run_reminder_flow(5)).pack(fill="x", pady=(0, 10))
    ttk.Button(actions, text=f"😴 {state.i18n.tr('snooze')}", style="Primary.TButton", command=lambda: run_reminder_flow(10)).pack(fill="x")

    refresh()
