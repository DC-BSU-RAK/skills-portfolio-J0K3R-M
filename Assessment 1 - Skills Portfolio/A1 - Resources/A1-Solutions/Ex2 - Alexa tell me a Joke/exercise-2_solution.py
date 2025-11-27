from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
# Function: Load jokes from file
def fetch_jokes():
    """
    Reads jokes from a text file.
    Each line should contain a question ending with '?' followed by the punchline.
    Example: "Why did the chicken cross the road? To get to the other side."
    Returns a list of (question, answer) tuples.
    """
    path = r"C:\Users\minha\OneDrive\Documents\GitHub\skills-portfolio-J0K3R-M\Assessment 1 - Skills Portfolio\A1 - Resources\A1-Solutions\Ex2 - Alexa tell me a Joke\randomJokes.txt"
    jokes = []
    try:
        with open(path, encoding="utf-8") as f:  # safer to specify encoding
            for line in f:
                if "?" in line:
                    q, a = line.split("?", 1)
                    jokes.append((q.strip() + "?", a.strip()))
    except FileNotFoundError:
        messagebox.showerror("Missing File", "Cannot locate randomJokes.txt")
    return jokes
# Function: Apply background image to frame
def apply_bg(frame, img_path):
    """
    Sets a background image that automatically resizes with the window.
    """
    img_orig = Image.open(img_path)
    lbl = Label(frame)
    lbl.place(x=0, y=0, relwidth=1, relheight=1)

    def resize(event):
        # Resize image to fit in the frame dynamically
        img_resized = img_orig.resize((event.width, event.height))
        photo = ImageTk.PhotoImage(img_resized)
        lbl.config(image=photo)
        lbl.image = photo  # keep reference to avoid garbage collection

    frame.bind("<Configure>", resize)
# Function: Shows a new random joke
def new_joke():
    global current
    if not joke_data:
        question_lbl.config(text="(No jokes available)")
        answer_lbl.config(text="")
        return
    current = random.choice(joke_data)
    question_lbl.config(text=current[0])
    answer_lbl.config(text="")
    reveal_btn.config(state=NORMAL)
    quit_btn.pack_forget()  # hide quit button until punchline is revealed
# Function: Reveal punchline
def show_answer():
    """
    Displays the punchline of the current joke.
    """
    if current:
        answer_lbl.config(text=current[1])
        reveal_btn.config(state=DISABLED)
        quit_btn.pack(pady=15)
# Function: Confirm exit
def leave():
    """
    Asks user for confirmation before closing the app.
    """
    if messagebox.askyesno("Quit", "Exit the program?"):
        root.destroy()
# Function: Switch screens
def switch():
    """
    Switches from welcome screen to joke screen.
    """
    screen1.pack_forget()
    screen2.pack(fill=BOTH, expand=True)
# Main Application Setup
root = Tk()
root.title("Joke Machine")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", leave)
# Load jokes at start
joke_data = fetch_jokes()
current = None
# Screen 1: Welcome Screen
screen1 = Frame(root)
apply_bg(screen1, r"C:\Users\minha\OneDrive\Documents\GitHub\skills-portfolio-J0K3R-M\Assessment 1 - Skills Portfolio\A1 - Resources\A1-Solutions\Ex2 - Alexa tell me a Joke\Images\5005979.jpg")
screen1.pack(expand=True, fill=BOTH)

Label(screen1, text="Welcome!", font=("Arial", 32), bg="#b6dcff").pack(pady=170)
Button(screen1, text="Start", font=("Arial", 20), bd=0, highlightthickness=0, command=switch).pack()

# Screen 2: Joke Screen
screen2 = Frame(root)
apply_bg(screen2, r"C:\Users\minha\OneDrive\Documents\GitHub\skills-portfolio-J0K3R-M\Assessment 1 - Skills Portfolio\A1 - Resources\A1-Solutions\Ex2 - Alexa tell me a Joke\Images\5005979.jpg")

question_lbl = Label(screen2, text="", font=("Arial", 24), wraplength=650, justify=CENTER)
question_lbl.pack(pady=70)

answer_lbl = Label(screen2, text="", font=("Arial", 20), fg="grey", wraplength=650, justify=CENTER)
answer_lbl.pack()

Button(screen2, text="Joke", font=("Arial", 18), bd=0, highlightthickness=0, command=new_joke).pack(pady=20)

reveal_btn = Button(screen2, text="Reveal Punchline", font=("Arial", 18), bd=0, highlightthickness=0, state=DISABLED, command=show_answer)
reveal_btn.pack()

quit_btn = Button(screen2, text="Exit", font=("Arial", 18), bd=0, highlightthickness=0, command=leave)

# Run the App
root.mainloop()
