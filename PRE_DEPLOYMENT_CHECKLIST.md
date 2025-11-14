# Pre-Deployment Checklist for Render.com

## ✅ Code & Repository
- [x] Git repository initialized
- [x] All files committed to GitHub
- [x] `.gitignore` configured (excludes `.env`, `__pycache__`, `.venv`)
- [x] `requirements.txt` up-to-date with all dependencies
- [x] `README.md` with clear instructions
- [x] `render.yaml` configured (or dashboard config ready)
- [x] `app.py` reads `PORT` from environment

## ✅ Application Configuration
- [x] Flask app set to `debug=False` for production
- [x] Host set to `0.0.0.0` (not `127.0.0.1`)
- [x] WSGI server configured (`gunicorn`)
- [x] All hardcoded secrets removed (use `os.environ.get()`)
- [x] Product catalog is working
- [x] Cart functionality working
- [x] Contact form with Telegram integration ready

## 🔧 Environment Variables (Set on Render Dashboard)
Create these **before** deploying:

| Variable | Example Value | Purpose |
|----------|---------------|---------|
| `FLASK_SECRET` | `a1b2c3d4e5f6...` | Session encryption key (must be random & long) |
| `BOT_TOKEN` | `8031877894:AAFq...` | Telegram bot token |
| `CHAT_ID` | `@your_channel` | Telegram chat/channel ID |
| `PYTHON_VERSION` | `3.11` | Python version (optional, Render defaults to latest) |

**Generate FLASK_SECRET:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📋 Security Pre-Deployment

### 1. Secrets Management
- [ ] Never commit `.env` files to GitHub
- [ ] All secrets in environment variables on Render
- [ ] Telegram bot token rotated if ever exposed
- [ ] FLASK_SECRET is unique per environment (dev/prod)

### 2. CORS & Headers (Optional but Recommended)
If you add API endpoints later, add security headers:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
```

### 3. Rate Limiting (Optional)
To prevent abuse, add Flask-Limiter:
```bash
pip install Flask-Limiter
```

## 🗄️ Database & Storage (Currently Not Used)

### For Production Later:
- [ ] If using database: Set up PostgreSQL add-on on Render
- [ ] If using files: Configure cloud storage (AWS S3, Cloudinary)
- [ ] Never store passwords in plain text
- [ ] Use parameterized queries to prevent SQL injection

## 🎨 Frontend & Assets

### Current Status:
- [x] Static files in `static/` folder (CSS, images)
- [x] Templates in `templates/` folder
- [x] Bootstrap CDN for styling
- [x] Product images from external URLs (placeholder.com)

### For Better UX (Optional):
- [ ] Add custom favicon: `static/favicon.ico`
- [ ] Optimize images (currently using placeholders)
- [ ] Add loading states to cart buttons
- [ ] Add form validation on client-side (JavaScript)
- [ ] Add 404 error page template
- [ ] Add 500 error page template

## 📊 Monitoring & Logging

### Render provides:
- [x] Free SSL/HTTPS
- [x] Access logs in dashboard
- [x] Real-time log streaming
- [x] Error tracking (check dashboard frequently)

### Recommended for Later:
- [ ] Set up error tracking (Sentry)
- [ ] Add application monitoring (New Relic)
- [ ] Set up email alerts for deployment failures

## 🚀 Deployment Steps Checklist

### Before Clicking Deploy:

1. [ ] Verify all files pushed to GitHub
   ```bash
   git status  # Should show "nothing to commit"
   git log --oneline -5  # Verify recent commits
   ```

2. [ ] Test locally one more time
   ```bash
   python app.py
   # Visit http://127.0.0.1:5000/
   # Test: Shop, Product Detail, Cart, Checkout, Contact
   ```

3. [ ] Verify `requirements.txt` has no errors
   ```bash
   pip install -r requirements.txt  # Should succeed
   ```

4. [ ] Verify `gunicorn` can start the app
   ```bash
   gunicorn app:app  # Should start without errors
   ```

5. [ ] Double-check environment variable names (case-sensitive!)
   - `FLASK_SECRET`
   - `BOT_TOKEN`
   - `CHAT_ID`

### On Render Dashboard:

1. [ ] Go to https://render.com → Sign in with GitHub
2. [ ] New Web Service → Select `e-commerce` repo
3. [ ] Configure:
   - **Name**: `store` (or your preferred name)
   - **Environment**: Python 3
   - **Region**: `oregon` (or closest to your users)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or Starter for better reliability)
4. [ ] Add environment variables (see table above)
5. [ ] Click **Deploy**

### Post-Deployment:

- [ ] Wait 2-3 minutes for build & deployment
- [ ] Check **Logs** tab for errors
- [ ] Visit your live URL: `https://store-xxxx.onrender.com`
- [ ] Test all functionality:
  - [ ] Shop page loads
  - [ ] Add to cart works
  - [ ] Cart displays correctly
  - [ ] Checkout functions
  - [ ] Contact form sends (check Telegram)
- [ ] Verify HTTPS works (look for padlock icon)

## 🔒 Production Hardening (Nice-to-Have)

### Add to `app.py` for extra security:
```python
import os
from flask import Flask, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "fallback-key")

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
```

### Add error handlers:
```python
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
```

## 📞 Support & Troubleshooting

### If deployment fails:
1. Check Render **Logs** tab (most common issues shown there)
2. Verify `requirements.txt` installs locally: `pip install -r requirements.txt`
3. Verify app starts locally: `gunicorn app:app`
4. Check environment variable names (typos = silent failures)
5. Ensure `app.py` has no syntax errors: `python -m py_compile app.py`

### Common Issues:
- **"ModuleNotFoundError"**: Add missing package to `requirements.txt`
- **"Port already in use"**: App is reading wrong PORT; verify code
- **"Static files not loading"**: Verify `static/` folder exists in repo
- **"502 Bad Gateway"**: App crashed; check logs for Python errors
- **"503 Service Unavailable"**: Build is still running; wait a few seconds

## 🎯 Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Render → Settings → Add custom domain
   - Requires domain ownership

2. **Monitor Performance**
   - Watch Render dashboard for errors
   - Monitor response times
   - Check error rates in logs

3. **Scale Up** (If needed)
   - Move from Free → Starter tier
   - Free tier may sleep after 15 min inactivity
   - Starter tier runs 24/7

4. **Backup & Recovery**
   - Set up GitHub auto-backups
   - Regular database backups (when you add DB)

5. **Future Enhancements**
   - Add user authentication
   - Integrate real payment processing
   - Add product search & filtering
   - Set up inventory management
   - Add order history

## 📚 Useful Links

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Telegram Bot API: https://core.telegram.org/bots/api
- Gunicorn Docs: https://gunicorn.org/

---

**You're almost ready!** Run through this checklist, then deploy on Render. 🚀
