from langchain_core.prompts import ChatPromptTemplate

chat_template=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant"),
    ("human","Explain in simple terms , what is {topic}")
])

prompt=chat_template.invoke({'domain':'AI','topic':'Artificial Intelligence'})

print(prompt)