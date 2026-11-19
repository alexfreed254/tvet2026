# 🚀 Render Quick Start Guide

## 5-Minute Deployment

### Step 1: Get Database URL (2 min)
1. Go to: https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc/settings/database
2. Copy **Connection String** → **URI**
3. Replace `[YOUR-PASSWORD]` with your database password

### Step 2: Deploy to Render (2 min)
1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect repo: `alexfreed254/tvet2026`
4. Click **"Apply"**

### Step 3: Add Environment Variables (1 min)

**Backend Service:**
```
SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk
SUPABASE_DB_URL=[paste from step 1]
```

**Frontend Service:**
```
VITE_SUPABASE_URL=https://psdxitqfusfmkutxsojc.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
```

### Done! 🎉

Your app will be live at:
- Frontend: `https://tvet-eassess-frontend.onrender.com`
- Backend: `https://tvet-eassess-api.onrender.com`

---

## Post-Deployment (After First Deploy)

### Update CORS:
1. Go to backend service in Render
2. Environment → Edit `ALLOWED_ORIGINS`
3. Change to: `http://localhost:5173,https://tvet-eassess-frontend.onrender.com`
4. Save (auto-redeploys)

### Update Supabase:
1. Supabase Dashboard → Authentication → URL Configuration
2. Site URL: `https://tvet-eassess-frontend.onrender.com`
3. Add to Redirect URLs: `https://tvet-eassess-frontend.onrender.com/**`

---

## Testing

Visit: `https://tvet-eassess-frontend.onrender.com`
- Register new user ✓
- Login ✓
- Navigate app ✓

---

## Important Notes

⚠️ **Free Tier**: Services sleep after 15 min of inactivity
- First request after sleep: 30-60 seconds
- Subsequent requests: Fast

🔒 **Security**: Never commit `.env` to GitHub (already in .gitignore)

🔄 **Auto-Deploy**: Pushes to `main` branch auto-deploy

---

## Need Help?

See `DEPLOYMENT-GUIDE.md` for detailed instructions
See `DEPLOYMENT-CHECKLIST.md` for step-by-step checklist
