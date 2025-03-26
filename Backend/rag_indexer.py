import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load image captions
with open("image_captions.json", "r") as f:
    captions_dict = json.load(f)

image_paths = list(captions_dict.keys())
captions = list(captions_dict.values())

# Load sentence embedding model (can swap with better one)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(captions, convert_to_numpy=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index and paths
faiss.write_index(index, "caption_index.faiss")
np.save("caption_image_paths.npy", np.array(image_paths))
print(f"✅ Indexed {len(image_paths)} image captions.")
