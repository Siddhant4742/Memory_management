import tkinter as tk
import subprocess
import time
import psutil
import threading

# Configuration
MEMORY_LIMIT_MB = 3000  # Set memory limit in MB
CHECK_INTERVAL = 1  # Check every second

# Mapping of known window titles to app names
WINDOW_TO_APP_NAME = {
    "Google Chrome": "chrome",
    "Visual Studio Code": "code",
}

def get_focused_window():
    """Get the application name of the currently focused window."""
    try:
        # Get the window ID of the focused window
        focused_window_id = subprocess.getoutput("xprop -root _NET_ACTIVE_WINDOW | awk -F' ' '{print $5}'").strip()

        # Check if the window ID is valid (non-zero)
        if focused_window_id != "0x0":
            # Get the window's name (title)
            focused_window_name = subprocess.getoutput(f"xprop -id {focused_window_id} | grep 'WM_NAME' | sed 's/WM_NAME(UTF8_STRING) = \"//g' | sed 's/\"//g'")
            return focused_window_name
        else:
            return None
    except Exception as e:
        return None

def get_processes_by_name(app_name):
    """Find all processes matching the application name."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():  # Case-insensitive match
            processes.append(proc)
    return processes

def monitor_memory(popup, label):
    """Monitor the combined memory usage of all processes matching the app name."""
    while True:
        try:
            # Get the focused window app name
            focused_window_name = get_focused_window()

            if focused_window_name is None:
                label.config(text="No focused window")
                time.sleep(CHECK_INTERVAL)
                continue

            # Map the focused window to an app name
            app_name = None
            for window_title, mapped_app_name in WINDOW_TO_APP_NAME.items():
                if window_title in focused_window_name:
                    app_name = mapped_app_name
                    break

            if not app_name:
                label.config(text="No tracked app in focus")
                time.sleep(CHECK_INTERVAL)
                continue

            # Get processes for the mapped application
            processes = get_processes_by_name(app_name)

            if not processes:
                label.config(text=f"No processes for {app_name}")
                time.sleep(CHECK_INTERVAL)
                continue

            # Calculate total memory usage
            total_memory_usage_mb = sum(
                proc.memory_info().rss / (1024 * 1024) for proc in processes
            )

            # Update the label with memory usage
            label.config(text=f"{app_name}: {total_memory_usage_mb:.2f} MB")

            time.sleep(CHECK_INTERVAL)

        except psutil.NoSuchProcess:
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            label.config(text=f"Error: {str(e)}")
            break

def create_popup():
    """Create a pop-up window to display memory usage."""
    popup = tk.Toplevel()
    popup.geometry("300x100")  # Adjust size of the pop-up
    popup.overrideredirect(True)  # Removes the title bar
    popup.configure(bg="lightyellow")

    # Get screen dimensions
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Position the pop-up at the left bottom of the screen
    x = 10  # 10 pixels from the left edge
    y = screen_height - 120  # Offset from the bottom (100 height + 20 padding)
    popup.geometry(f"300x100+{x}+{y}")

    # Add a label to display the notification message
    label = tk.Label(popup, text="Initializing...", font=("Arial", 12), bg="lightyellow", anchor="w")
    label.pack(padx=10, pady=10)

    # Start the memory monitoring in a separate thread
    threading.Thread(target=monitor_memory, args=(popup, label), daemon=True).start()

    return popup

if __name__ == "__main__":
    # Main application window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create and display the pop-up
    create_popup()

    # Run the event loop
    root.mainloop()
