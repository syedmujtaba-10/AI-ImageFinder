import os
import json
import base64
from io import BytesIO
import numpy as np
import faiss
import torch
import open_clip
import requests
from PIL import Image

# Set device for PyTorch computations
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the CLIP model using open_clip (ViT-L-14)
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-L-14", pretrained="openai", device=device
)
model = model.to(device)

# llava API details
LLAVA_API = "http://192.168.68.50:1234/v1/chat/completions"
LLAVA_MODEL = "llava-v1.5-7b"

def generate_caption(image: Image.Image) -> str:
    """
    Use the LLAVA API to generate a detailed caption for the given image.
    The image is converted to a properly formatted base64-encoded image URL.
    """
    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Create the image URL format expected by LLAVA
    image_data = {
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{img_str}"}
    }

    # Properly structure the messages array
    payload = {
        "model": LLAVA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this image? Describe it with detailed elements, unique objects, and background context."},
                    image_data  # Image is passed as an object
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,  # Use a reasonable limit
        "stream": False
    }

    try:
        response = requests.post(LLAVA_API, json=payload)
        response.raise_for_status()
        caption = response.json()["choices"][0]["message"]["content"].strip()
        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return ""


# Define the directory containing images
image_dir = "data/images"
if not os.path.exists(image_dir):
    raise Exception(f"Image directory '{image_dir}' does not exist.")

# Gather all image paths (supports jpg, jpeg, png)
paths = [os.path.join(image_dir, f)
         for f in os.listdir(image_dir)
         if f.lower().endswith(("jpg", "jpeg", "png"))]

embeddings = []
captions = {}  # Dictionary to store generated captions keyed by image path

for img_path in paths:
    try:
        # Open and preprocess the image
        image = Image.open(img_path).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image_tensor)
        embeddings.append(embedding.cpu().numpy())

        # Generate a descriptive caption using llava
        caption = generate_caption(image)
        captions[img_path] = caption
        print(f"Processed: {img_path} | Caption: {caption}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

if len(embeddings) == 0:
    raise Exception("No images were processed. Please check your image folder.")

# Stack all embeddings into a single NumPy array
embeddings_array = np.vstack(embeddings)

# Create a FAISS index (CPU version) using L2 distance
d = embeddings_array.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings_array)

# Save the FAISS index and metadata
faiss.write_index(index, "image_index.faiss")
np.save("image_paths.npy", np.array(paths))
with open("image_captions.json", "w") as f:
    json.dump(captions, f, indent=2)

print(f"✅ Indexed {len(paths)} images with generated captions.")
