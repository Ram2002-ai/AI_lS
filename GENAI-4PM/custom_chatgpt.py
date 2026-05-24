from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langsmith tracking
os.environ["LANGSMITH_TRACING_V2"] = "true"

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

# Promt Template

promt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant"),
    ('user','Question: {question}')])

# streamlit app

st.title('LLM-OPENAI PROJECT -CUSTOM GPT-5 ')
question=st.text_input('Enter your question here')

# openai model
llm=ChatOpenAI(model='gpt5.1',temperature=1)
output_parser=StrOutputParser()
chain=promt | llm | output_parser

if question:
    st.write(chain.invoke({"question": question}))