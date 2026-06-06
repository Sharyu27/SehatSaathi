from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

from vision.detection import compare_images


@dataclass(slots=True)
class VerifyResult:
    verified: bool
    captured_path: Optional[str]
    reason: str


def verify_medicine_with_camera_ui(
    root: tk.Tk,
    expected_image_path: str,
    medicine_name: str = "",
    timeout_s: int = 12,
) -> VerifyResult:
    """
    Shows a live camera preview in Elder Mode, asks user to show medicine,
    captures a snapshot, compares with expected image, returns result.
    """
    cap = None
    # Windows often works better with CAP_DSHOW/CAP_MSMF. Try indices too.
    backends = [getattr(cv2, "CAP_DSHOW", 0), getattr(cv2, "CAP_MSMF", 0), 0]
    indices = [0, 1, 2]
    for backend in backends:
        for idx in indices:
            try:
                candidate = cv2.VideoCapture(idx, backend) if backend else cv2.VideoCapture(idx)
                if candidate is not None and candidate.isOpened():
                    cap = candidate
                    break
                try:
                    candidate.release()
                except Exception:
                    pass
            except Exception:
                pass
        if cap is not None:
            break

    if cap is None:
        return VerifyResult(False, None, "camera_not_available")

    top = tk.Toplevel(root)
    top.title("Medicine Verification")
    top.resizable(False, False)
    top.transient(root)
    top.grab_set()

    frame = ttk.Frame(top)
    frame.pack(fill="both", expand=True, padx=14, pady=12)

    title = "📷 Show medicine to camera"
    if medicine_name:
        title = f"📷 Show {medicine_name} to camera"
    ttk.Label(frame, text=title, font=("Segoe UI", 14, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Hold the medicine steady and press Capture (auto closes).", foreground="#586174").pack(anchor="w", pady=(4, 10))

    preview = ttk.Label(frame)
    preview.pack()

    status = ttk.Label(frame, text="", foreground="#586174")
    status.pack(anchor="w", pady=(10, 0))

    result: dict[str, object] = {"done": False, "verified": False, "captured": None, "reason": "cancelled"}
    start = time.time()

    def close() -> None:
        result["done"] = True
        try:
            cap.release()
        except Exception:
            pass
        top.destroy()

    def capture() -> None:
        ret, bgr = cap.read()
        if not ret:
            result["verified"] = False
            result["captured"] = None
            result["reason"] = "capture_failed"
            close()
            return

        out_dir = Path(__file__).resolve().parents[1] / "assets" / "images" / "captures"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"capture_{int(time.time())}.jpg"
        cv2.imwrite(str(out_path), bgr)

        ok = False
        try:
            ok = compare_images(expected_image_path, str(out_path))
        except Exception:
            ok = False

        result["verified"] = bool(ok)
        result["captured"] = str(out_path)
        result["reason"] = "matched" if ok else "not_matched"
        close()

    def tick() -> None:
        if bool(result["done"]):
            return

        # Timeout
        remaining = int(timeout_s - (time.time() - start))
        if remaining <= 0:
            result["verified"] = False
            result["captured"] = None
            result["reason"] = "timeout"
            close()
            return

        status.configure(text=f"Time left: {remaining}s")

        ret, bgr = cap.read()
        if ret:
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((480, 320))
            imgtk = ImageTk.PhotoImage(image=img)
            preview.configure(image=imgtk)
            preview.image = imgtk

        top.after(50, tick)

    btns = ttk.Frame(frame)
    btns.pack(fill="x", pady=(10, 0))
    ttk.Button(btns, text="Capture", command=capture).pack(side="left")
    ttk.Button(btns, text="Skip", command=close).pack(side="right")

    tick()
    root.wait_window(top)

    return VerifyResult(
        verified=bool(result["verified"]),
        captured_path=result["captured"] if isinstance(result["captured"], str) else None,
        reason=str(result["reason"]),
    )

