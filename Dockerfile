# Green Guardian: Cloud Run Fast Production Container
FROM python:3.11-slim

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and pre-indexed statutory knowledge base
COPY .streamlit/ ./.streamlit/
COPY data/ ./data/
COPY storage/ ./storage/
COPY rag/ ./rag/
COPY app.py .

# Cloud Run environment settings
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "app.py"]

