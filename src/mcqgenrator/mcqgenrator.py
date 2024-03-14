
import os
import json
import traceback
import PyPDF2
from dotenv import load_dotenv
import pandas as pd
from src.mcqgenrator.logger import logging
from src.mcqgenrator.utils import read_file,get_table_data

# package from langchiain 
# from langchain.llms import OpenAI 
# from langchain_openai import ChatOpenAI
# from langchain.callbacks import get_openai_callback

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_community.callbacks import get_openai_callback
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI

# loadingg api key 
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")


# assing model 
llm = ChatOpenAI( 
            openai_api_key = KEY,
            model_name = "gpt-3.5-turbo"
            )

# making template 
TEMPLATE = """
Text: {text}
You are an expert MCQ (multiple-choice question) maker. Given the above text, it is your job to create a quiz for {number} multiple-choice questions for {subject} students in {tone} tone.
Make sure that questions are not repeated at all, check all questions to confirm text accuracy as well.
Ensure making {number} MCQs.
### RESPONSE_JSON 
{response_json}
"""

# lets write prompt

mcq_genration_prompt= PromptTemplate(
    input_variables = ["text","number","subject","tone","response_json"],
    template = TEMPLATE
    
)

quiz_chain= LLMChain(llm=llm,prompt=mcq_genration_prompt,output_key="quiz",verbose=True)


evaluation_template = """
You are an expert English grammarian and writer. Given a multiple-choice quiz for {subject} students,
you need to evaluate the complexity of questions and provide a complete analysis. Use a maximum of 50 words to describe complexity.
If the quiz doesn't align with students' cognitive and analytical abilities,
update questions needing changes and adjust the tone to better suit students.
Quiz MCQ:
{quiz}

Check from an expert English writer of the above quiz:
"""

evalutaion_prompt = PromptTemplate(
    input_variables= ["subject","quiz"],
    template= evaluation_template
) 

evalutaion_chain= LLMChain(llm=llm,prompt=evalutaion_prompt,output_key="review",verbose=True)

genrate_eval_chain = SequentialChain(
    chains = [quiz_chain,evalutaion_chain],
    input_variables = ["text","number","subject","tone","response_json"],
    output_variables = ["quiz","review"],
    verbose= True
)




