"""Gemini embedding calls - stub for demo (RAG uses keyword search)."""
import google.generativeai as genai
from config import GOOGLE_API_KEY, EMBEDDING_MODEL
genai.configure(api_key=GOOGLE_API_KEY)

async def embed_text(text: str):
    """Get embedding for text."""
    try:
        result = genai.embed_content(model=EMBEDDING_MODEL, content=text)
        return result['embedding']
    except:
        return [0.0] * 768
