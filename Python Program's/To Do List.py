import sqlite3

def create_table():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def list_tasks():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    for row in rows:
        print(row[1])
    conn.close()

create_table()
while True:
    action = input("Choose action: add/list/exit: ")
    if action == "add":
        task = input("Enter task: ")
        add_task(task)
    elif action == "list":
        list_tasks()
    elif action == "exit":
        break
    else:
        print("Invalid option")
