from __future__ import annotations

import threading
import tkinter as tk
from dataclasses import dataclass, field
from typing import Callable, Optional

from ui.i18n import I18n


RenderFn = Callable[["AppState"], None]


@dataclass(slots=True)
class ReminderPrompt:
    medicine_name: str
    scheduled_time: str
    stage: int
    text_en: str
    text_hi: str


@dataclass(slots=True)
class AppState:
    root: tk.Tk
    i18n: I18n
    lang_var: tk.StringVar
    current: Optional[RenderFn] = None
    pending_reminder: Optional[ReminderPrompt] = None
    _reminder_event: threading.Event = field(default_factory=threading.Event, repr=False)
    _reminder_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _reminder_response: Optional[tuple[str, str]] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        def _on_lang_change(*_args: object) -> None:
            value = self.lang_var.get()
            normalized = value.strip().lower()
            self.i18n.lang = "hi" if normalized in {"hi", "hindi", "à¤¹à¤¿à¤¨à¥à¤¦à¥€", "à¤¹à¤¿à¤‚à¤¦à¥€"} else "en"
            if self.current is not None:
                self.current(self)

        self.lang_var.trace_add("write", _on_lang_change)

    def navigate(self, page: RenderFn) -> None:
        self.current = page
        page(self)

    def request_reminder_response(self, prompt: ReminderPrompt, timeout_seconds: float) -> tuple[str, str]:
        with self._reminder_lock:
            self.pending_reminder = prompt
            self._reminder_response = None
            self._reminder_event.clear()

        self.root.after(0, lambda: self.current(self) if self.current is not None else None)
        got_response = self._reminder_event.wait(timeout_seconds)

        with self._reminder_lock:
            result = self._reminder_response if got_response and self._reminder_response is not None else ("Timeout", "No button response")
            self.pending_reminder = None
            self._reminder_response = None
            self._reminder_event.clear()

        self.root.after(0, lambda: self.current(self) if self.current is not None else None)
        return result

    def submit_reminder_response(self, response: str) -> None:
        with self._reminder_lock:
            self._reminder_response = (response, response)
            self._reminder_event.set()


def clear_root(root: tk.Misc) -> None:
    for w in root.winfo_children():
        w.destroy()
