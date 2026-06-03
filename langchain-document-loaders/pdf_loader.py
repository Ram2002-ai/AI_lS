from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader("E:\\dl.pdf")

docs=loader.load()

print(type(docs))
print(len(docs))
print(docs[1].page_content)
print(docs[0].metadata)