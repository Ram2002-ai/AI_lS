from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()

# Simple one-line prompt
prompt=PromptTemplate.from_template('{question}')

llm=ChatOpenAI(
    model="openai/gpt-oss-20b",   # Must support structured outputs
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

parser=StrOutputParser()

# chain : prompt->llm->parser
chain=prompt|llm|parser

# Run it
result=chain.invoke({'question':'Who win fifa world cup over the seasons?'})
print(result)