import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
import json
from pathlib import Path

class VectorStore:
    """
    ChromaDB-based vector store for RAG
    Stores objection responses, policy docs, objection library
    """
    
    def __init__(self, persist_dir: str = "database/chroma_db"):
        self.persist_dir = persist_dir
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize persistent ChromaDB
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=persist_dir,
                is_persistent=True
            )
        )
        
        self._init_collections()
    
    def _init_collections(self):
        """Initialize ChromaDB collections"""
        try:
            self.objection_collection = self.client.get_or_create_collection(
                name="objections",
                metadata={"description": "Objection handling responses"}
            )
            
            self.policy_collection = self.client.get_or_create_collection(
                name="policies",
                metadata={"description": "Policy documentation and FAQs"}
            )
            
            self.distress_collection = self.client.get_or_create_collection(
                name="distress_keywords",
                metadata={"description": "Distress detection keywords by language"}
            )
        except Exception as e:
            print(f"Error initializing collections: {e}")
    
    def load_objection_library(self, library_path: str = "backend/data/objection_library.json"):
        """Load objection library into ChromaDB"""
        try:
            with open(library_path, 'r', encoding='utf-8') as f:
                library = json.load(f)
            
            documents = []
            metadatas = []
            ids = []
            
            for category, responses in library.items():
                for idx, response in enumerate(responses):
                    doc_id = f"objection_{category}_{idx}"
                    
                    documents.append(response)
                    metadatas.append({
                        "category": category,
                        "type": "objection_response"
                    })
                    ids.append(doc_id)
            
            self.objection_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✓ Loaded {len(documents)} objection responses into ChromaDB")
        except Exception as e:
            print(f"Error loading objection library: {e}")
    
    def load_policy_documents(self, docs_dir: str = "backend/data/policies"):
        """Load policy documents into ChromaDB"""
        try:
            policy_files = Path(docs_dir).glob("*.json")
            documents = []
            metadatas = []
            ids = []
            
            for file_idx, file_path in enumerate(policy_files):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                
                # Split into chunks if large
                text = json.dumps(content)
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                
                for chunk_idx, chunk in enumerate(chunks):
                    doc_id = f"policy_{file_path.stem}_{chunk_idx}"
                    documents.append(chunk)
                    metadatas.append({
                        "source": file_path.stem,
                        "type": "policy_document"
                    })
                    ids.append(doc_id)
            
            if documents:
                self.policy_collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"✓ Loaded {len(documents)} policy document chunks into ChromaDB")
        except Exception as e:
            print(f"Error loading policy documents: {e}")
    
    def retrieve_objection_responses(self, 
                                     query: str, 
                                     category: str = None,
                                     top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant objection responses using semantic search
        
        Args:
            query: Customer objection text
            category: Optional filter by category
            top_k: Number of results to return
        
        Returns:
            List of relevant responses with metadata
        """
        where_filter = {"category": category} if category else None
        
        results = self.objection_collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
        
        responses = []
        if results['documents'] and len(results['documents']) > 0:
            for doc, metadata, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                responses.append({
                    "response": doc,
                    "category": metadata.get("category"),
                    "similarity_score": 1 - distance  # Convert distance to similarity
                })
        
        return responses
    
    def retrieve_policy_info(self,
                            query: str,
                            top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant policy information"""
        results = self.policy_collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        info = []
        if results['documents'] and len(results['documents']) > 0:
            for doc, metadata, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
                info.append({
                    "content": doc,
                    "source": metadata.get("source"),
                    "similarity_score": 1 - distance
                })
        
        return info
    
    def retrieve_distress_keywords(self, language: str = "English") -> List[str]:
        """Retrieve distress keywords for a language"""
        results = self.distress_collection.get(
            where={"language": language}
        )
        return results['documents'] if results else []