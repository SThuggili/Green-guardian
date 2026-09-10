"""
Script to generate the complete Medium Blog as a Word Document (.docx) and PDF (.pdf),
including the newly added Cross-Industry Expansion use cases.
"""

import sys
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m_name, m_val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m_name}')
        node.set(qn('w:w'), str(m_val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_blog_docx(docx_path="Green_Guardian_Medium_Blog.docx"):
    print(f"Creating Medium Blog Word Document: {docx_path}...")
    doc = Document()
    
    # Page Setup
    for s in doc.sections:
        s.top_margin = Inches(0.9)
        s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Green Guardian • Medium Technical Article")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Google Cloud Platform • Google Pachamama Challenge")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    PRIMARY_GREEN = RGBColor(6, 78, 59)      # #064E3B
    EMERALD = RGBColor(5, 150, 105)          # #059669
    DARK_SLATE = RGBColor(15, 23, 42)        # #0F172A
    MUTED_GRAY = RGBColor(100, 116, 139)     # #64748B

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_tag = p_title.add_run("MEDIUM TECHNICAL PUBLICATION  •  GOOGLE PACHAMAMA CHALLENGE\n")
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(10)
    r_tag.font.bold = True
    r_tag.font.color.rgb = EMERALD

    r_title = p_title.add_run("Green Guardian: Building an Enterprise Multi-Jurisdictional Environmental Law AI Copilot on Google Cloud")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY_GREEN

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("How we unified 52 global legal instruments, U.S. Federal statutes, and EU directives using Gemini 2.5 Flash, Cross-Encoder Neural Reranking, and Serverless Cloud Run.")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = MUTED_GRAY

    # Callout Box
    box_tbl = doc.add_table(rows=1, cols=1)
    box_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_cell = box_tbl.rows[0].cells[0]
    set_cell_background(b_cell, "ECFDF5")
    set_cell_margins(b_cell, top=120, bottom=120, left=160, right=160)
    bp = b_cell.paragraphs[0]
    r_box = bp.add_run("🌟 Executive Summary:\n\"Green Guardian is an enterprise-grade AI legal copilot on Google Cloud that transforms complex environmental statutes, EU directives, and global climate treaties into instant, verifiable statutory answers with zero-hallucination grounding audits.\"")
    r_box.font.name = "Calibri"
    r_box.font.size = Pt(10)
    r_box.font.italic = True
    r_box.font.color.rgb = DARK_SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 1
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Introduction: The Fragmented Reality of Environmental Law")
    r_h1.font.name = "Calibri"
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    r_h1.font.color.rgb = PRIMARY_GREEN

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Environmental law is universally recognized as one of the most critical, dense, and heavily penalized regulatory domains in modern governance. Whether evaluating a municipal infrastructure project, planning a renewable energy installation, or auditing an international corporate supply chain, compliance leads routinely navigate a labyrinth of overlapping frameworks:")

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.add_run("• U.S. Federal Statutes: NEPA, Clean Air Act (CAA), Clean Water Act (CWA), Endangered Species Act (ESA), and Superfund (CERCLA).")

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.add_run("• European Union Directives: Corporate Sustainability Due Diligence (CSDDD), Corporate Sustainability Reporting (CSRD), Carbon Border Adjustment (CBAM), and Industrial Emissions Directives (IED).")

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(6)
    p.add_run("• Global Multilateral Treaties: Paris Climate Agreement (Article 4 NDCs) and Kunming-Montreal Global Biodiversity Framework (CBD COP15).")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Three major bottlenecks currently hinder global compliance:")
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("1. Prohibitive Financial Barriers: ")
    r.font.bold = True
    p.add_run("Specialized environmental counsel costs $600 to $1,000+/hr, locking out NGOs and municipal planners.")
    
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("2. Jurisdictional Silos: ")
    r.font.bold = True
    p.add_run("Compilations reside in disconnected federal, EU, and treaty databases with varying nomenclatures (NPDES, WOTUS, NAAQS, CELEX, NDCs).")

    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("3. The AI Hallucination Trap: ")
    r.font.bold = True
    p.add_run("Commercial LLMs invent nonexistent sections and misinterpret legal exceptions, creating catastrophic compliance risks.")

    # Section 2
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("2. Core Environmental Use Cases")
    r_h2.font.name = "Calibri"
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = PRIMARY_GREEN

    use_cases = [
        ("🏛️ Municipal Impact Permitting (NEPA & CWA):", "Evaluates Environmental Assessment (EA) vs. Environmental Impact Statement (EIS) significance thresholds (§ 102(2)(C)) and Clean Water Act § 402/§ 404 wetland dredge/fill permits for civic infrastructure."),
        ("🏢 Corporate ESG, Supply-Chain Due Diligence & Carbon Tariffs (EU CSDDD & CBAM):", "Navigates EU cross-border supply chain due diligence (CSDDD), sustainability disclosure (CSRD), and carbon import levies (CBAM) with official EUR-Lex CELEX citations."),
        ("🦅 Renewable Energy & Critical Habitat Protections (ESA § 7 & § 9):", "Delineates Endangered Species Act (ESA) § 7 interagency consultation duties from § 9 private take prohibitions for solar and wind energy developers."),
        ("⚖️ Environmental Justice & Frontline Community Defense:", "Translates complex Superfund CERCLA § 107 strict liability provisions and Clean Air Act toxic standards into actionable citizen compliance checklists at zero cost.")
    ]
    for u_t, u_b in use_cases:
        p_u = doc.add_paragraph()
        p_u.paragraph_format.space_after = Pt(2)
        r_ut = p_u.add_run(f"• {u_t} ")
        r_ut.font.bold = True
        r_ut.font.color.rgb = PRIMARY_GREEN
        p_u.add_run(u_b)

    # Section 3
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    r_h3 = h3.add_run("3. System Architecture & Google Cloud Topology")
    r_h3.font.name = "Calibri"
    r_h3.font.size = Pt(14)
    r_h3.font.bold = True
    r_h3.font.color.rgb = PRIMARY_GREEN

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Green Guardian runs entirely serverless on Google Cloud Platform across 5 modular layers:")

    diag_tbl = doc.add_table(rows=1, cols=1)
    diag_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dc = diag_tbl.rows[0].cells[0]
    set_cell_background(dc, "0F172A")
    set_cell_margins(dc, top=140, bottom=140, left=160, right=160)
    
    diag_text = """+-----------------------------------------------------------------------------------+
|                     GREEN GUARDIAN SYSTEM ARCHITECTURE (GCP)                      |
+-----------------------------------------------------------------------------------+
  [ Client Browser / Mobile ] (HTTPS Responsive UI)
               │
               ▼  (User Question + Jurisdiction Scope Filter)
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │                 GOOGLE CLOUD RUN (Serverless Web Container)                     │
  │   1. Streamlit Presentation: Real-Time Token Streaming & Dataset Exports        │
  │   2. Hybrid Retrieval: Rank-BM25 + Legal Acronym Query Expansion (NAAQS, NPDES) │
  │   3. Neural Reranker: Sentence-Transformers (cross-encoder/ms-marco-MiniLM)     │
  └────────────────────────────────────────┬────────────────────────────────────────┘
                                           │ (Top Grounded Legal Excerpts)
                                           ▼
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │                 GOOGLE VERTEX AI (Agent Platform / Gemini Engine)               │
  │   4. Gemini 2.5 Flash: Structured Legal Reasoning via Enterprise ADC IAM Auth   │
  │   5. Verification Engine: Anti-Hallucination Audit Matrix & Confidence Ranking   │
  └────────────────────────────────────────┬────────────────────────────────────────┘
                                           │ (Streamed Response + Verified Citations)
  [ Rendered Legal Brief + Interactive Statutory Citations + Confidence Badge ]"""

    dp = dc.paragraphs[0]
    r_diag = dp.add_run(diag_text)
    r_diag.font.name = "Consolas"
    r_diag.font.size = Pt(7.5)
    r_diag.font.color.rgb = RGBColor(52, 211, 153)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 4: Step by Step Implementation
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)
    r_h4 = h4.add_run("4. Step-by-Step Technical Implementation")
    r_h4.font.name = "Calibri"
    r_h4.font.size = Pt(14)
    r_h4.font.bold = True
    r_h4.font.color.rgb = PRIMARY_GREEN

    steps = [
        ("Step 1: Multi-Jurisdiction Corpus Ingestion: ", "Indexed 52 primary legal instruments (4,495+ provisions) directly from GovInfo.gov, EUR-Lex, UN Treaty Series, and Hugging Face G4KMU/LEMUR."),
        ("Step 2: Legal Acronym Query Expansion: ", "Preprocessed domain acronyms (NAAQS, NPDES, WOTUS, NDCs, CBAM, CSDDD) to maximize BM25 lexical recall across complex statutory titles."),
        ("Step 3: Neural Cross-Encoder Reranking: ", "Employed sentence-transformers cross-encoder/ms-marco-MiniLM-L-6-v2 to re-score candidates in < 5ms, passing only operative paragraphs to the LLM."),
        ("Step 4: Vertex AI Gemini 2.5 Flash Reasoning: ", "Orchestrated generative synthesis using Gemini 2.5 Flash with Application Default Credentials (ADC) attached to green-guardian-sa."),
        ("Step 5: Real-Time Token Streaming & Audit: ", "Streamed responses word-by-word via Streamlit write-stream with sub-0.5s latency, paired with real-time confidence badges and citation cards."),
        ("Step 6: Serverless Deployment on Cloud Run: ", "Packaged in Python 3.11-slim Docker container, built via Cloud Build, stored in Artifact Registry, and deployed on Cloud Run with scale-to-zero compute.")
    ]
    for s_t, s_d in steps:
        p_s = doc.add_paragraph(style='List Bullet')
        p_s.paragraph_format.space_after = Pt(3)
        r_st = p_s.add_run(s_t)
        r_st.font.bold = True
        r_st.font.color.rgb = PRIMARY_GREEN
        p_s.add_run(s_d)

    # Section 5: Cross Industry Expansion
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    r_h5 = h5.add_run("5. Cross-Industry Expansion: Applying This Architecture to Other High-Stakes Fields")
    r_h5.font.name = "Calibri"
    r_h5.font.size = Pt(14)
    r_h5.font.bold = True
    r_h5.font.color.rgb = PRIMARY_GREEN

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("The architectural blueprint of Green Guardian—combining authoritative statutory corpus ingestion, acronym-aware hybrid retrieval, sub-millisecond Cross-Encoder reranking, Gemini 2.5 Flash reasoning, and deterministic anti-hallucination audits—is highly modular and directly transferable to other high-stakes, heavily regulated industries:")

    cross_industries = [
        ("🏥 1. Healthcare & Pharmaceutical Regulatory Compliance (FDA & HIPAA)",
         "Challenge: Navigating Title 21 CFR (FDA drug approvals, medical device 510(k) clearances), HIPAA privacy rules, and clinical trial regulations.\n"
         "Application: By indexing FDA statutory guidance, CFR titles, and clinical trial protocols, this architecture enables pharmaceutical researchers and hospital compliance teams to verify regulatory approval pathways with zero hallucination risk."),
        
        ("💳 2. Banking, Financial Regulations & Anti-Money Laundering (SEC, FinCEN & Dodd-Frank)",
         "Challenge: Financial institutions face severe regulatory penalties navigating SEC filings, Dodd-Frank disclosures, Basel III capital requirements, and FinCEN BSA/AML compliance.\n"
         "Application: Ingesting federal financial statutes and SEC guidance allows risk officers to cross-reference multi-jurisdictional financial rules and automate compliance checks in seconds."),
        
        ("✈️ 3. Aviation & Maritime Safety Standards (FAA, EASA & IMO)",
         "Challenge: Air carriers, aerospace manufacturers, and maritime operators must adhere to dense international safety standards spanning FAA Federal Aviation Regulations (FARs), EASA directives, and International Maritime Organization (IMO) emissions rules.\n"
         "Application: Enables aerospace engineers and maritime fleet managers to verify airworthiness directives, maintenance protocols, and MARPOL emissions limits instantly."),
        
        ("🔒 4. Cybersecurity, Data Privacy & AI Governance (GDPR, EU AI Act & ISO 27001)",
         "Challenge: Technology organizations operating globally must comply with GDPR, CCPA/CPRA, the EU Artificial Intelligence Act (risk classification & conformity assessments), and ISO/NIST cybersecurity controls.\n"
         "Application: Empowers Chief Information Security Officers (CISOs) and data protection leads to audit system architectures against statutory privacy and AI safety mandates with verifiable citations."),
        
        ("⚡ 5. Energy Grid Modernization & Nuclear Regulatory Compliance (FERC & NRC)",
         "Challenge: Clean energy utilities expanding solar, wind, and nuclear energy must navigate Federal Energy Regulatory Commission (FERC) grid interconnection rules and Nuclear Regulatory Commission (NRC) safety standards.\n"
         "Application: Provides utility engineers and energy policy makers with instant cross-jurisdictional statutory analysis to accelerate clean energy grid approvals.")
    ]

    for ci_t, ci_b in cross_industries:
        p_ci = doc.add_paragraph()
        p_ci.paragraph_format.space_before = Pt(4)
        p_ci.paragraph_format.space_after = Pt(2)
        r_cit = p_ci.add_run(f"• {ci_t}")
        r_cit.font.bold = True
        r_cit.font.size = Pt(10.5)
        r_cit.font.color.rgb = PRIMARY_GREEN

        p_cib = doc.add_paragraph()
        p_cib.paragraph_format.left_indent = Inches(0.2)
        p_cib.paragraph_format.space_after = Pt(4)
        r_cibx = p_cib.add_run(ci_b)
        r_cibx.font.size = Pt(9.5)

    # Section 6: Conclusion
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(4)
    r_h6 = h6.add_run("6. Conclusion & Live Demonstration")
    r_h6.font.name = "Calibri"
    r_h6.font.size = Pt(14)
    r_h6.font.bold = True
    r_h6.font.color.rgb = PRIMARY_GREEN

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Green Guardian proves that production-grade legal AI does not require multimillion-dollar infrastructures. By orchestrating Google Vertex AI Gemini 2.5 Flash, Cross-Encoder Neural Reranking, and Serverless Google Cloud Run, we democratize access to the statutory rules that protect our planet.")

    p_links = doc.add_paragraph(style='List Bullet')
    p_links.add_run("• Live Application Demo: Google Cloud Run Serverless Endpoint\n")
    p_links.add_run("• GitHub Repository: https://github.com/SThuggili/Green-guardian\n")
    p_links.add_run("• Built for: Google Pachamama Challenge (Google Cloud Platform)")

    # Save docx
    doc.save(docx_path)
    print(f"SUCCESS -> Word Document created at '{docx_path}'!")
    return docx_path

if __name__ == "__main__":
    generate_blog_docx("Green_Guardian_Medium_Blog.docx")
