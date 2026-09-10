import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

class Config:
    # GCP Project Settings
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", os.getenv("GOOGLE_CLOUD_PROJECT", ""))
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "")
    
    # Discovery Engine / Agent Builder Search Data Store
    DATA_STORE_ID: str = os.getenv("DATA_STORE_ID", "")
    DATA_STORE_LOCATION: str = os.getenv("DATA_STORE_LOCATION", "global")
    
    # Model Configurations (Flagship Enterprise Legal Reasoning)
    PRIMARY_MODEL: str = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-2.5-flash")
    REASONING_MODEL: str = os.getenv("GEMINI_REASONING_MODEL", "gemini-2.5-pro")
    
    # Developer API Key (Fallback for local testing without GCP credentials)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    PDF_DIR: Path = DATA_DIR / "pdfs"
    STORAGE_DIR: Path = BASE_DIR / "storage"
    
    # Retrieval Settings
    TOP_K_CANDIDATES: int = 12
    TOP_K_RERANKED: int = 5
    CROSS_ENCODER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    @classmethod
    def is_gcp_configured(cls) -> bool:
        return bool(cls.GCP_PROJECT_ID and cls.GCP_PROJECT_ID != "your-gcp-project-id")

    @classmethod
    def is_vertex_search_configured(cls) -> bool:
        return bool(cls.is_gcp_configured() and cls.DATA_STORE_ID and cls.DATA_STORE_ID != "green-guardian-data-store")
