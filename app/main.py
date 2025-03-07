from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import sys

# Ensure 'app' is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.es_client import get_es_client
from app.agents.summarization_agent import summarize_text

es = get_es_client()

app = FastAPI(title="Automated Research Assistant")

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve the index.html directly
@app.get("/")
def serve_index():
    return FileResponse("app/templates/index.html")

@app.get("/search")
async def search_papers(query: str = Query(..., min_length=3)):
    """
    Returns JSON data with matching papers.
    The frontend fetches this JSON and displays results dynamically.
    """
    es_query = {
        "query": {
            "match": {"content": query}  # Adjust field name as needed
        }
    }
    response = es.search(index="research_papers", body=es_query)
    papers = [
        {
            "id": hit["_id"],
            "title": hit["_source"].get("title", "Untitled Paper")
        }
        for hit in response["hits"]["hits"]
    ]
    return JSONResponse(content={"papers": papers})

@app.get("/summarize")
async def summarize_paper(paper_id: str = Query(...)):
    """
    Returns JSON data for a selected paper summary.
    Uses the local Ollama model (via summarize_text) for summarization.
    """
    # Get the paper from Elasticsearch
    resp = es.get(index="research_papers", id=paper_id)
    source = resp["_source"]
    
    # Use the summarization agent that calls Ollama
    summary = summarize_text(source.get("content", ""))
    
    return JSONResponse(content={"paper": {"title": source.get("title", "Untitled")}, "summary": summary})

