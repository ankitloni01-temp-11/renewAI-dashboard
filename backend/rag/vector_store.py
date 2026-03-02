"""ChromaDB vector store for objections + policy documents RAG."""
import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict

_client = None
_objections_collection = None
_docs_collection = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))
    return _client

def search_objections(query: str, items: List[Dict], n: int = 5) -> List[Dict]:
    """Search objection library for relevant responses."""
    q = query.lower()
    results = []
    for obj in items:
        score = sum(1 for w in q.split() if w in obj.get("objection_text","").lower())
        if score > 0:
            results.append({**obj, "_score": score})
    results.sort(key=lambda x: x["_score"], reverse=True)
    return results[:n]

def search_policy_docs(query: str, product_type: str = None, n: int = 3) -> List[Dict]:
    """Search policy documents for relevant sections."""
    seed_dir = os.path.join(os.path.dirname(__file__), '..', 'seed_data', 'policy_documents')
    results = []
    type_map = {"term": "term_shield", "endowment": "endowment_plus", "ulip": "wealth_builder_ulip", "pension": "pension_secure", "child": "child_future"}
    filename = f"suraksha_{type_map.get(product_type, 'term_shield')}_v1.txt" if product_type else None
    
    for fname in os.listdir(seed_dir):
        if filename and fname != filename:
            continue
        path = os.path.join(seed_dir, fname)
        try:
            with open(path) as f:
                content = f.read()
            q_terms = query.lower().split()
            relevance = sum(1 for t in q_terms if t in content.lower())
            if relevance > 0 or not filename:
                results.append({"filename": fname, "content": content[:800], "relevance": relevance})
        except:
            pass
    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results[:n]
