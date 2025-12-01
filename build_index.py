import os
import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pdfplumber
import docx

RAW_DIR = "data/raw"
INDEX_PATH = "embeddings/faiss_index.bin"
META_PATH = "embeddings/metadata.json"

# -----------------------------------------------------
# 1. TEXT EXTRACTION
# -----------------------------------------------------

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_documents():
    documents = []

    for module in os.listdir(RAW_DIR):
        module_path = os.path.join(RAW_DIR, module)

        if not os.path.isdir(module_path):
            continue  # skip non-folders

        for filename in os.listdir(module_path):
            file_path = os.path.join(module_path, filename)

            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith(".docx"):
                text = extract_text_from_docx(file_path)
            elif filename.lower().endswith(".txt") or filename.lower().endswith(".md"):
                text = extract_text_from_txt(file_path)
            else:
                print(f"Skipping unsupported file: {file_path}")
                continue

            documents.append({
                "module": module,
                "source": filename,
                "text": text
            })

    return documents

# -----------------------------------------------------
# 2. CHUNKING
# -----------------------------------------------------

def chunk_text(text, chunk_size=250):
    # A simple chunker (word-based)
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        if len(chunk.strip()) > 0:
            chunks.append(chunk)

    return chunks

# -----------------------------------------------------
# 3. BUILD INDEX
# -----------------------------------------------------

def build_index():
    print("Loading transcripts…")
    raw_docs = load_documents()

    print(f"Found {len(raw_docs)} raw documents.")

    processed = []
    for doc in raw_docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            processed.append({
                "text": chunk,
                "module": doc["module"],
                "source": doc["source"],
                "chunk_id": f"{doc['module']}_{doc['source']}_chunk{i}"
            })

    print(f"Generated {len(processed)} chunks.")

    # Embeddings
    print("Embedding…")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [item["text"] for item in processed]
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

    # FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2)

    print("FAISS index + metadata created!")
    print(f"Total chunks: {len(processed)}")
    print("Done.")

if __name__ == "__main__":
    build_index()
