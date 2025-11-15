# src/embeddings_local.py
"""
Local sentence-transformers embedding wrapper with lazy background loading.
Provides embed_documents() and embed_query() methods compatible with langchain_chroma usage.
"""

from typing import List
import threading


class LocalSentenceTransformerEmbeddings:
    """
    Wrapper for sentence-transformers models with lazy background loading.
    
    This class provides a langchain-compatible embedding interface that:
    - Uses sentence-transformers for local, offline embedding generation
    - Loads the model lazily in the background to avoid blocking the main thread
    - Default model: all-MiniLM-L6-v2 (lightweight, good for demos)
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the local embeddings wrapper.
        
        Args:
            model_name: The sentence-transformers model to use.
                       Default is 'all-MiniLM-L6-v2' (384-dim, fast, good quality)
        """
        self.model_name = model_name
        self._model = None
        self._loading = False
        self._load_lock = threading.Lock()
        
        # Start loading the model in the background
        self._start_background_load()
    
    def _start_background_load(self):
        """Start loading the model in a background thread."""
        def _load():
            with self._load_lock:
                if self._model is None and not self._loading:
                    self._loading = True
                    try:
                        from sentence_transformers import SentenceTransformer
                        print(f"Loading local embedding model: {self.model_name}")
                        self._model = SentenceTransformer(self.model_name)
                        print(f"Local embedding model loaded: {self.model_name}")
                    except Exception as e:
                        print(f"Error loading local embedding model: {e}")
                        raise
                    finally:
                        self._loading = False
        
        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
    
    def _ensure_model_loaded(self):
        """Ensure the model is loaded, blocking if necessary."""
        with self._load_lock:
            if self._model is None:
                if not self._loading:
                    # Model hasn't started loading yet
                    from sentence_transformers import SentenceTransformer
                    print(f"Loading local embedding model: {self.model_name}")
                    self._model = SentenceTransformer(self.model_name)
                    print(f"Local embedding model loaded: {self.model_name}")
        
        # Wait for background loading to complete
        while self._model is None:
            import time
            time.sleep(0.1)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        self._ensure_model_loaded()
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding vector as a list of floats
        """
        self._ensure_model_loaded()
        embedding = self._model.encode([text], convert_to_numpy=True)
        return embedding[0].tolist()
