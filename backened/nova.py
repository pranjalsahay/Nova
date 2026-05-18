from listener import listen
from speak import speak
from ai import ask_nova, is_draw_request, generate_image
from actions import perform_action
from state import assistant_state
import time


WAKE_WORDS = ["hello"]
EXIT_WORDS = ["sleep", "bye", "goodbye", "stop", "go to sleep"]

POST_SPEAK_DELAY = 0.8
MAX_RETRIES      = 2   # how many times Nova asks "will you say that again?"

def is_wake_word(text):
    return any(w in text for w in WAKE_WORDS)

def is_exit_word(text):
    return any(w in text for w in EXIT_WORDS)

def _speak_and_wait(text):
    speak(text)
    time.sleep(POST_SPEAK_DELAY)

def listen_with_retry(is_wake=False) -> str:
    """
    Listen and if nothing heard, ask the user to repeat.
    For wake word: just keep looping silently (don't ask to repeat).
    For commands: ask up to MAX_RETRIES times then give up.
    """
    if is_wake:
        # Silent loop waiting for wake word — no retry prompts
        while True:
            text = listen()
            if text:
                return text

    else:
        # Command mode — prompt to repeat if not heard
        text = listen()
        if text:
            return text

        for attempt in range(MAX_RETRIES):
            if attempt == 0:
                _speak_and_wait("Sorry, I didn't catch that. Will you say it again?")
            else:
                _speak_and_wait("I still couldn't hear you. Please try once more.")
            text = listen()
            if text:
                return text

        _speak_and_wait("I'm having trouble hearing you. Please check your microphone.")
        return ""

def main():
    print("\n" + "=" * 40)
    print("       NOVA AI ASSISTANT ONLINE")
    print("=" * 40 + "\n")

    _speak_and_wait("Nova is online. Say hello to wake me up.")

    while True:
        assistant_state["status"] = "Listening for wake word..."
        wake_text = listen_with_retry(is_wake=True)

        if not is_wake_word(wake_text):
            continue

        assistant_state["status"] = "Awake"
        _speak_and_wait("Yes, I am listening.")

        conversation_history = []

        while True:
            assistant_state["status"] = "Listening..."
            command = listen_with_retry(is_wake=False)

            # If still nothing after retries, go back to wake word mode
            if not command:
                assistant_state["status"] = "Idle"
                _speak_and_wait("Going back to sleep. Say hello to wake me again.")
                break

            assistant_state["last_command"] = command
            print(f"[Nova] Command: {command}")

            if is_exit_word(command):
                assistant_state["status"] = "Idle"
                _speak_and_wait("Going to sleep. Say hello when you need me.")
                break

            action_result = perform_action(command)
            if action_result:
                assistant_state["status"] = "Speaking..."
                assistant_state["last_response"] = action_result
                _speak_and_wait(action_result)
                conversation_history.append({"role": "user",      "content": command})
                conversation_history.append({"role": "assistant", "content": action_result})
                continue

            if is_draw_request(command):
                assistant_state["status"] = "Drawing..."
                _speak_and_wait("Sure, let me generate that for you.")
                result = generate_image(command)
                assistant_state["status"] = "Speaking..."
                assistant_state["last_response"] = result
                _speak_and_wait(result)
                conversation_history.append({"role": "user",      "content": command})
                conversation_history.append({"role": "assistant", "content": result})
                continue

            assistant_state["status"] = "Thinking..."
            response = ask_nova(command, conversation_history)

            assistant_state["status"] = "Speaking..."
            assistant_state["last_response"] = response
            _speak_and_wait(response)

            conversation_history.append({"role": "user",      "content": command})
            conversation_history.append({"role": "assistant", "content": response})

            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Nova] Shutting down. Goodbye!")