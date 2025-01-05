from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any

app = FastAPI()

# The following code is going to be dummy data for now as I try to connect the api to the frontend
class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str

def get_search_results(query: str) -> List[SearchResult]:
    return [
        SearchResult(url="https://example.com", title="Example", snippet="Example snippet..."),
        SearchResult(url="https://another.com", title="Another", snippet="Another snippet...")
    ]

@app.get("/search", response_model=List[SearchResult])
def search_endpoint(q: str):
    """
    Example endpoint:
    Send a GET request to: /search?q=<query>
    """
    results = get_search_results(q)
    return results

# To run: python -m uvicorn api:app --reload