from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnableBranch,RunnablePassthrough, RunnableLambda
import os
load_dotenv()

prompt1=PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=["topic"]
)

prompt2=PromptTemplate(
    template="summarize the following report {response}",
    input_variables=["response"]    
)

model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)

parser=StrOutputParser()

regort_gen_chain=RunnableSequence(prompt1,model,parser)

branch_chain=RunnableBranch(
    (lambda x: len(x.split())>300, prompt2 | model | parser),
    RunnablePassthrough()
)

final_chain=regort_gen_chain | branch_chain
result=final_chain.invoke({'topic':'AI'})
print(result)