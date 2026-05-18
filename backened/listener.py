"""
listener.py — Uses Google Speech Recognition (much more accurate than Whisper)
Install: pip install SpeechRecognition pyaudio
If pyaudio fails on Windows: pip install pipwin && pipwin install pyaudio
"""
import speech_recognition as sr

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
ENERGY_THRESHOLD    = 300    # mic sensitivity — lower if not detecting, raise if too sensitive
PAUSE_THRESHOLD     = 1.0    # seconds of silence before considering phrase complete
PHRASE_TIME_LIMIT   = 15     # max seconds per phrase
DYNAMIC_ENERGY      = True   # auto-adjusts to background noise

# ─────────────────────────────────────────
# Init recognizer once
# ─────────────────────────────────────────
recognizer = sr.Recognizer()
recognizer.energy_threshold    = ENERGY_THRESHOLD
recognizer.pause_threshold     = PAUSE_THRESHOLD
recognizer.dynamic_energy_threshold = DYNAMIC_ENERGY

mic = sr.Microphone()

# Calibrate to background noise at startup
print("[Nova] Calibrating microphone to background noise...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"[Nova] Mic ready. Energy threshold set to: {recognizer.energy_threshold:.0f}")


def listen() -> str:
    """
    Listen for a single phrase and return transcribed text.
    Uses Google Speech Recognition — accurate, handles accents well.
    Returns lowercased text or "" on failure/silence.
    """
    try:
        print("[Nova] Listening... (speak now)")

        with mic as source:
            audio = recognizer.listen(
                source,
                timeout=8,                      # wait up to 8s for speech to start
                phrase_time_limit=PHRASE_TIME_LIMIT,
            )

        print("[Nova] Recognizing...")
        text = recognizer.recognize_google(audio, language="en-IN")  # en-IN = Indian English accent
        text = text.lower().strip()
        print(f"[Nova] You said: {text}")
        return text

    except sr.WaitTimeoutError:
        print("[Nova] (No speech detected)")
        return ""
    except sr.UnknownValueError:
        print("[Nova] (Could not understand audio)")
        return ""
    except sr.RequestError as e:
        print(f"[Nova] Google Speech error: {e}")
        return ""
    except Exception as e:
        print(f"[Listen Error] {e}")
        return ""