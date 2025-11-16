# 🚀 Deployment Guide: Daily Tracker Web App

This guide will walk you through deploying your Daily Tracker app to the cloud using **GitHub** and **Render** (completely free).

## Prerequisites

- A GitHub account (free at [github.com](https://github.com))
- A Render account (free at [render.com](https://render.com))
- Git installed on your computer (download from [git-scm.com](https://git-scm.com))

---

## Step 1: Initialize Git and Push to GitHub

### 1.1 Initialize Git in your project folder

```bash
cd "c:\Users\SCC\Desktop\New folder (5)"
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### 1.2 Create a `.gitignore` file

Create a new file named `.gitignore` in your project root with this content:

```
__pycache__/
*.pyc
*.pyo
.venv/
venv/
env/
*.db
.DS_Store
.env
*.log
```

### 1.3 Stage and commit your files

```bash
git add .
git commit -m "Initial commit: Daily Tracker web app with SQLite"
```

### 1.4 Create a GitHub repository

1. Go to [github.com/new](https://github.com/new)
2. Name your repo `daily-tracker` (or any name you like)
3. Set it to **Public** (required for free Render deployment)
4. Click **Create repository**

### 1.5 Push to GitHub

After creating the repo, GitHub will show you commands. Run these in your terminal:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/daily-tracker.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 2: Create a `requirements.txt` file

In your project root, create a file named `requirements.txt` with:

```
Flask==2.3.3
Werkzeug==2.3.7
```

This tells Render what Python packages to install.

Then commit it:

```bash
git add requirements.txt
git commit -m "Add requirements.txt for deployment"
git push
```

---

## Step 3: Create a Render Deployment Configuration

In your project root, create a file named `render.yaml` with this content:

```yaml
services:
  - type: web
    name: daily-tracker
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

Also create a `Procfile` (no extension) in your project root:

```
web: gunicorn app:app
```

Then commit both:

```bash
git add render.yaml Procfile requirements.txt
git commit -m "Add deployment configuration files"
git push
```

### Important: Install gunicorn locally

```bash
pip install gunicorn
```

Then update `requirements.txt`:

```
Flask==2.3.3
Werkzeug==2.3.7
gunicorn==21.2.0
```

```bash
git add requirements.txt
git commit -m "Add gunicorn to requirements"
git push
```

---

## Step 4: Deploy on Render

### 4.1 Sign up for Render

1. Go to [render.com](https://render.com)
2. Click **Sign up** and choose **GitHub**
3. Authorize Render to access your GitHub account

### 4.2 Create a new Web Service

1. In Render dashboard, click **New +** → **Web Service**
2. Select **Daily Tracker** (or your repo name) from GitHub
3. Fill in the details:
   - **Name:** `daily-tracker`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Click **Create Web Service**

Render will now:
- Build your app (installs Flask, dependencies)
- Deploy it to the cloud
- Assign you a free URL like `https://daily-tracker-xxx.onrender.com`

### 4.3 Wait for deployment

The first build takes 2-3 minutes. You'll see logs on the Render dashboard. When it says **"Live"**, your app is online!

---

## Step 5: Your App is Live! 🎉

Visit your Render URL (e.g., `https://daily-tracker-xxx.onrender.com`) and your Daily Tracker is live on the internet!

### First Launch Note:
- The database will be created automatically on first use
- Your data persists in `tracker_data.db` (on Render's file system)
- CSV exports are also available

---

## Step 6: Make Changes and Re-Deploy

Every time you update your code:

```bash
git add .
git commit -m "Update your changes"
git push
```

Render will automatically re-deploy within 1-2 minutes.

---

## Free Tier Limits (Render)

- **Uptime:** App goes to sleep after 15 minutes of inactivity
- **Storage:** 0.5 GB (enough for thousands of records)
- **Bandwidth:** Limited but sufficient for personal use

**To keep it always on:** Upgrade to Render's paid plan ($7/month) or use a free "wake-up" service like [UptimeRobot](https://uptimerobot.com/).

---

## Troubleshooting

### App won't start?
1. Check the **Render logs** in the dashboard
2. Common issues:
   - Missing `gunicorn` in `requirements.txt`
   - Typo in `Procfile`
   - Python version mismatch

### Database not persisting?
- Render restarts containers periodically
- For persistent storage, upgrade to Render's paid plan or use a PostgreSQL database (free tier available)

### Can't push to GitHub?
```bash
git config --global credential.helper store
git push  # Enter your GitHub username and PAT (Personal Access Token)
```

---

## Next Steps (Optional)

- **Add a custom domain:** Render lets you point a domain name to your app
- **Switch to PostgreSQL:** For production-level database persistence
- **Add email notifications:** Alert yourself when you spend over budget
- **Mobile app:** Convert to a mobile app using React Native or Flutter

---

## Links

- 📚 Render Docs: [render.com/docs](https://render.com/docs)
- 📚 Flask Docs: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- 📚 Git Docs: [git-scm.com/doc](https://git-scm.com/doc)

---

**You did it! Your app is now on the web! 🚀**
