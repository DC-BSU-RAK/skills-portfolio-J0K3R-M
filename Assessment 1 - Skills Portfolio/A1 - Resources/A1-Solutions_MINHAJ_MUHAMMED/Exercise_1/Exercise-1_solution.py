import tkinter as tk
from tkinter import messagebox
import random

# Global variables
score = 0
question_count = 0
first_try = True
difficulty = None
num1 = num2 = 0
operation = ''

# Difficulty ranges
difficulty_ranges = {
    1: (1, 9),
    2: (10, 99),
    3: (1000, 9999)
}

# Functions
def displayMenu():
    clearWindow()
    tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="1. Easy", command=lambda: startQuiz(1)).pack(pady=5)
    tk.Button(root, text="2. Moderate", command=lambda: startQuiz(2)).pack(pady=5)
    tk.Button(root, text="3. Advanced", command=lambda: startQuiz(3)).pack(pady=5)

def randomInt(level):
    return random.randint(*difficulty_ranges[level])

def decideOperation():
    return random.choice(['+', '-'])

def displayProblem():
    global num1, num2, operation, first_try
    clearWindow()
    first_try = True
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()
    tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Arial", 16)).pack(pady=10)
    answer_entry.pack()
    submit_btn.pack()

def isCorrect():
    global score, question_count, first_try
    try:
        user_answer = int(answer_entry.get())
        correct_answer = num1 + num2 if operation == '+' else num1 - num2
        if user_answer == correct_answer:
            if first_try:
                score += 10
                messagebox.showinfo("Correct!", "Great job! +10 points")
            else:
                score += 5
                messagebox.showinfo("Correct!", "Correct on second try! +5 points")
            question_count += 1
            answer_entry.delete(0, tk.END)
            if question_count < 10:
                displayProblem()
            else:
                displayResults()
        else:
            if first_try:
                first_try = False
                messagebox.showwarning("Try Again", "Incorrect. Try once more.")
                answer_entry.delete(0, tk.END)
            else:
                question_count += 1
                messagebox.showinfo("Incorrect", "Incorrect again. Moving to next question.")
                answer_entry.delete(0, tk.END)
                if question_count < 10:
                    displayProblem()
                else:
                    displayResults()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def displayResults():
    clearWindow()
    tk.Label(root, text=f"Final Score: {score}/100", font=("Arial", 16)).pack(pady=10)
    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D"
    tk.Label(root, text=f"Grade: {grade}", font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="Play Again", command=resetQuiz).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack()

def startQuiz(level):
    global difficulty, score, question_count
    difficulty = level
    score = 0
    question_count = 0
    displayProblem()

def resetQuiz():
    answer_entry.delete(0, tk.END)
    displayMenu()

def clearWindow():
    for widget in root.winfo_children():
        widget.pack_forget()

# GUI setup
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("300x250")

# Entry and button (used in multiple places)
answer_entry = tk.Entry(root)
submit_btn = tk.Button(root, text="Submit", command=isCorrect)

# Start screen with image title
tk.Label(root, text="MATH QUIZ", font=("Comic Sans MS", 20, "bold")).pack(pady=20)
tk.Button(root, text="Start Quiz", command=displayMenu).pack(pady=10)

root.mainloop()
