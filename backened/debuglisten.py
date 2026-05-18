"""
debug_listen.py — paste your mic_test RMS values and this tells you exactly what's wrong.
Run: python debug_listen.py
"""
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np
import tempfile
import os

SAMPLE_RATE = 16000
THRESHOLD   = 200

print("\n[1] Testing sounddevice...")
try:
    info = sd.query_devices(None, 'input')
    print(f"    ✅ Default input: {info['name']}")
except Exception as e:
    print(f"    ❌ sounddevice error: {e}")

print("\n[2] Loading Whisper...")
try:
    model = WhisperModel("base", compute_type="int8")
    print("    ✅ Whisper loaded")
except Exception as e:
    print(f"    ❌ Whisper error: {e}")
    exit()

print("\n[3] Recording 4 seconds — SPEAK CLEARLY NOW...")
try:
    recording = sd.rec(4 * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    rms = float(np.sqrt(np.mean(recording.astype(np.float32) ** 2)))
    peak = int(np.max(np.abs(recording)))
    print(f"    RMS={rms:.1f}  Peak={peak}")
    if rms < 50:
        print("    ❌ Almost no audio — check mic permissions or wrong device")
    elif rms < THRESHOLD:
        print(f"    ⚠️  Audio detected but below threshold ({THRESHOLD}). Lower SILENCE_THRESHOLD to {int(rms*0.4)}")
    else:
        print("    ✅ Audio level is fine")
except Exception as e:
    print(f"    ❌ Recording error: {e}")
    exit()

print("\n[4] Saving and transcribing...")
try:
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(tmp.name, SAMPLE_RATE, recording)
    tmp.close()
    segments, _ = model.transcribe(tmp.name, language="en", beam_size=5)
    text = " ".join(s.text for s in segments).strip()
    os.unlink(tmp.name)
    if text:
        print(f"    ✅ Whisper heard: '{text}'")
    else:
        print("    ❌ Whisper returned nothing — audio may be too short or noisy")
except Exception as e:
    print(f"    ❌ Transcription error: {e}")

print("\n[5] Testing VAD chunked recording (the actual Nova loop)...")
print("    Speak after the prompt — it will stop when you go silent\n")

chunks = []
silent = 0.0
total  = 0.0
started = False
CHUNK  = 0.25

print("    >>> SPEAK NOW <<<")
while total < 10:
    c = sd.rec(int(CHUNK * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()
    total += CHUNK
    rms = float(np.sqrt(np.mean(c.astype(np.float32)**2)))
    bar = "█" * min(int(rms/80), 40)
    status = "VOICE" if rms >= THRESHOLD else "silence"
    print(f"    t={total:.1f}s  RMS={rms:6.1f}  [{status}]  {bar}")

    if rms >= THRESHOLD:
        started = True
        silent = 0.0
        chunks.append(c)
    else:
        if started:
            chunks.append(c)
            silent += CHUNK
            if silent >= 1.5:
                print("    --- silence detected, stopping ---")
                break

if chunks:
    rec2 = np.concatenate(chunks)
    tmp2 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(tmp2.name, SAMPLE_RATE, rec2)
    tmp2.close()
    segs, _ = model.transcribe(tmp2.name, language="en", beam_size=5)
    text2 = " ".join(s.text for s in segs).strip()
    os.unlink(tmp2.name)
    print(f"\n    Whisper result: '{text2}'")
else:
    print("\n    ❌ No chunks collected — threshold never triggered")

print("\n=== Done. Paste the full output here so we can fix it. ===\n")