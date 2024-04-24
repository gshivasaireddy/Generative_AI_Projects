import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file.get_table_data
from mcq_generator.logger import logging

# importing necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# load env variables from .env file
load_dotenv()

# access the env variables 
key = os.getenv('OPENAI_API_KEY')

llm=ChatOpenAI(openai_api_key=key,model_name='gpt-3.5.turbo',temperature=0.5)

TEMPLATE = """
Text:{text}
you are an expert MCQ Maker. Given the above text , it is your job to
create a quix of {number} multiple choice questions for {subject} students {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE
)

# chain to connect 2 prompts
quiz_chain = LLMChain(llm=llm,prompts=quiz_generation_prompt,output_key='quiz',verbose=True)

# second template
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple choice quiz for {subject} students.
You need to evaluate the complexity of the question and give a compelte analysis of the quiz. Only using
at max 50 words for complexity. if the quiz is not at par with the cognitive and analytical abilities of the students,
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the students
QUIZ_MCQs:
{quiz}

check from an expert English writer of the above quiz:
"""
quiz_evaluation_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=TEMPLATE2)

review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key"review",verbose=True)

# combine both the chains quiz_chain and review_chain using SequentialChain
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain,review_chain],
     input_variables=['text','number','subject','tone','response_json'],
    output_variables=['quiz','review'],
    verbose=True)

