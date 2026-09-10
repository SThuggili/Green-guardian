"""
Green Guardian: Google Cloud Storage PDF Uploader
Uploads the 10 statutory PDFs to your GCS bucket for Vertex AI Search / Cloud Run.
"""

import os
import sys
from pathlib import Path

# Load config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag.config import Config

def upload_pdfs_to_gcs(bucket_name: str = None, pdf_dir: Path = Config.PDF_DIR):
    bucket_name = bucket_name or Config.GCS_BUCKET_NAME
    if not bucket_name or bucket_name == "green-guardian-docs-your-project-id":
        print("ERROR: Please set GCS_BUCKET_NAME in .env or pass it as an argument.")
        print("Example: python scripts/upload_to_gcs.py my-gcs-bucket-name")
        return False
        
    try:
        from google.cloud import storage
        client = storage.Client(project=Config.GCP_PROJECT_ID or None)
        
        # Get or create bucket
        try:
            bucket = client.get_bucket(bucket_name)
            print(f"Using existing bucket: gs://{bucket_name}")
        except Exception:
            print(f"Bucket gs://{bucket_name} not found, creating in region {Config.GCP_LOCATION}...")
            bucket = client.create_bucket(bucket_name, location=Config.GCP_LOCATION)
            print(f"Created bucket: gs://{bucket_name}")
            
        pdf_files = list(pdf_dir.glob("*.pdf"))
        print(f"\nUploading {len(pdf_files)} PDF statutes to gs://{bucket_name}/pdfs/ ...")
        
        for pdf in sorted(pdf_files):
            blob_name = f"pdfs/{pdf.name}"
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(str(pdf))
            print(f"  Uploaded -> gs://{bucket_name}/{blob_name} ({pdf.stat().st_size / 1024:.1f} KB)")
            
        print("\nAll environmental statutes successfully uploaded to Google Cloud Storage!")
        return True
    except Exception as e:
        print(f"GCS Upload failed: {e}")
        return False

if __name__ == "__main__":
    b_name = sys.argv[1] if len(sys.argv) > 1 else None
    upload_pdfs_to_gcs(bucket_name=b_name)
