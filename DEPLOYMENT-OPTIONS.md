# 🚀 TVET e-ASSESS Deployment Options Guide

## 📊 Comparison Table

| Platform | Best For | Pros | Cons | Cost |
|----------|----------|------|------|------|
| **Vercel** | Frontend only | Fast CDN, Auto-deploy, Great DX | 10s timeout (free), Not for long-running | Free - $20/mo |
| **Railway** | Full-stack | Easy setup, Always-on, Good for APIs | Less global than Vercel | $5/mo credit |
| **Fly.io** | Backend APIs | Global edge, Docker support, Fast | Steeper learning curve | Free tier available |
| **Render** | Full-stack | Free tier, Easy setup, Good docs | Cold starts on free tier | Free - $7/mo |
| **Supabase** | Database | Managed DB + Auth + Storage | Not for compute | Free - $25/mo |

---

## ✅ Recommended: Split Stack

### Architecture

```
Frontend (Vercel) + Backend (Railway) + Database (Supabase)
```

**Why?**
- ✅ Each platform does what it's best at
- ✅ Optimal performance
- ✅ Easy to scale each part independently
- ✅ Free/low-cost for small projects

---

## 🎯 Deployment Scenarios

### Scenario 1: Development/Testing (FREE)

**Setup:**
- Frontend: Vercel (free tier)
- Backend: Railway (free $5 credit)
- Database: Supabase (free tier)

**Total Cost:** $0/month (with usage limits)

**Deploy:**
1. Frontend on Vercel (5 min)
2. Backend on Railway (5 min)
3. Connect to Supabase

**Good for:**
- Testing
- Development
- Small user base (<100 users)
- Low traffic

---

### Scenario 2: Production (Budget: ~$15/month)

**Setup:**
- Frontend: Vercel Pro ($20/mo - optional, can use free)
- Backend: Railway Hobby ($5-10/mo)
- Database: Supabase Free ($0) or Pro ($25/mo)

**Total Cost:** $5-35/month

**Good for:**
- Production apps
- 1000+ users
- Reliable uptime
- Custom domains

---

### Scenario 3: All-in-One (Simplest)

**Setup:**
- Everything on Render (free tier)
- Database: Supabase (free tier)

**Total Cost:** $0/month (with cold starts)

**Good for:**
- Quick demos
- MVPs
- Don't mind cold starts
- Single platform management

---

## 📝 Deployment Guides by Platform

### 1. Vercel (Frontend Only) - RECOMMENDED

**Time:** 5 minutes

**Steps:**
1. Go to https://vercel.com/new
2. Import: `alexfreed254/tvet2026`
3. Root Directory: `frontend`
4. Framework: Vite
5. Add environment variables:
   ```
   VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   VITE_API_BASE_URL=https://your-backend.railway.app
   ```
6. Deploy!

**Pros:**
- ✅ Fastest CDN
- ✅ Automatic HTTPS
- ✅ Zero config
- ✅ Preview deployments

**Cons:**
- ❌ Frontend only

**Full Guide:** [VERCEL-DEPLOYMENT.md](./VERCEL-DEPLOYMENT.md)

---

### 2. Railway (Backend) - RECOMMENDED

**Time:** 5 minutes

**Steps:**
1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Connect `alexfreed254/tvet2026`
5. Railway auto-detects Python
6. Add environment variables:
   ```
   SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_DB_URL=postgresql://postgres...
   JWT_SECRET=your-secret-key
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
7. Click "Deploy"
8. Get your backend URL: `https://xxx.railway.app`

**Pros:**
- ✅ Always-on (no cold starts)
- ✅ No timeout limits
- ✅ Easy setup
- ✅ Great for APIs

**Cons:**
- ❌ Uses free credit ($5/mo)

**Full Guide:** [RAILWAY-DEPLOYMENT.md](./RAILWAY-DEPLOYMENT.md) *(to be created)*

---

### 3. Fly.io (Backend Alternative)

**Time:** 10 minutes

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Launch app: `fly launch`
4. Set secrets:
   ```bash
   fly secrets set SUPABASE_URL=https://...
   fly secrets set SUPABASE_ANON_KEY=...
   fly secrets set JWT_SECRET=...
   ```
5. Deploy: `fly deploy`

**Pros:**
- ✅ Global edge deployment
- ✅ Docker support
- ✅ Free tier available

**Cons:**
- ❌ Requires CLI
- ❌ More complex setup

---

### 4. Render (Full-Stack Alternative)

**Time:** 10 minutes

**Note:** We removed Render config files. If you want to use Render:

**Steps:**
1. Create `render.yaml` (see git history)
2. Go to https://render.com
3. New → Blueprint
4. Connect repository
5. Add environment variables
6. Deploy

**Pros:**
- ✅ Free tier
- ✅ Full-stack support
- ✅ Easy setup

**Cons:**
- ❌ Cold starts on free tier (30s)
- ❌ Slower than Railway

---

## 🏆 Our Recommendation

### For TVET e-ASSESS:

