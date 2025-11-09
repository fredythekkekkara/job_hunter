import os
import hashlib
import json
from typing import List, Dict

import chromadb
# from chromadb.config import Settings

from sentence_transformers import SentenceTransformer

class RAGManager:
    def __init__(self, persist_dir: str = "chroma_db"):
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "resume_kb"
        self.collection = None
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def _hash_kb(self, kb_data: Dict[str, dict]) -> str:
        serialized = json.dumps(kb_data, sort_keys=True).encode()
        return hashlib.sha256(serialized).hexdigest()

    def build_or_load(self, kb_data: Dict[str, dict]) -> None:
        # Check hash file to detect KB changes
        hash_file = os.path.join(self.persist_dir, 'kb_hash.txt')
        new_hash = self._hash_kb(kb_data)

        rebuild = True
        if os.path.exists(hash_file):
            with open(hash_file, 'r') as f:
                old_hash = f.read()
            if old_hash == new_hash:
                rebuild = False

        if rebuild:
            print("Building RAG index from KB data...")
            if self.collection:
                self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)
            self._add_documents(kb_data)
            with open(hash_file, 'w') as f:
                f.write(new_hash)
        else:
            print("Loading existing RAG index...")
            self.collection = self.client.get_collection(self.collection_name)

    def _add_documents(self, kb_data: Dict[str, dict]):
        documents = []
        metadatas = []
        ids = []
        idx = 0
        for fname, content in kb_data.items():
            text = json.dumps(content)
            documents.append(text)
            metadatas.append({"source": fname})
            ids.append(f"doc_{idx}")
            idx += 1

        embeddings = self.embedder.encode(documents).tolist()
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        if not self.collection:
            raise ValueError("Collection is not initialized")
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        # returns dictionary with documents, metadatas, ids, distances
        return results['documents'][0]
