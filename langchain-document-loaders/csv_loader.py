from langchain_community.document_loaders import CSVLoader

loader=CSVLoader(file_path="E:\\data\\data_set\\Social_Network_Ads.csv")
docs=loader.load()
print(type(docs))
print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)