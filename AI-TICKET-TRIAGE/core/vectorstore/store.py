import json
import numpy as np
import faiss
from pathlib import Path
from loguru import logger
from core.embeddings.embedder import get_embedding

INDEX_DIR = Path("core/vectorstore/data")
INDEX_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "metadata.json"
DIMENSION = 1536


class VectorStore:
    def __init__(self):
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        self.metadata: list[dict] = []
        if INDEX_FILE.exists() and META_FILE.exists():
            self.index = faiss.read_index(str(INDEX_FILE))
            self.metadata = json.loads(META_FILE.read_text())
            logger.info(f"Loaded vector store with {self.index.ntotal} vectors")
        else:
            self.index = faiss.IndexFlatL2(DIMENSION)
            logger.info("Created new empty vector store")

    def add(self, text: str, meta: dict):
        vec = np.array([get_embedding(text)], dtype="float32")
        self.index.add(vec)
        self.metadata.append(meta)

    def add_batch(self, texts: list[str], metas: list[dict]):
        from core.embeddings.embedder import get_embeddings_batch
        vecs = np.array(get_embeddings_batch(texts), dtype="float32")
        self.index.add(vecs)
        self.metadata.extend(metas)

    def search(self, query: str, k: int = 3) -> list[dict]:
        if self.index.ntotal == 0:
            return []
        vec = np.array([get_embedding(query)], dtype="float32")
        distances, indices = self.index.search(vec, min(k, self.index.ntotal))
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            entry = {**self.metadata[idx], "score": float(dist)}
            results.append(entry)
        return results

    def save(self):
        faiss.write_index(self.index, str(INDEX_FILE))
        META_FILE.write_text(json.dumps(self.metadata, indent=2))
        logger.info(f"Saved vector store ({self.index.ntotal} vectors)")


vector_store = VectorStore()