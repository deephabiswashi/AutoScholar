from fastapi import APIRouter, Query
from app.agents.orchestrator import run_assistant_individual, run_assistant_aggregate

router = APIRouter()

@router.get("/assist/individual")
def assist_individual(query: str = Query(..., description="Enter your research query")):
    """
    Endpoint that returns individual summaries for each retrieved paper.
    """
    try:
        result = run_assistant_individual(query)
        return result
    except Exception as e:
        return {"error": f"Internal Server Error: {e}"}

@router.get("/assist/aggregate")
def assist_aggregate(query: str = Query(..., description="Enter your research query")):
    """
    Endpoint that returns one aggregated summary for all retrieved papers.
    """
    try:
        result = run_assistant_aggregate(query)
        return result
    except Exception as e:
        return {"error": f"Internal Server Error: {e}"}
