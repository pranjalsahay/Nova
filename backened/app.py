from flask import Flask, jsonify, request
from flask_cors import CORS
from state import assistant_state
from actions import perform_action
from ai import ask_nova
import threading
import time

app = Flask(__name__)

CORS(app)

# =========================
# STATUS ROUTE
# =========================
@app.route("/status")
def get_status():
    return jsonify(assistant_state)


# =========================
# COMMAND ROUTE
# =========================
@app.route("/command", methods=["POST"])
def command():

    data = request.json
    user_command = data.get("command", "")

    print("User Command:", user_command)

    # Update UI state
    assistant_state["status"] = "Thinking..."

    # =========================
    # FIRST CHECK ACTIONS
    # =========================
    action_result = perform_action(user_command)

    if action_result:

        assistant_state["status"] = "Speaking..."

        return jsonify({
            "response": action_result
        })

    # =========================
    # OTHERWISE USE AI
    # =========================
    try:
        ai_response = ask_nova(user_command)

        assistant_state["status"] = "Speaking..."

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        print("AI Error:", e)

        assistant_state["status"] = "Idle"

        return jsonify({
            "response":
            "Something went wrong."
        })


# =========================
# OPTIONAL STATUS LOOP
# =========================
def assistant_loop():

    while True:

        if assistant_state["status"] == "":
            assistant_state["status"] = "Idle"

        time.sleep(1)


# =========================
# START
# =========================
thread = threading.Thread(
    target=assistant_loop,
    daemon=True
)

thread.start()

app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)