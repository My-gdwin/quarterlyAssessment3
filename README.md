# quarterlyAssessment3

MUST RUN databaseSetup.py TO CREATE DATABASE BEFORE RUNNING quarterlyAssessment3.py

# quarterlyAssessment3.py
This Python code implements a GUI-based quiz application using `tkinter` for the user interface and `sqlite3` for managing quiz questions stored in a database (`quiz_bowl.db`). The application allows users to select from predefined quiz categories, each mapped to a database table containing multiple-choice questions. Once a category is chosen, the app retrieves up to 10 questions from the database and presents them one by one to the user. Each question displays four answer options, from which users can select and submit their answer. Correct and incorrect answers are scored in real time, with a summary of the final score shown upon quiz completion. The code structure includes separate classes and functions for streamlined question management, user feedback, and database interaction.

# databaseSetup.py
This code sets up a SQLite database for a quiz application, storing questions across multiple categories: Math, Science, History, Literature, and Geography. Each category is represented by its own table in the database. Upon initialization, the code checks if each table exists and creates it if not, then verifies if there are at least 10 questions already present in each category. If a category has fewer than 10 questions, it inserts predefined questions from the `CATEGORY_QUESTIONS` dictionary to reach the minimum threshold. This setup process ensures each category has a sufficient number of questions for a complete quiz experience.

# databaseManager
This code provides a full-featured GUI application in Python using `tkinter` and `sqlite3` to manage questions in a "Quiz Bowl" database. Here’s a breakdown of its main functions:

### Core Functions:
1. **Database Connection**: `connect_db()` establishes a connection to `quiz_bowl.db`.
2. **Dynamic Category Retrieval**: `get_categories()` dynamically fetches all table names in the database, representing different quiz categories.
3. **CRUD Operations**:
   - `view_questions(category)`: Fetches questions from a specific category.
   - `add_question(category, question_text, options, correct_answer)`: Adds a new question to the chosen category.
   - `delete_question(category, question_id)`: Deletes a question from the chosen category by its `question_id`.
   - `update_question(category, question_id, question_text, options, correct_answer)`: Updates an existing question.

### GUI Components:
1. **Main Window**: Displays all categories as buttons. Each button, when clicked, opens a new window to manage the questions for that category.
2. **View Category Window**:
   - Opens on clicking a category button and shows all questions in that category in a `Treeview` widget.
   - Includes buttons to **Add**, **Delete**, and **Edit** questions.
3. **Add Question Window**:
   - Allows entry of a question, four options, and the correct answer.
   - Saves the new question to the database upon confirmation.
4. **Edit Question Window**:
   - Allows modifying a selected question’s text, options, and answer.
   - Updates the database with the edited details.

### Helper Functions:
- **Adding a Question**: Opens a form for entering new question details, saves the input, and updates the database.
- **Deleting a Question**: Deletes the selected question from the displayed list and database.
- **Editing a Question**: Opens a pre-filled form for editing the selected question, updates it in the database, and refreshes the view.

### Running the App:
The main loop (`root.mainloop()`) initializes the interface, allowing users to manage questions across various quiz categories through the buttons created from the dynamic list of categories. The modular design keeps the database and UI operations well-separated, which makes it easy to maintain and expand.