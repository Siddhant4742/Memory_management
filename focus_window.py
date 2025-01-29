import subprocess
import time

while True:
    # Get the window ID of the focused window
    focused_window_id = subprocess.getoutput("xprop -root _NET_ACTIVE_WINDOW | awk -F' ' '{print $5}'").strip()

    # Check if the window ID is valid (non-zero)
    if focused_window_id != "0x0":
        # Get the window's name (title)
        focused_window_name = subprocess.getoutput(f"xprop -id {focused_window_id} | grep 'WM_NAME' | sed 's/WM_NAME(STRING) = \"//g' | sed 's/\"//g'")

        # Display the application in focus
        print(f"The application in focus is: {focused_window_name}")
    else:
        print("No valid window is currently in focus.")
    
    # Sleep for 1 second before checking again
    time.sleep(1)
