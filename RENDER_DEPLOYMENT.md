# Render.com Deployment Checklist

## Pre-Deployment Checklist

- [x] `requirements.txt` includes all dependencies (Flask, requests, gunicorn)
- [x] `render.yaml` or use dashboard config for build/start commands
- [x] `build.sh` script for build process
- [x] `app.py` reads PORT from environment variables
- [x] `app.py` sets `debug=False` for production
- [x] All hardcoded secrets (BOT_TOKEN, CHAT_ID, FLASK_SECRET) use `os.environ.get()`
- [ ] GitHub repository created and code pushed
- [ ] GitHub account connected to Render.com
- [ ] Environment variables set in Render dashboard

## Deployment Steps

### 1. Initialize Git (if not already done)
```bash
cd d:\y3s2\py
git init
git add .
git commit -m "Initial commit: e-commerce store"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Create Render Account & Connect GitHub
- Visit https://render.com
- Sign up or log in
- Connect your GitHub account (Settings → GitHub)

### 3. Create New Web Service on Render
1. Dashboard → **New** → **Web Service**
2. Select your GitHub repository
3. Fill in:
   - **Name**: `store` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or Starter/Standard for production)

### 4. Set Environment Variables
In Render dashboard for your service:
- Go to **Environment** tab
- Add three variables:

| Key | Value | Example |
|-----|-------|---------|
| `FLASK_SECRET` | Random 32-char hex string | `a1b2c3d4e5f6...` |
| `BOT_TOKEN` | Your Telegram bot token | `8031877894:AAFq...` |
| `CHAT_ID` | Your Telegram chat ID | `@your_channel_name` |

**Generate FLASK_SECRET**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Deploy
- Click **Deploy**
- Render will build and start your app
- Once live, visit: `https://store-xxxx.onrender.com`

### 6. Monitor Logs
- Dashboard → **Logs** tab
- Check for errors during build/startup

## What Render Provides (Free Tier)
- ✅ Free SSL/TLS (HTTPS)
- ✅ Auto-deploy on git push
- ✅ Environment variables
- ✅ Cron jobs (optional)
- ⚠️ Service spins down after 15 min inactivity (Pro tier removes this)

## Troubleshooting

### Build Fails
- Check `pip install -r requirements.txt` runs locally without errors
- Ensure no OS-specific dependencies in requirements

### App Won't Start
- Verify `gunicorn app:app` works locally: `pip install gunicorn; gunicorn app:app`
- Check Render logs for Python errors

### PORT Error
- The `app.py` now reads `PORT` from environment (code is updated)
- Ensure start command is exactly: `gunicorn app:app`

### Static Files Not Loading
- Verify `static/` folder exists in repo
- Render serves static files automatically if `Flask.static_folder` is set (default: `./static`)

### Environment Variables Not Working
- Restart the service after adding env vars (Service → **Restart**)
- Check capitalization (case-sensitive)

## Next Steps After Deployment

1. **Test the site**: Visit your live URL and test cart/checkout
2. **Custom Domain**: Render → **Settings** → Add custom domain (if you own one)
3. **Monitor Performance**: Check logs and response times
4. **Backup**: Configure regular backups if using a database later
5. **Upgrade Plan**: Move from Free to Starter/Standard for better reliability

## Important: Never Commit Secrets
Add a `.gitignore` to prevent accidental secret commits:
```
.venv/
__pycache__/
*.pyc
.env
.DS_Store
```

