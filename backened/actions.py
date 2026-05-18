import os
import sys
import webbrowser
from urllib.parse import quote
from vision import read_screen_text, detect_error
from memory import (
    save_personal_memory,
    get_personal_memory,
    get_all_memory
)


def _open_app(win_cmd, mac_cmd, linux_cmd):
    """Open native app cross-platform."""
    if sys.platform == "win32":
        os.system(win_cmd)
    elif sys.platform == "darwin":
        os.system(mac_cmd)
    else:
        os.system(linux_cmd)

def perform_action(command):
    """
    Check if command matches known actions.
    Returns confirmation string if handled,
    None if not handled.
    """
    cmd = command.lower().strip()

    # ─────────────────────────────────────────
    # PERSONAL MEMORY
    # ─────────────────────────────────────────

    # Remember something
    if cmd.startswith("remember "):

        text = cmd.replace(
            "remember",
            "",
            1
        ).strip()

        if " is " in text:

            key, value = text.split(
                " is ",
                1
            )

            key = key.strip()
            value = value.strip()

            save_personal_memory(
                key,
                value
            )

            return (
                f"I will remember that "
                f"{key} is {value}"
            )

        return (
            "Say it like this: "
            "Remember favorite editor is VS Code"
        )

    # Recall memory
    if (
        cmd.startswith("what is ")
        or cmd.startswith("who is ")
    ):

        key = (
            cmd.replace("what is ", "")
            .replace("who is ", "")
            .strip()
        )

        memory = get_personal_memory(key)

        if memory:
            return f"{key} is {memory}"

    # Show all memory
    if (
        "what do you know about me" in cmd
        or "show personal memory" in cmd
    ):

        memories = get_all_memory()

        if not memories:
            return (
                "I don't know anything "
                "about you yet."
            )

        result = (
            "Here is what I know "
            "about you. "
        )

        for key, value in memories:
            result += (
                f"{key} is {value}. "
            )

        return result

    # ─────────────────────────────────────────
    # YOUTUBE PLAY / SEARCH
    # ─────────────────────────────────────────
    if cmd.startswith("play "):
        search = cmd.replace("play", "", 1).strip()
        webbrowser.open(
            "https://www.youtube.com/results?search_query="
            + quote(search)
        )
        return f"Playing {search} on YouTube"

    # ─────────────────────────────────────────
    # OPEN WEBSITES
    # ─────────────────────────────────────────
    sites = {
        "open youtube": "https://youtube.com",
        "open google": "https://google.com",
        "open whatsapp": "https://web.whatsapp.com",
        "open gmail": "https://mail.google.com",
        "open chatgpt": "https://chat.openai.com",
        "open github": "https://github.com",
        "open netflix": "https://netflix.com",
        "open twitter": "https://twitter.com",
        "open instagram": "https://instagram.com",
        "open reddit": "https://reddit.com",
    }

    for phrase, url in sites.items():
        if phrase in cmd:
            webbrowser.open(url)
            return f"Opening {phrase.replace('open ', '').title()}"

    # GOOGLE SEARCH
    if cmd.startswith("search "):
        query = cmd.replace("search", "", 1).strip()
        webbrowser.open(
            "https://www.google.com/search?q="
            + quote(query)
        )
        return f"Searching Google for {query}"

    # OPEN CHROME
    if "open chrome" in cmd:
        _open_app(
            "start chrome",
            "open -a 'Google Chrome'",
            "google-chrome &"
        )
        return "Opening Chrome"

    # OPEN VS CODE
    if "open vs code" in cmd or "open vscode" in cmd:
        os.system("code")
        return "Opening VS Code"

    # OPEN SPOTIFY
    if "open spotify" in cmd:
        _open_app(
            "start spotify",
            "open -a Spotify",
            "spotify &"
        )
        return "Opening Spotify"

    # OPEN FILE EXPLORER
    if "open file explorer" in cmd:
        _open_app(
            "explorer",
            "open .",
            "xdg-open . &"
        )
        return "Opening File Explorer"

    # OPEN NOTEPAD
    if "open notepad" in cmd:
        _open_app(
            "notepad",
            "open -a TextEdit",
            "gedit &"
        )
        return "Opening Notepad"

    # SCREENSHOT
    if "take screenshot" in cmd or "screenshot" in cmd:
        _open_app(
            "snippingtool",
            "screencapture -i ~/Desktop/screenshot.png",
            "scrot ~/Desktop/screenshot.png"
        )
        return "Taking a screenshot"

    # SHUTDOWN
    if (
        "shutdown computer" in cmd
        or "shutdown pc" in cmd
    ):
        _open_app(
            "shutdown /s /t 5",
            "sudo shutdown -h now",
            "sudo shutdown -h now"
        )
        return "Shutting down your PC in 5 seconds"

    # RESTART
    if (
        "restart computer" in cmd
        or "restart pc" in cmd
    ):
        _open_app(
            "shutdown /r /t 5",
            "sudo shutdown -r now",
            "sudo reboot"
        )
        return "Restarting your PC in 5 seconds"

    # LOCK SCREEN
    if (
        "lock pc" in cmd
        or "lock screen" in cmd
    ):
        if sys.platform == "win32":
            os.system(
                "rundll32.exe user32.dll,LockWorkStation"
            )

        return "Locking your computer"

    # SCREEN VISION
    if (
        "what is on my screen" in cmd
        or "read screen" in cmd
    ):
        return read_screen_text()

    if (
        "read this error" in cmd
        or "check error" in cmd
    ):
        return detect_error()

    return None