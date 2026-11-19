# 🚀 TVET e-ASSESS with Supabase Backend

## Architecture Overview

Since Supabase Edge Functions only support TypeScript/JavaScript (Deno runtime), and your backend is Python/FastAPI, we have a few options:

### Option 1: Deploy Backend to Supabase-Compatible Platform ⭐ RECOMMENDED

**Use Fly.io or Railway with Supabase Database**

```
┌────────────────┐
│    Vercel      │  ← Frontend (React + Vite)
│   (Frontend)   │
└────────┬───────┘
         │
         │ API Calls
         ↓
┌────────────────┐
│   Fly.io       │  ← Backend (FastAPI)
│  or Railway    │     Connected to Supabase DB
│   ($5-10/mo)   │
└────────┬───────┘
         │
         │ Direct DB Connection
         ↓
┌────────────────┐
│   Supabase     │  ← Database + Auth + Storage
│  (Database)    │     • PostgreSQL
│   Free Tier    │     • Authentication
└────────────────┘     • File Storage
```

**Why this works best:**
- ✅ Keep your Python/FastAPI backend as-is
- ✅ Use Supabase for database, auth, and storage
- ✅ Fast and reliable
- ✅ Easy to deploy

---

### Option 2: Supabase Database + Auth Only

**Backend on any platform, using Supabase as data layer**

This is what we'll configure now:
- Supabase provides: Database, Authentication, Storage
- Fly.io/Railway provides: FastAPI backend hosting
- Vercel provides: Frontend hosting

---

## 🎯 Recommended Setup: Vercel + Fly.io + Supabase

### Why Fly.io with Supabase?

**Fly.io Benefits:**
- ✅ Free tier: 3 shared VMs (256MB RAM each)
- ✅ Global edge deployment
- ✅ Docker support (works great with Python)
- ✅ Direct database connections
- ✅ No cold starts
- ✅ Great for APIs

**Cost: $0-5/month** (free tier usually sufficient)

---

## 📋 Deployment Guide

### Part 1: Prepare Supabase (5 min)

#### 1.1 Database Setup
1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. **SQL Editor** → Run `database/schema.sql`
3. **Settings** → **Database** → Copy connection string:
   ```
   postgresql://postgres.[project]:[password]@db.psdxitqfusfmkutxsojc.supabase.co:5432/postgres
   ```

#### 1.2 Storage Setup
1. **Storage** → Create bucket: `evidence-files`
2. Set to **Private**
3. Configure policies if needed

#### 1.3 Authentication Setup
1. **Authentication** → **Providers**
2. Enable Email provider (already enabled)
3. Configure email templates if needed
4. **URL Configuration** → Add your frontend URL later

---

### Part 2: Deploy Backend to Fly.io (15 min)

#### 2.1 Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

#### 2.2 Login to Fly.io
```bash
fly auth login
```

#### 2.3 Create Fly.io App
```bash
cd backend
fly launch
```

