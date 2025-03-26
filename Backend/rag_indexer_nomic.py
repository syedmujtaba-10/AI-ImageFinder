import json
import numpy as np
import faiss
import requests

# Constants
LLM_EMBEDDING_API = ""
LLM_MODEL = "text-embedding-nomic-embed-text-v1.5"

# Load image captions
with open("image_captions.json", "r") as f:
    captions_dict = json.load(f)

image_paths = list(captions_dict.keys())
captions = list(captions_dict.values())

def get_embedding(text: str) -> np.ndarray:
    payload = {
        "model": LLM_MODEL,
        "input": text
    }
    try:
        response = requests.post(LLM_EMBEDDING_API, json=payload)
        response.raise_for_status()
        return np.array(response.json()["data"][0]["embedding"], dtype=np.float32)
    except Exception as e:
        print(f"❌ Failed to embed: {text[:30]}... | Error: {e}")
        return None

# Generate all embeddings
print(f"🧠 Embedding {len(captions)} captions using {LLM_MODEL}...")
vectors = []
valid_paths = []

for path, caption in zip(image_paths, captions):
    vec = get_embedding(caption)
    if vec is not None:
        vectors.append(vec)
        valid_paths.append(path)

if not vectors:
    raise Exception("❌ No valid embeddings returned.")

embedding_matrix = np.vstack(vectors)
dimension = embedding_matrix.shape[1]

# Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)

# Save index and image paths
faiss.write_index(index, "caption_index.faiss")
np.save("caption_image_paths.npy", np.array(valid_paths))

print(f"✅ Indexed {len(valid_paths)} captions with Nomic embeddings.")
