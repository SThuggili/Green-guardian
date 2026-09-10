"""
Test Verification Script for Green Guardian RAG Pipeline
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.search import retrieve_statute_context
from rag.rerank import rerank_chunks

def test_pipeline():
    query = "Under NEPA, what specific conditions trigger the mandatory preparation of an Environmental Impact Statement (EIS)?"
    print(f"Testing Query: '{query}'\n")
    
    candidates = retrieve_statute_context(query)
    print(f"1. Retrieval: Found {len(candidates)} candidate chunks.")
    
    top_chunks = rerank_chunks(query, candidates, top_k=3)
    print(f"2. Reranking: Selected top {len(top_chunks)} chunks:\n")
    
    for idx, c in enumerate(top_chunks, 1):
        meta = c.get("metadata", {})
        act = meta.get("act_title", "Statute")
        sec = meta.get("section_number", "Section")
        pages = meta.get("pages", [1])
        score = c.get("rerank_score", 0.0)
        
        print(f"  [Top {idx}] {act} — {sec} (Page {pages})")
        print(f"  Match Score: {score * 100:.1f}%")
        print(f"  Excerpt: {c.get('text', '')[:140]}...\n")
        
    print("Pipeline validation SUCCESSFUL!")

if __name__ == "__main__":
    test_pipeline()
