import os
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple
import pickle
import json

class VectorStore:
    """Manages FAISS vector store for document embeddings using TF-IDF"""
    
    def __init__(self, model_name: str = "tfidf", store_dir: str = "vector_store"):
        # Use TF-IDF for embeddings - pure Python, no DLL dependencies
        self.vectorizer = TfidfVectorizer(max_features=384, ngram_range=(1, 2), min_df=1)
        self.store_dir = store_dir
        self.embedding_dim = 384
        self.fitted = False
        
        # Create store directory if it doesn't exist
        os.makedirs(store_dir, exist_ok=True)
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts using TF-IDF"""
        if not self.fitted:
            # Fit the vectorizer on the texts
            embeddings = self.vectorizer.fit_transform(texts).toarray().astype(np.float32)
            self.fitted = True
        else:
            # Transform using fitted vectorizer
            embeddings = self.vectorizer.transform(texts).toarray().astype(np.float32)
        
        # Pad or truncate to fixed dimension
        if embeddings.shape[1] < self.embedding_dim:
            padding = np.zeros((embeddings.shape[0], self.embedding_dim - embeddings.shape[1]), dtype=np.float32)
            embeddings = np.hstack([embeddings, padding])
        elif embeddings.shape[1] > self.embedding_dim:
            embeddings = embeddings[:, :self.embedding_dim]
        
        return embeddings
    
    def create_index(self, embeddings: np.ndarray) -> faiss.IndexFlatL2:
        """Create a FAISS index from embeddings"""
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create a flat L2 index
        index = faiss.IndexFlatL2(self.embedding_dim)
        index.add(embeddings)
        
        return index
    
    def save_index(self, document_id: str, index: faiss.IndexFlatL2, chunks: List[str], metadata: dict):
        """Save FAISS index and associated data to disk"""
        doc_dir = os.path.join(self.store_dir, document_id)
        os.makedirs(doc_dir, exist_ok=True)
        
        # Save FAISS index
        index_path = os.path.join(doc_dir, "index.faiss")
        faiss.write_index(index, index_path)
        
        # Save chunks
        chunks_path = os.path.join(doc_dir, "chunks.pkl")
        with open(chunks_path, 'wb') as f:
            pickle.dump(chunks, f)
        
        # Save vectorizer
        vectorizer_path = os.path.join(doc_dir, "vectorizer.pkl")
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        # Save metadata
        metadata_path = os.path.join(doc_dir, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def load_index(self, document_id: str) -> Tuple[faiss.IndexFlatL2, List[str], dict]:
        """Load FAISS index and associated data from disk"""
        doc_dir = os.path.join(self.store_dir, document_id)
        
        if not os.path.exists(doc_dir):
            raise FileNotFoundError(f"Vector store for document {document_id} not found")
        
        # Load FAISS index
        index_path = os.path.join(doc_dir, "index.faiss")
        index = faiss.read_index(index_path)
        
        # Load chunks
        chunks_path = os.path.join(doc_dir, "chunks.pkl")
        with open(chunks_path, 'rb') as f:
            chunks = pickle.load(f)
        
        # Load vectorizer
        vectorizer_path = os.path.join(doc_dir, "vectorizer.pkl")
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
            self.fitted = True
        
        # Load metadata
        metadata_path = os.path.join(doc_dir, "metadata.json")
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return index, chunks, metadata
    
    def search(self, document_id: str, query: str, top_k: int = 3) -> List[Tuple[str, float, int]]:
        """Search for similar chunks in the vector store"""
        # Load the index
        index, chunks, metadata = self.load_index(document_id)
        
        # Create query embedding
        query_embedding = self.create_embeddings([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = index.search(query_embedding, min(top_k, len(chunks)))
        
        # Prepare results with relevance scores
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(chunks):
                # Convert L2 distance to similarity score (inverse relationship)
                similarity_score = 1.0 / (1.0 + distance)
                results.append((chunks[idx], float(similarity_score), int(idx)))
        
        return results
    
    def delete_index(self, document_id: str):
        """Delete vector store for a document"""
        doc_dir = os.path.join(self.store_dir, document_id)
        if os.path.exists(doc_dir):
            # Remove all files in the directory
            for file in os.listdir(doc_dir):
                file_path = os.path.join(doc_dir, file)
                os.remove(file_path)
            # Remove the directory
            os.rmdir(doc_dir)
    
    def process_and_store(self, document_id: str, chunks: List[str], metadata: dict):
        """Complete pipeline: embed, index, and store"""
        # Create embeddings
        embeddings = self.create_embeddings(chunks)
        
        # Create index
        index = self.create_index(embeddings)
        
        # Save everything
        self.save_index(document_id, index, chunks, metadata)
        
        return len(chunks)
