import tkinter as tk

def click(event):
    global sc_var
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(sc_var.get())
            sc_var.set(result)
        except Exception:
            sc_var.set("Error")
    elif text == "C":
        sc_var.set("")
    else:
        sc_var.set(sc_var.get() + text)

root = tk.Tk()
root.title("Calculator")
sc_var = tk.StringVar()
sc_var.set("")
entry = tk.Entry(root, textvar=sc_var, font=("Arial", 20), relief=tk.SUNKEN)
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    '7', '8', '9', '/', '4', '5', '6', '*',
    '1', '2', '3', '-', 'C', '0', '=', '+'
]

for i, button in enumerate(buttons):
    b = tk.Button(root, text=button, font=("Arial", 20), relief=tk.RAISED)
    b.grid(row=1 + i // 4, column=i % 4)
    b.bind("<Button-1>", click)

root.mainloop()
