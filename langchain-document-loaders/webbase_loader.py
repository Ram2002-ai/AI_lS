from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"    
)

prompt=PromptTemplate(
    template="Answer the following question \n {question} from the following text \n {text}",
    input_variables=["question","text"]
)

parser=StrOutputParser()

url="https://en.wikipedia.org/wiki/Artificial_intelligence"
loader=WebBaseLoader(url)

docs=loader.load()

chain=prompt | model | parser

print(chain.invoke({"question":"What is Artificial Intelligence?","text":docs[0].page_content}))