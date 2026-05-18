"""
speak_test.py — Run this to find exactly why Nova isn't speaking.
python speak_test.py
"""

print("\n" + "="*50)
print("  NOVA SPEAK DIAGNOSTIC")
print("="*50)

# ── Step 1: edge-tts installed? ──────────────────
print("\n[1] Checking edge-tts...")
try:
    import edge_tts
    print("    ✅ edge-tts is installed")
except ImportError:
    print("    ❌ edge-tts NOT installed")
    print("    Fix: pip install edge-tts")
    exit()

# ── Step 2: pygame installed? ────────────────────
print("\n[2] Checking pygame...")
try:
    import pygame
    print("    ✅ pygame is installed")
except ImportError:
    print("    ❌ pygame NOT installed")
    print("    Fix: pip install pygame")
    exit()

# ── Step 3: Generate audio file via edge-tts ─────
print("\n[3] Generating speech audio (needs internet)...")
import asyncio
import tempfile
import os

VOICE = "en-IN-PrabhatNeural"

async def generate(text):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(tmp.name)
    return tmp.name

try:
    # Use new_event_loop to avoid any asyncio conflicts
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mp3_path = loop.run_until_complete(generate("Hello, I am Nova."))
    loop.close()

    size = os.path.getsize(mp3_path)
    print(f"    ✅ Audio file created: {mp3_path}")
    print(f"    ✅ File size: {size} bytes")

    if size < 1000:
        print("    ⚠️  File is very small — may be empty or corrupted")

except Exception as e:
    print(f"    ❌ edge-tts failed: {e}")
    print("    Possible causes:")
    print("    - No internet connection")
    print("    - Firewall blocking Microsoft TTS servers")
    print("    Fix: Check your internet or try a VPN")
    mp3_path = None

# ── Step 4: Play the audio via pygame ────────────
if mp3_path and os.path.exists(mp3_path):
    print("\n[4] Playing audio via pygame (you should hear something)...")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()

        import time
        timeout = 10
        start = time.time()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            if time.time() - start > timeout:
                print("    ⚠️  Playback timed out")
                break

        pygame.mixer.music.unload()
        pygame.mixer.quit()
        os.unlink(mp3_path)
        print("    ✅ Playback finished")

    except Exception as e:
        print(f"    ❌ pygame playback failed: {e}")
        print("    Possible causes:")
        print("    - No audio output device / speakers")
        print("    - Audio driver issue")
        print("    Fix: Check Windows sound settings / speaker volume")

# ── Step 5: pyttsx3 fallback test ────────────────
print("\n[5] Testing pyttsx3 fallback (backup speaker)...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.say("This is the pyttsx3 fallback voice.")
    engine.runAndWait()
    print("    ✅ pyttsx3 worked — you should have heard it")
except Exception as e:
    print(f"    ❌ pyttsx3 failed: {e}")
    print("    Fix: pip install pyttsx3")

print("\n" + "="*50)
print("  Copy and paste the output above to share results")
print("="*50 + "\n")