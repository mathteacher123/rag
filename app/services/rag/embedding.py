from google.genai import types
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

from app.core.config import settings

embed_model = GoogleGenAIEmbedding(
    model_name=settings.EMBEDDING_MODEL,
    api_key=settings.GEMINI_API_KEY,
    embedding_config=types.EmbedContentConfig(
        output_dimensionality=settings.EMBEDDING_DIM,
    ),
)
