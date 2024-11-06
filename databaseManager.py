import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Connect to database
def connect_db():
    conn = sqlite3.connect('quiz_bowl.db')
    return conn

# Function to fetch all table names dynamically from the database
def get_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# Function to view questions in a selected category
def view_questions(category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT question_id, question_text, option_1, option_2, option_3, option_4, correct_answer FROM {category}")
    questions = cursor.fetchall()
    conn.close()
    return questions

# Function to add a question to a category
def add_question(category, question_text, options, correct_answer):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {category} (question_text, option_1, option_2, option_3, option_4, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question_text, *options, correct_answer))
    conn.commit()
    conn.close()

# Function to delete a question from a category
def delete_question(category, question_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {category} WHERE question_id = ?", (question_id,))
    conn.commit()
    conn.close()

# Function to update a question in a category
def update_question(category, question_id, question_text, options, correct_answer):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {category} SET question_text = ?, option_1 = ?, option_2 = ?, option_3 = ?, option_4 = ?, correct_answer = ?
        WHERE question_id = ?
    """, (question_text, *options, correct_answer, question_id))
    conn.commit()
    conn.close()

# GUI for viewing questions in a category
def view_category(category):
    questions = view_questions(category)
    view_window = tk.Toplevel(root)
    view_window.title(f"View {category} Questions")

    # Treeview to display questions
    tree = ttk.Treeview(view_window, columns=("ID", "Question", "Option1", "Option2", "Option3", "Option4", "Answer"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    
    # Populate the Treeview with data
    for question in questions:
        tree.insert("", "end", values=question)

    # Buttons for CRUD operations
    add_button = tk.Button(view_window, text="Add Question", command=lambda: add_question_window(category))
    delete_button = tk.Button(view_window, text="Delete Question", command=lambda: delete_selected_question(tree, category))
    edit_button = tk.Button(view_window, text="Edit Question", command=lambda: edit_selected_question(tree, category))

    add_button.pack(side="left", padx=10)
    delete_button.pack(side="left", padx=10)
    edit_button.pack(side="left", padx=10)

# GUI for adding a question
def add_question_window(category):
    add_window = tk.Toplevel(root)
    add_window.title(f"Add Question to {category}")

    tk.Label(add_window, text="Question Text:").grid(row=0, column=0)
    question_text = tk.Entry(add_window, width=50)
    question_text.grid(row=0, column=1)

    options = []
    for i in range(4):
        tk.Label(add_window, text=f"Option {i+1}:").grid(row=i+1, column=0)
        option = tk.Entry(add_window, width=50)
        option.grid(row=i+1, column=1)
        options.append(option)

    tk.Label(add_window, text="Correct Answer:").grid(row=5, column=0)
    correct_answer = tk.Entry(add_window, width=50)
    correct_answer.grid(row=5, column=1)

    def save_new_question():
        add_question(
            category,
            question_text.get(),
            [opt.get() for opt in options],
            correct_answer.get()
        )
        add_window.destroy()
        messagebox.showinfo("Success", "Question added successfully!")

    save_button = tk.Button(add_window, text="Save Question", command=save_new_question)
    save_button.grid(row=6, column=1, pady=10)

# GUI for deleting a selected question
def delete_selected_question(tree, category):
    selected_item = tree.selection()
    if selected_item:
        question_id = tree.item(selected_item)["values"][0]
        delete_question(category, question_id)
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Question deleted successfully!")

# GUI for editing a selected question
def edit_selected_question(tree, category):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a question to edit.")
        return

    question_data = tree.item(selected_item)["values"]
    question_id = question_data[0]

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Question")

    tk.Label(edit_window, text="Question Text:").grid(row=0, column=0)
    question_text = tk.Entry(edit_window, width=50)
    question_text.insert(0, question_data[1])
    question_text.grid(row=0, column=1)

    options = []
    for i in range(4):
        tk.Label(edit_window, text=f"Option {i+1}:").grid(row=i+1, column=0)
        option = tk.Entry(edit_window, width=50)
        option.insert(0, question_data[i+2])
        option.grid(row=i+1, column=1)
        options.append(option)

    tk.Label(edit_window, text="Correct Answer:").grid(row=5, column=0)
    correct_answer = tk.Entry(edit_window, width=50)
    correct_answer.insert(0, question_data[6])
    correct_answer.grid(row=5, column=1)

    def save_edited_question():
        update_question(
            category,
            question_id,
            question_text.get(),
            [opt.get() for opt in options],
            correct_answer.get()
        )
        edit_window.destroy()
        messagebox.showinfo("Success", "Question updated successfully!")

    save_button = tk.Button(edit_window, text="Save Changes", command=save_edited_question)
    save_button.grid(row=6, column=1, pady=10)

# Main Application
root = tk.Tk()
root.title("Quiz Bowl Management")

tk.Label(root, text="Select a Category to Manage:").pack(pady=10)
categories = get_categories()

for category in categories:
    tk.Button(root, text=category, command=lambda c=category: view_category(c)).pack(pady=5)

root.mainloop()
