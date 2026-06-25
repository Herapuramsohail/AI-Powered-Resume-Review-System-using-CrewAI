import os
import chromadb
from crewai.tools import BaseTool
from sentence_transformers import SentenceTransformer

class SearchKnowledgeBaseTool(BaseTool):
    name: str = "Search Knowledge Base"
    description: str = (
        "Searches the local resume review knowledge base. "
        "Use this tool to find information regarding ATS guidelines, resume writing best practices, "
        "and recommended training paths or certifications for specific career domains. "
        "Input should be a search query string containing keywords about the advice needed."
    )
    
    _client = None
    _collection = None
    _model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize lazily to ensure database path is correct and model is loaded when tool is actually executed
        self._init_resources()

    def _init_resources(self):
        if self._client is not None:
            return
            
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chroma_dir = os.path.join(current_dir, "chroma_db")
        
        # Load Chroma Client
        self._client = chromadb.PersistentClient(path=chroma_dir)
        try:
            self._collection = self._client.get_collection(name="resume_knowledge_base")
        except Exception:
            self._collection = None
            
        # Load SentenceTransformer
        self._model = SentenceTransformer('all-MiniLM-L6-v2')

    def _run(self, query: str) -> str:
        self._init_resources()
        
        if not self._collection:
            return (
                "Error: Knowledge base collection not found. "
                "Ensure that the setup_kb.py script has been executed to populate the vector store."
            )
            
        try:
            # Embed query
            query_embedding = self._model.encode(query).tolist()
            
            # Query collection
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            
            if not results or not results['documents'] or len(results['documents'][0]) == 0:
                return "No matching guides found in the knowledge base."
                
            formatted_results = []
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                formatted_results.append(
                    f"--- Recommendation {i+1} (Source: {meta.get('source', 'Unknown')}, Section: {meta.get('section', 'Unknown')}) ---\n"
                    f"{doc}\n"
                )
                
            return "\n".join(formatted_results)
        except Exception as e:
            return f"An error occurred while querying the knowledge base: {e}"

if __name__ == "__main__":
    # Test tool run
    tool = SearchKnowledgeBaseTool()
    print("Testing search for: 'ATS single column'")
    print(tool._run("ATS single column"))
