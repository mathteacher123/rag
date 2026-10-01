from llama_index.llms.google_genai import GoogleGenAI

from app.core.config import settings

llm = GoogleGenAI(
    api_key=settings.GEMINI_API_KEY,
    model=settings.LLM_MODEL,
    temperature=settings.LLM_TEMPERATURE,
    max_tokens=settings.LLM_MAX_TOKENS,
)
