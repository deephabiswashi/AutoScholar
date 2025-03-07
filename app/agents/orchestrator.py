from app.agents.retrieval_agent import retrieve_papers
from app.agents.summarization_agent import summarize_text

def run_assistant_individual(query: str):
    """
    Retrieve relevant papers and summarize each one individually.
    Returns a list of summaries, one per paper.
    """
    papers = retrieve_papers(query)
    if not papers:
        return {"error": "No papers found for the given query."}

    results = []
    for paper in papers:
        text = paper.get("content", "") or paper.get("full_text", "")
        summary = summarize_text(text)
        results.append({
            "id": paper.get("id"),
            "title": paper.get("title", "Untitled"),
            "summary": summary
        })
    return {"query": query, "results": results}

def run_assistant_aggregate(query: str):
    """
    Retrieve relevant papers, aggregate their contents, and summarize them in one go.
    Returns one combined summary for all papers.
    """
    papers = retrieve_papers(query)
    if not papers:
        return {"error": "No papers found for the given query."}
    aggregated_text = "\n\n".join(
        paper.get("content", "") or paper.get("full_text", "") for paper in papers
    )
    summary = summarize_text(aggregated_text)
    return {"query": query, "aggregated_summary": summary, "paper_count": len(papers)}
