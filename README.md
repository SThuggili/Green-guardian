# 🌿 Green Guardian: Environmental Law AI Agent
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run%20%7C%20Vertex%20AI-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Model](https://img.shields.io/badge/Gemini-2.0%20Flash-34A853?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Theme](https://img.shields.io/badge/Event-Google%20Pachamama-10B981)](https://cloud.google.com/)

**Green Guardian** is an enterprise-grade, layout-aware legal intelligence and statutory verification assistant built for the **Google Pachamama** challenge. It enables environmental lawyers, researchers, compliance teams, and grassroots advocates to query, cross-examine, and verify foundational environmental statutes and international climate treaties with statutory citations and anti-hallucination verification audits.

---

## ✨ Key Features

- **🏛️ Complete Primary Statutory Corpus**: Pre-indexed with 10 foundational U.S. Federal Environmental Compilations & UN Accords (Clean Air Act, Clean Water Act, NEPA, Endangered Species Act, Superfund/CERCLA, Safe Drinking Water Act, RCRA, TSCA, Paris Agreement, CBD Global Biodiversity Framework).
- **🛡️ Self-Verification & Confidence Rank Engine**: Every response is audited claim-by-claim by Gemini to calculate an explicit **Confidence Rank (High/Moderate/Low)** and an anti-hallucination audit report.
- **⚡ Ultra-Fast Gemini 2.0 Flash Reasoning**: State-of-the-art legal analysis with low latency and high quota availability.
- **🎯 Cross-Encoder Neural Reranking**: Re-scores candidate excerpts using transformer cross-encoders for statutory precision.
- **☁️ 100% Serverless & Cost-Efficient**: Runs on **Google Cloud Run** (scales to 0 instances when idle, incurring **<$3.00** total usage on your $300 GCP credit).

---

## 📁 Repository Structure

```text
GCP project/
├── app.py                     # Streamlit Frontend (Forest Emerald Glassmorphism)
├── Dockerfile                 # Cloud Run container definition
├── requirements.txt           # Python dependencies
├── deploy.sh                  # One-click deployment script (Linux / macOS / Cloud Shell)
├── deploy.ps1                 # One-click deployment script (Windows PowerShell)
├── PRESENTATION_GUIDE.md      # 3-Minute Pitch Script & 5 Golden Demo Questions for Judges
├── .env.example               # Environment variables template
│
├── data/
│   └── pdfs/                  # 10 Official full statutory compilation PDFs
│
├── rag/
│   ├── config.py              # Configuration loader (GCP & model settings)
│   ├── ingest.py              # Layout-aware PDF chunker & indexer
│   ├── search.py              # Vertex AI Search & local hybrid retrieval
│   ├── rerank.py              # Cross-Encoder neural reranker
│   ├── verify.py              # Gemini 2.0 Flash generation & audit engine
│   └── prompts.py             # Domain-tuned legal system prompts
│
└── scripts/
    ├── download_acts.py       # Automated downloader for official statutes
    └── upload_to_gcs.py       # One-click GCS PDF uploader
```

---

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env` and fill in your GCP project or API key:
```bash
cp .env.example .env
```

### 3. Build Local Index
```bash
python -m rag.ingest
```

### 4. Run Streamlit Application
```bash
streamlit run app.py
```

---

## 🌐 One-Click Cloud Run Deployment

To deploy directly to Google Cloud Platform and generate a public HTTPS URL:

### Using Google Cloud Shell (or Linux/macOS):
```bash
chmod +x deploy.sh
./deploy.sh
```

### Using Windows PowerShell:
```powershell
.\deploy.ps1
```

---

## 📊 Presentation Playbook for Your Team

See [PRESENTATION_GUIDE.md](file:///e:/data-science-projects/projects/data-science/GCP%20project/PRESENTATION_GUIDE.md) for:
- The **3-minute judge pitch script**.
- **5 pre-tested Golden Demo queries** with expected citations and reasoning.
- The **GCP architecture slide diagram**.
