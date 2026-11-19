# 🚀 Deploy TVET e-ASSESS with Supabase Backend (25 Minutes)

## Architecture: Vercel + Fly.io + Supabase

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Vercel   │────▶│ Fly.io   │────▶│ Supabase │
│ Frontend │     │ Backend  │     │ Database │
│  (Free)  │     │ (Free)   │     │  (Free)  │
└──────────┘     └──────────┘     └──────────┘
```

**Total Cost: $0/month** (All free tiers!)

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
3. Copy the **URI** format (looks like):
   ```
   postgresql://postgres.psdxitqfusfmkutxsojc:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with your actual database password
5. Save this string - you'll need it soon ✅

---

## Step 2: Deploy Backend to Fly.io (10 min)

### 2.1 Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

Close and reopen your terminal after installation.

### 2.2 Login to Fly.io
```bash
fly auth login
```

Browser will open - sign up or login with GitHub.

### 2.3 Navigate to Backend and Launch
```bash
cd backend
fly launch --no-deploy
```

Answer the prompts:
- **App name**: Press Enter (auto-generate) or type `tvet-eassess-api`
- **Region**: Choose closest to you (e.g., `iad` for US East)
- **Would you like to set up a Postgresql database?**: **No** (we're using Supabase)
- **Would you like to set up an Upstash Redis database?**: **No**

### 2.4 Set Environment Secrets

Copy and paste these commands one by one:

```bash
fly secrets set SUPABASE_URL="https://psdxitqfusfmkutxsojc.supabase.co"
```

```bash
fly secrets set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8"
```

```bash
fly secrets set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk"
```

**⚠️ IMPORTANT**: Replace with YOUR database URL from Step 1.3:
```bash
fly secrets set SUPABASE_DB_URL="postgresql://postgres.psdxitqfusfmkutxsojc:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
```

Generate a secure JWT secret (or use this example):
```bash
fly secrets set JWT_SECRET="your-super-secure-random-32-character-key-change-this"
```

```bash
fly secrets set JWT_ALGORITHM="HS256"
```

```bash
fly secrets set JWT_EXPIRATION_MINUTES="480"
```

```bash
fly secrets set SUPABASE_STORAGE_BUCKET="evidence-files"
```

```bash
fly secrets set MAX_FILE_SIZE_MB="100"
```

```bash
fly secrets set APP_NAME="TVET e-ASSESS"
```

```bash
fly secrets set DEBUG="false"
```

```bash
fly secrets set ALLOWED_ORIGINS="http://localhost:5173"
```

### 2.5 Deploy Backend
```bash
fly deploy
```

Wait 3-5 minutes for build and deployment.

### 2.6 Test Backend
```bash
fly status
```

Copy your app URL (e.g., `https://tvet-eassess-api.fly.dev`)

Test it:
```bash
curl https://your-app-name.fly.dev/api/health
```

Should return:
```json
{"status":"healthy","service":"TVET e-ASSESS API","version":"1.0.0"}
```

✅ **Backend deployed!**

**Save your backend URL**: `https://____________.fly.dev`

---

## Step 3: Deploy Frontend to Vercel (5 min)

### 3.1 Go to Vercel
Open: https://vercel.com/new

### 3.2 Import Project
1. Click **Import Git Repository**
2. Select **GitHub**
3. Find and import: `alexfreed254/tvet2026`

### 3.3 Configure Project
- **Project Name**: `tvet-eassess` (or any name)
- **Framework Preset**: Vite
- **Root Directory**: Click **Edit** → Select `frontend` folder
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)

### 3.4 Add Environment Variables

Click **Environment Variables** and add these three:

**Variable 1:**
- Name: `VITE_SUPABASE_URL`
- Value: `https://psdxitqfusfmkutxsojc.supabase.co`

**Variable 2:**
- Name: `VITE_SUPABASE_ANON_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8`

**Variable 3:** ⚠️ USE YOUR BACKEND URL FROM STEP 2.6
- Name: `VITE_API_BASE_URL`
- Value: `https://your-app-name.fly.dev` (YOUR Fly.io backend URL)

### 3.5 Deploy
Click **Deploy**

Wait 2-3 minutes for build.

Your frontend will be live at: `https://tvet-eassess.vercel.app`

✅ **Frontend deployed!**

**Save your frontend URL**: `https://____________.vercel.app`

---

## Step 4: Update CORS & Supabase (5 min)

### 4.1 Update Backend CORS

Back in your terminal:

```bash
cd backend
fly secrets set ALLOWED_ORIGINS="http://localhost:5173,https://your-frontend-url.vercel.app"
```

⚠️ Replace `your-frontend-url.vercel.app` with YOUR actual Vercel URL!

The app will automatically redeploy (takes ~2 min).

### 4.2 Configure Supabase Authentication

