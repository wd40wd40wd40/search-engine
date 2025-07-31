import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any
import asyncio
from pydantic import BaseModel

from utility import snippet_highlighter

from crawler.crawler import Crawler

app = FastAPI()

index_data: Dict[str, Any] = {
    "tokens": {},
    "titles": {},
    "full_texts": {}
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
    return {"message": "You shouldn't be here..."}

@app.get("/search")
def search(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter 'q'")
    
    tokens_dict = index_data.get("tokens", {})
    titles_dict = index_data.get("titles", {})
    full_texts_dict = index_data.get("full_texts", {})

    token = q.lower()
    if token not in tokens_dict:
        return {"results": []}
    
    postings = tokens_dict[token]

    results = []

    for doc_id, score in postings.items():
        title = titles_dict.get(doc_id, "(No title)")
        full_text = full_texts_dict.get(doc_id, "")
        snippet_html = snippet_highlighter(full_text, q, snippet_length=30)
        results.append({
            "doc_id": doc_id,
            "title": title,
            "score": score,
            "snippet": snippet_html
        })

    return {"results": results}
# To run: python -m uvicorn api:app --reload