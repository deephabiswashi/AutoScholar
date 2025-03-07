from elasticsearch import Elasticsearch
import os
import json
from PyPDF2 import PdfReader

# Connect to Elasticsearch (Update if needed)
es = Elasticsearch("http://yourhost", basic_auth=("your_id", "your_password"))

INDEX_NAME = "research_papers"

# Create index mapping (if not exists)
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body={
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "file_name": {"type": "keyword"},
            }
        }
    })

# Function to extract text from PDF safely
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text.encode("utf-8", "ignore").decode("utf-8")  # Avoid encoding issues
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Ingest PDFs from "papers" folder
PAPERS_DIR = "researchpdfs"
for file in os.listdir(PAPERS_DIR):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(PAPERS_DIR, file)
        content = extract_text_from_pdf(pdf_path)
        if content.strip():
            doc = {"title": file.replace(".pdf", ""), "content": content, "file_name": file}
            es.index(index=INDEX_NAME, document=doc)
            print(f"Indexed: {file}")
        else:
            print(f"Skipping empty or unreadable file: {file}")
