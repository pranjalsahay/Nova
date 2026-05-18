"""
Nova AI Assistant
Install:

pip install ollama openai
"""

import os
import re
import webbrowser
import urllib.request

from ollama import chat


# ==================================================
# LOAD .ENV
# ==================================================

def load_env():

    env_path = os.path.join(
        os.path.dirname(__file__),
        ".env"
    )

    if os.path.exists(env_path):

        with open(env_path) as f:

            for line in f:

                line = line.strip()

                if "=" in line and not line.startswith("#"):

                    key, _, val = line.partition("=")

                    os.environ[key.strip()] = val.strip()


load_env()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are Nova, a smart helpful AI voice assistant.

Rules:
Keep responses short.
Maximum 2 to 4 sentences.
Speak naturally.
No markdown.
Friendly and confident.
"""


# ==================================================
# IMAGE GENERATION
# ==================================================

DRAW_TRIGGERS = [

    "draw",
    "generate image",
    "create image",
    "make image",
    "paint",
    "sketch",
    "illustrate",
    "show me a picture of",
    "show me a drawing of"
]


def is_draw_request(command):

    return any(
        t in command.lower()
        for t in DRAW_TRIGGERS
    )


def extract_image_prompt(command):

    cmd = command.lower()

    for trigger in sorted(
        DRAW_TRIGGERS,
        key=len,
        reverse=True
    ):

        if trigger in cmd:

            cmd = cmd.replace(
                trigger,
                ""
            ).strip()

            break

    return cmd


def generate_image(command):

    try:

        from openai import OpenAI

        oa = OpenAI(
            api_key=OPENAI_API_KEY
        )

        subject = extract_image_prompt(
            command
        )

        print(
            f"[Nova] Generating: {subject}"
        )

        response = oa.images.generate(
            model="dall-e-3",
            prompt=subject,
            size="1024x1024",
            n=1
        )

        image_url = (
            response.data[0].url
        )

        save_path = os.path.join(
            os.path.dirname(__file__),
            "nova_image.png"
        )

        urllib.request.urlretrieve(
            image_url,
            save_path
        )

        webbrowser.open(
            f"file:///{save_path}"
        )

        return (
            f"Image created for {subject}"
        )

    except Exception as e:

        print(
            f"[Image Error] {e}"
        )

        return (
            "Could not create image."
        )


# ==================================================
# EXTRACT REPLY — handles old dict + new object API
# ==================================================

def _extract_reply(response) -> str:
    """
    The ollama Python package changed its response format.
    Older versions  → response["message"]["content"]  (dict)
    Newer versions  → response.message.content         (object)
    This helper handles both safely.
    """
    try:
        # New object-style (ollama >= 0.2)
        return response.message.content
    except AttributeError:
        pass

    try:
        # Old dict-style
        return response["message"]["content"]
    except (KeyError, TypeError):
        pass

    # Last resort — stringify whatever came back
    return str(response)


# ==================================================
# MAIN FUNCTION
# ==================================================

def ask_nova(
    prompt,
    conversation_history=None
):

    try:

        if is_draw_request(prompt):

            return generate_image(
                prompt
            )

        messages = [

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            }

        ]

        if conversation_history:

            messages.extend(
                conversation_history
            )

        messages.append(

            {
                "role":"user",
                "content":prompt
            }

        )

        response = chat(
            model="llama3.2",
            messages=messages
        )

        # ── FIX: use helper instead of response["message"]["content"] ──
        reply = _extract_reply(response)

        reply = re.sub(
            r"[*_`#]",
            "",
            reply
        )

        reply = re.sub(
            r"\n+",
            " ",
            reply
        )

        return reply


    except Exception as e:

        # Print the REAL error so you can see what's wrong
        print(f"[AI Error] {type(e).__name__}: {e}")

        # Give a more helpful message if Ollama isn't running
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            return (
                "I cannot reach Ollama. "
                "Please run: ollama serve"
            )

        return (
            "Sorry, something went wrong."
        )


# ==================================================
# TEST MODE
# ==================================================

if __name__ == "__main__":

    print("\nNova started")
    print("Type exit to quit\n")

    while True:

        user = input(
            "You: "
        )

        if user.lower()=="exit":

            break

        answer = ask_nova(
            user
        )

        print(
            "\nNova:",
            answer,
            "\n"
        )