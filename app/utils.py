import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts import EXTRACTION_PROMPT

SUMMARY_DATA_DIR = "data/summaries"
if not os.path.exists(SUMMARY_DATA_DIR):
    os.makedirs(SUMMARY_DATA_DIR)

def clean_text(text):
    """Basic text normalization."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_paper_summary(text, paper_id):
    """Generates structured summary using Gemini."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0
    )
    
    # Use first 10k characters for summary to stay within context and be efficient
    truncated_text = text[:10000]
    
    prompt = EXTRACTION_PROMPT.format(text=truncated_text)
    response = llm.invoke(prompt)
    
    # Try to parse JSON from response
    content = response.content
    try:
        # Extract JSON block if LLM included triple backticks
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        summary_data = json.loads(content)
        
        # Save to file
        summary_path = os.path.join(SUMMARY_DATA_DIR, f"{paper_id}.json")
        with open(summary_path, "w") as f:
            json.dump(summary_data, f, indent=4)
            
        return summary_data
    except Exception as e:
        print(f"Error parsing summary: {e}")
        return {"error": "Failed to parse summary", "raw": content}

def get_summary(paper_id):
    """Retrieves saved summary."""
    summary_path = os.path.join(SUMMARY_DATA_DIR, f"{paper_id}.json")
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            return json.load(f)
    return None
