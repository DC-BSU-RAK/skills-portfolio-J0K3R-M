
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random

# Main window setup
root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.resizable(0, 0)

# Save default background color (used for frames/labels)
default_bg = root.cget("bg")

# Try to load a background image (optional)
try:
    bg_img = Image.open("images/background.jpg")  # Ensure this image exists in the same directory
    bg_img = bg_img.resize((500, 400), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo  # keep reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # send to back
except Exception as e:
    # If image not found, continue with default background color
    print("Background image could not be loaded:", e)

# Quiz variables
score = 0
question_count = 0
TOTAL = 5  # number of questions per quiz
quiz_active = False
answer = None  # correct answer for current question

# Show simple guidelines
def show_guidelines():
    guidelines = (
        "MATH QUIZ GUIDELINES\n\n"
        "1. Solve 5 random math questions\n"
        "2. Each correct answer = 1 point\n"
        "3. Questions include +, -, and * operations\n"
        "4. Enter your answer as a number only\n"
        "5. Click Submit to check your answer\n"
        "6. Click Start to begin the quiz\n"
        "7. Click Pause to resume later\n"
        "8. Click Stop to end the quiz\n"
    )
    messagebox.showinfo("Guidelines", guidelines)

# Start a new quiz
def start_quiz():
    global quiz_active
    reset_quiz()           # reset counters and UI
    quiz_active = True
    start_btn.config(state=DISABLED, text="Start")
    pause_btn.config(state=NORMAL)
    stop_btn.config(state=NORMAL)
    guidelines_btn.config(state=DISABLED)
    generate_question()

# Pause the quiz (can be resumed)
def pause_quiz():
    global quiz_active
    if not quiz_active:
        return
    quiz_active = False
    messagebox.showinfo("Paused", "Quiz paused. Click Resume to continue.")
    start_btn.config(state=NORMAL, text="Resume")
    pause_btn.config(state=DISABLED)

# Stop the quiz and show score so far
def stop_quiz():
    global quiz_active
    quiz_active = False
    if question_count > 0:
        messagebox.showinfo("Quiz Stopped", f"Quiz ended. Your score: {score}/{question_count}")
    reset_quiz()

# Generate a random math question
def generate_question():
    global num1, num2, answer, score, question_count

    # If quiz not active or reached TOTAL, finish or reset
    if not quiz_active or question_count >= TOTAL:
        if question_count == TOTAL:
            messagebox.showinfo("Quiz Finished", f"Your score is {score}/{TOTAL}")
        reset_quiz()
        return

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    else:
        answer = num1 * num2

    question_label.config(text=f"{num1} {op} {num2} = ?")
    user_entry.delete(0, END)
    user_entry.focus()

# Check user's answer and proceed
def check_answer(event=None):
    global score, question_count

    if not quiz_active:
        messagebox.showwarning("Warning", "Please start the quiz first!")
        return

    user = user_entry.get().strip()
    if user == "":
        messagebox.showwarning("Warning", "Please enter a number.")
        return

    try:
        user_val = int(user)
    except ValueError:
        messagebox.showerror("Error", "Only whole numbers allowed!")
        return

    if answer is None:
        messagebox.showwarning("Warning", "No active question. Click Start.")
        return

    if user_val == answer:
        score += 1
        feedback_label.config(text="Correct!", fg="green")
    else:
        feedback_label.config(text=f"Wrong! Answer = {answer}", fg="red")

    question_count += 1
    score_label.config(text=f"Score: {score}/{question_count}")

    if question_count == TOTAL:
        messagebox.showinfo("Quiz Finished", f"Your score is {score}/{TOTAL}")
        reset_quiz()
    else:
        generate_question()

# Reset quiz variables and UI to initial state
def reset_quiz():
    global score, question_count, quiz_active, answer
    score = 0
    question_count = 0
    quiz_active = False
    answer = None
    score_label.config(text="Score: 0/0")
    feedback_label.config(text="")
    question_label.config(text="Click Start to begin")
    user_entry.delete(0, END)
    start_btn.config(state=NORMAL, text="Start")
    pause_btn.config(state=DISABLED)
    stop_btn.config(state=DISABLED)
    guidelines_btn.config(state=NORMAL)

# ----------------
# UI Widgets
# ----------------
# Frame for top buttons
button_frame = Frame(root, bg=default_bg, highlightthickness=0)
button_frame.place(x=50, y=15, width=400, height=50)

guidelines_btn = Button(button_frame, text="Guidelines", font=("Arial", 9),
                        bg="#2C5F8D", fg="white", command=show_guidelines, width=11, relief=FLAT, bd=0)
guidelines_btn.grid(row=0, column=0, padx=4, pady=5)

start_btn = Button(button_frame, text="Start", font=("Arial", 9),
                   bg="#4CAF50", fg="white", command=start_quiz, width=11, relief=FLAT, bd=0)
start_btn.grid(row=0, column=1, padx=4, pady=5)

pause_btn = Button(button_frame, text="Pause", font=("Arial", 9),
                   bg="#FF9800", fg="white", command=pause_quiz, width=11, relief=FLAT, bd=0, state=DISABLED)
pause_btn.grid(row=0, column=2, padx=4, pady=5)

stop_btn = Button(button_frame, text="Stop", font=("Arial", 9),
                  bg="#E74C3C", fg="white", command=stop_quiz, width=11, relief=FLAT, bd=0, state=DISABLED)
stop_btn.grid(row=0, column=3, padx=4, pady=5)

# Score display
score_label = Label(root, text="Score: 0/0", font=("Arial", 12, "bold"), bg=default_bg, fg="white")
score_label.place(x=210, y=75)

# Question display
question_label = Label(root, text="Click Start to begin", font=("Arial", 18, "bold"), bg=default_bg, fg="white")
question_label.place(x=120, y=140)

# Entry for user's answer
user_entry = Entry(root, font=("Arial", 14), width=8, bg="#FFFFFF", fg="#333333", relief=FLAT, bd=2)
user_entry.place(x=175, y=190)

# Submit button
submit_btn = Button(root, text="Submit", font=("Arial", 11, "bold"),
                    bg="#2C5F8D", fg="white", command=check_answer, width=10, relief=FLAT, bd=0)
submit_btn.place(x=170, y=230)

# Allow Enter key to submit answer
root.bind("<Return>", check_answer)

# Feedback label
feedback_label = Label(root, text="", font=("Arial", 12, "bold"), bg=default_bg, fg="white")
feedback_label.place(x=130, y=290)

# Start the GUI loop
root.mainloop()
# ...existing code...