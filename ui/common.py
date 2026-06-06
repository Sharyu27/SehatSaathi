from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui.state import AppState, clear_root
from ui.theme import COLORS, card


def topbar(parent: tk.Misc, state: AppState, title: str, on_back=None, show_logout: bool = False, on_logout=None) -> ttk.Frame:
    bar = ttk.Frame(parent)
    bar.pack(fill="x", padx=16, pady=(14, 8))

    left = ttk.Frame(bar)
    left.pack(side="left", fill="x", expand=True)

    if on_back is not None:
        ttk.Button(left, text=f"← {state.i18n.tr('back')}", style="Ghost.TButton", command=on_back).pack(side="left")

    ttk.Label(left, text=title, style="H2.TLabel").pack(side="left", padx=(10, 0))

    right = ttk.Frame(bar)
    right.pack(side="right")

    ttk.Label(right, text=state.i18n.tr("language"), style="Muted.TLabel").pack(side="left", padx=(0, 8))
    lang = ttk.Combobox(
        right,
        textvariable=state.lang_var,
        values=["English", "Hindi"],
        state="readonly",
        width=10,
    )
    lang.pack(side="left")

    if show_logout and on_logout is not None:
        ttk.Button(right, text=state.i18n.tr("logout"), style="Ghost.TButton", command=on_logout).pack(side="left", padx=(10, 0))

    return bar


def screen(parent: tk.Misc, state: AppState) -> ttk.Frame:
    clear_root(parent)
    container = ttk.Frame(parent)
    container.pack(fill="both", expand=True)
    return container


def center_card(container: ttk.Frame, width: int = 420) -> ttk.Frame:
    wrap = ttk.Frame(container)
    wrap.pack(fill="both", expand=True)

    c = card(wrap)
    c.place(relx=0.5, rely=0.5, anchor="center", width=width)
    return c


def stat_pill(parent: tk.Misc, label: str, value: str) -> ttk.Frame:
    pill = ttk.Frame(parent, style="Card.TFrame")
    pill.configure(padding=(12, 10))
    ttk.Label(pill, text=label, style="Muted.TLabel").pack(anchor="w")
    ttk.Label(pill, text=value, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(2, 0))
    return pill
