"""
Layout-Aware Statutory Ingestion and Chunking for Environmental Legal PDFs
"""

import os
import re
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from rag.config import Config

# Statutory Regex Patterns
SECTION_RE = re.compile(r"^\s*(?:SEC\.|SECTION|Section|Article|ARTICLE)\.?\s+([0-9A-Za-z\.\-]+)\b\.?\s*(.*)$", re.MULTILINE)
TITLE_RE = re.compile(r"^\s*(?:TITLE|Title|CHAPTER|Chapter)\s+([IVXLCDM\d]+)\b\.?\s*(.*)$", re.MULTILINE)

def parse_statute_pdf(pdf_path: str, act_title: str, citation: str = "") -> List[Dict[str, Any]]:
    """
    Parses an environmental law PDF with page tracking and statutory section extraction.
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is required for PDF parsing. Please install with: pip install pymupdf")
    
    doc = fitz.open(pdf_path)
    chunks = []
    
    current_section = "General Provisions"
    current_title = ""
    current_text = []
    current_pages = []
    chunk_idx = 1
    
    filename = os.path.basename(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.split("\n")
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
            
            # Check for Title/Chapter
            title_match = TITLE_RE.match(trimmed)
            if title_match:
                current_title = f"{title_match.group(1)} {title_match.group(2)}".strip()
            
            # Check for Section header
            sec_match = SECTION_RE.match(trimmed)
            if sec_match:
                # Flush existing chunk if substantial
                if current_text and len(" ".join(current_text)) > 200:
                    chunk_text = " ".join(current_text).strip()
                    chunks.append({
                        "chunk_id": f"{filename}_chunk_{chunk_idx}",
                        "text": chunk_text,
                        "metadata": {
                            "act_title": act_title,
                            "citation": citation,
                            "section_number": current_section,
                            "title_chapter": current_title,
                            "pages": list(sorted(set(current_pages))),
                            "filename": filename,
                            "source_path": f"data/pdfs/{filename}"
                        }
                    })
                    chunk_idx += 1
                    current_text = []
                    current_pages = []
                
                current_section = f"§ {sec_match.group(1)} {sec_match.group(2)}".strip()
            
            current_text.append(trimmed)
            current_pages.append(page_num + 1)
            
            # Flush by length threshold ~1200 chars while preserving section context
            if len(" ".join(current_text)) >= 1400:
                chunk_text = " ".join(current_text).strip()
                chunks.append({
                    "chunk_id": f"{filename}_chunk_{chunk_idx}",
                    "text": chunk_text,
                    "metadata": {
                        "act_title": act_title,
                        "citation": citation,
                        "section_number": current_section,
                        "title_chapter": current_title,
                        "pages": list(sorted(set(current_pages))),
                        "filename": filename,
                        "source_path": f"data/pdfs/{filename}"
                    }
                })
                chunk_idx += 1
                # Sliding overlap of last 2 lines
                current_text = current_text[-2:] if len(current_text) > 2 else []
                current_pages = current_pages[-2:] if len(current_pages) > 2 else [page_num + 1]

    # Final chunk
    if current_text:
        chunk_text = " ".join(current_text).strip()
        chunks.append({
            "chunk_id": f"{filename}_chunk_{chunk_idx}",
            "text": chunk_text,
            "metadata": {
                "act_title": act_title,
                "citation": citation,
                "section_number": current_section,
                "title_chapter": current_title,
                "pages": list(sorted(set(current_pages))),
                "filename": filename,
                "source_path": f"data/pdfs/{filename}"
            }
        })
        
    doc.close()
    return chunks

def build_local_index(pdf_dir: Path = Config.PDF_DIR, storage_dir: Path = Config.STORAGE_DIR):
    """Parses all PDFs in the pdf directory and saves indexed chunks + BM25 index."""
    from rank_bm25 import BM25Okapi
    
    storage_dir.mkdir(parents=True, exist_ok=True)
    all_chunks = []
    
    # Mapping of filenames to official titles
    law_titles = {
        "1_National_Environmental_Policy_Act_NEPA.pdf": ("National Environmental Policy Act (NEPA)", "42 U.S.C. § 4321 et seq."),
        "2_Clean_Air_Act_CAA.pdf": ("Clean Air Act (CAA)", "42 U.S.C. § 7401 et seq."),
        "3_Clean_Water_Act_CWA.pdf": ("Clean Water Act (CWA)", "33 U.S.C. § 1251 et seq."),
        "4_Endangered_Species_Act_ESA.pdf": ("Endangered Species Act (ESA)", "16 U.S.C. § 1531 et seq."),
        "5_Superfund_CERCLA.pdf": ("Comprehensive Environmental Response, Compensation, and Liability Act (CERCLA)", "42 U.S.C. § 9601 et seq."),
        "6_Safe_Drinking_Water_Act_SDWA.pdf": ("Safe Drinking Water Act (SDWA)", "42 U.S.C. § 300f et seq."),
        "7_Resource_Conservation_and_Recovery_Act_RCRA.pdf": ("Resource Conservation and Recovery Act (RCRA)", "42 U.S.C. § 6901 et seq."),
        "8_Toxic_Substances_Control_Act_TSCA.pdf": ("Toxic Substances Control Act (TSCA)", "15 U.S.C. § 2601 et seq."),
        "9_Paris_Climate_Agreement.pdf": ("The Paris Climate Agreement (UNFCCC)", "UN Treaty Series No. 54113"),
        "10_Kunming_Montreal_Global_Biodiversity_Framework.pdf": ("Kunming-Montreal Global Biodiversity Framework (CBD)", "CBD/COP/15/L.25")
    }
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {pdf_dir}")
        return []
        
    print(f"Processing {len(pdf_files)} PDF documents for ingestion...")
    for pdf in sorted(pdf_files):
        title, citation = law_titles.get(pdf.name, (pdf.stem.replace("_", " "), "U.S. Law / Treaty"))
        try:
            chunks = parse_statute_pdf(str(pdf), act_title=title, citation=citation)
            all_chunks.extend(chunks)
            print(f"  Processed {pdf.name}: {len(chunks)} chunks created")
        except Exception as e:
            print(f"  Error parsing {pdf.name}: {e}")
            
    # Save chunks metadata
    chunks_path = storage_dir / "chunks.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
        
    # Build and save BM25 tokenized corpus
    tokenized_corpus = [chunk["text"].lower().split() for chunk in all_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    
    bm25_path = storage_dir / "bm25_index.pkl"
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)
        
    print(f"\nIndex built successfully! Total chunks: {len(all_chunks)}. Saved to {storage_dir}")
    return all_chunks

if __name__ == "__main__":
    build_local_index()
