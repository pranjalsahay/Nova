# Nova AI Voice Assistant

A local AI voice assistant powered by **GPT-4o with web search**, Whisper STT, and pyttsx3 TTS.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your API key
Edit `.env` and paste your OpenAI API key:
```
OPENAI_API_KEY=sk-...your key here...
```

### 3. Run Nova
```bash
python nova.py
```

---

## How to use

| You say | Nova does |
|---|---|
| `Hello Nova` | Wakes up, ready to listen |
| `What's the weather in Mumbai?` | Searches web and answers |
| `Play Shape of You` | Opens YouTube search |
| `Search Python tutorials` | Google search |
| `Open Gmail` | Opens Gmail in browser |
| `Open VS Code` | Launches VS Code |
| `Who won the IPL 2025?` | Web search answer |
| `Sleep` / `Bye` | Goes back to sleep |

---

## Files

| File | Purpose |
|---|---|
| `nova.py` | Main loop — wake word, commands, AI |
| `listener.py` | Mic recording + Whisper transcription |
| `speak.py` | Text-to-speech via pyttsx3 |
| `ai.py` | GPT-4o with web search |
| `actions.py` | Built-in commands (open apps, sites) |
| `state.py` | Shared status dict |
| `server.py` | Flask API to expose status (optional) |

---

## Notes

- Nova uses **conversation memory** — it remembers the last 10 exchanges for context.
- The Flask `server.py` is optional — run it separately if you want a status dashboard.
- Works on Windows, macOS, and Linux.
