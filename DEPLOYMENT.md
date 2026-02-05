# Deployment Guide

Instructions for deploying The-Magician to various cloud platforms for iPad/web access.

## Quick Deploy to Render.com (Recommended)

Render offers free Python hosting with automatic deployments from GitHub.

### Setup Steps

1. **Fork/Push to GitHub**
   - Ensure your code is pushed to GitHub

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `NORS3AI/The-Magician`
   - Render will auto-detect the `render.yaml` configuration

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - You'll get a URL like: `https://the-magician.onrender.com`

5. **Access from iPad**
   - Open the provided URL in Safari
   - Add to Home Screen for app-like experience

### Configuration

The `render.yaml` file is already configured with:
- Python 3.11
- Flask + Gunicorn
- Automatic builds from GitHub

## Alternative: Railway.app

Railway offers a generous free tier and simple deployment.

### Setup Steps

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `NORS3AI/The-Magician`
5. Railway auto-detects Python and Flask
6. Add environment variables:
   - `PORT=5000`
   - `PYTHON_VERSION=3.11`
7. Deploy and get your URL

## Alternative: Fly.io

Fly.io offers edge deployment with free tier.

### Setup Steps

1. Install flyctl: `brew install flyctl` (or download from fly.io)
2. Login: `flyctl auth login`
3. Launch app: `flyctl launch`
4. Deploy: `flyctl deploy`

## Local Network Access (Quick Test)

For testing on local network without deployment:

```bash
# Run Flask on your network
python app.py

# Find your local IP
# Mac/Linux: ifconfig | grep inet
# Windows: ipconfig

# Access from iPad on same network
# http://YOUR_LOCAL_IP:5000
```

**Note:** This only works when iPad and computer are on the same WiFi network.

## Environment Variables

For production deployment, consider adding:

```
FLASK_ENV=production
SECRET_KEY=<generate-secure-key>
```

Generate secure key with:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Next Steps After Deployment

1. Test the game on your iPad browser
2. Add bookmark to home screen for quick access
3. Set up custom domain (optional, available on all platforms)
4. Enable HTTPS (automatic on Render/Railway/Fly)

## Troubleshooting

### App won't start
- Check build logs in platform dashboard
- Verify all dependencies in `requirements.txt`
- Ensure `gunicorn` is installed

### Can't access from iPad
- Verify deployment is "Live" or "Running"
- Check URL is HTTPS (not HTTP)
- Try incognito/private browsing mode

### Session issues
- Render free tier may sleep after 15 min of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to paid tier for always-on hosting
