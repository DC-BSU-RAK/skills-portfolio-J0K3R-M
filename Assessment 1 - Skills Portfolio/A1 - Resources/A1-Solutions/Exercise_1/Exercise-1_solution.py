# Import required libraries
import tkinter as tk
from tkinter import messagebox
import random

class MathQuiz:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Math Quiz")
        self.window.geometry("400x300")
        
        # Initialize score and question counter
        self.score = 0
        self.question_count = 0
        self.attempts = 0
        
        # Initialize variables to store current question data
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operation = ''
        self.correct_answer = 0
        
        # Create and display the initial menu
        self.display_menu()
        
    def display_menu(self):
        # Clear any existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Create and pack the difficulty level label
        menu_label = tk.Label(self.window, text="DIFFICULTY LEVEL", font=('Arial', 14, 'bold'))
        menu_label.pack(pady=20)
        
        # Create buttons for each difficulty level
        tk.Button(self.window, text="1. Easy", command=lambda: self.start_quiz("easy")).pack(pady=5)
        tk.Button(self.window, text="2. Moderate", command=lambda: self.start_quiz("moderate")).pack(pady=5)
        tk.Button(self.window, text="3. Advanced", command=lambda: self.start_quiz("advanced")).pack(pady=5)
    
    def random_int(self, difficulty):
        # Generate random numbers based on difficulty level
        if difficulty == "easy":
            return random.randint(0, 9)
        elif difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)
    
    def decide_operation(self):
        # Randomly choose between addition and subtraction
        return random.choice(['+', '-'])
    
    def display_problem(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Create and display the question label
        question = f"{self.current_num1} {self.current_operation} {self.current_num2} ="
        tk.Label(self.window, text=question, font=('Arial', 14)).pack(pady=20)
        
        # Create answer entry field
        self.answer_entry = tk.Entry(self.window)
        self.answer_entry.pack(pady=10)
        
        # Create submit button
        tk.Button(self.window, text="Submit", command=self.check_answer).pack(pady=10)
        
        # Display current score
        tk.Label(self.window, text=f"Score: {self.score}", font=('Arial', 12)).pack(pady=10)
    
    def check_answer(self):
        # Get user's answer from entry field
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                # Award points based on attempt number
                if self.attempts == 0:
                    self.score += 10
                    messagebox.showinfo("Correct!", "Well done! +10 points")
                else:
                    self.score += 5
                    messagebox.showinfo("Correct!", "Correct on second try! +5 points")
                    
                self.question_count += 1
                if self.question_count < 10:
                    self.generate_question()
                else:
                    self.display_results()
            else:
                if self.attempts == 0:
                    self.attempts += 1
                    messagebox.showwarning("Wrong", "Try again!")
                    self.answer_entry.delete(0, tk.END)
                else:
                    messagebox.showinfo("Wrong", f"The correct answer was {self.correct_answer}")
                    self.question_count += 1
                    if self.question_count < 10:
                        self.generate_question()
                    else:
                        self.display_results()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def start_quiz(self, difficulty):
        # Initialize quiz with selected difficulty
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.generate_question()
    
    def generate_question(self):
        # Generate new question
        self.attempts = 0
        self.current_num1 = self.random_int(self.difficulty)
        self.current_num2 = self.random_int(self.difficulty)
        self.current_operation = self.decide_operation()
        
        # Calculate correct answer
        if self.current_operation == '+':
            self.correct_answer = self.current_num1 + self.current_num2
        else:
            self.correct_answer = self.current_num1 - self.current_num2
            
        self.display_problem()
    
    def display_results(self):
        # Clear existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Calculate grade based on score
        grade = 'A+' if self.score >= 90 else 'A' if self.score >= 80 else 'B' if self.score >= 70 else 'C' if self.score >= 60 else 'D' if self.score >= 50 else 'F'
        
        # Display final score and grade
        tk.Label(self.window, text=f"Final Score: {self.score}/100", font=('Arial', 14, 'bold')).pack(pady=20)
        tk.Label(self.window, text=f"Grade: {grade}", font=('Arial', 14)).pack(pady=10)
        
        # Create buttons to play again or quit
        tk.Button(self.window, text="Play Again", command=self.display_menu).pack(pady=10)
        tk.Button(self.window, text="Quit", command=self.window.quit).pack(pady=10)

if __name__ == "__main__":
    # Create and start the quiz application
    quiz = MathQuiz()
    quiz.window.mainloop()