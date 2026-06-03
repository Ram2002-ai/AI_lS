import os

import streamlit as st
from google import genai
from google.genai import types


st.set_page_config(
    page_title="Gemini RAG App",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Prompt Engineering using Gemini")


def retriever_info(query):
    """Return extra context for the prompt.

    This is a demo retriever. In a real RAG app, this function can search a
    PDF, vector database, website, or normal database.
    """
    return (
        "India is one of the world's fastest-growing major economies. "
        "Important sectors include services, agriculture, manufacturing, "
        "technology, digital payments, startups, and infrastructure."
    )


def rag_query(query, api_key):
    retrieved_info = retriever_info(query)
    augmented_prompt = f"""
You are a helpful assistant.

User query:
{query}

Retrieved information:
{retrieved_info}

Answer clearly and use the retrieved information when it is relevant.
"""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=augmented_prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=1000,
            top_p=0.95,
            top_k=40,
            stop_sequences=["End"],
        ),
    )

    return response.text.strip()


api_key = st.text_input(
    "🔑 Enter your Gemini API Key",
    value=os.getenv("GEMINI_API_KEY", ""),
    type="password",
)

query = st.text_area(
    "💬 Ask a question",
    "Explain India's economy in simple words.",
)

if st.button("🔍 Generate Response"):
    if not api_key.strip():
        st.warning("Please enter your Gemini API key first.")
    elif not query.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Generating response..."):
            try:
                answer = rag_query(query, api_key)
                st.success("✅ Response generated!")
                st.markdown(f"**Answer:**\n\n{answer}")
            except Exception as e:
                st.error(f"Error: {e}")


st.markdown("---")
st.caption("Built with Streamlit + Google Gemini API + Prakash Senapati")
