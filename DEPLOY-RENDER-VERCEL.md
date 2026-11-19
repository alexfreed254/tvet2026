# 🚀 Deploy TVET e-ASSESS: Render + Vercel + Supabase

## Architecture Overview

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Vercel   │────▶│ Render   │────▶│ Supabase │
│ Frontend │     │ Backend  │     │ Database │
│  (Free)  │     │(Free/Paid)     │  (Free)  │
└──────────┘     └──────────┘     └──────────┘
```

**Cost**: $0/month (Render free tier) or $7/month (Render starter)

---

## ⚡ Quick Deploy (20 Minutes)

### Prerequisites
- GitHub account with repo: https://github.com/alexfreed254/tvet2026
- Render account (sign up: https://render.com)
- Vercel account (sign up: https://vercel.com)
- Supabase project ready

---

## Step 1: Setup Supabase Database (5 min)

### 1.1 Deploy Database Schema
1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **SQL Editor**
3. Open `database/schema.sql` from your project
4. Copy all content and paste into SQL Editor
5. Click **Run**
6. Wait for completion ✅

### 1.2 Create Storage Bucket
1. Click **Storage** in sidebar
2. Click **New bucket**
3. Name: `evidence-files`
4. Select: **Private**
5. Click **Create bucket** ✅

### 1.3 Get Database Connection String
1. Click **Settings** → **Database**
2. Find **Connection string** section
3. Scroll to **Connection pooling** (recommended for serverless)
4. Copy the **Transaction** mode URI:
   ```
   postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true
   ```
5. Replace `[YOUR-PASSWORD]` with your actual database password
6. Save this string ✅

---

## Step 2: Deploy Backend to Render (10 min)

### 2.1 Go to Render Dashboard
Open: https://dashboard.render.com

### 2.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if first time
   - Find and select: `alexfreed254/tvet2026`

### 2.3 Configure Service
- **Name**: `tvet-eassess-api` (or your choice)
- **Region**: Choose closest to you (e.g., Oregon)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: **Free** (or Starter $7/mo for no cold starts)

### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**, then add each:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://psdxitqfusfmkutxsojc.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk` |
| `SUPABASE_DB_URL` | *Your database URL from Step 1.3* |
| `JWT_SECRET` | `your-secure-random-32-character-key` |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRATION_MINUTES` | `480` |
| `SUPABASE_STORAGE_BUCKET` | `evidence-files` |
| `MAX_FILE_SIZE_MB` | `100` |
| `APP_NAME` | `TVET e-ASSESS` |
| `DEBUG` | `false` |
| `ALLOWED_ORIGINS` | `http://localhost:5173` |

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build and deployment
3. Watch the logs for any errors

### 2.6 Get Backend URL
Once deployed, your backend URL will be:
```
https://tvet-eassess-api.onrender.com
```

**Save this URL** - you'll need it for the frontend!

### 2.7 Test Backend
Visit: `https://tvet-eassess-api.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

✅ **Backend deployed!**

---

## Step 3: Deploy Frontend to Vercel (5 min)

### 3.1 Go to Vercel
Open: https://vercel.com/new

### 3.2 Import Project
1. Click **"Import Git Repository"**
2. Select **GitHub**
3. Find and import: `alexfreed254/tvet2026`

### 3.3 Configure Project
- **Project Name**: `tvet-eassess` (or your choice)
- **Framework Preset**: Vite
- **Root Directory**: Click **Edit** → Select `frontend` folder
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3.4 Add Environment Variables

Click **Environment Variables** and add:

| Name | Value |
|------|-------|
| `VITE_SUPABASE_URL` | `https://psdxitqfusfmkutxsojc.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8` |
| `VITE_API_BASE_URL` | `https://tvet-eassess-api.onrender.com` |

⚠️ **Replace `tvet-eassess-api.onrender.com` with YOUR actual Render backend URL from Step 2.6!**

### 3.5 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Your frontend will be live!

Your frontend URL: `https://tvet-eassess.vercel.app`

**Save this URL!**

✅ **Frontend deployed!**

---

## Step 4: Update CORS & Supabase (3 min)

