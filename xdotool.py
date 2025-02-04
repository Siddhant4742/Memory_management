import subprocess
import time
import os

def get_active_window_info():
    """Get the active window ID, title, and full application name."""
    try:
        # Get the active window ID
        window_id = subprocess.run(
            ["xdotool", "getactivewindow"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Get the window title
        window_title = subprocess.run(
            ["xdotool", "getwindowname", window_id],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Get the process ID (PID) of the window
        pid = subprocess.run(
            ["xdotool", "getwindowpid", window_id],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Get the full process name using `ps -o args=`
        process_args = subprocess.run(
            ["ps", "-p", pid, "-o", "args="],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Extract the process name (first part of the command)
        process_name = os.path.basename(process_args.split()[0])

        return window_id, window_title, process_name
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, None, None

def monitor_active_window(interval=1):
    """Continuously monitor the active window and print changes."""
    last_window_id = None
    last_window_title = None
    last_process_name = None

    print("Monitoring active window. Press Ctrl+C to stop...")
    try:
        while True:
            window_id, window_title, process_name = get_active_window_info()
            if window_id and window_title and process_name:
                # if (window_id != last_window_id or
                #     window_title != last_window_title or
                #     process_name != last_process_name):
                print(f"Active Window ID: {window_id}, Title: {window_title}, App: {process_name}")
                    # last_window_id = window_id
                    # last_window_title = window_title
                    # last_process_name = process_name
            time.sleep(interval)  # Wait for the specified interval
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    # Start monitoring with a 1-second interval
    monitor_active_window(interval=1)