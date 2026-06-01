from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel
from dotenv import load_dotenv
import os
load_dotenv()

prompt1=PromptTemplate(
    template="Genearte a tweet about {topic}",
    input_variables=["topic"]
)

prompt2=PromptTemplate(
    template="Genearte a LinkedIn post about {topic}",
    input_variables=["topic"]
)


model=ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-4o-mini"
)


parser=StrOutputParser()


parallel_chain=RunnableParallel({
    "tweet": prompt1|model|parser,
    "linkedin_post": prompt2|model|parser
})

result=parallel_chain.invoke({'topic':'AI'})
print(result)