from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# Initialize main window
root = Tk()
root.title("Math Quiz")
root.geometry("900x650")
root.resizable(False, False)

# Load background image
bg_image = Image.open("C:\\Users\\minha\\OneDrive\\Documents\\GitHub\\skills-portfolio-J0K3R-M\\Assessment 1 - Skills Portfolio\\A1 - Resources\\A1-Solutions\\EX1-Mathquizz\\Exercise_1\\images\\background.png")  # Ensure this matches your uploaded image filename
bg_photo = ImageTk.PhotoImage(bg_image)

# Global variables
score = 0
question_number = 1
difficulty = ""
right_answer = 0
quiz_running = False

# Function to switch frames
def show_frame(frame):
    for f in all_frames:
        f.place_forget()
    frame.place(relwidth=1, relheight=1)

# Function to generate a math question
def generate_question():
    global right_answer
    if not quiz_running:
        return

    if difficulty == "Easy":
        limit, ops = 10, ["+", "-"]
    elif difficulty == "Moderate":
        limit, ops = 20, ["*", "//"]
    else:
        limit, ops = 60, ["+", "-", "*", "//"]

    a, b = random.randint(1, limit), random.randint(1, limit)
    op = random.choice(ops)
    if op == "//" and b == 0:
        b = 1

    question_label.config(text=f"What is {a} {op} {b}?")
    score_label.config(text=f"Score: {score}")
    right_answer = eval(f"{a}{op}{b}")

# Function to handle answer submission
def submit_answer():
    global score, question_number
    if not quiz_running:
        return

    try:
        ans = int(answer_box.get())
    except ValueError:
        messagebox.showwarning("Oops!", "Please enter a valid number.")
        return

    if ans == right_answer:
        score += 1

    answer_box.delete(0, END)

    if question_number < 5:
        question_number += 1
        generate_question()
    else:
        show_results()

# Start quiz
def start_quiz(level):
    global score, question_number, difficulty, quiz_running
    difficulty = level
    score = 0
    question_number = 1
    quiz_running = True
    show_frame(frame_quiz)
    generate_question()

# Pause quiz
def pause_quiz():
    global quiz_running
    quiz_running = False
    question_label.config(text="Quiz Paused")

# Resume quiz
def resume_quiz():
    global quiz_running
    quiz_running = True
    generate_question()

# Stop quiz
def stop_quiz():
    global quiz_running
    quiz_running = False
    show_results()

# Show final score
def show_results():
    show_frame(frame_score)
    result_label.config(text=f"Your Score: {score} / 5")

# Exit confirmation
def confirm_exit():
    if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
        root.destroy()

# Button hover animation
def on_enter(e):
    e.widget.config(bg="#1f2a44")

def on_leave(e):
    e.widget.config(bg="#2c3e50")

# Create frames
frame_start = Frame(root)
frame_difficulty = Frame(root)
frame_quiz = Frame(root)
frame_score = Frame(root)
all_frames = [frame_start, frame_difficulty, frame_quiz, frame_score]

# Add background to each frame
for frame in all_frames:
    bg_label = Label(frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

# --- Start Frame ---
Label(frame_start, text="Welcome to the Math Quiz!", font=("Arial", 28), fg="white", bg="#2c3e50").pack(pady=150)
btn_start = Button(frame_start, text="Start Quiz", font=("Arial", 18), bg="#2c3e50", fg="white", command=lambda: show_frame(frame_difficulty))
btn_start.pack()
btn_start.bind("<Enter>", on_enter)
btn_start.bind("<Leave>", on_leave)

# --- Difficulty Frame ---
Label(frame_difficulty, text="Choose Difficulty", font=("Arial", 24), fg="white", bg="#2c3e50").pack(pady=80)
for level in ["Easy", "Moderate", "Hard"]:
    btn = Button(frame_difficulty, text=level, font=("Arial", 16), width=20, bg="#2c3e50", fg="white", command=lambda l=level: start_quiz(l))
    btn.pack(pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# --- Quiz Frame ---
question_label = Label(frame_quiz, text="", font=("Arial", 22), fg="white", bg="#2c3e50")
question_label.pack(pady=40)

answer_box = Entry(frame_quiz, font=("Arial", 18), width=10)
answer_box.pack()

btn_submit = Button(frame_quiz, text="Submit", font=("Arial", 16), bg="#2c3e50", fg="white", command=submit_answer)
btn_submit.pack(pady=10)
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

score_label = Label(frame_quiz, text="Score: 0", font=("Arial", 18), fg="white", bg="#2c3e50")
score_label.pack(pady=10)

# Control buttons
for text, cmd in [("Pause", pause_quiz), ("Resume", resume_quiz), ("Stop", stop_quiz)]:
    btn = Button(frame_quiz, text=text, font=("Arial", 14), bg="#2c3e50", fg="white", command=cmd)
    btn.pack(pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Guidelines box
guidelines = """📘 Guidelines:
- Choose your difficulty level
- Answer 5 questions to complete the quiz
- Use Pause/Resume/Stop anytime
- Score updates live
- Have fun and learn!"""

guidelines_box = Label(frame_quiz, text=guidelines, font=("Arial", 14), fg="white", bg="#2c3e50", justify=LEFT, bd=2, relief=SOLID, padx=10, pady=10)
guidelines_box.place(x=20, y=400)

# --- Score Frame ---
result_label = Label(frame_score, text="", font=("Arial", 26), fg="white", bg="#2c3e50")
result_label.pack(pady=120)

btn_home = Button(frame_score, text="Home", font=("Arial", 16), bg="#2c3e50", fg="white", command=lambda: show_frame(frame_start))
btn_home.pack()
btn_home.bind("<Enter>", on_enter)
btn_home.bind("<Leave>", on_leave)

# Start the app
show_frame(frame_start)
root.protocol("WM_DELETE_WINDOW", confirm_exit)
root.mainloop()
