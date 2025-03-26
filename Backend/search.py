from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np
import json
import requests
from fastapi.staticfiles import StaticFiles
import os




# === Constants ===
LLM_EMBEDDING_API = "http://192.168.68.50:1234/v1/embeddings"
LLM_MODEL = "text-embedding-nomic-embed-text-v1.5"

# === Load data once at startup ===
with open("image_captions.json", "r") as f:
    captions_dict = json.load(f)

paths = list(captions_dict.keys())
index = faiss.read_index("caption_index.faiss")

# === FastAPI App ===
app = FastAPI(title="Image Search API", version="1.0")

# === Allow frontend (adjust origins if needed) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
image_dir = os.path.abspath("data/images")
app.mount("/images", StaticFiles(directory=os.path.abspath("data/images")), name="images")
# === Data Model for Response ===
class SearchResult(BaseModel):
    image_path: str
    caption: str

# === Helper functions ===
def get_embedding(text: str) -> np.ndarray:
    payload = {
        "model": LLM_MODEL,
        "input": text
    }
    try:
        response = requests.post(LLM_EMBEDDING_API, json=payload)
        response.raise_for_status()
        embedding = response.json()["data"][0]["embedding"]
        return np.array([embedding], dtype=np.float32)
    except Exception as e:
        print(f"❌ Error getting embedding for query: {e}")
        return None

def search_captions(query: str, k=5):
    embedding = get_embedding(query)
    if embedding is None:
        return []
    distances, indices = index.search(embedding, k)
    return [paths[i] for i in indices[0]]

# === API Endpoint ===
@app.get("/search", response_model=list[SearchResult])
def search_images(query: str = Query(..., description="Your image description query"), k: int = 5):
    result_paths = search_captions(query, k)
    results = [
        SearchResult(
            image_path=os.path.basename(path),  # ✅ just '000001.png'
            caption=captions_dict.get(path, "No caption available.")
        )
        for path in result_paths
    ]
    return results
