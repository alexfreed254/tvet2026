# 🚀 TVET e-ASSESS - Quick Start Guide

## ⚡ Deploy in 20 Minutes

### What You'll Deploy

```
Frontend (Vercel) → Backend (Railway) → Database (Supabase)
```

**Cost:** ~$5/month (Railway free credit)

---

## 📋 Before You Start

Make sure you have:
- ✅ GitHub account with repo: https://github.com/alexfreed254/tvet2026
- ✅ Supabase project ready
- ✅ Database password from Supabase

---

## Step 1: Deploy Backend (Railway) - 10 min

### 1.1 Create Railway Account
Go to: https://railway.app
- Sign up with GitHub

### 1.2 Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose **`alexfreed254/tvet2026`**

### 1.3 Configure Root Directory (Optional)
- Settings → Root Directory: Leave as `/` or set to `backend`
- Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 1.4 Add Environment Variables
Click **Variables** → **New Variable**, add each:

```bash
SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co

SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8

SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk

SUPABASE_DB_URL=postgresql://postgres.[project-id]:[YOUR-PASSWORD]@db.psdxitqfusfmkutxsojc.supabase.co:5432/postgres

JWT_SECRET=generate-a-secure-random-32-character-key

JWT_ALGORITHM=HS256

JWT_EXPIRATION_MINUTES=480

SUPABASE_STORAGE_BUCKET=evidence-files

MAX_FILE_SIZE_MB=100

APP_NAME=TVET e-ASSESS

DEBUG=false

ALLOWED_ORIGINS=http://localhost:5173
```

**Note:** Replace `[YOUR-PASSWORD]` in `SUPABASE_DB_URL` with your actual Supabase database password.

### 1.5 Deploy
- Click **"Deploy"**
- Wait 3-5 minutes for build
- Copy your backend URL: e.g., `https://tvet-backend-production.up.railway.app`

✅ **Backend deployed!**

---

## Step 2: Deploy Frontend (Vercel) - 5 min

### 2.1 Create Vercel Account
Go to: https://vercel.com
- Sign up with GitHub

### 2.2 Import Project
- Click **"Add New..."** → **"Project"**
- Import **`alexfreed254/tvet2026`**

### 2.3 Configure Build
- **Framework Preset**: Vite
- **Root Directory**: `frontend` (click Edit, select frontend folder)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 2.4 Add Environment Variables
Click **Environment Variables**, add:

```bash
VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co

VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8

VITE_API_BASE_URL=https://tvet-backend-production.up.railway.app
```

**Note:** Replace `VITE_API_BASE_URL` with YOUR Railway backend URL from Step 1.5

### 2.5 Deploy
- Click **"Deploy"**
- Wait 2-3 minutes for build
- Copy your frontend URL: e.g., `https://tvet-eassess.vercel.app`

✅ **Frontend deployed!**

---

## Step 3: Update CORS - 2 min

### 3.1 Update Backend CORS
1. Go back to **Railway dashboard**
2. Open your backend project
3. Click **Variables**
4. Find `ALLOWED_ORIGINS`
5. Update to include your Vercel URL:
   ```
   http://localhost:5173,https://tvet-eassess.vercel.app
   ```
6. The app will automatically redeploy

✅ **CORS configured!**

---

## Step 4: Configure Supabase - 3 min

### 4.1 Update Authentication URLs
1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **Authentication** → **URL Configuration**
3. Set **Site URL**: `https://tvet-eassess.vercel.app`
4. **Redirect URLs** → Add: `https://tvet-eassess.vercel.app/**`
5. Click **Save**

### 4.2 Set Up Database (If Not Done)
1. Click **SQL Editor**
2. Run the schema: Copy contents of `database/schema.sql` and execute

### 4.3 Create Storage Bucket (If Not Done)
1. Click **Storage**
2. Create new bucket: `evidence-files`
3. Set to **Private**

✅ **Supabase configured!**

---

## Step 5: Test Your Deployment ✅

### 5.1 Test Backend
Visit: `https://your-backend.railway.app/api/health`

Should see:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

### 5.2 Test API Docs
Visit: `https://your-backend.railway.app/api/docs`

