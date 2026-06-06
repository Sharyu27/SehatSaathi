from __future__ import annotations

import tkinter as tk
from tkinter import ttk


COLORS = {
    "bg": "#f5f7ff",
    "card": "#ffffff",
    "text": "#1b1f2a",
    "muted": "#586174",
    "primary": "#3a6ff7",
    "primary_dark": "#2f5ad0",
    "danger": "#e55252",
    "success": "#2fbf71",
    "border": "#e6e9f2",
}


def apply_theme(root: tk.Tk) -> None:
    root.configure(bg=COLORS["bg"])
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["card"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 11))
    style.configure("Muted.TLabel", foreground=COLORS["muted"])
    style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
    style.configure("H2.TLabel", font=("Segoe UI", 14, "bold"))

    style.configure("TEntry", padding=7)
    style.configure("TCombobox", padding=5)

    style.configure(
        "Primary.TButton",
        padding=(14, 10),
        background=COLORS["primary"],
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_dark"]), ("disabled", COLORS["border"])],
        foreground=[("disabled", COLORS["muted"])],
    )

    style.configure(
        "Danger.TButton",
        padding=(14, 10),
        background=COLORS["danger"],
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
    )
    style.map("Danger.TButton", background=[("active", "#c94343")])

    style.configure(
        "Ghost.TButton",
        padding=(10, 8),
        background=COLORS["bg"],
        foreground=COLORS["primary"],
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    style.map("Ghost.TButton", foreground=[("active", COLORS["primary_dark"])])


def card(parent: tk.Misc, padx: int = 18, pady: int = 18) -> ttk.Frame:
    frame = ttk.Frame(parent, style="Card.TFrame")
    frame.configure(padding=(padx, pady))
    return frame

