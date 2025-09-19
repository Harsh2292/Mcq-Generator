import os
import json
from sys import exception
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.McqGenerator.utils import get_table_data, read_file
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.McqGenerator.mcqgenerator import generate_evaluate_chain
from src.McqGenerator.logger import logging
import openai


with open(r"E:\DevStuff\Mcq Generator\Response.json", "r") as file:
    responce = json.load(file)

st.title('Mcq Generator using Langchain :chains:')

with st.form("user_input"):

        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "txt"])
        
        number = st.number_input("Enter the number of questions", min_value=5, max_value=100, value=10)

        subject = st.text_input("Enter the subject",max_chars=20)

        tone = st.text_input("Complexity level of the questions",max_chars=20,placeholder="Simple")

        button = st.form_submit_button("Generate MCQs")

        if button and uploaded_file is not None and number and subject and tone:
            with st.spinner("Generating MCQs..."):
                try:
                    file_content = read_file(uploaded_file)
                    if not file_content or not str(file_content).strip():
                        st.error("No readable text extracted from the file. Try another file.")
                        st.stop()

                    with get_openai_callback() as cb:
                        llm_responce = generate_evaluate_chain(
                            {"text":file_content,
                            "number":number,
                            "subject":subject,
                            "tone":tone,
                            "response_json":responce}
                            )

                except openai.RateLimitError as e:
                    st.error("OpenAI quota exceeded. Check your plan/billing and try again.")
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error("Error generating MCQs. Please try again.")

                else:
                        print(f"Total tokens used: {cb.total_tokens}")
                        print(f"Total cost: ${cb.total_cost}")
                        print(f"Prompt tokens: {cb.prompt_tokens}")
                        print(f"Completion tokens: {cb.completion_tokens}")

                        if isinstance(llm_responce, dict):
                            quiz = llm_responce.get("quiz", None)
                            if quiz is not None:
                                table_data = get_table_data(quiz)
                                if table_data:
                                    df = pd.DataFrame(table_data)
                                    df.index = df.index + 1
                                    st.table(df)

                                    st.text_area(label = "Review" , value= llm_responce["review"])
                                else:
                                    st.warning("Could not parse quiz into a table. Showing raw output below.")
                                    st.code(quiz)
                                    st.text_area(label = "Review" , value= llm_responce.get("review", ""))
                            else:
                                st.error("No quiz content returned.")
                        else:
                            st.write(llm_responce)