import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, index_path="embeddings/faiss_index.bin", metadata_path="embeddings/metadata.json"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if os.path.exists(index_path):
            print("Loading FAISS index...")
            self.index = faiss.read_index(index_path)
            with open(self.metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            print("No index found. Please run build_index.py first.")
            self.index = None
            self.metadata = None

    def embed(self, texts):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.astype("float32")

    def query(self, query_text, module_filter=None, k=5):
        if self.index is None:
            raise ValueError("RAG index not loaded.")

        q_emb = self.embed([query_text])
        scores, ids = self.index.search(q_emb, k)

        results = []
        for idx in ids[0]:
            doc = self.metadata[idx]

            if module_filter and doc["module"] != module_filter:
                continue

            results.append(doc)

        return results
