import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.McqGenerator.logger import logging
from src.McqGenerator.utils import read_file, get_table_data
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

ai_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, api_key=key)

template_quiz_creator="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

template_quiz_checker="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template_quiz_creator
    )

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=template_quiz_checker)    

# Create the quiz generation chain
quiz_chain = quiz_generation_prompt | ai_model

# Create the review chain  
review_chain = quiz_evaluation_prompt | ai_model

# Create a function to run both chains sequentially
def generate_evaluate_chain(inputs):
    # Generate quiz first
    quiz_result = quiz_chain.invoke(inputs)
    
    # Then evaluate the quiz
    review_inputs = {
        "subject": inputs["subject"],
        "quiz": quiz_result.content
    }
    review_result = review_chain.invoke(review_inputs)
    
    return {
        "quiz": quiz_result.content,
        "review": review_result.content
    }