# Google Cloud Deployment Guide

## Prerequisites

1. **Google Cloud Account** - [Create one](https://console.cloud.google.com)
2. **gcloud CLI** - [Install](https://cloud.google.com/sdk/docs/install)
3. **Docker** - [Install](https://docs.docker.com/get-docker/)

## Step 1: Setup Google Cloud Project

```bash
# Create a new project
gcloud projects create voice-shopping-assistant --set-as-default

# Set the project ID
export PROJECT_ID="voice-shopping-assistant"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  speech.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com
```

## Step 2: Setup Service Account for Speech-to-Text

```bash
# Create service account
gcloud iam service-accounts create voice-assistant-sa \
  --display-name="Voice Shopping Assistant Service Account"

# Grant Speech-to-Text API access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:voice-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/speech.client"

# Create and download key
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=voice-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com
```

## Step 3: Deploy Backend to Cloud Run

```bash
cd backend

# Build and push to Cloud Build
gcloud run deploy voice-shopping-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_ENV=production,GOOGLE_CLOUD_CREDENTIALS=/var/secrets/sa-key.json"

# Note the service URL
export BACKEND_URL="https://voice-shopping-api-xxxxx-uc.a.run.app"
```

## Step 4: Deploy Frontend to Cloud Run

```bash
cd ../frontend

# Update backend URL in environment
export VITE_API_URL=$BACKEND_URL

# Build Docker image
docker build -t gcr.io/$PROJECT_ID/voice-shopping-frontend .

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/voice-shopping-frontend

# Deploy to Cloud Run
gcloud run deploy voice-shopping-frontend \
  --image gcr.io/$PROJECT_ID/voice-shopping-frontend \
  --platform managed \
  --region us-central1 \
  --port 3000 \
  --allow-unauthenticated

# Note the frontend URL
export FRONTEND_URL="https://voice-shopping-frontend-xxxxx-uc.a.run.app"
```

## Step 5: Setup Cloud SQL (Production Database)

```bash
# Create Cloud SQL instance
gcloud sql instances create voice-shopping-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create shopping_list \
  --instance=voice-shopping-db

# Create database user
gcloud sql users create shopping_user \
  --instance=voice-shopping-db \
  --password=YOUR_SECURE_PASSWORD
```

## Step 6: Update Backend to Use Cloud SQL

Update `backend/app/config.py`:

```python
class ProductionConfig(Config):
    DATABASE = os.getenv(
        'DATABASE_URL',
        'postgresql://shopping_user:password@/shopping_list?host=/cloudsql/PROJECT_ID:us-central1:voice-shopping-db'
    )
```

## Step 7: Deploy Updated Backend

```bash
gcloud run deploy voice-shopping-api \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_ENV=production,DATABASE_URL=postgresql://..." \
  --memory 512Mi
```

## Accessing Your Application

- **Frontend:** `$FRONTEND_URL`
- **Backend API:** `$BACKEND_URL/api`

## Monitoring

```bash
# View logs
gcloud run logs read voice-shopping-api --limit 50

# View metrics in Cloud Console
# https://console.cloud.google.com/run
```

## Cost Optimization

- Use Cloud Run's pay-per-use model - you only pay when requests are made
- Use `db-f1-micro` tier for Cloud SQL in development
- Enable Cloud CDN for frontend distribution

## Troubleshooting

### Service won't start
```bash
# Check logs
gcloud run logs read service-name --limit 100
```

### Speech API not working
```bash
# Verify service account has correct permissions
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:voice-assistant-sa*"
```

### Frontend can't reach backend
```bash
# Check CORS configuration
# Update backend with correct frontend URL
```

## Cleanup

```bash
# Delete services
gcloud run services delete voice-shopping-api voice-shopping-frontend

# Delete Cloud SQL instance
gcloud sql instances delete voice-shopping-db

# Delete service account
gcloud iam service-accounts delete voice-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com

# Delete project (careful!)
gcloud projects delete $PROJECT_ID
```

---

**Total estimated cost for MVP:** ~$0.25/month (including free tier credits)
