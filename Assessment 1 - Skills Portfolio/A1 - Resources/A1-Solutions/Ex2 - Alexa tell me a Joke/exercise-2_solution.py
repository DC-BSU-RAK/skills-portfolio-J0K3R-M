import tkinter as tk
import random

# Load jokes from file
with open("C:\\Users\\minha\\OneDrive\\Documents\\GitHub\\skills-portfolio-J0K3R-M\\Assessment 1 - Skills Portfolio\\A1 - Resources\\A1-Solutions\\Ex2 - Alexa tell me a Joke\\randomJokes.txt") as f:
    jokes = [line.strip() for line in f if line.strip()]

# Split jokes into (setup, punchline)
jokes = [j.split("?", 1) for j in jokes]

class JokeApp:
    def __init__(self, root):
        self.root = root
        root.title("Alexa Joke Assistant")

        self.setup_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.setup_label.pack(pady=10)

        self.punchline_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", wraplength=400)
        self.punchline_label.pack(pady=10)

        tk.Button(root, text="Alexa tell me a Joke", command=self.show_joke).pack(pady=5)
        tk.Button(root, text="Show Punchline", command=self.show_punchline).pack(pady=5)
        tk.Button(root, text="Next Joke", command=self.show_joke).pack(pady=5)
        tk.Button(root, text="Quit", command=root.quit).pack(pady=5)

        self.current_joke = None

    def show_joke(self):
        self.current_joke = random.choice(jokes)
        self.setup_label.config(text=self.current_joke[0] + "?")
        self.punchline_label.config(text="")  # clear punchline

    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])

# Run app
root = tk.Tk()
app = JokeApp(root)
root.mainloop()
