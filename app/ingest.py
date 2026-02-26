import os
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.vectorstore import add_to_vectorstore

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for i, page in enumerate(doc):
        text += f"\n--- Page {i+1} ---\n"
        text += page.get_text()
    return text

def extract_text_from_url(url):
    """Extracts text from a URL using BeautifulSoup."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    return soup.get_text(separator=' ', strip=True)

def process_and_ingest(text, source_name, metadata=None):
    """Chunks text and adds to vector store."""
    if metadata is None:
        metadata = {}
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    chunks = text_splitter.split_text(text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc_metadata = metadata.copy()
        doc_metadata.update({
            "source": source_name,
            "chunk_id": i
        })
        documents.append(Document(page_content=chunk, metadata=doc_metadata))
    
    add_to_vectorstore(documents)
    return len(documents)
