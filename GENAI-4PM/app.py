import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini response function
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-3.1-flash-lite")

    response = model.generate_content(question)

    return response.text

# Streamlit UI
st.set_page_config(page_title="Gemini AI App")

st.title("Gemini AI Chatbot")

user_input = st.text_input("Ask Something")

if st.button("Generate"):

    if user_input:

        response = get_gemini_response(user_input)

        st.subheader("Response")
        st.write(response)

    else:
        st.warning("Please enter a question")