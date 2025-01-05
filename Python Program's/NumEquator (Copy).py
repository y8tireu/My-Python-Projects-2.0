import tkinter as tk
from tkinter import ttk
from sympy import isprime
import webbrowser


# Open GitHub profile
def open_github():
    webbrowser.open("https://github.com/y8tireu")


# Generate equations
def generate_equations():
    try:
        target = int(entry_number.get())
        operation = operation_var.get()
        number_type = number_type_var.get()

        # Validate the input number range
        if target <= 0 or target > 100000:
            raise ValueError("Please enter a number between 1 and 100,000.")

        # Generate numbers based on the type
        numbers = range(1, min(target + 1, 1000))  # Limit range for better performance
        if number_type == "Prime":
            numbers = [num for num in numbers if isprime(num)]
        elif number_type == "Composite":
            numbers = [num for num in numbers if num > 1 and not isprime(num)]

        equations = []
        for x in numbers:
            for y in numbers:
                if operation == "Addition" and x + y == target:
                    equations.append(f"{x} + {y} = {target}")
                elif operation == "Subtraction" and x - y == target:
                    equations.append(f"{x} - {y} = {target}")
                elif operation == "Multiplication" and x * y == target:
                    equations.append(f"{x} x {y} = {target}")
                elif operation == "Division" and y != 0 and abs(x / y - target) < 1e-9:
                    equations.append(f"{x} ÷ {y} = {target:.2f}")

        if not equations:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "No equations found for the given input.")
        else:
            display_equations(equations)
    except ValueError as e:
        tk.messagebox.showerror("Error", str(e))


def display_equations(equations):
    result_text.delete("1.0", tk.END)
    for eq in equations:
        result_text.insert(tk.END, eq + "\n")


# GUI setup
root = tk.Tk()
root.title("Equation Generator")
root.geometry("800x600")
root.configure(bg="black")

# Styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), background="#1e90ff", foreground="white", padding=10)
style.map("TButton", background=[("active", "#4682b4")], foreground=[("active", "white")])
font_label = ("Helvetica", 12, "bold")
font_result = ("Courier", 10)
fg_color = "white"

# Header
header = tk.Label(root, text="Equation Generator", font=("Helvetica", 18, "bold"), fg="white", bg="black")
header.pack(pady=20)

# Input frame
frame_input = tk.Frame(root, bg="black")
frame_input.pack(pady=10)
tk.Label(frame_input, text="Enter a Number (1-100,000):", font=font_label, fg=fg_color, bg="black").grid(row=0, column=0, padx=5)
entry_number = tk.Entry(frame_input, font=font_label, bg="#2b2b2b", fg="white", insertbackground="white", width=10)
entry_number.grid(row=0, column=1, padx=5)

# Number type frame
frame_type = tk.Frame(root, bg="black")
frame_type.pack(pady=10)
tk.Label(frame_type, text="Number Type:", font=font_label, fg=fg_color, bg="black").grid(row=0, column=0, padx=5)
number_type_var = tk.StringVar(value="All")
tk.Radiobutton(frame_type, text="All", variable=number_type_var, value="All", font=font_label, fg=fg_color, bg="black", selectcolor="black").grid(row=0, column=1)
tk.Radiobutton(frame_type, text="Prime", variable=number_type_var, value="Prime", font=font_label, fg=fg_color, bg="black", selectcolor="black").grid(row=0, column=2)
tk.Radiobutton(frame_type, text="Composite", variable=number_type_var, value="Composite", font=font_label, fg=fg_color, bg="black", selectcolor="black").grid(row=0, column=3)

# Operation selection frame
frame_operation = tk.Frame(root, bg="black")
frame_operation.pack(pady=10)
tk.Label(frame_operation, text="Operation:", font=font_label, fg=fg_color, bg="black").grid(row=0, column=0, padx=5)
operation_var = tk.StringVar(value="Addition")
operation_menu = ttk.OptionMenu(frame_operation, operation_var, "Addition", "Addition", "Subtraction", "Multiplication", "Division")
operation_menu.grid(row=0, column=1)

# Buttons
btn_generate = ttk.Button(root, text="Generate Equations", command=generate_equations)
btn_generate.pack(pady=20)

# Results display
result_text = tk.Text(root, wrap="word", height=15, width=70, font=font_result, bg="#2b2b2b", fg="white", insertbackground="white")
result_text.pack(pady=10)

# GitHub Profile Button
btn_github = ttk.Button(root, text="GitHub Profile", command=open_github)
btn_github.place(x=650, y=550)  # Adjusted to fit within the window

# Run the app
root.mainloop()