1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **Authentication** → **URL Configuration**
3. **Site URL**: Enter your Vercel URL: `https://your-frontend-url.vercel.app`
4. **Redirect URLs** → Click **Add URL**
5. Add: `https://your-frontend-url.vercel.app/**` (with the `/**` at the end)
6. Click **Save**

✅ **Configuration complete!**

---

## Step 5: Test Everything (3 min)

### 5.1 Test Backend Health
Visit: `https://your-backend.fly.dev/api/health`

Should show:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

### 5.2 Test API Documentation
Visit: `https://your-backend.fly.dev/api/docs`

You should see FastAPI interactive documentation.

### 5.3 Test Frontend
Visit: `https://your-frontend.vercel.app`

Check:
- ✅ Page loads without errors
- ✅ No console errors (F12 to check)
- ✅ Can navigate around

### 5.4 Test Authentication
1. Click **Register** or **Sign Up**
2. Create a test account
3. Check if registration works
4. Try logging in
5. Should redirect to dashboard

✅ **Everything works!**

---

## 🎉 Success! You're Live!

### Your Deployment:

**Frontend**: `https://your-frontend.vercel.app`
**Backend**: `https://your-backend.fly.dev`
**API Docs**: `https://your-backend.fly.dev/api/docs`
**Database**: Supabase (https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc)

### Total Cost: **$0/month**

All on free tiers! 🎊

---

## 📝 Save These URLs

Create a note with:

```
TVET e-ASSESS Deployment

Frontend: https://________________.vercel.app
Backend:  https://________________.fly.dev
Database: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc

Deployed: [Today's Date]
```

---

## 🔄 Making Updates

Both platforms auto-deploy when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

- ✅ Vercel auto-deploys frontend
- ✅ Fly.io auto-deploys backend (if GitHub Actions setup)

### Manual Redeploy

**Vercel:**
```
Dashboard → Deployments → Redeploy
```

**Fly.io:**
```bash
cd backend
fly deploy
```

---

## 🆘 Troubleshooting

### Backend won't start
```bash
fly logs
fly status
```

Check secrets are set:
```bash
fly secrets list
```

### Frontend can't reach backend

**Check:**
1. Backend is running: `fly status`
2. `VITE_API_BASE_URL` is correct in Vercel
3. CORS includes your frontend URL
4. No typos in URLs

**Fix:**
- Redeploy frontend after fixing env vars
- Update CORS in Fly.io secrets

### Authentication fails

**Check:**
1. Supabase redirect URLs include your Vercel URL
2. Site URL is set correctly
3. Browser console for errors

---

## 💡 Useful Commands

### Fly.io Commands
```bash
fly status              # Check app status
fly logs               # View logs
fly ssh console        # SSH into container
fly secrets list       # List all secrets
fly apps list          # List your apps
fly scale count 1      # Scale to 1 instance
```

### Check Deployments
```bash
# Backend
curl https://your-backend.fly.dev/api/health

# Frontend
curl -I https://your-frontend.vercel.app
```

---

## 📊 Free Tier Limits

### Fly.io (Free)
- ✅ 3 shared VMs (256MB RAM each)
- ✅ 160GB bandwidth/month
- ✅ Auto stop/start (no cold starts under 1s)

### Vercel (Free)
- ✅ 100GB bandwidth/month
- ✅ Unlimited sites
- ✅ Global CDN

### Supabase (Free)
- ✅ 500MB database
- ✅ 1GB file storage
- ✅ 50K monthly active users

**This is plenty for development and small production use!**

---

## 🚀 Next Steps

### 1. Create Admin User
1. Register through the UI
2. Go to Supabase → Authentication → Users
3. Find your user
4. Go to SQL Editor:
   ```sql
   UPDATE public.users 
   SET role = 'super_admin' 
   WHERE email = 'your-email@example.com';
   ```

### 2. Custom Domain (Optional)
**Vercel:**
- Settings → Domains → Add your domain

**Fly.io:**
```bash
fly certs add your-domain.com
```

### 3. Monitoring
- Fly.io: Built-in metrics
- Vercel: Analytics dashboard
- Supabase: Database logs

---

## 📚 More Help

- **Detailed Guide**: [SUPABASE-BACKEND.md](./SUPABASE-BACKEND.md)
- **Fly.io Docs**: https://fly.io/docs
- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs

---

## ✅ Deployment Checklist

- [x] Supabase database schema deployed
- [x] Supabase storage bucket created
- [x] Fly.io CLI installed
- [x] Backend deployed to Fly.io
- [x] Backend URL saved
- [x] Frontend deployed to Vercel
- [x] Frontend URL saved
- [x] CORS updated
- [x] Supabase auth URLs configured
- [x] Health check passes
- [x] Frontend loads
- [x] Authentication tested

---

**🎊 Congratulations! Your TVET e-ASSESS platform is live!**

**Time Taken**: ~25 minutes
**Cost**: $0/month
**Status**: Production-ready ✅

Enjoy your deployment! 🚀
