"""Run this once to find your correct device index."""
import sounddevice as sd
import numpy as np

devices = sd.query_devices()
print("\nAll INPUT devices:\n")
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        print(f"  [{i}] {d['name']}")

print("\nTesting each device for 1 second (speak while running)...\n")
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        try:
            rec = sd.rec(16000, samplerate=16000, channels=1, dtype="int16", device=i)
            sd.wait()
            rms = float(np.sqrt(np.mean(rec.astype(np.float32)**2)))
            flag = "✅ GOOD" if rms > 100 else "❌ dead/quiet"
            print(f"  [{i}] {d['name'][:45]:<45} RMS={rms:7.1f}  {flag}")
        except Exception as e:
            print(f"  [{i}] {d['name'][:45]:<45} ERROR: {e}")

print("\n→ Use the index of the ✅ GOOD device in listener.py as DEVICE_INDEX")