import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# File location (your path)
FILE_PATH = r"C:\Users\minha\OneDrive\Documents\GitHub\skills-portfolio-J0K3R-M\Assessment 1 - Skills Portfolio\A1 - Resources\A1-Solutions\EX3- student manager\studentMarks.txt"

# ---------- Load Students ----------
def load_students(filename=FILE_PATH):
    students = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines[1:]:  # skip first line (count)
        parts = line.strip().split(",")
        if len(parts) == 6:
            code, name, c1, c2, c3, exam = parts
            coursework = int(c1) + int(c2) + int(c3)
            total = coursework + int(exam)
            percentage = (total / 160) * 100
            grade = get_grade(percentage)
            students.append({
                "code": code,
                "name": name,
                "coursework": coursework,
                "exam": int(exam),
                "percentage": percentage,
                "grade": grade
            })
    return students

# ---------- Grade Function ----------
def get_grade(p):
    if p >= 70: return "A"
    elif p >= 60: return "B"
    elif p >= 50: return "C"
    elif p >= 40: return "D"
    else: return "F"

# ---------- Table Helpers ----------
def clear_table():
    for row in table.get_children():
        table.delete(row)

def fill_table(data):
    clear_table()
    for i, s in enumerate(data):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        table.insert("", tk.END, values=(
            s["code"], s["name"], s["coursework"], s["exam"],
            f"{s['percentage']:.2f}", s["grade"]
        ), tags=(tag,))

# ---------- Menu Actions ----------
def view_all():
    fill_table(students)

def view_individual():
    code = simpledialog.askstring("Search", "Enter student code or name:")
    if not code: return
    for s in students:
        if s["code"] == code or s["name"].lower() == code.lower():
            fill_table([s])
            return
    messagebox.showerror("Error", "Student not found!")

def show_highest():
    best = max(students, key=lambda s: s["percentage"])
    fill_table([best])

def show_lowest():
    worst = min(students, key=lambda s: s["percentage"])
    fill_table([worst])

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Student Manager")
root.configure(bg="#cce7ff")  # light blue background

# Menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)
menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=menu)
menu.add_command(label="1. View all records", command=view_all)
menu.add_command(label="2. View individual record", command=view_individual)
menu.add_command(label="3. Show highest score", command=show_highest)
menu.add_command(label="4. Show lowest score", command=show_lowest)

# Table design
columns = ("Code", "Name", "Coursework", "Exam", "Percentage", "Grade")
table = ttk.Treeview(root, columns=columns, show="headings")

# Style the table
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), anchor="center")
style.configure("Treeview", font=("Arial", 11), rowheight=25)

# Add striped row colors
table.tag_configure("evenrow", background="#f2f2f2")  # light gray
table.tag_configure("oddrow", background="#ffffff")   # white

# Add headings
for col in columns:
    table.heading(col, text=col, anchor="center")
    table.column(col, width=120, anchor="center")

table.pack(fill="both", expand=True, padx=10, pady=10)

# Load data
students = load_students()

root.mainloop()
