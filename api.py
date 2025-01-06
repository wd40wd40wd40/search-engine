from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any
import asyncio
from pydantic import BaseModel

from crawler.crawler import Crawler

app = FastAPI()

index_data: Dict[str, Dict[str,float]] = {} # holds loaded index data

# Handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrawlRequest(BaseModel):
    url: str
    max_pages: int = 10
    max_depth: int = 2

@app.post("/crawl")
async def crawl_endpoint(data: CrawlRequest):
    global index_data
    crawler = Crawler(
        start_url=data.url, 
        max_pages=data.max_pages, 
        max_depth=data.max_depth
    )

    await crawler.crawl()

    index_data = crawler.indexer.storage.get_index()

    with open("index_data.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False)
    
    return {
        "message": f"Crawl Finished"
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI. Try /search?q=<query>!"}

@app.get("/search")
def search(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter 'q'")
    
    token = q.lower()
    if token not in index_data:
        return {"results": []}
    
    postings = index_data[token]

    results = [{"doc_id": doc_id, "score": score} for doc_id, score in postings.items()]
    return {"results": results}
# To run: python -m uvicorn api:app --reload