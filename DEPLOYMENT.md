# Beat Sender - Railway Deployment Guide

Deploy your Beat Sender application to the cloud for free with Railway!

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app with GitHub)
- Your code pushed to GitHub

## Option 1: Deploy to Railway (Recommended)

### Step 1: Push Code to GitHub

If you haven't already:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Railway Project

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `BeatSendernOrganizer` repository
5. Railway will automatically detect it's a Python app

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Click on your project
2. Go to "Variables" tab
3. Add these variables:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Your Producer Name
```

**Important**: Use Gmail App Password, not your regular password!
- Enable 2FA on Gmail
- Generate App Password: https://myaccount.google.com/apppasswords

### Step 4: Deploy

Railway automatically deploys! You'll see:
- Build logs
- Deploy logs
- Your live URL (like: `https://your-app.up.railway.app`)

### Step 5: Access Your App

1. Click the generated URL
2. Login screen appears with floating UFO
3. Password: `queendog`
4. Start sending beats!

## Option 2: Deploy to Render

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service

1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: beat-sender
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### Step 3: Add Environment Variables

Same as Railway - add all SMTP variables

### Step 4: Deploy

Render will build and deploy automatically!

## Option 3: Deploy to Fly.io

### Step 1: Install Fly CLI

```bash
# Mac
brew install flyctl

# Windows
iwr https://fly.io/install.ps1 -useb | iex

# Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Launch

```bash
flyctl auth login
flyctl launch
```

Follow prompts to configure your app.

### Step 3: Set Environment Variables

```bash
flyctl secrets set SMTP_SERVER=smtp.gmail.com
flyctl secrets set SMTP_PORT=587
flyctl secrets set SMTP_USERNAME=your-email@gmail.com
flyctl secrets set SMTP_PASSWORD=your-app-password
flyctl secrets set SENDER_EMAIL=your-email@gmail.com
flyctl secrets set SENDER_NAME="Your Name"
```

### Step 4: Deploy

```bash
flyctl deploy
```

## After Deployment

### Update Artist Emails

After deploying, update `config.json` with real artist emails:

1. Edit `config.json` in your local repo
2. Replace example emails with real ones
3. Commit and push:
   ```bash
   git add config.json
   git commit -m "Update artist emails"
   git push
   ```
4. Railway/Render will auto-redeploy

### Test Email Sending

1. Visit your deployed URL
2. Login with password: `queendog`
3. Try sending a test beat to yourself first
4. Verify email arrives with attachment

## Troubleshooting

### "Failed to send email"

- Check SMTP credentials in Railway Variables
- Verify Gmail App Password is correct
- Make sure 2FA is enabled on Gmail

### "Application Error"

- Check Railway logs: Dashboard → Logs tab
- Verify all environment variables are set
- Check that requirements.txt has all dependencies

### Port Already in Use (Local)

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

## Cost

**Railway**:
- Free tier: $5 credit/month
- Enough for this app!

**Render**:
- Free tier available
- May sleep after inactivity

**Fly.io**:
- Free tier: 3 apps
- Perfect for small apps

## Custom Domain (Optional)

### On Railway:

1. Go to Settings → Domains
2. Click "Add Domain"
3. Enter your domain
4. Update DNS records as shown

## Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Use environment variables for all secrets
- Password `queendog` is hardcoded - change if needed
- SMTP credentials stored securely in Railway

## Support

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Fly.io Docs: https://fly.io/docs

---

Your Beat Sender is now live and accessible from anywhere! 🚀🛸
