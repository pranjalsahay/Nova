from flask import Flask, jsonify, request
from flask_cors import CORS

from state import assistant_state
from ai import ask_nova
from actions import perform_action

app = Flask(__name__)

# Allow frontend connection
CORS(app)

# NOTE: pyttsx3 removed — the React frontend already handles TTS via the
# Web Speech API (SpeechSynthesisUtterance). Running pyttsx3's
# engine.runAndWait() inside a Flask route blocks the HTTP response until
# the audio finishes playing, so the frontend never gets its reply.
# It also crashes with Flask's debug-mode reloader thread.


@app.route("/status")
def get_status():
    return jsonify(assistant_state)

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    text = data.get("command", "")

    assistant_state["status"] = "Thinking"
    assistant_state["last_command"] = text

    action = perform_action(text)

    if action:
        response = action
    else:
        response = ask_nova(text)

    assistant_state["status"] = "Speaking"
    assistant_state["last_response"] = response

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    # use_reloader=False prevents pyttsx3-style threading issues if you ever
    # re-add background audio; safe to keep regardless.
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)