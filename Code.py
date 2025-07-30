import os
os.environ['Open_Ai_Key'] ='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'
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
def build_rag_chain():
    loader=PyPDFLoader('General Notes.pdf')
    docs=loader.load()
    print(len(docs))
    print(docs[0])
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        )
    chunks = splitter.split_documents(docs)
    len(chunks)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("embeddings/faiss_index")
    retriever = db.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(OpenAI(), retriever=retriever)
    return qa_chain