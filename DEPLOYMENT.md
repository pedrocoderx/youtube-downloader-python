# Deployment Guide - Railway

## 🚀 Quick Deploy to Railway

### Step 1: Prepare Your Repository
1. Make sure all files are committed to your Git repository
2. Ensure you have the following files:
   - `app_simple.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`
   - `templates/index_simple.html`

### Step 2: Deploy to Railway

#### Option A: Deploy via Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect it's a Python app
6. Deploy!

#### Option B: Deploy via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Step 3: Configure Environment (Optional)
Railway will automatically:
- Install Python dependencies from `requirements.txt`
- Install FFmpeg via Nixpacks
- Set up the web service

### Step 4: Access Your App
- Railway will provide a URL like: `https://your-app-name.railway.app`
- Your YouTube downloader will be live!

## 🔧 Troubleshooting

### If FFmpeg is not found:
Railway's Nixpacks should automatically install FFmpeg, but if you have issues:

1. Check the build logs in Railway dashboard
2. Ensure your `railway.json` is properly configured
3. The app will fall back to downloading single files if FFmpeg isn't available

### If downloads fail:
- Check that `/tmp` directory is writable
- Verify yt-dlp is working in the logs
- Downloads are stored in `/tmp` on Railway

## 💡 Tips for Railway Deployment

1. **Free Tier Limits**: 
   - $5/month credit (usually enough for small projects)
   - Monitor usage in Railway dashboard

2. **File Storage**: 
   - Downloads are stored in `/tmp` (temporary)
   - Files may be cleared between deployments
   - Consider adding cloud storage for permanent file storage

3. **Performance**: 
   - Railway provides good performance for this type of app
   - Background downloads work well
   - No cold start issues like serverless platforms

## 🔄 Alternative: Render Deployment

If you prefer Render:

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app_simple:app --bind 0.0.0.0:$PORT`
6. Deploy!

Render's free tier includes 750 hours/month and is also suitable for this project.

## 🎯 Why Railway is Recommended

✅ **Perfect for this project**: Supports FFmpeg, background processes, file storage
✅ **Free tier**: $5/month credit is generous
✅ **Easy deployment**: Git-based, automatic builds
✅ **Good performance**: No cold starts, reliable
✅ **Python support**: Excellent for Flask apps
✅ **File system access**: Can write to `/tmp` for downloads 