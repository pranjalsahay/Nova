import mss
import cv2
import numpy as np
import pytesseract
from PIL import Image


# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def capture_screen():
    """Take screenshot of current screen"""

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        img = np.array(screenshot)

        return cv2.cvtColor(
            img,
            cv2.COLOR_BGRA2BGR
        )


def read_screen_text():
    """Read text from screen"""

    frame = capture_screen()

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    text = pytesseract.image_to_string(gray)

    if text.strip():
        return text[:700]

    return "I could not read anything on screen."


def detect_error():
    """Try to read error text"""

    text = read_screen_text()

    error_words = [
        "error",
        "failed",
        "exception",
        "warning",
        "traceback"
    ]

    for word in error_words:
        if word.lower() in text.lower():
            return f"I found an error:\n{text}"

    return "I could not detect an error."