import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

# Load environment variables from .env
load_dotenv()

# Read from environment variables
ES_ENDPOINT = os.getenv("ES_ENDPOINT", "http://localhost:9200")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

def get_es_client():
    """Creates and returns an Elasticsearch client."""
    if ES_API_KEY:
        client = Elasticsearch(
            ES_ENDPOINT,
            api_key=ES_API_KEY
        )
    elif ES_USERNAME and ES_PASSWORD:
        client = Elasticsearch(
            ES_ENDPOINT,
            http_auth=(ES_USERNAME, ES_PASSWORD)
        )
    else:
        client = Elasticsearch(ES_ENDPOINT)

    return client

# Create client instance
es_client = get_es_client()

# Optional: Test the connection
try:
    if es_client.ping():
        print("✅ Connected to Elasticsearch!")
    else:
        print("❌ Failed to connect to Elasticsearch.")
except Exception as e:
    print(f"❌ Error connecting to Elasticsearch: {e}")
