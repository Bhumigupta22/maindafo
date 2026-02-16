#!/usr/bin/env bash

# Script to deploy to Google Cloud Run
# Prerequisites: gcloud CLI installed and authenticated

set -e

PROJECT_ID=${1:-"voice-shopping-assistant"}
REGION=${2:-"us-central1"}

echo "🚀 Deploying Voice Shopping Assistant to Google Cloud"
echo "=================================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Set project
gcloud config set project $PROJECT_ID

echo "📦 Building and deploying backend..."

# Build backend image
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/voice-shopping-api

# Deploy backend to Cloud Run
gcloud run deploy voice-shopping-api \
  --image gcr.io/$PROJECT_ID/voice-shopping-api \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600s

# Get backend URL
BACKEND_URL=$(gcloud run services describe voice-shopping-api \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)')

echo "✓ Backend deployed at: $BACKEND_URL"
echo ""

echo "📦 Building and deploying frontend..."

# Build frontend image
cd ../frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/voice-shopping-frontend

# Update frontend for production URL
export VITE_API_URL=$BACKEND_URL

# Deploy frontend to Cloud Run
gcloud run deploy voice-shopping-frontend \
  --image gcr.io/$PROJECT_ID/voice-shopping-frontend \
  --platform managed \
  --region $REGION \
  --port 3000 \
  --allow-unauthenticated \
  --memory 256Mi \
  --cpu 1

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe voice-shopping-frontend \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)')

echo "✓ Frontend deployed at: $FRONTEND_URL"
echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📍 Access your application:"
echo "   Frontend: $FRONTEND_URL"
echo "   Backend API: $BACKEND_URL"
echo ""
echo "💾 To view logs:"
echo "   gcloud run logs read voice-shopping-api --limit 50"
echo "   gcloud run logs read voice-shopping-frontend --limit 50"
