# Nova AI Assistant

A local AI voice assistant project with a Python backend and a React frontend.

Nova combines speech recognition, AI-driven responses, web search, and browser-based controls into a single assistant experience.

## Repository structure

- `backened/` — Python backend for voice input, AI orchestration, actions, and optional Flask status API.
- `frontend/` — React + Vite UI with Three.js visuals.
- `start_nova.bat` — Windows startup helper that launches the backend and frontend together.

## Key features

- Wake-word voice assistant experience
- Speech-to-text via Whisper/faster-whisper
- AI responses using OpenAI and/oullama
- Text-to-speech support
- Built-in actions for opening apps and web searches
- Visual frontend with React and Three.js

## Prerequisites

- Python 3.10+ (recommended)
- Node.js 18+ / npm
- Windows audio drivers for microphone/playback
- OpenAI API key

## Backend setup

1. Create and activate a Python virtual environment:

```powershell
cd d:\aiassistant\backened
python -m venv venv
venv\Scripts\Activate
```

2. Install backend dependencies:

```powershell
pip install -r "requirements (1).txt"
```

3. Create a `.env` file inside `backened/` with your OpenAI key:

```text
OPENAI_API_KEY=sk-...your-key...
```

4. (Optional) add other API keys if used by services in `backened/service.py`:

- `WEATHER_KEY`
- `NEWS_KEY`
- `OCR_KEY`
- `TMDB_KEY`

## Frontend setup

1. Install dependencies:

```powershell
cd d:\aiassistant\frontend
npm install
```

2. Start the frontend:

```powershell
npm run dev
```

## Run Nova

### Recommended: use the Windows helper

```powershell
cd d:\aiassistant
start_nova.bat
```

This launches the backend, the frontend, and opens `http://localhost:5173` in your browser.

### Manual start

Backend:

```powershell
cd d:\aiassistant\backened
python app.py
```

Frontend:

```powershell
cd d:\aiassistant\frontend
npm run dev
```

Then open `http://localhost:5173`.

## Example voice commands

- `Hello Nova`
- `What's the weather in Mumbai?`
- `Play Shape of You`
- `Search Python tutorials`
- `Open Gmail`
- `Open VS Code`
- `Who won the IPL 2025?`
- `Sleep` / `Bye`

## Useful files

- `backened/app.py` — backend application launcher
- `backened/nova.py` — main assistant loop and command handling
- `backened/ai.py` — AI prompt/response integration and API key loading
- `backened/actions.py` — built-in command actions
- `backened/listener.py` — microphone capture and speech transcription
- `backened/speak.py` — text-to-speech functionality
- `backened/server.py` — optional Flask status API for frontend integration
- `frontend/package.json` — frontend dependencies and scripts
- `frontend/src/App.jsx` — main React application
- `start_nova.bat` — launch helper for Windows

## Notes

- The backend loads environment variables from `backened/.env`.
- If audio capture fails on Windows, ensure microphone access is enabled and relevant drivers are installed.
- The frontend runs on Vite and uses React 19 with Three.js.
- `backened/server.py` is optional and can be used when you want a local API dashboard or UI status endpoint.
