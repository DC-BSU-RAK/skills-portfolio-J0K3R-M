# Exercise 3 - Student Manager

import tkinter as tk
from tkinter import ttk, messagebox

# File path
FILE_PATH = r"C:\Users\minha\OneDrive\Documents\GitHub\skills-portfolio-J0K3R-M\Assessment 1 - Skills Portfolio\A1 - Resources\A1-Solutions\EX3- student manager\studentMarks.txt"

# student data 
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

# grading function
def get_grade(p):
    if p >= 70: return "A"
    elif p >= 60: return "B"
    elif p >= 50: return "C"
    elif p >= 40: return "D"
    else: return "F"

# table helpers
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

# action handlers
def view_all():
    fill_table(students)
    hide_search()

def show_highest():
    best = max(students, key=lambda s: s["percentage"])
    fill_table([best])
    hide_search()

def show_lowest():
    worst = min(students, key=lambda s: s["percentage"])
    fill_table([worst])
    hide_search()

def view_individual():
    # Show search bar when this button is clicked
    search_frame.pack(fill="x", padx=10, pady=5)

def search_student():
    query = search_entry.get().strip().lower()
    if not query:
        messagebox.showwarning("Warning", "Please enter a student code or name.")
        return
    results = [s for s in students if s["code"] == query or s["name"].lower() == query]
    if results:
        fill_table(results)
    else:
        messagebox.showerror("Error", "Student not found!")

def hide_search():
    # Hide search bar when not needed
    search_frame.pack_forget()

# setting up the gui
root = tk.Tk()
root.title("Student Manager")
root.geometry("950x500")
root.configure(bg="#e6f2ff")  # light background

# Sidebar Frame
sidebar = tk.Frame(root, bg="#22263d", width=200)
sidebar.pack(side="left", fill="y")

# Main Frame
main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(side="right", fill="both", expand=True)

# Sidebar Buttons
btn_style = {"font": ("Arial", 12, "bold"), "bg": "#444c63", "fg": "white", "width": 20, "height": 2}
tk.Button(sidebar, text="View All Records", command=view_all, **btn_style).pack(pady=10)
tk.Button(sidebar, text="View Individual Record", command=view_individual, **btn_style).pack(pady=10)
tk.Button(sidebar, text="Show Highest Score", command=show_highest, **btn_style).pack(pady=10)
tk.Button(sidebar, text="Show Lowest Score", command=show_lowest, **btn_style).pack(pady=10)

# Search Bar Frame (initially hidden)
search_frame = tk.Frame(main_frame, bg="#f0f0f0")
tk.Label(search_frame, text="Search Student:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
search_entry.pack(side="left", padx=5)
tk.Button(search_frame, text="Search", command=search_student, font=("Arial", 12), bg="#0066cc", fg="white").pack(side="left", padx=5)

# Table in Main Frame
columns = ("Code", "Name", "Coursework", "Exam", "Percentage", "Grade")
table = ttk.Treeview(main_frame, columns=columns, show="headings")

# Style the table
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), anchor="center")
style.configure("Treeview", font=("Arial", 11), rowheight=25)
table.tag_configure("evenrow", background="#f9f9f9")
table.tag_configure("oddrow", background="#ffffff")

# Add headings
for col in columns:
    table.heading(col, text=col, anchor="center")
    table.column(col, width=120, anchor="center")

table.pack(fill="both", expand=True, padx=10, pady=10)

# Load data
students = load_students()

root.mainloop()
