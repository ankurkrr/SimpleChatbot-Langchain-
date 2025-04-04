import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = 'true'

def get_openai_response(input_text1):
    response = requests.post("http://localhost:5000/essay/invoke", json={"input": {'topic': input_text1}})
    return response.json()['output']['content']

def get_llama_response(input_text2):
    response = requests.post("http://localhost:5000/poem/invoke", json={"input": {'topic': input_text2}})
    return response.json()['output']

st.title('LangChain Demo')
input_text1 = st.text_input('Write a essay on')
input_text2 = st.text_input('Write a poem on')


if input_text1:
    st.write(get_openai_response(input_text1))

if input_text2:
    st.write(get_llama_response(input_text2))