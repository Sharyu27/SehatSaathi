from __future__ import annotations

from tkinter import messagebox, ttk

from analytics.patterns import detect_pattern
from database.db import get_logs
from ui.common import screen, stat_pill, topbar
from ui.state import AppState
from ui.theme import apply_theme, card


def _safe_logs() -> list[dict]:
    try:
        return get_logs() or []
    except Exception:
        return []


def show_dashboard(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)

    from ui.login import show_login
    from ui.screens import show_add_medicine, show_alerts, show_reports

    topbar(
        container,
        state,
        title=f"📊 {state.i18n.tr('dashboard')}",
        show_logout=True,
        on_logout=lambda: state.navigate(show_login),
    )

    content = ttk.Frame(container)
    content.pack(fill="both", expand=True, padx=16, pady=10)

    logs = _safe_logs()
    taken = sum(1 for d in logs if str(d.get("status", "")).lower() == "taken")
    missed = sum(1 for d in logs if str(d.get("status", "")).lower() == "missed")
    total = max(taken + missed, 1)
    adherence = int(round((taken / total) * 100))

    stats = ttk.Frame(content)
    stats.pack(fill="x")

    p1 = stat_pill(stats, state.i18n.tr("taken"), str(taken))
    p2 = stat_pill(stats, state.i18n.tr("missed"), str(missed))
    p3 = stat_pill(stats, state.i18n.tr("adherence"), f"{adherence}%")
    p1.pack(side="left", fill="x", expand=True, padx=(0, 10))
    p2.pack(side="left", fill="x", expand=True, padx=(0, 10))
    p3.pack(side="left", fill="x", expand=True)

    actions = card(content)
    actions.pack(fill="x", pady=(14, 12))

    ttk.Button(actions, text=f"➕ {state.i18n.tr('add_medicine')}", style="Primary.TButton", command=lambda: state.navigate(show_add_medicine)).pack(fill="x", pady=(0, 10))
    ttk.Button(actions, text=f"📈 {state.i18n.tr('reports')}", style="Primary.TButton", command=lambda: state.navigate(show_reports)).pack(fill="x", pady=(0, 10))
    ttk.Button(actions, text=f"🚨 {state.i18n.tr('alerts')}", style="Danger.TButton", command=lambda: state.navigate(show_alerts)).pack(fill="x")

    tip = card(content)
    tip.pack(fill="x")

    try:
        pattern = detect_pattern()
    except Exception as e:
        pattern = f"{state.i18n.tr('pattern')}: {e}"

    ttk.Label(tip, text=f"💡 {state.i18n.tr('tip')}", style="Muted.TLabel").pack(anchor="w")
    ttk.Label(tip, text=pattern).pack(anchor="w", pady=(4, 0))

    if not logs:
        ttk.Label(content, text=f"({state.i18n.tr('db_not_connected')})", style="Muted.TLabel").pack(anchor="w", pady=(10, 0))
