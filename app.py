import streamlit as st
import backend as be

# Title and description
st.title("🤖 Smart SQL Tool")
st.write("This tool uses AI to convert your English questions into SQL queries and runs them on a sample database.")

# load example.json only once and cache it
@st.cache_data
def load_example_data():
    return be.load_examples()

examples = load_example_data()

# Get the API key from secrets.toml
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found! Please add it to your .streamlit/secrets.toml file.")
    st.stop() 

# User input
user_question = st.text_area("Please enter your question in English:")

if st.button("Generate and Run Query"):
    if not user_question:
        st.error("Please enter your question.")
    else:
        with st.spinner("Processing your request..."):
            # 1. Find the best example (The "Junior Researcher") - THIS STILL RUNS IN THE BACKGROUND
            helpful_example = be.find_best_example(user_question, examples)
            
            # --- THIS SECTION HAS BEEN REMOVED FROM THE DISPLAY ---
            # The st.info(...) box that showed the example is now gone.

            # 2. Get the SQL from Gemini (The "Translator")
            generated_sql = be.get_sql_from_gemini(user_question, api_key, helpful_example)
            
            st.subheader("Generated SQL Query:")
            st.code(generated_sql, language="sql")

            # 3. Validate the SQL (The "Quality Checker")
            is_valid = be.is_sql_valid(generated_sql)
            
            if is_valid:
                st.success("✅ SQL Syntax is Valid.")
                # 4. Execute the query and display results
                results = be.run_sql_query(generated_sql, "school.db")
                st.subheader("Query Results:")
                if isinstance(results, str): # Check if an error message was returned
                    st.error(results)
                else:
                    st.dataframe(results)
            else:
                st.error("❌ The generated SQL has invalid syntax. Please try rephrasing your question.")

