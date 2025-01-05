import tkinter as tk
from tkinter import messagebox, scrolledtext

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_and_composite_numbers(start, end):
    """Return two lists: one of prime numbers and one of composite numbers within a given range."""
    prime_numbers = []
    composite_numbers = []

    for num in range(start, end + 1):
        if is_prime(num):
            prime_numbers.append(num)
        elif num > 1:
            composite_numbers.append(num)
    
    return prime_numbers, composite_numbers

def display_numbers():
    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
        if start > end:
            messagebox.showerror("Error", "Start value should be less than or equal to the end value.")
            return

        primes, composites = prime_and_composite_numbers(start, end)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, f"Prime Numbers between {start} and {end}:\n")
        text_area.insert(tk.END, f"{primes}\n\n")
        text_area.insert(tk.END, f"Composite Numbers between {start} and {end}:\n")
        text_area.insert(tk.END, f"{composites}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for the range.")

# Create the main window
window = tk.Tk()
window.title("Prime and Composite Numbers Finder")

# Create and place labels, entries, and buttons
label_start = tk.Label(window, text="Start:")
label_start.grid(row=0, column=0, padx=10, pady=10)

entry_start = tk.Entry(window)
entry_start.grid(row=0, column=1, padx=10, pady=10)

label_end = tk.Label(window, text="End:")
label_end.grid(row=1, column=0, padx=10, pady=10)

entry_end = tk.Entry(window)
entry_end.grid(row=1, column=1, padx=10, pady=10)

btn_display = tk.Button(window, text="Find Numbers", command=display_numbers)
btn_display.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create a text area to display results
text_area = scrolledtext.ScrolledText(window, width=50, height=15)
text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI main loop
window.mainloop()
