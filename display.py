import tkinter as tk

def create_popup():
    # Create a small pop-up window
    popup = tk.Toplevel()
    popup.geometry("200x100")  # Adjust size of the pop-up
    popup.overrideredirect(True)  # Removes the title bar
    popup.configure(bg="lightyellow")
    
    # Get screen dimensions
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    
    # Position the pop-up at the left bottom of the screen
    x = 10  # 10 pixels from the left edge
    y = screen_height - 120  # Offset from the bottom (100 height + 20 padding)
    popup.geometry(f"200x100+{x}+{y}")
    
    # Initialize the count variable
    count = -1
    
    # Create the label to display the count
    label = tk.Label(popup, text=f"Count: {count}", font=("Arial", 12), bg="lightyellow", anchor="w")
    label.pack(padx=10, pady=10)

    # Function to update the count
    def update_count():
        nonlocal count
        count += 1
        label.config(text=f"Count: {count}")
        
        # Call this function again after 3 seconds
        popup.after(300, update_count)
    
    # Start the count increment after 3 seconds
    update_count()

    # Automatically close the popup and stop the script after 10 seconds
    popup.after(10000, lambda: (popup.destroy(), window.destroy()))

# Main application window
window = tk.Tk()
window.withdraw()  # Hide the main window

# Show the notification
create_popup()

# Run the event loop
window.mainloop()
