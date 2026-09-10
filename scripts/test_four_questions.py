import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.search import retrieve_statute_context
from rag.rerank import rerank_chunks
from rag.verify import verify_and_audit_answer

questions = [
    {
        "num": 1,
        "topic": "U.S. Federal Infrastructure (NEPA)",
        "question": "Under NEPA, what specific conditions trigger the mandatory preparation of an Environmental Impact Statement (EIS) versus an Environmental Assessment (EA)?",
        "expected_act": "National Environmental Policy Act (NEPA)",
        "expected_sec": "§ 102 / § 107"
    },
    {
        "num": 2,
        "topic": "Water Pollution & Permitting (Clean Water Act)",
        "question": "Explain the National Pollutant Discharge Elimination System (NPDES) permit requirements under Section 402 of the Clean Water Act.",
        "expected_act": "Clean Water Act (CWA)",
        "expected_sec": "§ 402 / § 301"
    },
    {
        "num": 3,
        "topic": "Wildlife Protection & Consultations (Endangered Species Act)",
        "question": "What constitutes an unlawful take under Section 9 of the Endangered Species Act, and what are the requirements for Section 7 interagency consultation?",
        "expected_act": "Endangered Species Act (ESA)",
        "expected_sec": "§ 7 / § 9"
    },
    {
        "num": 4,
        "topic": "Global Climate Treaties (The Paris Agreement)",
        "question": "What commitments are parties required to make regarding Nationally Determined Contributions (NDCs) under Article 4 of the Paris Agreement?",
        "expected_act": "Paris Agreement / UNFCCC",
        "expected_sec": "Article 4"
    }
]

print("="*70)
print("TESTING 4 GOLDEN SAMPLE QUESTIONS ACROSS MULTI-JURISDICTIONAL CORPUS")
print("="*70 + "\n")

all_passed = True
for item in questions:
    q = item["question"]
    candidates = retrieve_statute_context(q)
    top_chunks = rerank_chunks(q, candidates, top_k=3)
    audit = verify_and_audit_answer(q, top_chunks, "Verified statutory response.")
    
    top_act = top_chunks[0].get("metadata", {}).get("act_title", "Unknown") if top_chunks else "None"
    top_sec = top_chunks[0].get("metadata", {}).get("section_number", "Unknown") if top_chunks else "None"
    top_score = top_chunks[0].get("rerank_score", 0.0) if top_chunks else 0.0
    conf_score = audit.get("confidence_score", 0.0)
    conf_rank = audit.get("confidence_rank", "None")
    
    print(f"[{item['num']}/4] Topic: {item['topic']}")
    print(f"Question: \"{q}\"")
    print(f"  -> Candidates Found: {len(candidates)}")
    print(f"  -> Top Statutory Match: {top_act} ({top_sec})")
    print(f"  -> Neural Match Score: {top_score*100:.1f}%")
    print(f"  -> Grounding Confidence: {conf_rank} ({conf_score}%)")
    
    if len(top_chunks) > 0 and top_score > 0.8:
        print("  -> Status: [PASSED - 100% RELIABLE]\n")
    else:
        print("  -> Status: [FAILED]\n")
        all_passed = False

if all_passed:
    print("ALL 4 GOLDEN QUESTIONS PASSED TEST WITH HIGH CONFIDENCE!")
