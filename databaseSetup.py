import sqlite3

# Category-specific questions for initial setup
CATEGORY_QUESTIONS = {
    "Math": [
        ("What is 5 + 3?", ["7", "8", "9", "10"], "8"),
        ("What is 12 - 4?", ["6", "7", "8", "9"], "8"),
        ("What is 9 * 3?", ["27", "26", "25", "24"], "27"),
        ("What is 16 / 4?", ["2", "3", "4", "5"], "4"),
        ("What is the square root of 81?", ["7", "8", "9", "10"], "9"),
        ("What is 2 to the power of 3?", ["6", "7", "8", "9"], "8"),
        ("What is 100 - 25?", ["70", "75", "80", "85"], "75"),
        ("What is 45 / 5?", ["8", "9", "10", "11"], "9"),
        ("What is 15 + 10?", ["20", "25", "30", "35"], "25"),
        ("What is 3 * 7?", ["20", "21", "22", "23"], "21")
    ],
    "Science": [
        ("What planet is known as the Red Planet?", ["Earth", "Venus", "Mars", "Jupiter"], "Mars"),
        ("What gas do plants absorb from the atmosphere?", ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "Carbon Dioxide"),
        ("What is the chemical symbol for water?", ["O", "H2O", "CO2", "H2"], "H2O"),
        ("Which part of the plant conducts photosynthesis?", ["Roots", "Stem", "Leaves", "Flower"], "Leaves"),
        ("What is the powerhouse of the cell?", ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "Mitochondria"),
        ("What gas do humans exhale?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "Carbon Dioxide"),
        ("What is the boiling point of water?", ["50°C", "75°C", "100°C", "150°C"], "100°C"),
        ("What organ pumps blood throughout the body?", ["Lungs", "Heart", "Brain", "Liver"], "Heart"),
        ("Which planet is closest to the sun?", ["Earth", "Venus", "Mercury", "Mars"], "Mercury"),
        ("What is the symbol for gold?", ["Au", "Ag", "Go", "Gd"], "Au")
    ],
    "History": [
        ("Who was the first president of the United States?", ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"], "George Washington"),
        ("In which year did World War II end?", ["1942", "1945", "1950", "1955"], "1945"),
        ("Who discovered America?", ["Christopher Columbus", "Amerigo Vespucci", "Marco Polo", "Leif Erikson"], "Christopher Columbus"),
        ("What ancient civilization built the pyramids?", ["Romans", "Greeks", "Egyptians", "Mayans"], "Egyptians"),
        ("The Great Wall of China was built to protect against?", ["Mongols", "Japanese", "Europeans", "Africans"], "Mongols"),
        ("Who was the famous queen of Ancient Egypt?", ["Nefertiti", "Cleopatra", "Hatshepsut", "Nefertari"], "Cleopatra"),
        ("Where did the Renaissance begin?", ["France", "Italy", "Germany", "England"], "Italy"),
        ("What was the first successful colony in America?", ["Plymouth", "Jamestown", "Roanoke", "Salem"], "Jamestown"),
        ("Who was the Soviet leader during World War II?", ["Lenin", "Stalin", "Khrushchev", "Trotsky"], "Stalin"),
        ("What year did the Berlin Wall fall?", ["1987", "1988", "1989", "1990"], "1989")
    ],
    "Literature": [
        ("Who wrote 'To Kill a Mockingbird'?", ["Harper Lee", "Mark Twain", "F. Scott Fitzgerald", "John Steinbeck"], "Harper Lee"),
        ("Who wrote 'Romeo and Juliet'?", ["Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain"], "William Shakespeare"),
        ("What is the first book of the Bible?", ["Genesis", "Exodus", "Leviticus", "Numbers"], "Genesis"),
        ("Who wrote 'The Odyssey'?", ["Homer", "Virgil", "Sophocles", "Euripides"], "Homer"),
        ("In 'Moby-Dick,' what is the name of the whale?", ["Willy", "Flipper", "Moby-Dick", "Jaws"], "Moby-Dick"),
        ("Who wrote 'Pride and Prejudice'?", ["Mary Shelley", "Jane Austen", "Emily Bronte", "Charlotte Bronte"], "Jane Austen"),
        ("What novel begins with 'Call me Ishmael'?", ["War and Peace", "The Odyssey", "Moby-Dick", "To Kill a Mockingbird"], "Moby-Dick"),
        ("What type of animal is the title character in 'Charlotte's Web'?", ["Dog", "Horse", "Pig", "Spider"], "Pig"),
        ("What genre is 'The Catcher in the Rye'?", ["Science Fiction", "Romance", "Drama", "Coming-of-Age"], "Coming-of-Age"),
        ("Who wrote '1984'?", ["George Orwell", "Aldous Huxley", "J.K. Rowling", "Ernest Hemingway"], "George Orwell")
    ],
    "Geography": [
        ("What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], "Paris"),
        ("What is the longest river in the world?", ["Nile", "Amazon", "Yangtze", "Mississippi"], "Nile"),
        ("Mount Everest is located in which country?", ["India", "Nepal", "China", "Bhutan"], "Nepal"),
        ("What is the largest ocean?", ["Atlantic", "Indian", "Arctic", "Pacific"], "Pacific"),
        ("In which continent is Brazil located?", ["Asia", "Africa", "South America", "Europe"], "South America"),
        ("Which U.S. state is known as the 'Sunshine State'?", ["California", "Texas", "Florida", "Arizona"], "Florida"),
        ("What is the capital of Japan?", ["Seoul", "Beijing", "Tokyo", "Bangkok"], "Tokyo"),
        ("What country has the largest population?", ["USA", "India", "China", "Russia"], "China"),
        ("The Sahara Desert is primarily located in which continent?", ["Asia", "South America", "Africa", "Australia"], "Africa"),
        ("Which country has the largest land area?", ["USA", "China", "Canada", "Russia"], "Russia")
    ]
}

def setup_database():
    conn = sqlite3.connect('quiz_bowl.db')
    cursor = conn.cursor()

    # Create tables for each category and add initial questions if necessary
    for category, questions in CATEGORY_QUESTIONS.items():
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {category} (
                question_id INTEGER PRIMARY KEY,
                question_text TEXT NOT NULL,
                option_1 TEXT,
                option_2 TEXT,
                option_3 TEXT,
                option_4 TEXT,
                correct_answer TEXT
            )
        """)

        # Check how many questions are already in the category
        cursor.execute(f"SELECT COUNT(*) FROM {category}")
        count = cursor.fetchone()[0]

        # If less than 10 questions, add category-specific questions
        if count < 10:
            for question_text, options, correct_answer in questions[:10 - count]:
                cursor.execute(f"""
                    INSERT INTO {category} (question_text, option_1, option_2, option_3, option_4, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (question_text, *options, correct_answer))

    conn.commit()
    conn.close()

# Initialize the database
setup_database()