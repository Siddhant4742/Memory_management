import time
import pyautogui
import pygetwindow

def get_active_window_title():
    """
    Gets the title of the currently active window.

    Returns:
        str: The title of the active window.
    """
    try:
        active_window = pygetwindow.getActiveWindow()
        if active_window:
            return active_window.title
        else:
            return "No active window found."
    except Exception as e:
        print(f"Error getting active window: {e}")
        return "Error getting active window."

if __name__ == "__main__":
    while True:
        active_window_title = get_active_window_title()
        print(f"Active Window: {active_window_title}")
        time.sleep(1)  # Print every second