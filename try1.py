import psutil
import time

# Configuration
APP_NAME = "code"  # Process name for Chrome
MEMORY_LIMIT_MB = 3000#Set memory limit in MB
CHECK_INTERVAL = 1 # Check every 5 seconds


def get_processes_by_name(app_name):
    """Find all processes matching the application name."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():  # Case-insensitive match
            processes.append(proc)
    return processes


def monitor_memory(app_name, memory_limit_mb):
    """Monitor the combined memory usage of all processes matching the app name."""
    print(f"Monitoring total memory usage of '{app_name}' processes...")

    while True:
        try:
            processes = get_processes_by_name(app_name)
            if not processes:
                print(f"Error: No processes found for '{app_name}'.")
                break

            # Calculate total memory usage
            total_memory_usage_mb = sum(
                proc.memory_info().rss / (1024 * 1024) for proc in processes
            )

            if total_memory_usage_mb > memory_limit_mb:
                print(
                    f"Warning: Total memory usage of '{app_name}' processes is {total_memory_usage_mb:.2f} MB, "
                    f"exceeding the limit of {memory_limit_mb} MB!"
                )
            else:
                print(
                    f"'{app_name}' processes are within memory limits: {total_memory_usage_mb:.2f} MB used."
                )
            time.sleep(CHECK_INTERVAL)
        except psutil.NoSuchProcess:
            print(f"A process terminated during monitoring.")
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    monitor_memory(APP_NAME, MEMORY_LIMIT_MB)
