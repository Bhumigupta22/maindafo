# GitHub Repository Setup & Deployment Instructions

## Getting Your Project on GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **"New"** repository button
3. Fill in:
   - **Repository name:** `voice-shopping-assistant`
   - **Description:** "Voice-based shopping list manager with smart suggestions"
   - **Public/Private:** Choose preference
   - **Initialize README:** Don't check (we have one)
4. Click **"Create repository"**

### Step 2: Push Code to GitHub

```bash
cd voice-shopping-assistant

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Voice Shopping Assistant v1.0.0"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/voice-shopping-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Setup GitHub Pages (Optional - for README preview)

1. Go to repository **Settings**
2. Scroll to **GitHub Pages**
3. Select **Deploy from branch**
4. Choose **main** branch, **/root** folder
5. Click **Save**

---

## Deploying to Google Cloud Run

### Prerequisites

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth login

# Create a Google Cloud project
# https://console.cloud.google.com
```

### Quick Deployment

```bash
# From project root directory
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh voice-shopping-assistant us-central1
```

The script will:
1. ✅ Build and push backend image
2. ✅ Deploy backend to Cloud Run
3. ✅ Build and push frontend image  
4. ✅ Deploy frontend to Cloud Run
5. ✅ Output live URLs

### Manual Deployment (Step-by-step)

**Deploy Backend:**
```bash
cd backend

# Build and push image
gcloud builds submit --tag gcr.io/$PROJECT_ID/voice-shopping-api

# Deploy to Cloud Run
gcloud run deploy voice-shopping-api \
  --image gcr.io/$PROJECT_ID/voice-shopping-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Get service URL
gcloud run services describe voice-shopping-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

**Deploy Frontend:**
```bash
cd ../frontend

# Update backend URL
export BACKEND_URL="https://voice-shopping-api-xxxxx.run.app"

# Build and push image
gcloud builds submit --tag gcr.io/$PROJECT_ID/voice-shopping-frontend

# Deploy to Cloud Run
gcloud run deploy voice-shopping-frontend \
  --image gcr.io/$PROJECT_ID/voice-shopping-frontend \
  --platform managed \
  --region us-central1 \
  --port 3000 \
  --allow-unauthenticated
```

---

## Post-Deployment

### 1. Update GitHub README

Add deployment URLs to your README:

```markdown
## Live Demo

🌐 **[Frontend](https://voice-shopping-frontend-xxxxx.run.app)**  
🔌 **Backend API:** https://voice-shopping-api-xxxxx.run.app

### Getting Started

Visit the [live demo](https://voice-shopping-frontend-xxxxx.run.app) to try it now!
```

### 2. Setup CI/CD

GitHub Actions are already configured (`.github/workflows/ci.yml`):

```bash
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI pipeline"
git push
```

Now commits will:
- Run backend tests
- Build frontend
- Store artifacts

### 3. Create Release

```bash
# Create a git tag
git tag -a v1.0.0 -m "Initial release - Voice Shopping Assistant v1.0.0"

# Push tag to GitHub
git push origin v1.0.0
```

Go to GitHub → **Releases** → Create release from tag v1.0.0

---

## Monitoring Deployed Application

### View Cloud Run Metrics
```bash
# Backend logs
gcloud run logs read voice-shopping-api --limit 100

# Frontend logs
gcloud run logs read voice-shopping-frontend --limit 100

# View in console
# https://console.cloud.google.com/run
```

### Enable Monitoring Alerts
```bash
# View metrics dashboard
# https://console.cloud.google.com/monitoring
```

---

## Custom Domain (Optional)

### Setup Custom Domain

1. Register domain (GoDaddy, Google Domains, etc.)
2. In Google Cloud Console:
   - Go to **Cloud Run**
   - Select service
   - Click **Manage Custom Domains**
   - Add your domain
   - Follow DNS setup instructions

---

## Cost Summary

| Component | Cost |
|-----------|------|
| Cloud Run (frontend + backend) | Free tier ($11.50/month) |
| Cloud Storage (optional) | Free tier |
| Cloud SQL (optional) | ~$3-5/month |
| Domain (optional) | $0-15/year |
| **Total Estimated** | **Free-$15/month** |

---

## Troubleshooting Deployment

### Service won't start
```bash
# Check recent logs
gcloud run logs read service-name --limit 50

# Verify image built correctly
docker run -p 5000:5000 gcr.io/$PROJECT_ID/voice-shopping-api

# Check environment variables
gcloud run services describe service-name
```

### Frontend can't reach backend
```bash
# Update VITE_API_URL to correct backend URL
# Rebuild and redeploy frontend
```

### Out of quota
```bash
# Check usage in Cloud Console
# Edit service quotas in limits page
```

---

## Sharing Your Project

### Share Live Demo
- Share frontend URL with friends/colleagues
- They can immediately try it without installation

### Share on Social Media
```
🛒 I built a Voice Shopping Assistant! 

Use voice commands to manage your shopping list:
- "Add milk" → automatically categorized
- Smart recommendations based on history
- Works on mobile and desktop

Try it: [URL]

#VoiceAI #WebDevelopment #GoogleCloud
```

### Share on Dev Platforms
- Product Hunt
- Dev.to
- GitHub Trending
- Hacker News

---

## Maintenance & Updates

### Regular Updates
```bash
# Make changes locally
git add .
git commit -m "Fix: Voice command processing"
git push

# GitHub Actions automatically tests
# Then manually redeploy when ready:
./deploy-cloud-run.sh voice-shopping-assistant us-central1
```

### Version Management
```bash
# Create version tags
git tag -a v1.1.0 -m "Add offline mode support"
git push origin v1.1.0
```

---

## Backup & Recovery

### Backup Database
```bash
# Download Cloud SQL backup
gcloud sql backups create my-backup \
  --instance=voice-shopping-db

# Export to Cloud Storage
gcloud sql export sql voice-shopping-db \
  gs://my-bucket/backup.sql
```

### Rollback Previous Version
```bash
git revert <commit-hash>
git push
./deploy-cloud-run.sh
```

---

## Next Steps

1. **✅ Deploy to GitHub**
   ```bash
   git push origin main
   ```

2. **✅ Deploy to Google Cloud**
   ```bash
   ./deploy-cloud-run.sh
   ```

3. **✅ Share the demo URL**
   - Post in your portfolio
   - Share with friends
   - Add to resume

4. **✅ Monitor metrics**
   - Check logs regularly
   - Set up alerts
   - Track usage

5. **✅ Iterate & improve**
   - Add features
   - Fix bugs
   - Optimize performance

---

## Resources

- **Google Cloud Documentation:** https://cloud.google.com/docs
- **GitHub Help:** https://docs.github.com
- **Flask Documentation:** https://flask.palletsprojects.com
- **React Documentation:** https://react.dev
- **Vite Documentation:** https://vitejs.dev

---

**Congratulations on building this awesome project! 🎉**

Your application is now **production-ready** and **deployed to the cloud**.

Share it with the world! 🚀
