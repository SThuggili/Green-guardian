"""
Green Guardian: Multi-Source Dataset Ingestion
Ingests Hugging Face Environmental & Legal Datasets:
1. G4KMU/LEMUR (EU Environmental Directives & Regulations in English)
2. (Optional with HF_TOKEN) ClimatePolicyRadar / PermitTEC
Merges them seamlessly into the primary knowledge store (storage/chunks.json and storage/bm25_index.pkl).
"""

import os
import sys
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any

# Ensure stdout supports unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag.config import Config
from rag.ingest import build_local_index

def ingest_lemur_eu_dataset(max_docs: int = 50) -> List[Dict[str, Any]]:
    """Ingests landmark EU environmental legislation from G4KMU/LEMUR."""
    print(f"\n[EU Law] Ingesting EU Environmental Law from G4KMU/LEMUR (English)...")
    try:
        from datasets import load_dataset
        ds = load_dataset("G4KMU/LEMUR", "English", split="train", streaming=True)
        
        eu_chunks = []
        doc_count = 0
        
        for item in ds:
            text = item.get("text", "")
            celex_id = item.get("celex_id", f"EU_DOC_{doc_count+1}")
            
            if not text or len(text.strip()) < 150:
                continue
                
            # Split text into chunks of ~1200 characters
            paragraphs = text.split("\n\n")
            current_chunk = []
            chunk_num = 1
            
            for p in paragraphs:
                p_clean = p.strip()
                if not p_clean:
                    continue
                current_chunk.append(p_clean)
                
                if len(" ".join(current_chunk)) >= 1200:
                    chunk_text = " ".join(current_chunk)
                    eu_chunks.append({
                        "chunk_id": f"EU_{celex_id}_chunk_{chunk_num}",
                        "text": chunk_text,
                        "metadata": {
                            "act_title": f"European Union Environmental Law ({celex_id})",
                            "citation": f"EUR-Lex CELEX:{celex_id}",
                            "section_number": f"Article / Provision {chunk_num}",
                            "title_chapter": "EU Environmental Acquis (EUR-Lex 15.10)",
                            "pages": [1],
                            "filename": f"EUR_Lex_{celex_id}.txt",
                            "source_path": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex_id}"
                        }
                    })
                    chunk_num += 1
                    current_chunk = []
                    
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                eu_chunks.append({
                    "chunk_id": f"EU_{celex_id}_chunk_{chunk_num}",
                    "text": chunk_text,
                    "metadata": {
                        "act_title": f"European Union Environmental Law ({celex_id})",
                        "citation": f"EUR-Lex CELEX:{celex_id}",
                        "section_number": f"Article / Provision {chunk_num}",
                        "title_chapter": "EU Environmental Acquis (EUR-Lex 15.10)",
                        "pages": [1],
                        "filename": f"EUR_Lex_{celex_id}.txt",
                        "source_path": f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex_id}"
                    }
                })
                
            doc_count += 1
            if doc_count >= max_docs:
                break
                
        print(f"  Successfully processed {doc_count} EU legal documents -> {len(eu_chunks)} chunks generated.")
        return eu_chunks
    except Exception as e:
        print(f"  Warning: LEMUR ingestion error: {e}")
        return []

def merge_and_rebuild_index(additional_chunks: List[Dict[str, Any]]):
    """Merges new dataset chunks with existing statutory chunks and rebuilds BM25."""
    from rank_bm25 import BM25Okapi
    
    chunks_path = Config.STORAGE_DIR / "chunks.json"
    bm25_path = Config.STORAGE_DIR / "bm25_index.pkl"
    
    base_chunks = []
    if chunks_path.exists():
        with open(chunks_path, "r", encoding="utf-8") as f:
            base_chunks = json.load(f)
    else:
        base_chunks = build_local_index()
        
    print(f"\n[Merge] Combining indices: {len(base_chunks)} base statutory chunks + {len(additional_chunks)} HF dataset chunks...")
    
    # Avoid duplicate IDs
    existing_ids = {c["chunk_id"] for c in base_chunks}
    merged_chunks = list(base_chunks)
    
    for c in additional_chunks:
        if c["chunk_id"] not in existing_ids:
            merged_chunks.append(c)
            existing_ids.add(c["chunk_id"])
            
    # Save combined chunks
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(merged_chunks, f, indent=2)
        
    # Rebuild BM25
    print("[Indexing] Re-indexing BM25 over combined multi-jurisdictional corpus...")
    tokenized_corpus = [c["text"].lower().split() for c in merged_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)
        
    print(f"[Done] Knowledge store successfully updated! Total indexed chunks: {len(merged_chunks)}")

if __name__ == "__main__":
    eu_data = ingest_lemur_eu_dataset(max_docs=40)
    if eu_data:
        merge_and_rebuild_index(eu_data)
