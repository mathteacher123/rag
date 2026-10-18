# /workspaces/rag/evals/embeddings.py
from typing import List
import httpx
from langchain_core.embeddings import Embeddings

class FreeLLMAPIEmbeddings(Embeddings):
    # 🚀 Update __init__ to accept flexible keyword arguments (**kwargs)
    def __init__(self, model: str, api_key: str = None, api_base: str = None, **kwargs):
        self.model = model
        
        # 💡 Capture whatever variant Ragas or LangChain passes down
        raw_key = api_key or kwargs.get("openai_api_key")
        raw_base = api_base or kwargs.get("openai_api_base") or "http://localhost:3001/v1"
        
        if not raw_key:
            raise ValueError("An API key must be provided via 'api_key' or 'openai_api_key'.")
            
        self.api_key = raw_key
        self.api_base = raw_base.rstrip('/')

    def _embed(self, texts: List[str]) -> List[List[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "input": texts  
        }
        
        with httpx.Client() as client:
            response = client.post(
                f"{self.api_base}/embeddings", 
                json=payload, 
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return [item["embedding"] for item in data["data"]]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])
