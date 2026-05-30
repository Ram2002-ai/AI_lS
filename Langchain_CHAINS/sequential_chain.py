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
    template="Generate a 5 pointer summary from the following text \n {text}",
    input_variable=['text']
)

model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)

parser=StrOutputParser()

chain=prompt1|model|parser|prompt2|model|parser

result=chain.invoke({'topic':"Genai Jobs In Hyderabad"})

print(result)
chain.get_graph().print_ascii()