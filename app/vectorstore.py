import os
from langchain_community.vectorstores import FAISS
from app.embeddings import get_embeddings

VECTOR_DB_PATH = "data/vectordb"

def load_or_create_vectorstore(documents=None):
    """Loads existing FAISS index or creates a new one."""
    embeddings = get_embeddings()
    
    if os.path.exists(os.path.join(VECTOR_DB_PATH, "index.faiss")):
        return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    if documents:
        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local(VECTOR_DB_PATH)
        return vectorstore
    
    return None

def add_to_vectorstore(documents):
    """Adds documents to the existing FAISS index."""
    embeddings = get_embeddings()
    
    if os.path.exists(os.path.join(VECTOR_DB_PATH, "index.faiss")):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(documents)
    else:
        vectorstore = FAISS.from_documents(documents, embeddings)
    
    vectorstore.save_local(VECTOR_DB_PATH)
    return vectorstore
