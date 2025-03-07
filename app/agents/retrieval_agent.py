# File: app/agents/retrieval_agent.py

from app.config.es_client import es_client

def retrieve_papers(query: str):
    """
    Retrieve academic papers matching the query using Elasticsearch.
    """
    search_body = {
        "query": {
            "match": {"full_text": query}
        }
    }
    res = es_client.search(index="papers", body=search_body)
    papers = []
    for hit in res.get('hits', {}).get('hits', []):
        paper = hit.get('_source', {})
        paper['id'] = hit.get('_id')
        papers.append(paper)
    return papers
