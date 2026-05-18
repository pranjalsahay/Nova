"""
speak.py — edge-tts + pygame for playback (no ffmpeg needed)
Install: pip install edge-tts pygame
"""
import asyncio
import edge_tts
import tempfile
import os

VOICE  = "en-IN-PrabhatNeural"  # Indian English male
# Alternatives:
# "en-IN-NeerjaNeural"  — Indian English female
# "en-US-GuyNeural"     — US male
# "en-GB-RyanNeural"    — British male
RATE   = "+5%"
VOLUME = "+0%"


async def _generate(text: str) -> str:
    """Generate mp3 from text, return temp file path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME)
    await communicate.save(tmp.name)
    return tmp.name


def _run_async(coro):
    """
    Safely run an async coroutine whether or not an event loop
    is already running (fixes RuntimeError on Windows / Python 3.10+).
    """
    try:
        # Try to get the running loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're inside an already-running loop (e.g. Jupyter / some servers)
            # Create a brand-new loop in a thread instead
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No current event loop at all — create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def _play_mp3(path: str):
    """Play mp3 using pygame, blocks until done."""
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    pygame.mixer.quit()


def speak(text: str):
    """Speak text aloud. Falls back to pyttsx3 if anything fails."""
    if not text or not text.strip():
        return

    print(f"\nNova: {text}\n")

    try:
        mp3_path = _run_async(_generate(text))
        _play_mp3(mp3_path)
        os.unlink(mp3_path)
        return  # success — don't fall through

    except Exception as e:
        print(f"[Speak Error] {e} — falling back to pyttsx3")

    # ── pyttsx3 fallback (cross-platform) ──────────────────────────
    try:
        import pyttsx3
        # Don't pass 'sapi5' — let pyttsx3 pick the right driver
        # (sapi5 = Windows only; espeak = Linux; nsss = macOS)
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e2:
        print(f"[Speak Fallback Error] {e2}")