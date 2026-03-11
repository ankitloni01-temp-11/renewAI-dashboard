"""ChromaDB vector store for objections + policy documents RAG."""
import os
import json
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from config import GOOGLE_API_KEY, EMBEDDING_MODEL

# Custom embedding function for Gemini
class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.genai = genai

    def __call__(self, input: List[str]) -> List[List[float]]:
        try:
            result = self.genai.embed_content(model=self.model_name, content=input)
            if 'embeddings' in result:
                return result['embeddings']
            elif 'embedding' in result:
                return result['embedding']
            return [[0.0] * 768 for _ in range(len(input))]
        except Exception as e:
            print(f"Embedding error: {e}")
            return [[0.0] * 768 for _ in range(len(input))]

# Custom embedding function for Gemini
_emb_fn = None

def get_embedding_function():
    global _emb_fn
    if _emb_fn is None:
        _emb_fn = GeminiEmbeddingFunction(api_key=GOOGLE_API_KEY, model_name=EMBEDDING_MODEL)
    return _emb_fn

_client = None
_objections_collection = None
_docs_collection = None

def get_client():
    global _client
    if _client is None:
        persist_dir = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')
        os.makedirs(persist_dir, exist_ok=True)
        _client = chromadb.PersistentClient(path=persist_dir, settings=Settings(anonymized_telemetry=False))
    return _client

def get_objections_collection():
    global _objections_collection
    if _objections_collection is None:
        client = get_client()
        _objections_collection = client.get_or_create_collection(
            name="objection_library",
            embedding_function=get_embedding_function(),
            metadata={"hnsw:space": "cosine"}
        )
    return _objections_collection

def get_docs_collection():
    global _docs_collection
    if _docs_collection is None:
        client = get_client()
        _docs_collection = client.get_or_create_collection(
            name="policy_documents",
            embedding_function=get_embedding_function(),
            metadata={"hnsw:space": "cosine"}
        )
    return _docs_collection

def ingest_objections(items: List[Dict]):
    """Ingest objection library into ChromaDB."""
    collection = get_objections_collection()
    
    # If already ingested, skip (or you could check for updates)
    if collection.count() > 0:
        return

    ids = [f"obj_{i}" for i in range(len(items))]
    # The JSON field is "objection", we map it to documents
    documents = [item.get("objection", "") for item in items]
    metadatas = [
        {
            "category": item.get("category", ""),
            "response": item.get("response", ""),
            "effectiveness_score": item.get("effectiveness_score", 0),
            "language": item.get("language", "en")
        } for item in items
    ]
    
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

def ingest_policy_docs():
    """Ingest policy document chunks into ChromaDB."""
    collection = get_docs_collection()
    if collection.count() > 0:
        return

    seed_dir = os.path.join(os.path.dirname(__file__), '..', 'seed_data', 'policy_documents')
    if not os.path.exists(seed_dir):
        return

    ids = []
    documents = []
    metadatas = []
    
    for fname in os.listdir(seed_dir):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(seed_dir, fname)
        # Extract product type from filename: suraksha_[type]_v1.txt
        parts = fname.split("_")
        product_type = parts[1] if len(parts) > 1 else "generic"
        
        try:
            with open(path) as f:
                content = f.read()
            
            # Simple chunking for demo
            chunks = [content[i:i+1000] for i in range(0, len(content), 800)]
            for i, chunk in enumerate(chunks):
                ids.append(f"{fname}_chunk_{i}")
                documents.append(chunk)
                metadatas.append({"filename": fname, "product_type": product_type})
        except:
            pass
            
    if ids:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

def search_objections(query: str, n: int = 5) -> List[Dict]:
    """Semantic search for objections."""
    collection = get_objections_collection()
    results = collection.query(query_texts=[query], n_results=n)
    
    formatted = []
    for i in range(len(results['ids'][0])):
        formatted.append({
            "objection_text": results['documents'][0][i],
            "category": results['metadatas'][0][i]['category'],
            "response": results['metadatas'][0][i]['response'],
            "effectiveness_score": results['metadatas'][0][i]['effectiveness_score'],
            "language": results['metadatas'][0][i]['language'],
            "_score": 1 - results['distances'][0][i]
        })
    return formatted

def search_policy_docs(query: str, product_type: str = None, n: int = 3) -> List[Dict]:
    """Semantic search for policy sections."""
    collection = get_docs_collection()
    
    where = {}
    if product_type:
        where = {"product_type": product_type}
        
    results = collection.query(query_texts=[query], n_results=n, where=where if where else None)
    
    formatted = []
    for i in range(len(results['ids'][0])):
        formatted.append({
            "filename": results['metadatas'][0][i]['filename'],
            "content": results['documents'][0][i],
            "relevance": 1 - results['distances'][0][i]
        })
    return formatted
