"""
Unified Multi-Jurisdictional Retrieval Engine for Green Guardian
Searches across 4,495+ indexed statutory provisions, international treaties, and EU environmental directives.
"""

import os
import re
import json
import pickle
from typing import List, Dict, Any
from pathlib import Path
from rag.config import Config

_cached_chunks = None
_cached_bm25 = None

def load_knowledge_base():
    """Loads and caches the multi-jurisdictional statutory corpus."""
    global _cached_chunks, _cached_bm25
    if _cached_chunks is not None and _cached_bm25 is not None:
        return _cached_chunks, _cached_bm25
        
    chunks_path = Config.STORAGE_DIR / "chunks.json"
    bm25_path = Config.STORAGE_DIR / "bm25_index.pkl"
    
    if not chunks_path.exists() or not bm25_path.exists():
        from rag.ingest import build_local_index
        build_local_index()
        
    if chunks_path.exists() and bm25_path.exists():
        with open(chunks_path, "r", encoding="utf-8") as f:
            _cached_chunks = json.load(f)
        with open(bm25_path, "rb") as f:
            _cached_bm25 = pickle.load(f)
        return _cached_chunks, _cached_bm25
    return [], None

# Common Environmental Law Acronym Dictionary for Query Expansion
ACRONYM_MAP = {
    "caa": "Clean Air Act CAA National Ambient Air Quality Standards NAAQS",
    "cwa": "Clean Water Act CWA NPDES discharge pollutant water quality",
    "nepa": "National Environmental Policy Act NEPA EIS Environmental Impact Statement EA",
    "esa": "Endangered Species Act ESA Section 7 Section 9 take jeopardy critical habitat",
    "cercla": "Comprehensive Environmental Response Compensation and Liability Act CERCLA Superfund hazardous substance liability",
    "rcra": "Resource Conservation and Recovery Act RCRA hazardous solid waste cradle to grave",
    "tsca": "Toxic Substances Control Act TSCA chemical safety risk evaluation",
    "sdwa": "Safe Drinking Water Act SDWA public water systems MCL contaminants",
    "fifra": "Federal Insecticide Fungicide and Rodenticide Act FIFRA pesticide regulation",
    "paris": "Paris Agreement Article 4 Nationally Determined Contributions NDCs climate treaty",
    "cbd": "Convention on Biological Diversity CBD genetic resources biodiversity",
    "unfccc": "United Nations Framework Convention on Climate Change UNFCCC greenhouse gas emissions",
    "csddd": "Corporate Sustainability Due Diligence Directive CSDDD European Union supply chain environmental",
    "csrd": "Corporate Sustainability Reporting Directive CSRD EU ESG sustainability reporting",
    "cbam": "Carbon Border Adjustment Mechanism CBAM EU carbon pricing import",
    "ets": "Emissions Trading System ETS EU carbon market allowances cap and trade",
    "eia": "Environmental Impact Assessment EIA directive environmental review",
    "ied": "Industrial Emissions Directive IED BAT best available techniques",
    "reach": "REACH Regulation chemical substances registration authorization restriction EU",
    "wfd": "Water Framework Directive WFD river basin ecological status EU"
}

def expand_legal_query(query: str) -> str:
    """Cleans typos and expands legal acronyms to improve retrieval recall."""
    # Split common concatenated query words
    cleaned = re.sub(r'\bwhatis\b', 'what is', query, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bhowis\b', 'how is', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bwhois\b', 'who is', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bwhatare\b', 'what are', cleaned, flags=re.IGNORECASE)
    
    # Strip punctuation for token matching
    tokens = re.findall(r'\b\w+\b', cleaned.lower())
    expansions = []
    
    for token in tokens:
        if token in ACRONYM_MAP:
            expansions.append(ACRONYM_MAP[token])
            
    if expansions:
        return f"{cleaned} {' '.join(expansions)}"
    return cleaned

def retrieve_statute_context(
    query: str, 
    top_k: int = Config.TOP_K_CANDIDATES, 
    jurisdiction: str = "all"
) -> List[Dict[str, Any]]:
    """
    Unified multi-jurisdiction search across:
    - US Federal Statutes (NEPA, CAA, CWA, ESA, CERCLA, SDWA, RCRA, TSCA)
    - Global Climate Treaties (Paris Agreement, CBD)
    - European Union Environmental Directives & Regulations (EUR-Lex)
    """
    chunks, bm25 = load_knowledge_base()
    if not chunks or bm25 is None:
        return []
        
    expanded_query = expand_legal_query(query)
    tokenized_query = expanded_query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    
    scored_candidates = []
    j_filter = (jurisdiction or "all").lower()

    for idx, score in enumerate(scores):
        if score > 0:
            chunk = dict(chunks[idx])
            chunk["bm25_score"] = float(score)
            
            # Optional jurisdiction filtering
            if j_filter != "all":
                meta_str = f"{chunk.get('metadata', {}).get('act_title', '')} {chunk.get('metadata', {}).get('citation', '')} {chunk.get('metadata', {}).get('filename', '')}".lower()
                if "us" in j_filter or "united states" in j_filter or "federal" in j_filter:
                    if not any(k in meta_str for k in ["u.s.c", "act", "nepa", "clean air", "clean water", "cercla", "esa", "rcra", "sdwa", "tsca"]):
                        continue
                elif "eu" in j_filter or "europe" in j_filter or "directive" in j_filter:
                    if not any(k in meta_str for k in ["eu", "eur-lex", "celex", "directive", "regulation", "csddd", "csrd", "cbam", "ets"]):
                        continue
                elif "treaty" in j_filter or "global" in j_filter or "climate" in j_filter:
                    if not any(k in meta_str for k in ["paris", "unfccc", "treaty", "cbd", "biodiversity", "unts"]):
                        continue
                        
            scored_candidates.append(chunk)
            
    scored_candidates.sort(key=lambda x: x["bm25_score"], reverse=True)
    return scored_candidates[:top_k]

