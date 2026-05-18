"""
Nova Mic Diagnostic
Run this first to find your mic and the right silence threshold.
"""

import sounddevice as sd
import numpy as np

def list_devices():
    print("\n" + "="*50)
    print("  AVAILABLE AUDIO DEVICES")
    print("="*50)
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d['max_input_channels'] > 0:
            print(f"  [{i}] {d['name']}  (inputs: {d['max_input_channels']})")
    print("="*50)
    return devices

def test_mic(device_index=None, duration=5, sample_rate=16000):
    print(f"\n[Test] Recording for {duration} seconds from device {device_index}...")
    print("       >>> SPEAK NOW <<<\n")

    try:
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
            device=device_index
        )
        sd.wait()
        rms = np.sqrt(np.mean(recording.astype(np.float32) ** 2))
        peak = np.max(np.abs(recording))
        print(f"  RMS  (avg loudness) : {rms:.1f}")
        print(f"  Peak (max loudness) : {peak}")

        if rms < 50:
            print("\n  ❌ Very low — mic may not be picking up audio.")
            print("     Try a different device index or check mic permissions.")
        elif rms < 300:
            print("\n  ⚠️  Low — detectable but quiet. Set SILENCE_THRESHOLD = 100")
        elif rms < 1000:
            print("\n  ✅ Good — Set SILENCE_THRESHOLD = 300")
        else:
            print("\n  ✅ Loud and clear — Set SILENCE_THRESHOLD = 500")

        return rms

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return 0

def live_monitor(device_index=None, sample_rate=16000, chunk=0.3):
    """Show live RMS so you can speak and see values in real time."""
    print(f"\n[Live Monitor] Speak into mic — watching RMS for 10 seconds (device {device_index})")
    print("  (Use Ctrl+C to stop early)\n")
    import time
    try:
        for _ in range(int(10 / chunk)):
            block = sd.rec(
                int(chunk * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
                device=device_index
            )
            sd.wait()
            rms = np.sqrt(np.mean(block.astype(np.float32) ** 2))
            bar = "█" * int(rms / 50)
            print(f"  RMS: {rms:6.1f}  {bar}")
    except KeyboardInterrupt:
        pass

# ─────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    devices = list_devices()

    print("\nStep 1: Testing DEFAULT mic (no device index)...")
    rms = test_mic(device_index=None)

    print("\n" + "-"*50)
    print("Step 2: Live RMS monitor (speak now to see values)...")
    live_monitor(device_index=None)

    print("\n" + "="*50)
    print("  RESULT")
    print("="*50)
    print("  If the default mic worked well → you are done.")
    print("  If it failed → run again with a device index:")
    print("    test_mic(device_index=2)   ← try each input device")
    print("  Then update DEVICE_INDEX and SILENCE_THRESHOLD in listener.py")
    print("="*50)