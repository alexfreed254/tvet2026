# 🚀 Vercel Deployment Guide - TVET e-ASSESS

## Overview

This guide covers deploying TVET e-ASSESS to Vercel. The deployment consists of:
1. **Backend API** - FastAPI serverless functions
2. **Frontend** - React + Vite static site

## ⚠️ Important Note

Vercel is optimized for **frontend** and **serverless functions**. For the full-stack TVET e-ASSESS app:
- ✅ **Frontend**: Perfect for Vercel (React + Vite)
- ⚠️ **Backend**: Limited by serverless constraints (10s timeout on free tier)

**Recommended Alternative**: Deploy backend on Railway, Fly.io, or DigitalOcean, frontend on Vercel.

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **GitHub Repository**: https://github.com/alexfreed254/tvet2026
3. **Supabase Project**: Database and authentication ready
4. **Vercel CLI** (optional): `npm install -g vercel`

---

## 🎯 Deployment Options

### Option 1: Frontend Only on Vercel (Recommended)

Deploy only the frontend to Vercel, host backend elsewhere.

**Steps:**

1. **Deploy Backend Elsewhere**
   - Railway: https://railway.app
   - Fly.io: https://fly.io
   - DigitalOcean App Platform: https://www.digitalocean.com/products/app-platform

2. **Deploy Frontend to Vercel**
   
   Go to https://vercel.com/new
   
   - Import repository: `alexfreed254/tvet2026`
   - **Root Directory**: Select `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

3. **Add Environment Variables**
   
   In Vercel dashboard → Settings → Environment Variables:
   
   ```
   VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
   VITE_API_BASE_URL=https://your-backend-url.com
   ```

4. **Deploy**
   - Click **"Deploy"**
   - Wait for build to complete
   - Access your site at: `https://your-project.vercel.app`

---

### Option 2: Full-Stack on Vercel (With Limitations)

⚠️ **Limitations**:
- 10-second timeout on free tier
- 50MB deployment size limit
- No persistent connections
- Cold starts
- Not suitable for long-running tasks

**Steps:**

#### 1. Deploy Backend as Serverless Function

1. **Go to Vercel Dashboard**: https://vercel.com/new
2. **Import Repository**: `alexfreed254/tvet2026`
3. **Root Directory**: Keep as root (/)
4. **Framework**: Other
5. **Build Settings**: Leave default

#### 2. Add Backend Environment Variables

In Vercel dashboard → Settings → Environment Variables:

```
SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk
SUPABASE_DB_URL=postgresql://postgres.[project-id]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
JWT_SECRET=your-secure-random-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=480
SUPABASE_STORAGE_BUCKET=evidence-files
MAX_FILE_SIZE_MB=100
APP_NAME=TVET e-ASSESS
DEBUG=false
ALLOWED_ORIGINS=https://your-project.vercel.app
```

#### 3. Deploy

Click **"Deploy"** and wait for completion.

**Access Points:**
- Frontend: `https://your-project.vercel.app`
- Backend API: `https://your-project.vercel.app/api`
- API Docs: `https://your-project.vercel.app/api/docs`

---

## 🛠 Using Vercel CLI

### Install Vercel CLI

```bash
npm install -g vercel
```

### Deploy Frontend Only

```bash
cd frontend
vercel
```

Follow the prompts:
- Set up and deploy: `Y`
- Which scope: Select your account
- Link to existing project: `N` (first time)
- Project name: `tvet-eassess-frontend`
- Directory: `./` (already in frontend)
- Override settings: `N`

### Deploy Backend (If Attempting)

```bash
cd ..  # back to root
vercel
```

---

## 📱 Post-Deployment Configuration

### 1. Update CORS in Backend

If backend is deployed elsewhere, update CORS settings to allow your Vercel frontend URL.

### 2. Configure Supabase

1. Go to https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **Authentication** → **URL Configuration**
3. Set **Site URL**: `https://your-project.vercel.app`
4. Add to **Redirect URLs**: `https://your-project.vercel.app/**`

### 3. Update Frontend API URL

If backend is deployed separately:

1. Go to Vercel dashboard → Your project
2. Settings → Environment Variables
3. Update `VITE_API_BASE_URL` to your backend URL
4. Redeploy: Deployments → Latest → Redeploy

---

## 🔧 Vercel Configuration Files

