import os
from dotenv import load_dotenv

from langsmith import traceable 

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

LANGCHAIN_PROJECT="pdf_rag_demo"

PDF_PATH=r"E:\notes\islr.pdf"

# ============= helpers (not traced individually) ===========
@traceable(name='load_pdf')
def load_pdf(path:str):
    loader=PyPDFLoader(path)
    return loader.load()

@traceable(name='split_documents')
def split_documents(docs,chunk_size=1000,chunk_overlap=150):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

@traceable(name='build_vectorstore')
def build_vectorstore(splits):
    emb=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return FAISS.from_documents(splits,emb)

# ==================== parent setup function (traced) =====================
@traceable(name='setup_pipeline',tag=['setup'])
def setup_pipeline(pdf_path:str,chunk_size=1000,chunk_overlap=150):
    # these three steps are clubbed under this parent function
    docs=load_pdf(pdf_path)
    spilts=split_documents(docs,chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    vs=build_vectorstore(spilts)

    return vs

# =========================== model,prompt and run ===================

llm=ChatOpenAI(
    model="openai/gpt-oss-20b",   # Must support structured outputs
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)




prompt=ChatPromptTemplate([
    ('system','Answer only from the provided context. If not found , say you dont know.'),
    ('human',"Question:{question}\n\nContext:\n{context}")
])

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


# =========================== One top level (root) run =================
@traceable(name='pdf_rag_full_run')
def setup_pipeline_and_query(pdf_path:str,question:str):
    # parent setup run (child of root)
    vectorstore=setup_pipeline(pdf_path,chunk_size=1000,chunk_overlap=150)

    retriever=vectorstore.as_retriever(search_type='similarity',search_kwargs={'k':4})

    parallel=RunnableParallel({
        'context':retriever | RunnableLambda(format_docs),
        'question':RunnablePassthrough()
    })

    chain= parallel|prompt|llm | StrOutputParser()

    # This Langchain run stays under the same root (since we're inside this traced function)
    lc_config={'run_name':'pdf_rag_query'}
    return chain.invoke(question,config=lc_config)

if __name__=='__main__':
    print('PDF RAG ready. Ask a question (or Ctrl+C to exit).')
    q=input("\Q: ").strip()

    ans=setup_pipeline_and_query(PDF_PATH,q)
    print("\nA:",ans)