You should see FastAPI interactive documentation.

### 5.3 Test Frontend
Visit: `https://your-frontend.vercel.app`

- ✅ Page loads
- ✅ No console errors (F12)
- ✅ Can navigate

### 5.4 Test Authentication
- ✅ Register a new user
- ✅ Login with credentials
- ✅ Access dashboard

---

## 🎉 Success!

Your TVET e-ASSESS platform is now live!

**Your URLs:**
- Frontend: `https://tvet-eassess.vercel.app`
- Backend: `https://tvet-backend-production.up.railway.app`
- API Docs: `https://tvet-backend-production.up.railway.app/api/docs`

---

## 📝 Save These URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | `https://_____.vercel.app` | Main app |
| Backend | `https://_____.railway.app` | API |
| API Docs | `https://_____.railway.app/api/docs` | Documentation |
| Supabase | `https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc` | Database |

---

## 🔄 Making Updates

### Deploy Updates Automatically

Both Vercel and Railway auto-deploy when you push to GitHub:

```bash
# Make your changes
git add .
git commit -m "Add new feature"
git push origin main

# ✅ Automatically deploys to both Vercel and Railway
```

### Manual Redeploy

**Vercel:**
- Dashboard → Deployments → Latest → Redeploy

**Railway:**
- Dashboard → Your service → Deploy → Redeploy

---

## 🆘 Troubleshooting

### Frontend can't connect to backend

**Check:**
1. `VITE_API_BASE_URL` is correct (with https://)
2. Backend `ALLOWED_ORIGINS` includes frontend URL
3. No typos in URLs

**Fix:**
- Update env vars in Vercel/Railway
- Redeploy both services

### "Network Error" on login

**Check:**
1. Backend is running (visit `/api/health`)
2. CORS configured correctly
3. Supabase credentials are correct

### Authentication redirects fail

**Check:**
1. Supabase redirect URLs include your Vercel URL
2. URLs have `/**` wildcard
3. Site URL is set correctly

---

## 📚 More Help

- **Platform Comparison**: [DEPLOYMENT-OPTIONS.md](./DEPLOYMENT-OPTIONS.md)
- **Vercel Details**: [VERCEL-DEPLOYMENT.md](./VERCEL-DEPLOYMENT.md)
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs

---

## 💰 Cost Breakdown

| Service | Plan | Cost | What You Get |
|---------|------|------|--------------|
| **Railway** | Hobby | $5/mo credit | Always-on backend |
| **Vercel** | Free | $0 | Frontend hosting + CDN |
| **Supabase** | Free | $0 | Database + Auth + Storage |
| **Total** | | **~$5/mo** | Full production stack |

### Upgrade Options

**For more traffic/features:**
- Vercel Pro: $20/mo (analytics, better support)
- Railway Pro: ~$10-20/mo (more resources)
- Supabase Pro: $25/mo (more storage, better performance)

---

## ✅ Deployment Checklist

- [ ] Railway account created
- [ ] Backend deployed to Railway
- [ ] Backend URL copied
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Frontend URL copied
- [ ] CORS updated in Railway
- [ ] Supabase URLs configured
- [ ] Database schema deployed
- [ ] Storage bucket created
- [ ] Backend health check works
- [ ] Frontend loads successfully
- [ ] User registration works
- [ ] User login works
- [ ] URLs documented

---

## 🎯 Next Steps

1. **Create Admin User**
   - Register through the UI
   - Manually set role to `super_admin` in Supabase

2. **Configure Email**
   - Set up email templates in Supabase
   - Configure SMTP settings

3. **Custom Domain** (Optional)
   - Add domain to Vercel
   - Add domain to Railway
   - Update Supabase redirect URLs

4. **Monitoring**
   - Set up error tracking (Sentry)
   - Configure uptime monitoring
   - Review logs regularly

---

**🎊 Congratulations! Your TVET e-ASSESS platform is live!**

**Repository**: https://github.com/alexfreed254/tvet2026

Need help? Check the [DEPLOYMENT-OPTIONS.md](./DEPLOYMENT-OPTIONS.md) guide!
