import sqlite3

# Add a question to a specific category table
def add_question(category, question_text, options, correct_answer):
    conn = sqlite3.connect('quiz_bowl.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {category} (question_text, option_1, option_2, option_3, option_4, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question_text, *options, correct_answer))
    conn.commit()
    conn.close()

# Retrieve questions from a specific category
def get_questions(category):
    conn = sqlite3.connect('quiz_bowl.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {category}")
    questions = cursor.fetchall()
    conn.close()
    return questions

import tkinter as tk
from tkinter import messagebox, ttk
from random import shuffle

# Class for question format and handling
class Question:
    def __init__(self, question_text, options, correct_answer):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer

    def check_answer(self, answer):
        return answer == self.correct_answer

# Main Application Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl")
        self.categories = ["Math", "Science", "History", "Literature", "Geography"]
        self.selected_category = tk.StringVar(value="")  # Default to empty string for no category selected
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.setup_category_selection()

    def setup_category_selection(self):
        tk.Label(self.root, text="Select a Quiz Category", font=("Helvetica", 14)).pack(pady=10)

        # Dropdown menu for category selection
        self.category_menu = ttk.Combobox(self.root, values=self.categories, state="readonly", width=20)
        self.category_menu.set("Select a category")  # Default text
        self.category_menu.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Quiz Now", command=self.start_quiz, state=tk.DISABLED)
        self.start_button.pack(pady=20)

        # Bind the dropdown change event to check if a category is selected
        self.category_menu.bind("<<ComboboxSelected>>", self.check_category_selection)

    def check_category_selection(self, event=None):
        selected_category = self.category_menu.get()
        if selected_category != "Select a category":
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def start_quiz(self):
        category = self.category_menu.get()
        if category == "Select a category" or not category:
            messagebox.showwarning("Selection Required", "Please select a category!")
            return
        
        questions = get_questions(category)
        if len(questions) < 10:
            messagebox.showerror("Insufficient Questions", "Not enough questions in this category.")
            return

        self.quiz_questions = [Question(q[1], q[2:6], q[6]) for q in questions]
        shuffle(self.quiz_questions)
        self.current_question_index = 0
        self.score = 0
        self.show_question_window()

    def show_question_window(self):
        self.root.withdraw()
        self.question_window = tk.Toplevel(self.root)
        self.question_window.title("Quiz Bowl - Quiz")

        self.question_text = tk.StringVar()
        self.option_vars = [tk.StringVar() for _ in range(4)]
        
        tk.Label(self.question_window, textvariable=self.question_text, wraplength=400, font=("Helvetica", 12)).pack(pady=10)
        
        self.radio_value = tk.StringVar()
        for i in range(4):
            tk.Radiobutton(self.question_window, variable=self.radio_value, value=i, textvariable=self.option_vars[i]).pack(anchor=tk.W)
        
        tk.Button(self.question_window, text="Submit Answer", command=self.submit_answer).pack(pady=20)
        
        self.display_question()

    def display_question(self):
        question = self.quiz_questions[self.current_question_index]
        self.question_text.set(question.question_text)
    
        # Convert options to a list so we can shuffle them
        options = list(question.options)
        shuffle(options)
    
        for i in range(4):
            self.option_vars[i].set(options[i])
    
        self.radio_value.set(None)


    def submit_answer(self):
        selected_option = self.radio_value.get()
        if not selected_option:
            messagebox.showwarning("No Answer", "Please select an answer.")
            return
        
        question = self.quiz_questions[self.current_question_index]
        selected_answer = self.option_vars[int(selected_option)].get()
        
        if question.check_answer(selected_answer):
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer was: {question.correct_answer}")
        
        self.current_question_index += 1
        if self.current_question_index < 10:
            self.display_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        messagebox.showinfo("Quiz Completed", f"Your final score is {self.score} out of 10.")
        self.question_window.destroy()
        self.root.deiconify()

# Run the application
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
