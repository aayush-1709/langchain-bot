import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.ingest import extract_text_from_pdf, extract_text_from_url, process_and_ingest
from app.utils import generate_paper_summary, get_summary
from app.chat import get_chat_chain

router = APIRouter()

class URLIngestRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    question: str

@router.post("/upload-pdf")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    paper_id = str(uuid.uuid4())
    pdf_path = f"data/pdfs/{paper_id}.pdf"
    
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(pdf_path)
    process_and_ingest(text, file.filename, {"paper_id": paper_id})
    
    # Generate summary in background
    background_tasks.add_task(generate_paper_summary, text, paper_id)
    
    return {"message": "PDF uploaded and processing started", "paper_id": paper_id}

@router.post("/ingest-url")
async def ingest_url(request: URLIngestRequest, background_tasks: BackgroundTasks):
    text = extract_text_from_url(request.url)
    paper_id = str(uuid.uuid4())
    
    process_and_ingest(text, request.url, {"paper_id": paper_id})
    
    # Generate summary in background
    background_tasks.add_task(generate_paper_summary, text, paper_id)
    
    return {"message": "URL content ingested and processing started", "paper_id": paper_id}

from pathlib import Path

@router.get("/list-papers")
async def list_papers():
    pdf_dir = Path("data/pdfs")
    papers = []

    for f in pdf_dir.glob("*.pdf"):
        papers.append({
            "id": f.stem,
            "name": f.name
        })

    return papers


@router.post("/chat")
async def chat(request: ChatRequest):
    chain = get_chat_chain()
    if not chain:
        raise HTTPException(status_code=400, detail="No documents ingested yet. Please upload a PDF or URL.")
    
    result = chain.invoke({"question": request.question})
    
    return {
        "answer": result["answer"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }

@router.get("/paper-summary/{paper_id}")
async def paper_summary(paper_id: str):
    summary = get_summary(paper_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found or still processing.")
    return summary
