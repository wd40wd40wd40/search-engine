from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any
import asyncio
from pydantic import BaseModel

from crawler.crawler import Crawler

app = FastAPI()

index_data: Dict[str, Any] = {
    "tokens": {},
    "titles": {},
    "descriptions": {}
}

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
    
    tokens_dict = index_data.get("tokens", {})
    titles_dict = index_data.get("titles", {})
    descriptions_dict = index_data.get("descriptions", {})

    token = q.lower()
    if token not in tokens_dict:
        return {"results": []}
    
    postings = tokens_dict[token]

    results = []

    for doc_id, score in postings.items():
        title = titles_dict.get(doc_id, "(No title)")
        description = descriptions_dict.get(doc_id, "(No description)")
        results.append({
            "doc_id": doc_id,
            "title": title,
            "score": score,
            "description": description
        })

    return {"results": results}
# To run: python -m uvicorn api:app --reload