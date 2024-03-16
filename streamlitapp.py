import os 
import json 
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenrator.utils import read_file, get_table_data
from langchain_community.callbacks import get_openai_callback
from src.mcqgenrator.mcqgenrator import genrate_eval_chain
from src.mcqgenrator.logger import logging

# Load .env file if necessary
# load_dotenv()

# Reading the JSON file
# Construct the file path relative to the current directory
json_file_path = "./response.json"
with open(json_file_path, "r") as file:
    response_json = json.load(file)

# Making title for app 
st.title("MCQ Creator Application")

# Create form using st.form
with st.form("user_inputs"):
    # File upload 
    uploaded_file = st.file_uploader("Upload PDF or Text file")
    
    # Input field 
    mcq_count = st.number_input("No of MCQs", min_value=3, max_value=50)
    
    # Subject 
    subject = st.text_input("Insert Subject", max_chars=50)
    
    # Quiz tone 
    tone = st.text_input("Complexity", max_chars=20, placeholder="simple/intermediate/difficult")
    
    button = st.form_submit_button("Create MCQs")

# Process user input
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Loading..."):
        try:
            text = read_file(uploaded_file)
            response = genrate_eval_chain({
                "text": text,
                "number": mcq_count,
                "subject": subject,
                "tone": tone,
                "response_json": json.dumps(response_json)
            })
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error: Failed to generate MCQs.")
        else:
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index += 1  # Start index from 1
                        st.table(df)
                        # Display review in text box 
                        st.text_area(label="Review", value=response["review"])
                    else:
                        st.error("Error: Failed to generate table data.")
                else:
                    st.write(response)