from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint   
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser,ResponseSchema

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,    
)

model = ChatHuggingFace(llm=llm)

# Define the output schema
schema = [
    ResponseSchema(name="fact", description="A fact about the topic"),
    ResponseSchema(name="source", description="The source of the fact"),
]

parser = StructuredOutputParser.from_response_schemas(schema)

# Define the prompt template
template = PromptTemplate(
    template="Give me a fact about {topic} along with its source. {format_instruction}",
    input_variables=["topic"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

chain = template | model | parser

result = chain.invoke({"topic": "Artificial Intelligence"})
print(result)