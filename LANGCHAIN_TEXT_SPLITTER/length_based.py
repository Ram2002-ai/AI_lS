from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"E:\Placement\5.SQL.pdf")
documents = loader.load()

splitter = CharacterTextSplitter(
    separator="",
    chunk_size=200,
    chunk_overlap=0
)

result = splitter.split_documents(documents)

print(result[0])