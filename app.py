from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Load OpenAI API key from environment variable

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langsmith Tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACKING_V2'] = 'true'


# Create Chatbot

prompt = ChatPromptTemplate.from_messages([
    
        ("system","You are a Language Teacher. Help user to Teach the language."),
        ("user","Question: {question}")
    
])

# Streamlit Framework

st.title("LangChain Language Teacher")
input_text = st.text_input("Enter your question:")

# Open AI LLM Call
llm = ChatOpenAI(model="gpt-2")
output_parser= StrOutputParser()

# chain
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))