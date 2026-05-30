from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
load_dotenv()

prompt=PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variable=['topic']
)

model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)

parser=StrOutputParser()

chain=prompt|model|parser

result=chain.invoke({'topic':"ipl"})

print(result)

chain.get_graph().print_ascii()