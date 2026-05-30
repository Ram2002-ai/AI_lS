from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from langchain_core.messages import SystemMessage, HumanMessage,AIMessage

from dotenv import load_dotenv
load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,  
)
model = ChatHuggingFace(llm=llm)

chat_history = [
    SystemMessage(content="You are a helpful assistant."), 
]

while True:
    user_input=input("you: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break
    result=model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("assistant:", result.content)

print("Chat ended.",chat_history)