### 4.1 Update Backend CORS

1. Go back to Render dashboard
2. Open your backend service: `tvet-eassess-api`
3. Click **Environment** in sidebar
4. Find `ALLOWED_ORIGINS`
5. Click **Edit**
6. Update to include your Vercel URL:
   ```
   http://localhost:5173,https://tvet-eassess.vercel.app
   ```
   ⚠️ Replace with YOUR actual Vercel URL!
7. Click **Save Changes**
8. Service will automatically redeploy (~2 min)

### 4.2 Configure Supabase Authentication

1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **Authentication** → **URL Configuration**
3. **Site URL**: Enter your Vercel URL
   ```
   https://tvet-eassess.vercel.app
   ```
4. **Redirect URLs** → Click **Add URL**
5. Add your Vercel URL with wildcard:
   ```
   https://tvet-eassess.vercel.app/**
   ```
6. Click **Save**

✅ **Configuration complete!**

---

## Step 5: Test Everything (2 min)

### 5.1 Test Backend
Visit: `https://your-backend.onrender.com/api/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

### 5.2 Test API Documentation
Visit: `https://your-backend.onrender.com/api/docs`

Should see FastAPI interactive documentation.

### 5.3 Test Frontend
Visit: `https://your-frontend.vercel.app`

Check:
- ✅ Page loads without errors
- ✅ No console errors (press F12 to check)
- ✅ Can navigate around

### 5.4 Test Authentication
1. Click **Register** or **Sign Up**
2. Create a test account with your email
3. Check if registration works
4. Try logging in
5. Should redirect to dashboard

✅ **Everything works!**

---

## 🎉 Success! You're Live!

### Your Deployment URLs:

**Frontend**: `https://your-app.vercel.app`
**Backend**: `https://your-api.onrender.com`
**API Docs**: `https://your-api.onrender.com/api/docs`
**Database**: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc

---

## 💰 Cost Breakdown

### Free Tier (Good for Testing/Small Projects)

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| Render | Free | **$0** | 750 hrs/month, spins down after 15 min |
| Vercel | Free | **$0** | 100GB bandwidth, unlimited sites |
| Supabase | Free | **$0** | 500MB DB, 1GB storage |
| **Total** | | **$0/mo** | Sufficient for development |

⚠️ **Free Tier Limitation**: Render free tier has cold starts (30-60 seconds after inactivity)

### Recommended for Production

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| Render | Starter | **$7** | Always-on, no cold starts, 512MB RAM |
| Vercel | Free | **$0** | Same as above |
| Supabase | Free | **$0** | Same as above |
| **Total** | | **$7/mo** | Production-ready |

**Upgrade Render to $7/mo Starter plan** to eliminate cold starts!

---

## 🔄 Making Updates

Both platforms auto-deploy on git push:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

- ✅ Vercel auto-deploys frontend (1-2 min)
- ✅ Render auto-deploys backend (3-5 min)

### Manual Redeploy

**Render**:
```
Dashboard → Your service → Manual Deploy → Deploy latest commit
```

**Vercel**:
```
Dashboard → Deployments → Redeploy
```

---

## 🆘 Troubleshooting

### Backend Takes Long to Respond (Free Tier)

**Issue**: First request takes 30-60 seconds

**Cause**: Render free tier spins down after 15 minutes of inactivity

**Solutions**:
1. **Upgrade to Starter ($7/mo)** - No cold starts
2. **Use a ping service** (e.g., UptimeRobot) to keep it warm
3. **Accept the delay** for development/testing

### Backend Won't Start

**Check Render Logs**:
1. Go to your service
2. Click **Logs** tab
3. Look for error messages

**Common Issues**:
- Missing environment variables
- Incorrect database URL
- Python dependency errors

**Fix**:
- Verify all env vars are set
- Check database URL format
- Review `requirements.txt`

### Frontend Can't Reach Backend

**Check**:
1. Backend is running (visit health endpoint)
2. `VITE_API_BASE_URL` is correct in Vercel
3. CORS includes your frontend URL
4. No typos in URLs

**Fix**:
1. Update CORS in Render
2. Redeploy backend
3. Check browser console (F12) for specific errors

