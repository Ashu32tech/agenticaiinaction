
import faiss
import numpy as np
from backend.rag.embeddings import embed

class QuadrantDB:
    def __init__(self):
        self.data = {
            "logs": ["OOMKilled error", "CrashLoopBackOff restart"],
            "incidents": ["OOMKilled due to memory", "ImagePullError"],
            "runbooks": ["Increase memory limits", "Fix image repo"],
            "metrics": ["High memory usage causes restart"]
        }
        self.indexes = {}

    def build(self):
        for key, texts in self.data.items():
            vectors = embed(texts)
            index = faiss.IndexFlatL2(len(vectors[0]))
            index.add(np.array(vectors).astype("float32"))
            self.indexes[key] = (index, texts)

    def search(self, query):
        q = embed([query])
        results = []
        for key in self.indexes:
            index, texts = self.indexes[key]
            D, I = index.search(np.array(q).astype("float32"), 1)
            results.append({key: texts[I[0][0]]})
        return results
