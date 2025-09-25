import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
connection = sqlite3.connect('school.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Good practice: Drop the table if it already exists so we can rerun the script
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# Create the STUDENT table - CORRECTED
table_info = """
CREATE TABLE STUDENT(
    STUDENT_ID INT PRIMARY KEY,
    NAME VARCHAR(25),
    CITY VARCHAR(25),
    ENGLISH INT,
    MATHS INT,
    SCIENCE INT,
    HINDI INT,
    HISTORY INT,
    GEOGRAPHY INT,
    COMPUTER INT,
    TOTAL INT,
    PERCENTAGE FLOAT,
    GRADE CHAR(1)
);
"""
cursor.execute(table_info)

# Insert some sample records into the table - CORRECTED
students = [
    # Added a value for the COMPUTER column in each row
    (1, 'Rohan', 'Nagpur', 90, 85, 88, 92, 80, 95, 88, 530, 88.33, 'A'),
    (2, 'Priya', 'Mumbai', 75, 80, 78, 70, 85, 90, 79, 478, 79.67, 'B'),
    (3, 'Amit', 'Nagpur', 81, 79, 85, 88, 90, 87, 85, 510, 85.00, 'A'),
    (4, 'Sneha', 'Pune', 95, 92, 90, 94, 88, 91, 93, 560, 93.33, 'A'),
    (5, 'Vikram', 'Nagpur', 65, 70, 72, 68, 75, 80, 71, 430, 71.67, 'C'),
    (6, 'Anjali', 'Nagpur', 92, 89, 94, 90, 85, 88, 90, 538, 89.67, 'A'),
    (7, 'Karan', 'Delhi', 78, 82, 80, 76, 79, 85, 81, 480, 80.00, 'B'),
    (8, 'Meera', 'Nagpur', 88, 90, 85, 87, 92, 91, 89, 533, 88.83, 'A'),
    (9, 'Ravi', 'Chennai', 70, 75, 78, 72, 74, 80, 75, 449, 74.83, 'C'),
    (10, 'Sonal', 'Nagpur', 85, 88, 90, 86, 84, 89, 87, 522, 87.00, 'A')
]

# Corrected the INSERT statement to have 13 placeholders
cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", students)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database created and populated successfully!")
