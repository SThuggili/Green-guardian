# Green Guardian: Cloud Run Production Container
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-build local storage index
COPY .streamlit/ ./.streamlit/
COPY data/ ./data/
COPY storage/ ./storage/
COPY rag/ ./rag/
COPY app.py .

# Run initial chunking and pre-warm neural reranker model during build
ENV HF_HOME=/app/.cache/huggingface
RUN python -m rag.ingest && \
    python -c "from sentence_transformers import CrossEncoder; CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# Cloud Run environment settings
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "app.py"]
