# embedding_service.py
# Description: Semantic search and vector embeddings utilities
# Dependencies: sentence_transformers, numpy, logging
# Author: AI Generated Code
# Created: August 15, 2025

from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import List, Dict, Any
import logging

class EmbeddingService:
    """Handles semantic embedding and similarity search."""
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.logger = logging.getLogger(__name__)
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        try:
            return self.model.encode(texts, convert_to_tensor=True, show_progress_bar=False)
        except Exception as e:
            self.logger.error(f"Embedding error: {e}")
            return np.array([])
    
    def find_similar_chunks(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Find document chunks most similar to the query."""
        try:
            candidates = []
            chunk_texts = []
            chunk_meta = []
            for doc in documents:
                if 'chunks' in doc:
                    for chunk in doc['chunks']:
                        chunk_texts.append(chunk['content'])
                        chunk_meta.append({'source': doc.get('filename', ''), 'content': chunk['content']})
            if not chunk_texts:
                return []
            query_emb = self.embed([query])
            chunk_embs = self.embed(chunk_texts)
            scores = util.pytorch_cos_sim(query_emb, chunk_embs).squeeze(0).cpu().numpy()
            # Pair with metadata
            results = sorted([
                {**chunk_meta[i], 'similarity': float(scores[i])}
                for i in range(len(scores))
            ], key=lambda x: x['similarity'], reverse=True)
            return results[:top_k]
        except Exception as e:
            self.logger.error(f"Similarity search error: {e}")
            return []