
import streamlit as st
import sqlite3
import google.genai as genai
import pandas as pd  

# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyABDRl2z7DDmzrG7kXyTH1A40_WSXkBadQ')


#Loading gemini and get sql query as response

def get_response(question, prompt):
    full_prompt = f"{prompt[0]}\n\n{question}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # or "gemini-2.0-flash" if you want faster, cheaper responses
        contents=full_prompt
    )
    
    return response.text

#retreving the queried data from the db
def read_sql_query(sql,db):
    connn=sqlite3.connect(db)
    cur=connn.cursor()
    cur.execute(sql)

    #retrieving column names
    column=[description[0] for description in cur.description] 
    rows=cur.fetchall()

    connn.commit()
    connn.close()

    for i in rows:
        print(i)
    return column,rows


prompt=[
    """
    You are an expert at converting English questions to SQL queries!
The SQL database is named transactions and has the following columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

For example:
Example 1 – How many total transactions are recorded?
The SQL command will be something like:
SELECT COUNT(\*) FROM transactions;

Example 2 – Show all records where the country is United Kingdom.
The SQL command will be like:
SELECT \* FROM transactions WHERE Country = 'United Kingdom';

Example 3 – What is the total revenue generated?
The SQL command will be:
SELECT SUM(Quantity \* UnitPrice) AS TotalRevenue FROM transactions;

The SQL code should not have \`\`\` in the beginning or the end, and should not include the word "sql" in the output. Only return the SQL query.
"""]

st.set_page_config(page_title="Lets get you a SQL query")
st.header("Talking with the database using AI")


# 💡 Table Preview block

st.subheader("📋 Table Preview (first 30 rows)")
preview_query = "SELECT * FROM transactions LIMIT 30"
try:
    cols, preview_data = read_sql_query(preview_query, "customers.db")
    df_preview = pd.DataFrame(preview_data, columns=cols)
    st.dataframe(df_preview)
except Exception as e:
    st.error(f"Error loading preview: {e}")

#User Query block
questions=st.text_input("Input",key="input")
submit=st.button("Ask the query")

#Checking if submit button is clicked and the text given is non empty
if submit and questions.strip() != "":
    response = get_response(questions, prompt)
    st.subheader("🔍 SQL Query Generated")
    st.code(response)


    try:
        cols, data = read_sql_query(response, "customers.db")
        st.subheader("📊 Query Result")
        df = pd.DataFrame(data, columns=cols)
        st.dataframe(df)


    except Exception as e:
        st.error(f"Query failed: {e}")