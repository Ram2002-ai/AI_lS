from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os
load_dotenv()

prompt1=PromptTemplate(
    template="write a joke about {topic}",
    input_variables=["topic"]
)

model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)


parser=StrOutputParser()

prompt2=PromptTemplate(
    template='explain the following joke {response}',
    input_variables=['response']
)

chain=RunnableSequence(prompt1,model,parser,prompt2,model,parser)
result=chain.invoke({'topic':'programming'})
print(result)