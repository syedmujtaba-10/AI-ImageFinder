# 🧠 ImageFinder: AI-Powered Image Search with FastAPI + React

ImageFinder is a full-stack **AI-powered semantic image search engine** that lets users describe what they want to see and instantly retrieves relevant images from a local dataset. It uses **LLaVA for caption generation** and **Nomic embeddings for search**, all hosted locally via **LM Studio**.

---

## 🚀 Features

- 🔍 Semantic image search via **natural language**
- 🧠 **LLaVA** (via local API) for automatic image caption generation
- 🔎 **Nomic `text-embedding-nomic-embed-text-v1.5`** for fast and accurate embedding vectors
- ⚡ Local vector search using **FAISS**
- 💻 Clean and fast React frontend built with Tailwind CSS
- 🖼️ Image serving directly from your filesystem (no cloud dependencies)
- 🔐 100% Local — No OpenAI or external API keys needed

---


## 🧠 AI Under the Hood

### 🖼️ **Captioning** (LLaVA):
Each image is processed using **LLaVA** (`llava-v1.5-7b`) running locally using LM Studio
This generates human-like, descriptive captions for all images in your dataset.

### 📌 **Embeddings** (Nomic via LM Studio):
We use the powerful **Nomic text embedding model**: Model ID: text-embedding-nomic-embed-text-v1.5
It converts both image captions and search queries into vector space for **fast and accurate similarity search** via FAISS.

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/syedmujtaba-10/AI-ImageFinder.git
cd Backend
```

### 2️. Backend Setup
```bash
cd backend
```

• Place your images

Copy your images into data/images/ (create folder if missing).

• Create & activate a Python virtual environment

python -m venv .venv
### Windows
```bash
.venv\Scripts\activate
```
### macOS/Linux
```bash
source .venv/bin/activate
```
• Install dependencies
```bash
pip install -r requirements.txt
```
• Configure LM Studio
Launch LM Studio
Load llava-v1.5-7b and nomic models
Start the local API server
Copy each model’s API URL (e.g. http://localhost:1234)

• Wire in the APIs
Open index_images.py, paste your llava API URL into the LLAVA_API constant.
Open rag_indexer_nomic.py, paste your nomic API URL into the NOMIC_API constant.

• Build the index
```bash
python index_images.py
python rag_indexer_nomic.py
```
### Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Visit http://localhost:3000 to interact with your local AI image search app.

