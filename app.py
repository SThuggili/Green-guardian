"""
Green Guardian: Environmental Law Conversational AI
Unified Multi-Jurisdictional Intelligence (US Federal Statutes • EU Directives • Global Treaties)
Built for Google Cloud Platform & Google Pachamama
"""

import streamlit as st
import time
import os
from pathlib import Path

# Page Config: Collapsed sidebar by default for clean presentation
st.set_page_config(
    page_title="Green Guardian - Environmental Law AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium High-Contrast Emerald Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at 10% 15%, rgba(6, 44, 25, 0.75) 0%, rgba(10, 15, 13, 0.98) 75%, #070a08 100%);
        color: #f1f5f9;
    }
    
    /* Hero Header */
    .hero-container {
        padding: 1.4rem 2.0rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.08) 100%);
        border: 1.5px solid rgba(16, 185, 129, 0.45);
        border-radius: 16px;
        backdrop-filter: blur(16px);
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #34d399 0%, #10b981 50%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    
    .hero-sub {
        font-size: 1.0rem;
        color: #cbd5e1;
        font-weight: 400;
    }
    
    /* =========================================================================
       COLOR-CODED TAB NAVIGATION WITH OUTER LAYER CONTAINER
       ========================================================================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px !important;
        background: rgba(15, 23, 42, 0.85) !important;
        padding: 10px 14px !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(71, 85, 105, 0.5) !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 1.2rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.96rem !important;
        padding: 0 22px !important;
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(71, 85, 105, 0.5) !important;
        transition: all 0.25s ease-in-out !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(51, 65, 85, 0.9) !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Completely Disable Sidebar & Chevron */
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Tab 1 Active: Emerald (Green Guardian) */
    .stTabs [data-baseweb="tab"]:nth-child(1)[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.35) 0%, rgba(5, 150, 105, 0.2) 100%) !important;
        color: #34d399 !important;
        border: 1.5px solid #10b981 !important;
        box-shadow: 0 0 18px rgba(16, 185, 129, 0.4), inset 0 0 8px rgba(16, 185, 129, 0.2) !important;
    }
    
    /* Tab 2 Active: Sky Blue (Knowledge Base of Acts) */
    .stTabs [data-baseweb="tab"]:nth-child(2)[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.35) 0%, rgba(2, 132, 199, 0.2) 100%) !important;
        color: #38bdf8 !important;
        border: 1.5px solid #0ea5e9 !important;
        box-shadow: 0 0 18px rgba(14, 165, 233, 0.4), inset 0 0 8px rgba(14, 165, 233, 0.2) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* =========================================================================
       CHAT INPUT: ULTRA-CLEAR VISIBILITY WHILE TYPING
       ========================================================================= */
    div[data-testid="stChatInput"] {
        background: transparent !important;
        padding: 0 !important;
    }
    
    div[data-testid="stChatInput"] > div,
    .stChatInputContainer,
    .stChatInput {
        background-color: #0f172a !important;
        background: rgba(15, 23, 42, 0.95) !important;
        border: 2px solid #10b981 !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.45), 0 0 16px rgba(16, 185, 129, 0.25) !important;
    }
    
    div[data-testid="stChatInput"] textarea,
    .stChatInput textarea,
    .stChatInputContainer textarea,
    textarea[data-testid="stChatInputTextArea"],
    div[data-testid="stChatInputTextArea"] textarea,
    .stChatInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: transparent !important;
        background: transparent !important;
        caret-color: #34d399 !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        padding: 10px 14px !important;
    }
    
    div[data-testid="stChatInput"] textarea::placeholder,
    .stChatInput textarea::placeholder,
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        opacity: 0.95 !important;
        font-weight: 400 !important;
    }
    
    div[data-testid="stChatInput"] button {
        background: rgba(16, 185, 129, 0.2) !important;
        color: #34d399 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-testid="stChatInput"] button:hover {
        background: #10b981 !important;
        color: #052e16 !important;
        transform: scale(1.05);
    }
    
    /* =========================================================================
       CHAT MESSAGES & CARDS
       ========================================================================= */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 1.0rem;
        background: rgba(15, 23, 42, 0.88) !important;
        border: 1px solid rgba(51, 65, 85, 0.6) !important;
        padding: 1.2rem !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    
    .stChatMessage p, .stChatMessage div, .stChatMessage span, .stChatMessage li {
        color: #f8fafc !important;
        font-size: 0.98rem;
        line-height: 1.6;
    }
    
    .stChatMessage strong, .stChatMessage b {
        color: #6ee7b7 !important;
    }
    
    /* Confidence Badge */
    .confidence-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .badge-high {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    
    .badge-mod {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24 !important;
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    
    /* Citation Card */
    .citation-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-left: 4px solid #10b981;
        padding: 1.0rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
    }
    
    .citation-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #34d399 !important;
        margin-bottom: 0.25rem;
    }
    
    .citation-meta {
        font-size: 0.82rem;
        color: #94a3b8 !important;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.4rem;
    }
    
    .citation-snippet {
        font-size: 0.88rem;
        color: #cbd5e1 !important;
        line-height: 1.5;
    }
    
    /* Audit Box */
    .audit-box {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1.1rem;
        margin-top: 0.8rem;
    }
    
    .audit-box p, .audit-box li {
        color: #e2e8f0 !important;
    }
    
    /* Suggested Question Buttons - Dark Emerald Theme */
    .stButton>button {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1.5px solid rgba(16, 185, 129, 0.35) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.7rem 0.9rem !important;
        transition: all 0.25s ease !important;
        text-align: left !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.28) 0%, rgba(5, 150, 105, 0.18) 100%) !important;
        color: #34d399 !important;
        border-color: #34d399 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.3);
    }
    
    /* Tables Styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.9rem;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(51, 65, 85, 0.6);
    }
    
    .styled-table thead tr {
        background-color: #064e3b;
        color: #ffffff;
        text-align: left;
        font-weight: 600;
    }
    
    .styled-table th, .styled-table td {
        padding: 10px 14px;
        border-bottom: 1px solid rgba(51, 65, 85, 0.4);
    }
    
    .styled-table tbody tr {
        background: rgba(15, 23, 42, 0.6);
        color: #cbd5e1;
    }
    
    .styled-table tbody tr:nth-of-type(even) {
        background: rgba(30, 41, 59, 0.4);
    }
    
    .styled-table tbody tr:hover {
        background: rgba(16, 185, 129, 0.1);
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Import RAG Modules
from rag.config import Config
from rag.search import retrieve_statute_context, load_knowledge_base
from rag.rerank import rerank_chunks
from rag.verify import generate_statutory_answer, stream_statutory_answer, verify_and_audit_answer
import json
import io
import csv

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌿 Green Guardian: Environmental Law AI</div>
    <div class="hero-sub">Unified Multi-Jurisdictional Intelligence &bull; U.S. Federal Statutes &bull; EU Directives &bull; Global Climate Treaties</div>
</div>
""", unsafe_allow_html=True)

# Load Knowledge Base Info
load_knowledge_base()

# Main Top-Level Navigation Tabs
tab_chat, tab_kb = st.tabs([
    "🌿 Green Guardian", 
    "📚 Knowledge Base of Acts (52 Instruments)"
])

# ==============================================================================
# TAB 1: CONVERSATIONAL CHAT ASSISTANT
# ==============================================================================
with tab_chat:
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 **Welcome to Green Guardian!** I am your enterprise environmental legal intelligence assistant.\n\nAsk me any question about **U.S. Federal Environmental Acts**, **European Union Directives**, or **Global Climate Treaties**. Every answer provides verifiable statutory citations and an anti-hallucination confidence audit.",
                "citations": [],
                "audit": None
            }
        ]

    # Jurisdiction Filter Pills
    st.markdown("###### 🌐 Legal Jurisdiction Scope:")
    selected_jurisdiction = st.radio(
        "Select Jurisdiction Filter",
        options=["🌐 All Jurisdictions", "🇺🇸 U.S. Federal Statutes", "🇪🇺 EU Directives & Regulations", "🌍 Global Climate Treaties"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Quick Suggested Prompt Buttons (Rendered cleanly with dark emerald pills)
    st.markdown("##### 💡 Suggested Inquiries (Click to Ask):")
    col1, col2, col3 = st.columns(3)
    with col1:
        b1 = st.button("🌲 NEPA EIS vs EA Triggers", use_container_width=True)
        b4 = st.button("💧 Clean Water Act NPDES Permitting", use_container_width=True)
    with col2:
        b2 = st.button("🦅 ESA §7 Consultation vs §9 Take", use_container_width=True)
        b5 = st.button("🌍 Paris Agreement Article 4 NDCs", use_container_width=True)
    with col3:
        b3 = st.button("🏭 Clean Air Act NAAQS & SIPs", use_container_width=True)
        b6 = st.button("🇪🇺 EU Environmental Due Diligence", use_container_width=True)

    # Prompt Mapping
    clicked_prompt = None
    if b1:
        clicked_prompt = "Under NEPA, what specific conditions trigger the mandatory preparation of an Environmental Impact Statement (EIS) versus an Environmental Assessment (EA)?"
    elif b2:
        clicked_prompt = "What constitutes an unlawful 'take' under Section 9 of the Endangered Species Act, and what are the requirements for Section 7 interagency consultation?"
    elif b3:
        clicked_prompt = "How does the Clean Air Act regulate National Ambient Air Quality Standards (NAAQS) and what is the role of State Implementation Plans (SIPs)?"
    elif b4:
        clicked_prompt = "Explain the National Pollutant Discharge Elimination System (NPDES) permit requirements under Section 402 of the Clean Water Act."
    elif b5:
        clicked_prompt = "What commitments are parties required to make regarding Nationally Determined Contributions (NDCs) under Article 4 of the Paris Agreement?"
    elif b6:
        clicked_prompt = "How does European Union environmental legislation regulate corporate sustainability due diligence and cross-border environmental standards?"

    st.markdown("---")

    # Container for all messages
    chat_container = st.container()

    # Render Chat History
    with chat_container:
        for msg_idx, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👤"):
                if msg.get("audit"):
                    audit = msg["audit"]
                    conf_score = audit.get("confidence_score", 95)
                    conf_rank = audit.get("confidence_rank", "High (Verified)")
                    badge_class = "badge-high" if conf_score >= 80 else "badge-mod"
                    
                    st.markdown(f"""
                    <div class="confidence-badge {badge_class}">
                        🛡️ Confidence Rank: <strong>{conf_rank}</strong> ({conf_score}%)
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(msg["content"])
                
                # Grounded Citations & Audit Matrix
                citations = msg.get("citations", [])
                if citations:
                    with st.expander(f"📜 Grounded Statutory Citations & Verification Audit ({len(citations)} source excerpts)"):
                        c_tab1, c_tab2 = st.tabs(["🏛️ Statutory Citations", "🛡️ Anti-Hallucination Audit"])
                        with c_tab1:
                            for idx, c in enumerate(citations, 1):
                                meta = c.get("metadata", {})
                                act = meta.get("act_title", "Statute")
                                sec = meta.get("section_number", "Section")
                                pages = meta.get("pages", [1])
                                score = c.get("rerank_score", 0.9)
                                
                                st.markdown(f"""
                                <div class="citation-card">
                                    <div class="citation-title">[{idx}] {act} — {sec}</div>
                                    <div class="citation-meta">Page(s): {pages} &bull; Neural Match: {score*100:.1f}% &bull; Source: {meta.get('filename', 'Doc')}</div>
                                    <div class="citation-snippet">{c.get('text', '')[:450]}...</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                        with c_tab2:
                            if msg.get("audit"):
                                aud = msg["audit"]
                                st.markdown(f"""
                                <div class="audit-box">
                                    <p><strong>Audit Verdict:</strong> <span style="color: #34d399; font-weight: 600;">{aud.get('audit_verdict', 'Verified')}</span></p>
                                    <hr style="border-color: rgba(51, 65, 85, 0.5); margin: 0.6rem 0;">
                                    <p style="font-size: 0.88rem; font-weight: 600; margin-bottom: 0.4rem;">Verified Statutory Claims:</p>
                                    <ul style="font-size: 0.85rem; color: #cbd5e1; padding-left: 1.2rem;">
                                        {"".join([f"<li>{claim}</li>" for claim in aud.get('supported_claims', [])[:5]])}
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)

                    # Export Compliance Brief (Markdown Report)
                    brief_md = f"# Green Guardian: Legal Compliance Brief\n\n**Generated:** {Config.PRIMARY_MODEL} via Google Vertex AI\n**Confidence Rank:** {msg.get('audit', {}).get('confidence_rank', 'High')} ({msg.get('audit', {}).get('confidence_score', 95)}%)\n\n---\n\n## Statutory Analysis\n\n{msg['content']}\n\n---\n\n## Grounded Statutory Citations\n\n"
                    for idx, c in enumerate(citations, 1):
                        m = c.get("metadata", {})
                        brief_md += f"### [{idx}] {m.get('act_title', 'Statute')} — {m.get('section_number', '')}\n- **Citation:** {m.get('citation', '')}\n- **Page:** {m.get('pages', [1])}\n- **Neural Match Score:** {c.get('rerank_score', 0.9)*100:.1f}%\n\n> {c.get('text', '')}\n\n"
                    
                    st.download_button(
                        label="📄 Export Compliance Brief (Markdown)",
                        data=brief_md,
                        file_name=f"Green_Guardian_Compliance_Brief_{msg_idx}.md",
                        mime="text/markdown",
                        key=f"dl_brief_{msg_idx}"
                    )

    # Process New Input
    user_input = st.chat_input("Ask any legal, regulatory, or policy question on environmental law...")
    active_prompt = clicked_prompt or user_input

    if active_prompt:
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(active_prompt)

            with st.chat_message("assistant", avatar="🌿"):
                status_box = st.empty()
                status_box.markdown("🔍 *1/2 Retrieving statutory provisions across multi-jurisdictional corpus...*")
                
                # Map selected jurisdiction
                j_key = "all"
                if "u.s." in selected_jurisdiction.lower():
                    j_key = "us"
                elif "eu" in selected_jurisdiction.lower():
                    j_key = "eu"
                elif "treaty" in selected_jurisdiction.lower():
                    j_key = "treaty"
                    
                candidates = retrieve_statute_context(active_prompt, jurisdiction=j_key)
                top_chunks = rerank_chunks(active_prompt, candidates, top_k=Config.TOP_K_RERANKED)
                
                status_box.empty()
                
                # Real-Time Streaming Generation
                stream_gen = stream_statutory_answer(active_prompt, top_chunks, model_name=Config.PRIMARY_MODEL)
                answer_text = st.write_stream(stream_gen)
                
                # Fast Deterministic Audit
                audit_result = verify_and_audit_answer(active_prompt, top_chunks, answer_text, model_name=Config.PRIMARY_MODEL)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "citations": top_chunks,
            "audit": audit_result
        })
        st.rerun()

# ==============================================================================
# TAB 2: KNOWLEDGE BASE OF ACTS (52 LEGAL INSTRUMENTS)
# ==============================================================================
with tab_kb:
    st.markdown("### 📚 Comprehensive Knowledge Base of Acts & Treaties")
    st.markdown("The Green Guardian RAG index contains **52 primary legal instruments** spanning U.S. Federal Acts, EU Directives, and Global Treaties.")
    
    # Dataset Download Buttons
    chunks_data, _ = load_knowledge_base()
    if chunks_data:
        st.markdown("##### 📥 Download Pre-Indexed Statutory Corpus:")
        json_str = json.dumps(chunks_data, indent=2)
        
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["chunk_id", "act_title", "citation", "section_number", "pages", "filename", "text"])
        for c in chunks_data:
            m = c.get("metadata", {})
            csv_writer.writerow([c.get("chunk_id", ""), m.get("act_title", ""), m.get("citation", ""), m.get("section_number", ""), str(m.get("pages", "")), m.get("filename", ""), c.get("text", "")])
        csv_str = csv_buffer.getvalue()

        dcol1, dcol2 = st.columns(2)
        with dcol1:
            st.download_button(
                "📥 Download Legal Corpus (JSON - 4,495+ Provisions)",
                data=json_str,
                file_name="green_guardian_statutory_corpus.json",
                mime="application/json",
                use_container_width=True
            )
        with dcol2:
            st.download_button(
                "📊 Download Legal Corpus (CSV - Metadata & Excerpts)",
                data=csv_str,
                file_name="green_guardian_statutory_corpus.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("#### 🇺🇸 1. U.S. Federal Environmental Statutes (Full Compilations)")
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>#</th>
                <th>Statute Name</th>
                <th>Citation</th>
                <th>Key Regulatory Focus</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td><strong>Clean Air Act (CAA)</strong></td>
                <td>42 U.S.C. § 7401 et seq.</td>
                <td>NAAQS (§ 109), SIPs (§ 110), Hazardous Air Pollutants (§ 112), Mobile Sources</td>
            </tr>
            <tr>
                <td>2</td>
                <td><strong>Clean Water Act (CWA)</strong></td>
                <td>33 U.S.C. § 1251 et seq.</td>
                <td>NPDES Permits (§ 402), Effluent Limits (§ 301), Dredge/Fill Wetlands (§ 404), WOTUS</td>
            </tr>
            <tr>
                <td>3</td>
                <td><strong>Resource Conservation & Recovery Act (RCRA)</strong></td>
                <td>42 U.S.C. § 6901 et seq.</td>
                <td>Cradle-to-grave hazardous waste tracking (Subtitle C), solid waste disposal (Subtitle D)</td>
            </tr>
            <tr>
                <td>4</td>
                <td><strong>Superfund / CERCLA</strong></td>
                <td>42 U.S.C. § 9601 et seq.</td>
                <td>Strict joint & several liability (§ 107), National Priorities List, Brownfield cleanup</td>
            </tr>
            <tr>
                <td>5</td>
                <td><strong>Safe Drinking Water Act (SDWA)</strong></td>
                <td>42 U.S.C. § 300f et seq.</td>
                <td>Public water systems, Maximum Contaminant Levels (MCLs), Underground Injection Control</td>
            </tr>
            <tr>
                <td>6</td>
                <td><strong>Endangered Species Act (ESA)</strong></td>
                <td>16 U.S.C. § 1531 et seq.</td>
                <td>Section 7 Interagency Consultation, Section 9 Take Prohibitions, Critical Habitat (§ 4)</td>
            </tr>
            <tr>
                <td>7</td>
                <td><strong>Toxic Substances Control Act (TSCA)</strong></td>
                <td>15 U.S.C. § 2601 et seq.</td>
                <td>Chemical risk reviews, Pre-Manufacture Notices (PMNs), PFAS & toxic restrictions</td>
            </tr>
            <tr>
                <td>8</td>
                <td><strong>National Environmental Policy Act (NEPA)</strong></td>
                <td>42 U.S.C. § 4321 et seq.</td>
                <td>Environmental Impact Statements (EIS § 102(2)(C)), Environmental Assessments, CEQ</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🌐 2. Global Climate & Biodiversity Treaties")
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>#</th>
                <th>International Treaty</th>
                <th>Official Treaty Reference</th>
                <th>Core Commitments & Mechanisms</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>9</td>
                <td><strong>The Paris Climate Agreement</strong></td>
                <td>UN Treaty Series No. 54113</td>
                <td>1.5°C threshold (Art 2), Nationally Determined Contributions (Art 4), Carbon Markets (Art 6)</td>
            </tr>
            <tr>
                <td>10</td>
                <td><strong>Kunming-Montreal Global Biodiversity Framework</strong></td>
                <td>CBD/COP/15/L.25</td>
                <td>30x30 global conservation targets, ecosystem restoration, genetic resource benefit-sharing</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🇪🇺 3. European Union Environmental Directives (EUR-Lex 15.10)")
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>#</th>
                <th>EU Directive / Regulation</th>
                <th>EUR-Lex Reference</th>
                <th>Subject Matter</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>11</td>
                <td><strong>EU Ambient Air Quality Directive</strong></td>
                <td>Directive 2008/50/EC</td>
                <td>PM2.5, PM10, and NO2 limit values, clean air zone plans</td>
            </tr>
            <tr>
                <td>12</td>
                <td><strong>EU Water Framework Directive</strong></td>
                <td>Directive 2000/60/EC</td>
                <td>Good ecological & chemical status for river basins and groundwater</td>
            </tr>
            <tr>
                <td>13</td>
                <td><strong>EU Habitats & Birds Directives</strong></td>
                <td>Directive 92/43/EEC</td>
                <td>Natura 2000 network, strict species conservation, impact assessments</td>
            </tr>
            <tr>
                <td>14</td>
                <td><strong>EU Industrial Emissions Directive (IED)</strong></td>
                <td>Directive 2010/75/EU</td>
                <td>Best Available Techniques (BAT) and integrated pollution permits</td>
            </tr>
            <tr>
                <td>15</td>
                <td><strong>EU Carbon Border Adjustment (CBAM)</strong></td>
                <td>Regulation (EU) 2023/956</td>
                <td>Carbon tariff on imported emissions-intensive goods (steel, cement)</td>
            </tr>
            <tr>
                <td>16-52</td>
                <td><strong>Additional 37 EU Environmental Acts</strong></td>
                <td>EUR-Lex Acquis 15.10</td>
                <td>Corporate Due Diligence (CSDDD), REACH chemicals, deforestation rules</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 0.8rem;">
    🌿 <strong>Green Guardian</strong> &bull; Built for Google Cloud Platform & Google Pachamama Challenge &bull; Powered by Gemini 2.5 Flash
</div>
""", unsafe_allow_html=True)

