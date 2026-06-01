from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough
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

joke_gen_chain=RunnableSequence(prompt1,model,parser)

parallel_chain=RunnableParallel({
    'joke': RunnablePassthrough() ,
    'explanation': RunnableSequence(prompt2,model,parser)
})

final_chain=joke_gen_chain | parallel_chain
result=final_chain.invoke({'topic':'programming'})
print(result)