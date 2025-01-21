import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, amount REAL, category TEXT)")
conn.commit()

def add_expense(amount, category):
    cur.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
    conn.commit()

def view_expenses():
    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def visualize_expenses():
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cur.fetchall()
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.show()

while True:
    action = input("Choose action: add/view/visualize/exit: ")
    if action == "add":
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        add_expense(amount, category)
    elif action == "view":
        view_expenses()
    elif action == "visualize":
        visualize_expenses()
    elif action == "exit":
        break
conn.close()
