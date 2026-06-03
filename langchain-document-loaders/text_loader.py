from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)

prompt=PromptTemplate(
    template='Write a summary for the following poem- \n {poem}',
    input_variables=['poem']
)   

parser=StrOutputParser()

loader=TextLoader("cricket.txt",encoding="utf-8")

docs=loader.load()

print(type(docs))
print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)