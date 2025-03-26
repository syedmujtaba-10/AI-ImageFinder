# search.py

import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Load caption data and model
with open("image_captions.json", "r") as f:
    captions_dict = json.load(f)

paths = list(captions_dict.keys())
captions = list(captions_dict.values())

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("caption_index.faiss")

def search_captions(query: str, k=5):
    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)
    return [paths[i] for i in indices[0]]

def get_caption_for_image(image_path: str) -> str:
    return captions_dict.get(image_path, "No caption available.")
