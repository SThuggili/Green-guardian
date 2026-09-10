# Green Guardian: Team Presentation & Handoff Guide
**Event**: Google Pachamama • **Theme**: Environmental Law Intelligence • **Platform**: Google Cloud Platform

---

## 🎯 3-Minute Hackathon Pitch Script (For Judges)

### 0:00 - 0:45 | The Problem & Motivation
> *"Good morning judges. Environmental compliance and policy advocacy are critical to protecting our planet, yet environmental law is among the most fragmented and dense legal systems in existence. A single project review can involve the Clean Air Act, NEPA, Endangered Species Act consultations, and international climate treaties.*
> 
> *Grassroots advocacy groups, municipal planners, and environmental compliance teams often cannot afford $800/hr legal retainers to verify cross-statute requirements. Generic AI chatbots fail because they hallucinate section numbers and miss layout structures like statutory sub-clauses and tables."*

### 0:45 - 1:30 | The Solution: Green Guardian
> *"That is why we built **Green Guardian** on Google Cloud Platform.*
> 
> *Green Guardian is an enterprise-grade, layout-aware legal cognitive agent that combines:*
> 1. *Official statutory source texts (10 foundational US Acts and Global Treaties).*
> 2. *Cross-Encoder Neural Reranking for pinpoint statutory precision.*
> 3. *Gemini 2.0 Flash for lightning-fast legal reasoning.*
> 4. *An automated Self-Verification & Anti-Hallucination Audit Engine that inspects every single claim and provides a Confidence Rank before returning the answer to the user."*

### 1:30 - 2:30 | Live Demonstration
*(Click one of the Golden Demo prompt buttons on the UI)*
> *"Let's test Green Guardian on a complex multi-statute inquiry:*
> 
> 👉 **Query**: *'Under NEPA, what specific conditions trigger the mandatory preparation of an Environmental Impact Statement (EIS) versus an Environmental Assessment (EA)?'*
> 
> *Notice three key things:*
> 1. **Immediate Statutory Citation**: It extracts Section 102(2)(C) and links directly to the specific page of the federal compilation.
> 2. **Confidence Rank Bar**: Shows a **98% High Confidence** badge with exact neural match percentages.
> 3. **Anti-Hallucination Audit Matrix**: On the right, the audit engine verifies that every single factual claim is 100% grounded in the text."*

### 2:30 - 3:00 | Architecture & Budget Efficiency
> *"Under the hood, Green Guardian is built 100% serverless on Google Cloud:*
> - *Frontend & Engine deployed on **Google Cloud Run** with scale-to-zero compute (costing $0 when idle).*
> - *Connected to **Vertex AI Gemini 2.0 Flash**.*
> - *Our entire event deployment costs less than **$3.00** total, making it extraordinarily scalable and cost-effective for grassroots organizations.*
> 
> *Thank you, and we welcome your questions!"*

---

## 🏆 5 Golden Demo Queries (Pre-Tested for Judges)

| # | Question Button | What to Highlight to Judges | Expected Statutory Citation |
|---|---|---|---|
| **1** | **🌲 NEPA EIS vs EA Triggers** | Distinguishes between "Categorical Exclusions", "Environmental Assessments (EA)", and "Major Federal Actions significantly affecting the quality of the human environment". | NEPA § 102(2)(C) (42 U.S.C. § 4332) |
| **2** | **🦅 ESA §7 vs §9** | Shows inter-statute nuance: Federal agency duty to consult under Section 7 vs. private take prohibitions & incidental take permits under Section 9 & 10. | Endangered Species Act § 7(a)(2) & § 9(a)(1) (16 U.S.C. § 1536, § 1538) |
| **3** | **🏭 Clean Air Act NAAQS & SIPs** | Explains primary (health) vs secondary (welfare) standards and mandatory state compliance plans under Section 110. | Clean Air Act § 109(b) & § 110 (42 U.S.C. § 7409, § 7410) |
| **4** | **💧 Clean Water Act NPDES Permits** | Explains point-source discharges into navigable waters / WOTUS requiring Section 402 permitting. | Clean Water Act § 402 & § 301 (33 U.S.C. § 1342, § 1311) |
| **5** | **🌍 Paris Agreement NDCs** | Explains 5-year ratcheting mechanism and progression principle for Nationally Determined Contributions under Article 4. | Paris Climate Agreement Article 4.2 & Article 4.3 |

---

## ☁️ GCP Architecture Diagram for Presentation Slides

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GREEN GUARDIAN ARCHITECTURE                        │
│                                                                         │
│   [ Client Browser ] ──────> [ Cloud Run (Streamlit Container) ]        │
│                                            │                            │
│                                            ▼                            │
│                   ┌───────────────────────────────────┐                 │
│                   │ 1. Layout-Aware Hybrid Retrieval  │                 │
│                   │    (BM25 + Extractive Chunks)     │                 │
│                   └─────────────────┬─────────────────┘                 │
│                                     ▼                                   │
│                   ┌───────────────────────────────────┐                 │
│                   │ 2. Neural Cross-Encoder Reranker  │                 │
│                   │    (Calculates Relevance Scores)  │                 │
│                   └─────────────────┬─────────────────┘                 │
│                                     ▼                                   │
│                   ┌───────────────────────────────────┐                 │
│                   │ 3. Vertex AI Gemini 2.0 Flash     │                 │
│                   │    (Drafts Statutory Analysis)    │                 │
│                   └─────────────────┬─────────────────┘                 │
│                                     ▼                                   │
│                   ┌───────────────────────────────────┐                 │
│                   │ 4. Gemini Self-Verification Loop  │                 │
│                   │    (Outputs Confidence Rank &     │                 │
│                   │     Hallucination Audit Matrix)   │                 │
│                   └───────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 How Your Team Can Run and Present This

### Option 1: Live Cloud Run URL (Recommended for Presentation)
Run `deploy.sh` (or `.\deploy.ps1` on Windows) to generate a live HTTPS link that works on any laptop, tablet, or phone without needing any local software installed.

### Option 2: Local Development
To run locally on your teammate's machine:
```bash
pip install -r requirements.txt
python -m rag.ingest
streamlit run app.py
```
