from __future__ import annotations

import os
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from alerts.notify import check_and_alert
from analytics.graphs import generate_graph
from analytics.patterns import detect_pattern
from config import IMAGE_FOLDER
from database.db import add_medicine, get_logs, normalize_hhmm
from ui.common import center_card, screen, topbar
from ui.state import AppState
from ui.theme import apply_theme, card


def show_add_medicine(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)
    from ui.caretaker_dashboard import show_dashboard
    from ui.login import show_login

    topbar(container, state, title=f"➕ {state.i18n.tr('add_medicine')}", on_back=lambda: state.navigate(show_dashboard), show_logout=True, on_logout=lambda: state.navigate(show_login))

    c = center_card(container, width=520)
    ttk.Label(c, text=state.i18n.tr("add_medicine"), style="Title.TLabel").pack(anchor="w", pady=(0, 12))

    form = card(c)
    form.pack(fill="x")

    name = ttk.Entry(form)
    time = ttk.Entry(form)
    image_path = ttk.Entry(form, validate="none")

    ttk.Label(form, text=state.i18n.tr("medicine_name"), style="Muted.TLabel").pack(anchor="w")
    name.pack(fill="x", pady=(4, 10))

    ttk.Label(form, text=state.i18n.tr("medicine_time"), style="Muted.TLabel").pack(anchor="w")
    time.pack(fill="x", pady=(4, 10))

    ttk.Label(form, text=state.i18n.tr("medicine_image"), style="Muted.TLabel").pack(anchor="w")
    row = ttk.Frame(form, style="Card.TFrame")
    row.pack(fill="x", pady=(4, 0))
    image_path.pack(in_=row, side="left", fill="x", expand=True, padx=(0, 10))

    def browse() -> None:
        p = filedialog.askopenfilename(
            title=state.i18n.tr("browse"),
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.gif"), ("All files", "*.*")],
        )
        if p:
            image_path.delete(0, "end")
            image_path.insert(0, p)

    ttk.Button(row, text=state.i18n.tr("browse"), style="Ghost.TButton", command=browse).pack(side="right")

    def save() -> None:
        try:
            normalized_time = normalize_hhmm(time.get().strip())
            img = image_path.get().strip()
            stored_img = ""
            if img:
                base_dir = Path(__file__).resolve().parents[1]
                dest_dir = base_dir / Path(IMAGE_FOLDER) / "medicines"
                dest_dir.mkdir(parents=True, exist_ok=True)
                ext = Path(img).suffix or ".jpg"
                safe_name = "".join(ch for ch in name.get().strip() if ch.isalnum() or ch in {"_", "-"}).strip() or "medicine"
                dest = dest_dir / f"{safe_name}_{normalized_time.replace(':','')}{ext}"
                shutil.copyfile(img, dest)
                stored_img = str(dest)

            add_medicine(name.get().strip(), normalized_time, stored_img)
            messagebox.showinfo(state.i18n.tr("saved"), state.i18n.tr("saved"))
            state.navigate(show_dashboard)
        except Exception as e:
            messagebox.showerror(state.i18n.tr("save_failed"), f"{state.i18n.tr('save_failed')}\n\n{e}")

    ttk.Button(c, text=state.i18n.tr("save"), style="Primary.TButton", command=save).pack(fill="x", pady=(14, 0))


def show_reports(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)
    from ui.caretaker_dashboard import show_dashboard
    from ui.login import show_login

    topbar(container, state, title=f"📈 {state.i18n.tr('reports_title')}", on_back=lambda: state.navigate(show_dashboard), show_logout=True, on_logout=lambda: state.navigate(show_login))

    c = center_card(container, width=520)
    ttk.Label(c, text=state.i18n.tr("reports_title"), style="Title.TLabel").pack(anchor="w", pady=(0, 12))

    box = card(c)
    box.pack(fill="x")

    def open_graph() -> None:
        try:
            generate_graph()
        except Exception as e:
            messagebox.showerror(state.i18n.tr("reports_title"), str(e))

    ttk.Button(box, text=f"📊 {state.i18n.tr('open_graph')}", style="Primary.TButton", command=open_graph).pack(fill="x", pady=(0, 10))

    try:
        p = detect_pattern()
    except Exception as e:
        p = str(e)

    ttk.Label(box, text=f"{state.i18n.tr('pattern')}: ", style="Muted.TLabel").pack(anchor="w")
    ttk.Label(box, text=p).pack(anchor="w", pady=(4, 0))


def show_alerts(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)
    from ui.caretaker_dashboard import show_dashboard
    from ui.login import show_login

    topbar(container, state, title=f"🚨 {state.i18n.tr('alerts_title')}", on_back=lambda: state.navigate(show_dashboard), show_logout=True, on_logout=lambda: state.navigate(show_login))

    c = center_card(container, width=520)
    ttk.Label(c, text=state.i18n.tr("alerts_title"), style="Title.TLabel").pack(anchor="w", pady=(0, 12))

    box = card(c)
    box.pack(fill="x")

    logs = []
    try:
        logs = get_logs() or []
    except Exception:
        logs = []

    missed = sum(1 for d in logs if str(d.get("status", "")).lower() == "missed")
    msg = state.i18n.tr("alert_triggered") if missed >= 3 else state.i18n.tr("alert_ok")

    ttk.Label(box, text=msg).pack(anchor="w")
    ttk.Label(box, text=f"{state.i18n.tr('missed')}: {missed}", style="Muted.TLabel").pack(anchor="w", pady=(6, 0))

    def run_check() -> None:
        try:
            check_and_alert()
            messagebox.showinfo(state.i18n.tr("alerts_title"), "OK")
        except Exception as e:
            messagebox.showerror(state.i18n.tr("alerts_title"), str(e))

    ttk.Button(c, text=f"✅ {state.i18n.tr('alerts')}", style="Primary.TButton", command=run_check).pack(fill="x", pady=(14, 0))
