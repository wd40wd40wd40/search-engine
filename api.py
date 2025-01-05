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

INDEX_DATA: Dict[str, Dict[str,float]] = {} # holds loaded index data

@app.on_event("startup")
def load_index_data():
    global INDEX_DATA
    try:
        with open("index_data.json", "r", encoding="utf-8") as f:
            INDEX_DATA = json.load(f)
        print("Index data loaded")
    except FileNotFoundError:
        print("Index data not generated")


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI. Try /search?q=<query>!"}

@app.get("/search")
def search(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter 'q'")
    
    token = q.lower()
    if token not in INDEX_DATA:
        return {"results": []}
    
    postings = INDEX_DATA[token]

    results = [{"doc_id": doc_id, "score": score} for doc_id, score in postings.items()]
    return {"results": results}

# To run: python -m uvicorn api:app --reload