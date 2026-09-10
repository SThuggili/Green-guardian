#!/usr/bin/env bash
# =====================================================================
# Green Guardian: One-Click Google Cloud Run Deployment Script
# =====================================================================

set -e

echo "🌿 ==========================================================="
echo "   Deploying Green Guardian to Google Cloud Run (Serverless)  "
echo "   Theme: Environmental Law • Event: Google Pachamama         "
echo "=============================================================="

# 1. Check or ask for Project ID
if [ -z "$GCP_PROJECT_ID" ]; then
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || true)
    if [ -n "$CURRENT_PROJECT" ]; then
        read -p "Enter your GCP Project ID [default: $CURRENT_PROJECT]: " INPUT_ID
        PROJECT_ID=${INPUT_ID:-$CURRENT_PROJECT}
    else
        read -p "Enter your GCP Project ID: " PROJECT_ID
    fi
else
    PROJECT_ID=$GCP_PROJECT_ID
fi

REGION=${GCP_LOCATION:-"us-central1"}
REPO_NAME="green-guardian-repo"
IMAGE_NAME="green-guardian-app"
SERVICE_NAME="green-guardian"

echo ""
echo "🚀 Using Project: $PROJECT_ID | Region: $REGION"
gcloud config set project "$PROJECT_ID"

# 2. Enable Required APIs & Permissions
echo ""
echo "📦 Step 1/4: Enabling GCP Services & Vertex AI IAM Permissions..."
gcloud services enable \
    aiplatform.googleapis.com \
    discoveryengine.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)" 2>/dev/null || true)
if [ -n "$PROJECT_NUMBER" ]; then
    echo "🔑 Granting Vertex AI User role to Cloud Run service account..."
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/aiplatform.user" >/dev/null 2>&1 || true
fi

# 3. Create Artifact Registry Repository if not exists
echo ""
echo "📦 Step 2/4: Ensuring Artifact Registry is ready..."
gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" >/dev/null 2>&1 || \
gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Docker repository for Green Guardian RAG Agent"

BUILD_ID=$(date +%Y%m%d%H%M%S)
IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$BUILD_ID"

# 4. Build Container using Cloud Build
echo ""
echo "🏗️ Step 3/4: Building Docker container with Google Cloud Build (Tag: $BUILD_ID)..."
gcloud builds submit --tag "$IMAGE_URI"

ENV_VARS="GCP_PROJECT_ID=$PROJECT_ID,GCP_LOCATION=$REGION,GEMINI_PRIMARY_MODEL=gemini-2.5-flash"
if [ -n "$GEMINI_API_KEY" ]; then
    ENV_VARS="$ENV_VARS,GEMINI_API_KEY=$GEMINI_API_KEY"
fi

# 5. Deploy to Cloud Run
echo ""
echo "🌐 Step 4/4: Deploying new revision to Google Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_URI" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --min-instances 0 \
    --max-instances 3 \
    --set-env-vars "$ENV_VARS"

echo ""
echo "✅ ==========================================================="
echo "🎉 DEPLOYMENT COMPLETE!                                       "
echo "   Share the live URL above with your team and the judges!    "
echo "=============================================================="
