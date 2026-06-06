import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from ui.common import center_card, screen, topbar
from ui.state import AppState
from ui.theme import apply_theme


def show_login(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)

    topbar(container, state, title=state.i18n.tr("app_name"))

    c = center_card(container, width=440)
    ttk.Label(c, text=f"🩺 {state.i18n.tr('headline')}", style="Title.TLabel").pack(anchor="w")
    ttk.Label(c, text=state.i18n.tr("choose_role"), style="Muted.TLabel").pack(anchor="w", pady=(6, 18))

    actions = ttk.Frame(c, style="Card.TFrame")
    actions.pack(fill="x")

    from ui.caretaker_dashboard import show_dashboard
    from ui.elder_screen import show_elder_screen

    def go_caretaker_login() -> None:
        show_login_form(state)

    ttk.Button(actions, text=f"🧑‍⚕️ {state.i18n.tr('caretaker_login')}", style="Primary.TButton", command=go_caretaker_login).pack(fill="x", pady=(0, 10))
    ttk.Button(actions, text=f"👵 {state.i18n.tr('elder_mode')}", style="Primary.TButton", command=lambda: state.navigate(show_elder_screen)).pack(fill="x")


def show_login_form(state: AppState) -> None:
    apply_theme(state.root)
    container = screen(state.root, state)

    from ui.caretaker_dashboard import show_dashboard

    topbar(container, state, title=state.i18n.tr("login_title"), on_back=lambda: state.navigate(show_login))

    c = center_card(container, width=440)

    ttk.Label(c, text=f"🔐 {state.i18n.tr('login_title')}", style="Title.TLabel").pack(anchor="w", pady=(0, 10))

    form = ttk.Frame(c, style="Card.TFrame")
    form.pack(fill="x")

    ttk.Label(form, text=state.i18n.tr("username"), style="Muted.TLabel").pack(anchor="w")
    user = ttk.Entry(form)
    user.pack(fill="x", pady=(4, 10))

    ttk.Label(form, text=state.i18n.tr("password"), style="Muted.TLabel").pack(anchor="w")
    pwd = ttk.Entry(form, show="•")
    pwd.pack(fill="x", pady=(4, 14))

    def do_login() -> None:
        if user.get() == "admin" and pwd.get() == "1234":
            state.navigate(show_dashboard)
        else:
            messagebox.showerror(state.i18n.tr("login_title"), state.i18n.tr("invalid_login"))

    ttk.Button(form, text=state.i18n.tr("login"), style="Primary.TButton", command=do_login).pack(fill="x")
