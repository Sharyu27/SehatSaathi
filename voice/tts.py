from __future__ import annotations

import ctypes
import os
import tempfile
import time
from pathlib import Path

from gtts import gTTS

_ENGINE = None
_ENGINE_AVAILABLE = True
_PYTTSX3_WARNING_SHOWN = False
_GTTS_FALLBACK_NOTICE_SHOWN = False
_DEFAULT_PLAYER_NOTICE_SHOWN = False


def _get_engine():
    global _ENGINE, _ENGINE_AVAILABLE, _PYTTSX3_WARNING_SHOWN
    if not _ENGINE_AVAILABLE:
        return None
    if _ENGINE is not None:
        return _ENGINE
    try:
        import pyttsx3  # type: ignore

        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        _ENGINE = engine
        return engine
    except Exception as exc:
        if not _PYTTSX3_WARNING_SHOWN:
            print(f"pyttsx3 unavailable: {exc}")
            _PYTTSX3_WARNING_SHOWN = True
        _ENGINE_AVAILABLE = False
        _ENGINE = None
        return None


def _play_mp3_via_mci(path: str) -> bool:
    winmm = getattr(ctypes, "windll", None)
    if winmm is None or not hasattr(winmm, "winmm"):
        return False

    alias = f"tts_{int(time.time() * 1000)}"
    player = winmm.winmm
    try:
        open_cmd = f'open "{path}" alias {alias}'
        if player.mciSendStringW(open_cmd, None, 0, 0) != 0:
            return False
        if player.mciSendStringW(f"play {alias} wait", None, 0, 0) != 0:
            return False
        return True
    finally:
        player.mciSendStringW(f"close {alias}", None, 0, 0)


def _play_via_default_app(path: str) -> bool:
    try:
        os.startfile(path)  # type: ignore[attr-defined]
        return True
    except Exception as exc:
        print(f"Default audio player launch failed: {exc}")
        return False


def _speak_with_gtts(text: str, lang: str) -> bool:
    global _DEFAULT_PLAYER_NOTICE_SHOWN
    try:
        tmp_dir = Path(tempfile.gettempdir())
        audio_path = tmp_dir / f"sehatsaathi_tts_{int(time.time() * 1000)}.mp3"
        gTTS(text=text, lang=lang).save(str(audio_path))

        if _play_mp3_via_mci(str(audio_path)):
            return True

        if not _DEFAULT_PLAYER_NOTICE_SHOWN:
            print("Native MP3 playback unavailable. Opening audio in the default player.")
            _DEFAULT_PLAYER_NOTICE_SHOWN = True
        return _play_via_default_app(str(audio_path))
    except Exception as exc:
        print(f"gTTS fallback failed: {exc}")
        return False


def speak(text: str, lang: str = "hi") -> bool:
    """Generate speech audio and play it synchronously when possible."""
    global _GTTS_FALLBACK_NOTICE_SHOWN
    try:
        engine = _get_engine()
        if engine is not None:
            engine.say(text)
            engine.runAndWait()
            return True

        if not _GTTS_FALLBACK_NOTICE_SHOWN:
            print("Falling back to gTTS audio generation.")
            _GTTS_FALLBACK_NOTICE_SHOWN = True
        return _speak_with_gtts(text, lang=lang)
    except Exception as e:
        print(f"TTS Error: {e}")
        return False


def speak_hindi(text):
    """Generates Hindi audio and plays it."""
    return speak(text, lang="hi")


def speak_english(text: str) -> bool:
    return speak(text, lang="en")
