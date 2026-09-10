# =====================================================================
# Green Guardian: One-Click Google Cloud Run Deployment Script (PowerShell)
# =====================================================================

$ErrorActionPreference = "Stop"

Write-Host "🌿 ===========================================================" -ForegroundColor Green
Write-Host "   Deploying Green Guardian to Google Cloud Run (Serverless)  " -ForegroundColor Cyan
Write-Host "   Theme: Environmental Law • Event: Google Pachamama         " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

# 1. Project ID
$defaultProject = $(gcloud config get-value project 2>$null)
if ($env:GCP_PROJECT_ID) {
    $projectId = $env:GCP_PROJECT_ID
} elseif ($defaultProject) {
    $inputProject = Read-Host "Enter your GCP Project ID [default: $defaultProject]"
    if ([string]::IsNullOrWhiteSpace($inputProject)) { $projectId = $defaultProject } else { $projectId = $inputProject }
} else {
    $projectId = Read-Host "Enter your GCP Project ID"
}

$region = if ($env:GCP_LOCATION) { $env:GCP_LOCATION } else { "us-central1" }
$repoName = "green-guardian-repo"
$imageName = "green-guardian-app"
$serviceName = "green-guardian"

Write-Host "`n🚀 Using Project: $projectId | Region: $region" -ForegroundColor Yellow
gcloud config set project $projectId

# 2. Enable Required APIs & Permissions
Write-Host "`n📦 Step 1/4: Enabling GCP Services & Vertex AI IAM Permissions..." -ForegroundColor Cyan
gcloud services enable `
    aiplatform.googleapis.com `
    discoveryengine.googleapis.com `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    storage.googleapis.com

$projectNumber = $(gcloud projects describe $projectId --format="value(projectNumber)" 2>$null)
if ($projectNumber) {
    Write-Host "🔑 Granting Vertex AI User role to Cloud Run service account..." -ForegroundColor Yellow
    gcloud projects add-iam-policy-binding $projectId `
        --member="serviceAccount:${projectNumber}-compute@developer.gserviceaccount.com" `
        --role="roles/aiplatform.user" 2>$null
}

# 3. Artifact Registry
Write-Host "`n📦 Step 2/4: Ensuring Artifact Registry is ready..." -ForegroundColor Cyan
$repoCheck = gcloud artifacts repositories describe $repoName --location=$region 2>$null
if (-not $repoCheck) {
    gcloud artifacts repositories create $repoName `
        --repository-format=docker `
        --location=$region `
        --description="Docker repository for Green Guardian RAG Agent"
}

$buildId = Get-Date -Format "yyyyMMddHHmmss"
$imageUri = "$region-docker.pkg.dev/$projectId/$repoName/${imageName}:$buildId"

# 4. Cloud Build
Write-Host "`n🏗️ Step 3/4: Building Docker container with Google Cloud Build (Tag: $buildId)..." -ForegroundColor Cyan
gcloud builds submit --tag $imageUri

$envVars = "GCP_PROJECT_ID=$projectId,GCP_LOCATION=$region,GEMINI_PRIMARY_MODEL=gemini-2.5-flash"
if ($env:GEMINI_API_KEY) {
    $envVars += ",GEMINI_API_KEY=$($env:GEMINI_API_KEY)"
}

# 5. Cloud Run Deploy
Write-Host "`n🌐 Step 4/4: Deploying new revision to Google Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $serviceName `
    --image $imageUri `
    --platform managed `
    --region $region `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 1 `
    --timeout 300 `
    --min-instances 0 `
    --max-instances 3 `
    --set-env-vars "$envVars"

Write-Host "`n✅ ===========================================================" -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "   Share the live URL generated above with your team and the judges!" -ForegroundColor Yellow
Write-Host "==============================================================" -ForegroundColor Green
