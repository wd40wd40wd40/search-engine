from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any

app = FastAPI()

# Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search", response_model=List[SearchResult])
def search_endpoint(q: str):
    """
    Example endpoint:
    Send a GET request to: /search?q=<query>
    """
    results = get_search_results(q)
    return results

# To run: python -m uvicorn api:app --reload