import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# ===== setting up of math quizz =====
root = tk.Tk()
root.title("Maths Quiz")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.update_idletasks()
SCR_W, SCR_H = root.winfo_width(), root.winfo_height()

# adding background image and color
BG_PATH = "C:\\Users\\minha\\OneDrive\\Documents\\GitHub\\skills-portfolio-J0K3R-M\\Assessment 1 - Skills Portfolio\\A1 - Resources\\A1-Solutions_MINHAJ_MUHAMMED\\Exercise_1\\images\\Gemini_Generated_Image_vbpofzvbpofzvbpo.png"
BG_COLOR = "#222222"
bg_image = Image.open(BG_PATH).resize((SCR_W, SCR_H), Image.LANCZOS) if os.path.exists(BG_PATH) else Image.new("RGB", (SCR_W, SCR_H), BG_COLOR)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()

# adding Button and Style
BTN_STYLE = {"bg": BG_COLOR, "fg": "white", "activebackground": BG_COLOR, "activeforeground": "white", "bd": 0, "highlightthickness": 0, "relief": "flat", "font": ("Roboto", 14)}

# Variables in order to track quiz state    
TOTAL_Q = 10
current_q = score = tries = answer = 0
paused = quiz_active = False
difficulty = tk.IntVar(value=1)
q_var = tk.StringVar()
result_var = tk.StringVar()
info_var = tk.StringVar(value="Press Start to begin. Esc to quit.")

# functions to handle quiz logic
def rand_int(level):
    a, b = (random.randint(0, 9), random.randint(0, 9)) if level == 1 else (random.randint(10, 99), random.randint(10, 99)) if level == 2 else (random.randint(1000, 9999), random.randint(1000, 9999))
    op = random.choice(["+", "-"])
    if op == "-" and a < b:
        a, b = b, a
    return a, b, op

def new_question(): # generate a new question
    global answer, tries
    tries = 0
    a, b, op = rand_int(difficulty.get())
    answer = a + b if op == "+" else a - b
    q_var.set(f"{a} {op} {b} = ?")
    result_var.set("")
    entry.config(state="normal")
    entry.delete(0, "end")
    submit_btn.config(state="normal")
    next_btn.config(state="disabled")

def start_quiz(): # start the quiz
    global current_q, score, quiz_active
    current_q = score = 0
    quiz_active = True
    new_question()
    info_var.set(f"Q {current_q+1}/{TOTAL_Q}   Score: {score}")
    btn_start.config(state="disabled")
    btn_pause.config(state="normal")
    btn_stop.config(state="normal")
    for rb in diff_radiobtn:
        rb.config(state="disabled")

def pause_quiz(): # pause or resume the quiz
    global paused
    paused = not paused
    state = "disabled" if paused else "normal"
    for w in (entry, submit_btn, next_btn):
        w.config(state=state)
    btn_pause.config(text="Resume" if paused else "Pause")

def stop_quiz():# stop the quiz
    global current_q, score, quiz_active, paused
    current_q = score = 0
    quiz_active = paused = False
    q_var.set("")
    result_var.set("")
    info_var.set("Quiz stopped. Press Start.")
    entry.config(state="disabled")
    entry.delete(0, "end")
    btn_start.config(state="normal")
    btn_pause.config(state="disabled", text="Pause")
    btn_stop.config(state="disabled")
    for rb in diff_radiobtn:
        rb.config(state="normal")

def check_answer(): # check the user's answer and return feedback
    global score, tries
    tries += 1
    try:
        user = int(entry.get())
    except ValueError:
        result_var.set("Enter a number!")
        return
    if user == answer:
        pts = 10 if tries == 1 else 5
        score += pts
        result_var.set(f"Correct! +{pts}")
        entry.config(state="disabled")
        submit_btn.config(state="disabled")
        next_btn.config(state="normal")
    else:
        if tries >= 2:
            result_var.set(f"Wrong. Answer: {answer}")
            entry.config(state="disabled")
            submit_btn.config(state="disabled")
            next_btn.config(state="normal")
        else:
            result_var.set("Wrong. Try once more.")

def next_question():
    global current_q
    current_q += 1
    if current_q >= TOTAL_Q:
        messagebox.showinfo("Done", f"Quiz complete!\nScore: {score}/{TOTAL_Q*10}")
        stop_quiz()
    else:
        info_var.set(f"Q {current_q+1}/{TOTAL_Q}   Score: {score}")
        new_question()

def show_guidelines(): # show quiz guidelines
    messagebox.showinfo("Guidelines", "10 questions.\n10 pts – first try.\n5 pts – second try.\nPress Esc to quit.")

# UI of the quizz application
# Control Bar
ctrl_frame = tk.Frame(root, bg=BG_COLOR)
ctrl_frame.place(relx=0.5, rely=0.08, anchor="n")
btn_start = tk.Button(ctrl_frame, text="Start", **BTN_STYLE, command=start_quiz)
btn_pause = tk.Button(ctrl_frame, text="Pause", **BTN_STYLE, command=pause_quiz, state="disabled")
btn_stop = tk.Button(ctrl_frame, text="Stop", **BTN_STYLE, command=stop_quiz, state="disabled")
btn_guide = tk.Button(ctrl_frame, text="Guidelines", **BTN_STYLE, command=show_guidelines)
btn_quit = tk.Button(ctrl_frame, text="Quit", **BTN_STYLE, command=root.destroy)
for b in (btn_start, btn_pause, btn_stop, btn_guide, btn_quit):
    b.pack(side="left", padx=10)

# Info Label
tk.Label(root, textvariable=info_var, bg=BG_COLOR, fg="white", font=("Roboto", 12)).place(relx=0.5, rely=0.18, anchor="n")

# Difficulty
diff_frame = tk.Frame(root, bg=BG_COLOR)
diff_frame.place(relx=0.5, rely=0.28, anchor="n")
tk.Label(diff_frame, text="Difficulty:", bg=BG_COLOR, fg="white", font=("Roboto", 12)).pack(side="left", padx=5)
diff_radiobtn = []
for txt, val in (("Easy", 1), ("Medium", 2), ("Hard", 3)):
    rb = tk.Radiobutton(diff_frame, text=txt, variable=difficulty, value=val, bg=BG_COLOR, fg="white", selectcolor=BG_COLOR, font=("Roboto", 12))
    rb.pack(side="left", padx=5)
    diff_radiobtn.append(rb)

# Quiz Area
quiz = tk.Frame(root, bg=BG_COLOR)
quiz.place(relx=0.5, rely=0.35, anchor="n")
tk.Label(quiz, textvariable=q_var, bg=BG_COLOR, fg="white", font=("Roboto", 24)).pack(pady=15)
entry = tk.Entry(quiz, font=("Roboto", 18), justify="center", width=10, state="disabled")
entry.pack(pady=5)
tk.Label(quiz, textvariable=result_var, bg=BG_COLOR, fg="white", font=("Roboto", 12)).pack(pady=5)

btn_bar = tk.Frame(quiz, bg=BG_COLOR)
btn_bar.pack(pady=10)
submit_btn = tk.Button(btn_bar, text="Submit", **BTN_STYLE, command=check_answer, state="disabled")
next_btn = tk.Button(btn_bar, text="Next", **BTN_STYLE, command=next_question, state="disabled")
submit_btn.pack(side="left", padx=8)
next_btn.pack(side="left", padx=8)

root.mainloop()