```
┌──────────────┐
│   Vercel     │ ← Frontend (React + Vite)
│   (Free)     │   Fast, Global CDN
└──────┬───────┘
       │
       │ HTTPS/API calls
       ↓
┌──────────────┐
│   Railway    │ ← Backend (FastAPI)
│   ($5/mo)    │   Always-on, No timeouts
└──────┬───────┘
       │
       │ PostgreSQL
       ↓
┌──────────────┐
│   Supabase   │ ← Database + Auth + Storage
│   (Free)     │   Managed, Reliable
└──────────────┘
```

**Total Cost:** ~$5/month (Railway free credit)

**Why This Stack?**
1. **Vercel** - Best-in-class frontend deployment
2. **Railway** - Reliable backend with no cold starts
3. **Supabase** - Managed database + auth + storage

---

## 📋 Step-by-Step: Recommended Deployment

### Part 1: Deploy Backend to Railway (10 min)

1. **Create Railway Account**: https://railway.app
2. **New Project** → "Deploy from GitHub repo"
3. **Select**: `alexfreed254/tvet2026`
4. **Settings** → Change Root Directory to `backend` (optional)
5. **Variables** → Add all backend env vars:
   ```
   SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk
   SUPABASE_DB_URL=postgresql://postgres.[YOUR-PASSWORD]@db.psdxitqfusfmkutxsojc.supabase.co:5432/postgres
   JWT_SECRET=generate-a-secure-random-key-here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=480
   SUPABASE_STORAGE_BUCKET=evidence-files
   MAX_FILE_SIZE_MB=100
   APP_NAME=TVET e-ASSESS
   DEBUG=false
   ALLOWED_ORIGINS=http://localhost:5173
   ```
6. **Deploy** → Wait for build
7. **Copy Backend URL**: e.g., `https://tvet-backend-production.up.railway.app`

### Part 2: Deploy Frontend to Vercel (5 min)

1. **Create Vercel Account**: https://vercel.com
2. **Import Project**: `alexfreed254/tvet2026`
3. **Root Directory**: `frontend`
4. **Framework**: Vite
5. **Environment Variables**:
   ```
   VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
   VITE_API_BASE_URL=https://tvet-backend-production.up.railway.app
   ```
6. **Deploy** → Wait for build
7. **Copy Frontend URL**: e.g., `https://tvet-eassess.vercel.app`

### Part 3: Update CORS (2 min)

1. Go back to **Railway** → Your backend project
2. **Variables** → Edit `ALLOWED_ORIGINS`
3. Update to: `http://localhost:5173,https://tvet-eassess.vercel.app`
4. Redeploy

### Part 4: Configure Supabase (2 min)

1. Go to https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. **Authentication** → **URL Configuration**
3. **Site URL**: `https://tvet-eassess.vercel.app`
4. **Redirect URLs**: Add `https://tvet-eassess.vercel.app/**`

### Part 5: Test Everything ✅

- [ ] Visit frontend: `https://tvet-eassess.vercel.app`
- [ ] Check backend health: `https://your-backend.railway.app/api/health`
- [ ] Test registration
- [ ] Test login
- [ ] Test navigation

**Done! 🎉**

---

## 💡 Pro Tips

### 1. Custom Domains

**Vercel:**
- Settings → Domains → Add your domain
- Free SSL included

**Railway:**
- Settings → Networking → Custom Domain
- Add CNAME record

### 2. Monitoring

- **Vercel**: Built-in analytics
- **Railway**: Built-in metrics
- **Supabase**: Database logs
- **External**: Use Sentry for error tracking

### 3. CI/CD

Both Vercel and Railway auto-deploy on `git push`:
```bash
git add .
git commit -m "Update feature"
git push origin main
# → Auto-deploys to both platforms
```

### 4. Environment-Specific URLs

**Development:**
- Frontend: `https://tvet-dev.vercel.app`
- Backend: `https://tvet-backend-dev.railway.app`

**Production:**
- Frontend: `https://tvet.your-domain.com`
- Backend: `https://api.your-domain.com`

---

## 🆘 Troubleshooting

### Frontend can't reach backend

**Check:**
1. `VITE_API_BASE_URL` is correct
2. Backend CORS includes frontend URL
3. Backend is actually running
4. No typos in URLs

### Backend won't start

**Check:**
1. All environment variables set
2. `SUPABASE_DB_URL` is correct
3. Railway logs for errors
4. Dependencies in `requirements.txt`

### Authentication fails

**Check:**
1. Supabase redirect URLs configured
2. JWT_SECRET is set
3. Supabase keys are correct
4. Check browser console errors

---

## 📚 Documentation

- **Vercel**: [VERCEL-DEPLOYMENT.md](./VERCEL-DEPLOYMENT.md)
- **Supabase**: [Supabase Docs](https://supabase.com/docs)
- **Railway**: [Railway Docs](https://docs.railway.app)

---

## ✅ Quick Reference

**Your Current Setup:**
- **Repository**: https://github.com/alexfreed254/tvet2026
- **Supabase**: https://psdxitqfusfmkutxsojc.supabase.co
- **Deployment Files**: ✅ Ready

**Next Steps:**
1. Deploy backend to Railway (10 min)
2. Deploy frontend to Vercel (5 min)
3. Configure CORS and Supabase (5 min)
4. Test and go live! 🚀

---

**Total Time: ~20 minutes**
**Total Cost: ~$5/month**

Good luck with your deployment! 🎉