### Authentication Fails

**Check**:
1. Supabase redirect URLs include your Vercel URL
2. Site URL is set correctly
3. Anon key is correct in both frontend and backend

**Fix**:
1. Update Supabase URL configuration
2. Verify environment variables
3. Clear browser cache and cookies

### Database Connection Errors

**Check**:
1. Database URL format is correct
2. Password doesn't have special characters causing issues
3. Using connection pooling URL (port 6543, not 5432)

**Fix**:
```
# Correct format (with pooling):
postgresql://postgres.[ref]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true

# NOT the direct connection (port 5432)
```

---

## 📊 Render Free vs Starter Comparison

### Free Tier
✅ Good for: Development, testing, demos
❌ Cold starts: 30-60 seconds after 15 min inactivity
✅ 750 hours/month
✅ 512MB RAM
✅ Auto-deploy

### Starter ($7/mo)
✅ Good for: Production, always-on apps
✅ No cold starts
✅ Always-on
✅ 512MB RAM
✅ Auto-deploy
✅ Better support

**Recommendation**: Start with free, upgrade to Starter when going to production.

---

## 🎯 Post-Deployment Tasks

### 1. Create Admin User
1. Register through the UI with your email
2. Go to Supabase → **SQL Editor**
3. Run:
   ```sql
   UPDATE public.users 
   SET role = 'super_admin' 
   WHERE email = 'your-email@example.com';
   ```

### 2. Configure Email Templates
1. Supabase → **Authentication** → **Email Templates**
2. Customize confirmation and recovery emails
3. Add your branding

### 3. Set Up Custom Domain (Optional)

**Vercel**:
1. Dashboard → Settings → Domains
2. Add your domain (e.g., `app.yourdomain.com`)
3. Update DNS records
4. Update Supabase URLs

**Render**:
1. Service → Settings → Custom Domain
2. Add your domain (e.g., `api.yourdomain.com`)
3. Update DNS records
4. Update Vercel frontend env vars

### 4. Set Up Monitoring

**Uptime Monitoring** (Keep Render warm):
- UptimeRobot: https://uptimerobot.com (free)
- Ping your health endpoint every 5 minutes

**Error Tracking**:
- Sentry: https://sentry.io (free tier available)
- Track errors in both frontend and backend

**Analytics**:
- Vercel Analytics: Built-in
- Google Analytics: Add to frontend

---

## 📝 Save Your URLs

Create a document with:

```
TVET e-ASSESS Deployment

Frontend:  https://________________.vercel.app
Backend:   https://________________.onrender.com
API Docs:  https://________________.onrender.com/api/docs
Database:  https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc

Deployed: [Today's Date]
Render Plan: Free / Starter ($7/mo)
```

---

## 🚀 Quick Commands

### Check Backend Status
```bash
curl https://your-backend.onrender.com/api/health
```

### View Backend Logs
```
Render Dashboard → Your service → Logs
```

### Redeploy Backend
```
Render Dashboard → Your service → Manual Deploy
```

### Check Frontend
```
Vercel Dashboard → Your project → Deployments
```

---

## 📚 Documentation Links

- **Render Docs**: https://render.com/docs
- **Render Python Guide**: https://render.com/docs/deploy-fastapi
- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs

---

## ✅ Deployment Checklist

- [ ] Supabase database schema deployed
- [ ] Supabase storage bucket created
- [ ] Database connection string saved
- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] Backend URL saved
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Frontend URL saved
- [ ] CORS updated in Render
- [ ] Supabase auth URLs configured
- [ ] Backend health check works
- [ ] Frontend loads successfully
- [ ] Registration works
- [ ] Login works

---

## 🎊 Congratulations!

Your TVET e-ASSESS platform is now live!

**Next Steps**:
1. Test all features thoroughly
2. Create admin users
3. Invite team members
4. Consider upgrading Render to Starter for production

**Need help?** Check the troubleshooting section above or open an issue on GitHub.

---

**Deployment Time**: ~20 minutes
**Cost**: $0-7/month
**Status**: Production-ready ✅

Enjoy your deployment! 🚀
