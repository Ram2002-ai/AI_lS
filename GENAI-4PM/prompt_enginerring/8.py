
import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# Set your OpenAI API key
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Use environment variable for security

def retriever_info(query):
    # Dummy implementation for example purposes
    return "about prime minister of india"

def rag_query(query):
    retrieved_info = retriever_info(query)
    augmented_prompt = f"User query: {query}. Retrieved information: {retrieved_info}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": augmented_prompt}],
        max_tokens=300,
        temperature=0.2,
    )
    
    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title("RAG Prompt Query Interface")
user_input = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_input:
        response = rag_query(user_input)
        st.write("Response:", response)
    else:
        st.write("Please enter a query.")