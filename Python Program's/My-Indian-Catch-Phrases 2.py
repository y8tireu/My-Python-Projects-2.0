import tkinter as tk
from tkinter import scrolledtext

def start_loop():
    global running, count
    count = 0
    running = True
    update_text()

def stop_loop():
    global running
    running = False

def update_text():
    global count
    if running and count < 100000:  # Change 100000 to desired repetitions
        text_area.insert(tk.END, "Amuku Damkuka Amkuku Dumal Attam pota Attam Pota Pakka Pushpa Addadey pushpa enna thotu ey thumbi poda attam pota pakka pushpa adadey ")
        text_area.see(tk.END)  # Auto-scroll to the end
        count += 1
        root.after(10, update_text)  # Adjust the delay if needed (in milliseconds)

# Initialize the main window
root = tk.Tk()
root.title("Amuku Dumal")

# Create a text area to display the output
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack(padx=10, pady=10)

# Create start and stop buttons
start_button = tk.Button(root, text="Start", command=start_loop)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_loop)
stop_button.pack(side=tk.LEFT, padx=10, pady=10)

# Initialize loop control variable
running = False
count = 0

# Run the Tkinter event loop
root.mainloop()
