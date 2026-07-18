from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

prompt1=PromptTemplate(
    template="Generate a detailed report on {topic}",
    input_variable=['topic']
)

prompt2=PromptTemplate(
    template=' Generate a 5 pointer summary from the following text \n {text}',
    input_variable=['text']
)

llm=ChatOpenAI(
    model="openai/gpt-oss-20b",   # Must support structured outputs
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

parser=StrOutputParser()

chain=prompt1|llm|parser|prompt2|llm|parser

result=chain.invoke({'topic':'Unemployement in India'})

print(result)