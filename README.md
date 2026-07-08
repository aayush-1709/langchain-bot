# AI Research Assistant Agent

A production-ready AI Research Assistant that allows you to upload PDFs or provide URLs, index them into a FAISS vector database, and chat with the content using Gemini-2.5-Flash.

## Architecture
- **Backend**: FastAPI
- **LLM**: Gemini API (via LangChain)
- **Vector DB**: FAISS (local persistence)
- **Ingestion**: PyMuPDF (PDFs) and BeautifulSoup (URLs)

## Setup

1. **Clone the repository** (or navigate to the folder).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   Create a `.env` file from `.env.example` and add your Google API Key:
   ```
   GOOGLE_API_KEY=AIza...
   ```
4. **Run the Backend**:
   ```bash
   python -m app.main
   ```
5. **Open the Frontend**:
   Simply open `frontend/index.html` in your browser.

## API Endpoints

- `POST /api/upload-pdf`: Upload a PDF file.
- `POST /api/ingest-url`: Provide a URL to scrape and index.
- `POST /api/chat`: Ask questions across all ingested documents.
- `GET /api/paper-summary/{paper_id}`: Get an auto-generated structured summary.

## Example Usage

### Chat via CURL
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the main findings of this research?"}'
```

---
Built with LangChain & Gemini.
