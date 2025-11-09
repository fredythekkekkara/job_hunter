import os
import hashlib
import json
from typing import List, Dict

import chromadb
# from chromadb.config import Settings

from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List
from langchain_community.embeddings import SentenceTransformerEmbeddings

from sentence_transformers import SentenceTransformer

class RAGManager:
    def __init__(self, persist_dir: str = "chroma_db"):
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "resume_kb"
        self.collection = None
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.lc_embedder = SentenceTransformerEmbeddings(
            model_name='all-MiniLM-L6-v2'
        )
        self.vector_store = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.lc_embedder,
            persist_directory=self.persist_dir 
        )

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

    def fetch_relevant_experience(
        self, 
        keywords: List[str], 
        top_k: int = 10,
        metadata_filter_type: str = "professional_experience.yml" 
    ) -> List[Document]:
        """
        Performs a similarity search on ChromaDB, filtered for professional experience, 
        using a set of extracted keywords as the query.

        Args:
            vectorstore: The initialized LangChain Chroma vector store instance.
            keywords: A list of relevant keywords extracted from the job description.
            top_k: The number of most similar documents to retrieve.
            metadata_filter_type: The value in the 'doc_type' metadata field 
                                that identifies professional experience documents.

        Returns:
            A list of LangChain Document objects containing the relevant experience content.
        """
        # 1. Construct the query string from keywords
        query_text = " ".join(keywords)
        
        # 2. Define the metadata filter
        # This assumes your YML files were loaded with metadata, for example:
        # {'doc_type': 'professional_experience', 'source': 'experience_1.yml'}
        
        # Chroma filter structure is a dictionary
        filter_dict = {
            "source": metadata_filter_type
        }
        
        # 3. Perform the similarity search with the filter
        # similarity_search returns a list of Document objects
        relevant_docs = self.vector_store.similarity_search(
            query=query_text, 
            k=top_k, 
            filter=filter_dict
        )

        results = self.collection.get(
            ids=None, # Retrieve all IDs
            where={}, # No filtering
            limit=None, # No limit
            include=["documents", "metadatas", "ids"]
        )
        return relevant_docs        