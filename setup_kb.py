import os
import glob
import chromadb
from sentence_transformers import SentenceTransformer

def chunk_markdown_file(filepath: str):
    """
    Reads a markdown file and splits it into logical chunks based on headings
    and paragraph breaks to preserve context.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    # Split by markdown headers
    sections = content.split('\n## ')
    chunks = []
    
    # Process the first section (usually the file title and intro)
    first_sec = sections[0].strip()
    if first_sec:
        chunks.append({
            "text": first_sec,
            "metadata": {"source": filename, "section": "Introduction"}
        })
        
    # Process subsequent sections
    for sec in sections[1:]:
        sec = sec.strip()
        if not sec:
            continue
        # Extract heading
        lines = sec.split('\n')
        heading = lines[0].strip()
        text = "Section: " + heading + "\n" + "\n".join(lines[1:])
        chunks.append({
            "text": text,
            "metadata": {"source": filename, "section": heading}
        })
        
    return chunks

def build_knowledge_base():
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")
    chroma_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    
    print("Reading documents from:", kb_dir)
    md_files = glob.glob(os.path.join(kb_dir, "*.md"))
    
    if not md_files:
        print("No markdown documents found in knowledge_base/ directory!")
        return
        
    all_chunks = []
    for filepath in md_files:
        print(f"Processing: {filepath}")
        chunks = chunk_markdown_file(filepath)
        all_chunks.extend(chunks)
        
    print(f"Total chunks created: {len(all_chunks)}")
    
    # Initialize SentenceTransformer
    print("Loading embedding model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize Chroma client
    print("Initializing ChromaDB persistent storage at:", chroma_dir)
    client = chromadb.PersistentClient(path=chroma_dir)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="resume_knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Check if there are existing documents and delete them to avoid duplicates
    existing = collection.get()
    if existing and existing.get('ids'):
        print(f"Removing {len(existing['ids'])} existing documents...")
        collection.delete(ids=existing['ids'])
        
    # Prepare documents, embeddings, metadatas, and ids
    ids = [f"doc_{i}" for i in range(len(all_chunks))]
    documents = [c["text"] for c in all_chunks]
    metadatas = [c["metadata"] for c in all_chunks]
    
    print("Computing embeddings...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()
    
    print("Adding documents to ChromaDB collection...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print("Successfully built the local vector database!")
    print("Collection count:", collection.count())

if __name__ == "__main__":
    build_knowledge_base()
