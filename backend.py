import os
import json
import sqlite3
import google.generativeai as genai

# --- 1. The "Junior Researcher" Module ---
def load_examples(filepath="examples.json"):
    """Loads the example library from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def find_best_example(user_question, examples):
    """
    Finds the best example from a list based on word overlap.
    A simple but effective keyword matching approach.
    """
    best_example = None
    max_overlap = 0
    user_words = set(user_question.lower().split())

    for example in examples:
        example_words = set(example["question"].lower().split())
        overlap = len(user_words.intersection(example_words))

        if overlap > max_overlap:
            max_overlap = overlap
            best_example = example
    
    # Return a default if no good match is found to prevent errors
    if best_example is None:
        return examples[0]
    return best_example

# --- 2. The "Quality Checker" Module (NEW RELIABLE VERSION) ---
def is_sql_valid(sql_query, db_path="school.db"):
    """
    Checks if the generated SQL syntax is valid by attempting to execute it
    within a transaction and then immediately rolling back.
    This is a safe way to use the database's own parser for validation.
    """
    if not sql_query.strip():
        return False
        
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Begin a transaction to create a safe "sandbox"
        cursor.execute("BEGIN TRANSACTION")
        
        # Try to execute the query. This will parse it and check syntax.
        cursor.execute(sql_query)
        
        # If we reach here, the syntax is valid. 
        # IMPORTANT: Immediately rollback to undo everything.
        conn.rollback()
        conn.close()
        return True
    except sqlite3.Error as e:
        # The execute failed, so syntax is invalid.
        # The transaction ensures no changes were made.
        if conn:
            conn.rollback()
            conn.close()
        return False

# --- 3. The "Translator" and "Executor" Modules ---
def get_sql_from_gemini(user_question, api_key, helpful_example=None):
    """
    Sends the request to the Gemini model to get the SQL query.
    Now includes a helpful example in the prompt if one is found.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prompt with the fully CORRECTED schema
    prompt = """
    You are an expert at converting English questions into SQL queries.
    Your task is to write a SQL query that answers the user's question based on the provided database schema.

    IMPORTANT: When filtering by a text field like NAME or CITY, the comparison must be case-insensitive. To achieve this, use the LOWER() function on both the column and the user's value. For example: LOWER(CITY) = LOWER('Nagpur')

    ## Database Schema
    The database has one table named `STUDENT` with the following columns:
    - STUDENT_ID (INTEGER, PRIMARY KEY)
    - NAME (TEXT)
    - CITY (TEXT)
    - ENGLISH (INTEGER)
    - MATHS (INTEGER)
    - SCIENCE (INTEGER)
    - HINDI (INTEGER)
    - HISTORY (INTEGER)
    - GEOGRAPHY (INTEGER)
    - COMPUTER (INTEGER)
    - TOTAL (INTEGER)
    - PERCENTAGE (REAL)
    - GRADE (TEXT)
    """
    
    if helpful_example:
        prompt += """
        \n## Here is a similar, helpful example to guide you:
        Question: {example_question}
        SQL: {example_query}
        """.format(
            example_question=helpful_example["question"],
            example_query=helpful_example["query"]
        )
    
    prompt += "\n## User Question\n" + user_question
    prompt += "\n\n## SQL Query"

    response = model.generate_content(prompt)
    sql_query = response.text.replace("```sql", "").replace("```", "").strip()
    return sql_query

def run_sql_query(sql, db):
    """Executes a SQL query and fetches the results."""
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        return f"Database error: {e}"

