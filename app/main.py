import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(title="AI Research Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("data/pdfs", exist_ok=True)
os.makedirs("data/vectordb", exist_ok=True)
os.makedirs("data/summaries", exist_ok=True)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to AI Research Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
