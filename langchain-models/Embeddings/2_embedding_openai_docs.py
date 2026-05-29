from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding=OpenAIEmbeddings(model='text-embedding-3-large',dimensions=32)

document=[
    "India is a country in South Asia. It is the seventh-largest country by land area and the second-most populous country in the world. The capital of India is New Delhi.",
    "The capital of India is New Delhi. It is a bustling metropolis that serves as the political, cultural, and economic center of the country. New Delhi is known for its rich history, vibrant culture, and diverse population.",
    "The economy of India is the world's fifth-largest by nominal GDP and the third-largest by purchasing power parity. It is a rapidly growing economy that is expected to be the world's largest economy by 2030.",
]

result = embedding.embed_documents(document)
print(str(result))