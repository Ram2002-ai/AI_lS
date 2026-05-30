from langchain_huggingface  import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,
)

model = ChatHuggingFace(llm=llm)

# 1st prompt -> detailed report

template = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

# 2nd prompt -> summary of the report
template2 = PromptTemplate(
    template="Summarize the following report in 3-4 sentences:\n\n{report}",
    input_variables=["report"]
)

prompt1=template.invoke({"topic":"The impact of AI on society"})
result=model.invoke(prompt1)
prompt2=template2.invoke({"report":result.content})
final_result=model.invoke(prompt2)
print(final_result.content)