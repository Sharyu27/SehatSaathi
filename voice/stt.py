import audioop
import time

import speech_recognition as sr


def _pick_input_device() -> int:
    import sounddevice as sd

    default_input, _ = sd.default.device
    if isinstance(default_input, int) and default_input >= 0:
        return default_input

    devices = sd.query_devices()
    input_indices = [i for i, d in enumerate(devices) if int(d.get("max_input_channels", 0)) > 0]
    if not input_indices:
        raise RuntimeError("No input audio devices found")
    return input_indices[0]


def _record_with_sounddevice(seconds: int, sample_rate: int = 16000) -> sr.AudioData:
    import sounddevice as sd

    try:
        device_index = _pick_input_device()
        device_info = sd.query_devices(device_index)
        sd.default.device = (device_index, None)
        print(f">>> Recording with sounddevice on: {device_info['name']}")
    except Exception as e:
        raise RuntimeError(f"Audio device selection failed: {e}") from e

    frames = int(sample_rate * seconds)
    print(f">>> Listening now for {seconds} seconds...")
    audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    print(">>> Recording complete.")
    return sr.AudioData(audio.tobytes(), sample_rate=sample_rate, sample_width=2)


def _audio_is_too_quiet(audio: sr.AudioData, threshold: int = 120) -> tuple[bool, int]:
    rms = audioop.rms(audio.get_raw_data(), audio.sample_width)
    return rms < threshold, rms


def _recognize_audio(audio: sr.AudioData, language: str):
    recognizer = sr.Recognizer()
    quiet, rms = _audio_is_too_quiet(audio)
    print(f">>> Mic level (RMS): {rms}")
    if quiet:
        return "Timeout", "Audio too quiet / no speech detected"

    print(">>> Recognizing speech...")
    text = recognizer.recognize_google(audio, language=language)
    print(f">>> Raw Text: {text}")
    return process_text(text)


def _listen_with_sounddevice(timeout: int, phrase_time_limit: int, language: str):
    print(f">>> Speak after the prompt. Recording starts in {min(timeout, 3)} second(s).")
    if timeout > 0:
        time.sleep(min(timeout, 3))

    audio = _record_with_sounddevice(phrase_time_limit)
    return _recognize_audio(audio, language=language)


def _listen_with_pyaudio(timeout: int, phrase_time_limit: int, language: str):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    mic = sr.Microphone()
    with mic as source:
        print(">>> Adjusting for noise... (Please stay quiet)")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print(f">>> Listening ({language})...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    return _recognize_audio(audio, language=language)


def listen_for_confirmation(timeout: int = 5, phrase_time_limit: int = 5, language: str = "hi-IN"):
    try:
        return _listen_with_sounddevice(timeout=timeout, phrase_time_limit=phrase_time_limit, language=language)
    except sr.UnknownValueError:
        return "Unknown", ""
    except sr.RequestError as request_error:
        return "Error", f"Speech service error: {request_error}"
    except Exception as sounddevice_error:
        print(f">>> sounddevice listening failed: {sounddevice_error}")

    try:
        return _listen_with_pyaudio(timeout=timeout, phrase_time_limit=phrase_time_limit, language=language)
    except sr.WaitTimeoutError:
        return "Timeout", "No speech detected"
    except sr.UnknownValueError:
        return "Unknown", ""
    except sr.RequestError as request_error:
        return "Error", f"Speech service error: {request_error}"
    except Exception as mic_error:
        return "Error", f"sounddevice failed; microphone backend unavailable: {mic_error}"


def process_text(text: str):
    normalized = text.strip().lower()

    keywords = {
        "Yes": ["yes", "haan", "han", "taken", "ok", "sahi"],
        "No": ["no", "nahin", "nahi", "not taken", "na"],
        "Skip": ["skip", "later", "snooze", "delay", "rok", "baad"],
    }

    for category, words in keywords.items():
        if any(word in normalized for word in words):
            return category, text

    return "Unclear", text


def listen_yes_no_skip() -> tuple[str, str]:
    return listen_for_confirmation(language="en-IN")
