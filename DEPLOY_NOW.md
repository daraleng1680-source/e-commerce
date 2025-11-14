# 🚀 DEPLOY NOW - Step by Step

## You're on Render.com Dashboard ✅

### Configure These 4 Fields:

#### 1. Build Command
```
pip install -r requirements.txt
```

#### 2. Start Command  
```
gunicorn app:app
```

#### 3. Instance Type
- Select: **Free** (for testing)
- OR **Starter** ($7/month, always-on)

#### 4. Region
- Select: **oregon** (or closest to you)

---

## Environment Variables (IMPORTANT!)

Before clicking Deploy, you MUST add these 3 variables:

### Generate FLASK_SECRET:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
**Copy the output** (e.g., `a1b2c3d4e5f6...`)

### Add to Render → Environment:

| Key | Value | Example |
|-----|-------|---------|
| `FLASK_SECRET` | Your generated key | `a1b2c3d4e5f6a7b8c9d0e1f2...` |
| `BOT_TOKEN` | Your Telegram bot token | `8031877894:AAFqRcUIatER...` |
| `CHAT_ID` | Your Telegram chat ID | `@daraleng1234` or `123456789` |

---

## Final Checklist Before Deploy:

- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:app`
- [ ] Instance Type: Free or Starter selected
- [ ] Environment variables added (3 variables)
- [ ] All 3 environment variable values filled in
- [ ] Region selected

---

## Click Deploy! 🎉

Once you click **"Deploy Web Service"**:

1. ⏱️ Wait 2-3 minutes
2. 📊 Check **Logs** tab (should see "Listening on...")
3. 🌐 Your URL will appear (e.g., `https://store-xxxx.onrender.com`)
4. ✅ Visit your site and test!

---

## Test After Deploy:

1. Shop page: `/`
2. Add to cart
3. View cart: `/cart`
4. Checkout
5. Contact form: `/contact`
6. Submit contact (check Telegram)

---

## If Deploy Fails:

Check **Logs** tab for errors. Common issues:

- ❌ "ModuleNotFoundError" → Package missing in `requirements.txt`
- ❌ "502 Bad Gateway" → Start Command syntax error
- ❌ Variables not working → Restart service after adding them
- ❌ Port error → Make sure start command is `gunicorn app:app`

---

## Your Live Site URL:

Once deployed, you'll get something like:
```
https://store-xxxx.onrender.com
```

This is your **LIVE E-COMMERCE STORE!** 🎉

---

**Status: READY TO DEPLOY** ✅

Go ahead and click Deploy on Render!
