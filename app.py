
import streamlit as st
import pandas as pd  

from ai_utils import get_response
from read_query import read_sql_query
from config import prompt

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