### Root `vercel.json`

For backend serverless deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### Frontend `vercel.json`

For frontend-only deployment:

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 🚨 Common Issues

### 1. Build Fails - Frontend

**Error**: `npm ERR! missing script: build`

**Solution**:
- Ensure you're deploying from `frontend` directory
- Check `package.json` has build script
- Verify all dependencies in `package.json`

### 2. Serverless Timeout

**Error**: `Function execution timed out`

**Solution**:
- Upgrade to Pro plan (60s timeout)
- Or deploy backend to traditional hosting
- Optimize slow database queries

### 3. Environment Variables Not Working

**Error**: `undefined is not a valid URL`

**Solution**:
- Redeploy after adding env vars
- Check variable names match exactly (case-sensitive)
- Verify `VITE_` prefix for frontend vars

### 4. CORS Errors

**Error**: `Access-Control-Allow-Origin`

**Solution**:
- Add Vercel URL to backend `ALLOWED_ORIGINS`
- Include `https://` in URL (not `http://`)
- Redeploy backend after updating

### 5. API Routes Not Working

**Error**: `404 Not Found` on `/api/*`

**Solution**:
- Check `vercel.json` routes configuration
- Verify `api/index.py` exists
- Check build logs for Python errors

---

## 🎯 Recommended Architecture

### Best Practice Setup:

```
┌─────────────────┐
│  Vercel         │
│  (Frontend)     │ ← React + Vite
│  Vite Static    │
└────────┬────────┘
         │
         │ HTTPS
         ↓
┌─────────────────┐
│  Railway/Fly    │
│  (Backend)      │ ← FastAPI
│  Always-on      │
└────────┬────────┘
         │
         │ PostgreSQL
         ↓
┌─────────────────┐
│  Supabase       │
│  (Database)     │ ← PostgreSQL + Auth + Storage
└─────────────────┘
```

**Why?**
- Vercel: Excellent for static sites, CDN, fast deploys
- Railway/Fly: Better for persistent backend services
- Supabase: Managed database, auth, and storage

---

## 💰 Pricing Comparison

### Vercel
- **Free Tier**: 
  - 100GB bandwidth/month
  - Unlimited sites
  - 10s serverless timeout
  - Good for frontend

- **Pro ($20/month)**:
  - 1TB bandwidth
  - 60s serverless timeout
  - Better for full-stack

### Alternative Backend Hosting

**Railway** (Recommended)
- Free tier: $5 credit/month
- Always-on services
- No timeout limits
- Pay-as-you-go: ~$5-10/month

**Fly.io**
- Free tier: 3 shared VMs
- Always-on
- Global edge network
- ~$0-5/month small apps

---

## 📚 Documentation Links

- **Vercel Docs**: https://vercel.com/docs
- **Vercel CLI**: https://vercel.com/docs/cli
- **Vercel Python**: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- **Railway Docs**: https://docs.railway.app
- **Fly.io Docs**: https://fly.io/docs

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Supabase project ready
- [ ] Database schema deployed
- [ ] Storage bucket created
- [ ] Environment variables prepared
- [ ] Code pushed to GitHub

### Vercel Frontend
- [ ] Import repository
- [ ] Set root directory to `frontend`
- [ ] Configure build settings
- [ ] Add environment variables
- [ ] Deploy
- [ ] Test site loads

### Vercel Backend (if applicable)
- [ ] Verify serverless compatibility
- [ ] Add all environment variables
- [ ] Deploy
- [ ] Test API endpoints
- [ ] Check function logs

### Post-Deployment
- [ ] Update Supabase URLs
- [ ] Configure CORS
- [ ] Test authentication
- [ ] Test file uploads
- [ ] Monitor errors

---

## 🆘 Getting Help

- **Vercel Discord**: https://vercel.com/discord
- **Vercel Support**: https://vercel.com/support
- **GitHub Issues**: https://github.com/alexfreed254/tvet2026/issues

---

## 🎊 Quick Start (Frontend Only)

1. Go to https://vercel.com/new
2. Import: `alexfreed254/tvet2026`
3. Root Directory: `frontend`
4. Add env vars (VITE_*)
5. Deploy!

**Done in 5 minutes!** 🚀

---

**Repository**: https://github.com/alexfreed254/tvet2026
**Recommended**: Frontend on Vercel + Backend on Railway/Fly.io