Answer prompts:
- App name: `tvet-eassess-api` (or auto-generate)
- Region: Choose closest to you
- Setup Postgres: **No** (we're using Supabase)
- Deploy now: **No** (set secrets first)

#### 2.4 Set Environment Secrets
```bash
fly secrets set SUPABASE_URL="https://psdxitqfusfmkutxsojc.supabase.co"

fly secrets set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8"

fly secrets set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk"

fly secrets set SUPABASE_DB_URL="postgresql://postgres.[project]:[password]@db.psdxitqfusfmkutxsojc.supabase.co:5432/postgres"

fly secrets set JWT_SECRET="your-secure-random-32-character-key"

fly secrets set ALLOWED_ORIGINS="http://localhost:5173"
```

#### 2.5 Deploy
```bash
fly deploy
```

Wait 3-5 minutes for deployment.

#### 2.6 Get Backend URL
```bash
fly status
```

Your backend URL: `https://tvet-eassess-api.fly.dev`

Test health endpoint:
```bash
curl https://tvet-eassess-api.fly.dev/api/health
```

---

### Part 3: Deploy Frontend to Vercel (5 min)

#### 3.1 Go to Vercel
https://vercel.com/new

#### 3.2 Import Repository
- Import: `alexfreed254/tvet2026`
- Root Directory: `frontend`
- Framework: Vite

#### 3.3 Add Environment Variables
```
VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co

VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8

VITE_API_BASE_URL=https://tvet-eassess-api.fly.dev
```

#### 3.4 Deploy
Click **Deploy** and wait 2-3 minutes.

Your frontend URL: `https://tvet-eassess.vercel.app`

---

### Part 4: Update Configuration (5 min)

#### 4.1 Update Backend CORS
```bash
fly secrets set ALLOWED_ORIGINS="http://localhost:5173,https://tvet-eassess.vercel.app"
```

App will auto-redeploy.

#### 4.2 Update Supabase URLs
1. Go to Supabase dashboard
2. **Authentication** → **URL Configuration**
3. **Site URL**: `https://tvet-eassess.vercel.app`
4. **Redirect URLs**: Add `https://tvet-eassess.vercel.app/**`

---

## ✅ Testing

### Test Backend
```bash
curl https://tvet-eassess-api.fly.dev/api/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

### Test Frontend
Visit: `https://tvet-eassess.vercel.app`
- ✅ Page loads
- ✅ Can register user
- ✅ Can login
- ✅ No console errors

---

## 💰 Cost Breakdown

| Service | Plan | Cost | What You Get |
|---------|------|------|--------------|
| **Fly.io** | Free | $0 | 3 VMs, 160GB bandwidth |
| **Vercel** | Free | $0 | 100GB bandwidth, CDN |
| **Supabase** | Free | $0 | 500MB DB, 1GB storage |
| **Total** | | **$0/mo** | Full production stack |

### Upgrade When Needed

**Fly.io** ($1.94/mo per VM):
- More memory/CPU
- More instances

**Vercel Pro** ($20/mo):
- Analytics, better support

**Supabase Pro** ($25/mo):
- 8GB database, 100GB storage

---

## 🛠 Fly.io Configuration

We'll create a `fly.toml` configuration file for you.

---

## 🔄 CI/CD Setup

### Auto-Deploy on Git Push

**For Fly.io:**
1. Add GitHub Actions workflow
2. Auto-deploys on push to main

**For Vercel:**
- Already auto-deploys on push

---

## 📊 Comparison: Why This Setup?

### Vercel + Fly.io + Supabase
✅ All free tiers available
✅ Supabase handles DB + Auth + Storage
✅ Fly.io perfect for Python/FastAPI
✅ Vercel best for frontend
✅ No cold starts
✅ Global edge deployment

### Alternative: Vercel + Railway + Supabase
✅ Railway easier than Fly.io
✅ Railway has $5/mo free credit
❌ Railway charges after credit used
✅ Web UI (no CLI needed)

**Choose:**
- **Fly.io**: If you want truly free backend (CLI required)
- **Railway**: If you prefer web UI and don't mind $5/mo

---

## 🚀 Quick Start Commands

### Fly.io Deployment
```bash
# Install Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Login
fly auth login

# Deploy backend
cd backend
fly launch --no-deploy
fly secrets set [your-secrets]
fly deploy

# Check status
fly status
fly logs
```

### Vercel Deployment
```bash
# Option 1: Web UI
# Go to vercel.com/new

# Option 2: CLI
npm install -g vercel
cd frontend
vercel
```

---

## 📚 Next Steps

1. Deploy backend to Fly.io (or Railway)
2. Deploy frontend to Vercel
3. Configure CORS and Supabase
4. Test everything
5. Go live!

---

## 🆘 Troubleshooting

### Fly.io Issues

**Connection refused:**
- Check app is running: `fly status`
- View logs: `fly logs`
- Restart: `fly apps restart tvet-eassess-api`

**Secrets not set:**
```bash
fly secrets list
fly secrets set KEY=VALUE
```

### Supabase Connection Issues

**Can't connect to database:**
- Verify connection string format
- Check password is correct
- Ensure IP is allowed (Supabase allows all by default)

**Auth not working:**
- Check redirect URLs in Supabase
- Verify anon key is correct
- Check browser console for errors

---

## 📖 Documentation Links

- **Fly.io Docs**: https://fly.io/docs
- **Fly.io Python**: https://fly.io/docs/languages-and-frameworks/python/
- **Supabase Docs**: https://supabase.com/docs
- **Vercel Docs**: https://vercel.com/docs

---

## ✅ Deployment Checklist

- [ ] Supabase database schema deployed
- [ ] Supabase storage bucket created
- [ ] Fly.io CLI installed
- [ ] Backend deployed to Fly.io
- [ ] Backend URL obtained
- [ ] Frontend deployed to Vercel
- [ ] Frontend URL obtained
- [ ] CORS updated
- [ ] Supabase URLs configured
- [ ] Health check passes
- [ ] Frontend loads
- [ ] Authentication works

---

**Total Time**: ~25 minutes
**Total Cost**: $0/month (free tiers)

Deploy now and you'll have a production-ready TVET e-ASSESS platform! 🚀
