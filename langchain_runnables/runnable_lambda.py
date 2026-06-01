from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda
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

def word_count(text):
    return len(text.split())

joke_gen_chain=RunnableSequence(prompt1,model,parser)


parallel_chain=RunnableParallel({
    'joke': RunnablePassthrough() ,
    "word_count":RunnableLambda(word_count)
    # or
    # "word_count":RunnableLambda(lambda x: len(x.split()))
})

final_chain=joke_gen_chain | parallel_chain
result=final_chain.invoke({'topic':'programming'})
print(result)