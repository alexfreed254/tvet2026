# TVET@2026 Render Deployment Guide

## Prerequisites
- GitHub account with the repository: https://github.com/alexfreed254/tvet2026.git
- Render account (sign up at https://render.com)
- Supabase project configured

## Your Supabase Credentials
- **Project URL**: `https://psdxitqfusfmkutxsojc.supabase.co`
- **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8`
- **Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk`

---

## Step 1: Get Supabase Database URL

1. Go to https://supabase.com/dashboard/project/psdxitqfusfmkutxsojc
2. Click **Settings** → **Database**
3. Scroll to **Connection String** section
4. Copy the **URI** format (looks like):
   ```
   postgresql://postgres.psdxitqfusfmkutxsojc:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual database password
6. Save this - you'll need it in Step 4

---

## Step 2: Deploy to Render Using Blueprint

### Option A: Using Blueprint (Recommended - Deploys Everything at Once)

1. **Log in to Render**: https://dashboard.render.com
2. **Click "New +"** → Select **"Blueprint"**
3. **Connect Repository**:
   - Click "Connect a repository"
   - Authorize Render to access your GitHub
   - Select `alexfreed254/tvet2026`
4. **Name your blueprint**: `tvet-eassess` (or any name)
5. **Click "Apply"** - but WAIT! Don't deploy yet, we need to add environment variables first

---

## Step 3: Configure Environment Variables

After connecting the repository but BEFORE deploying, you'll see two services created:

### Service 1: `tvet-eassess-api` (Backend)

Click on the backend service and add these environment variables:

| Variable Name | Value |
|--------------|-------|
| `SUPABASE_URL` | `https://psdxitqfusfmkutxsojc.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk` |
| `SUPABASE_DB_URL` | *Use the database URL from Step 1* |
| `JWT_SECRET` | *Render will auto-generate this* |
| `ALLOWED_ORIGINS` | `http://localhost:5173` *(we'll update this after frontend deploys)* |

### Service 2: `tvet-eassess-frontend` (Frontend)

Click on the frontend service and add these environment variables:

| Variable Name | Value |
|--------------|-------|
| `VITE_SUPABASE_URL` | `https://psdxitqfusfmkutxsojc.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8` |
| `VITE_API_BASE_URL` | *This will auto-populate from the backend service* |

---

## Step 4: Deploy the Services

1. **Click "Apply" or "Create"** to start deployment
2. Watch the build logs:
   - Backend will install Python dependencies and start FastAPI
   - Frontend will build the React app with Vite
3. **Wait for both services to turn green** (this may take 5-10 minutes)

---

## Step 5: Update CORS Settings

After both services are deployed:

1. **Get your frontend URL**: 
   - Go to the frontend service dashboard
   - Copy the URL (e.g., `https://tvet-eassess-frontend.onrender.com`)

2. **Update backend CORS**:
   - Go to the backend service (`tvet-eassess-api`)
   - Click **Environment** tab
   - Find `ALLOWED_ORIGINS`
   - Update to: `http://localhost:5173,https://tvet-eassess-frontend.onrender.com`
   - Click **Save Changes**
   - The backend will automatically redeploy

---

## Step 6: Configure Supabase for Production

1. Go to your Supabase dashboard
2. Navigate to **Authentication** → **URL Configuration**
3. Add your Render frontend URL to:
   - **Site URL**: `https://tvet-eassess-frontend.onrender.com`
   - **Redirect URLs**: Add `https://tvet-eassess-frontend.onrender.com/**`

---

## Step 7: Test Your Deployment

1. Visit your frontend URL: `https://tvet-eassess-frontend.onrender.com`
2. Try to:
   - Register a new user
   - Log in
   - Navigate through the app
3. Check browser console for any errors
4. Verify backend API health: `https://tvet-eassess-api.onrender.com/api/health`

---

## Your Deployed URLs

After successful deployment, save these URLs:

- **Frontend**: `https://tvet-eassess-frontend.onrender.com`
- **Backend API**: `https://tvet-eassess-api.onrender.com`
- **API Docs**: `https://tvet-eassess-api.onrender.com/docs`
- **Health Check**: `https://tvet-eassess-api.onrender.com/api/health`

---

## Troubleshooting

### Build Fails
- Check the build logs for specific errors
- Verify all environment variables are set correctly
- Ensure `requirements.txt` and `package.json` are up to date

### Backend Won't Start
- Verify `SUPABASE_DB_URL` is correct
- Check that all required environment variables are set
- Look for Python errors in the logs

### Frontend Shows API Errors
- Check that `VITE_API_BASE_URL` points to your backend
- Verify CORS is configured correctly in backend
- Check browser console for specific error messages

### Cold Starts (Free Tier)
- Free services spin down after 15 minutes of inactivity
- First request may take 30-60 seconds
- Consider upgrading to paid plan for always-on services

### Authentication Issues
- Verify Supabase redirect URLs include your Render frontend URL
- Check that environment variables match between services
- Ensure JWT_SECRET is the same across deployments

---

## Monitoring & Logs

- **View Logs**: Click on each service → **Logs** tab
- **Metrics**: Monitor CPU, memory, and bandwidth usage
- **Health Checks**: Backend has health endpoint at `/api/health`

---

## Continuous Deployment

Render automatically deploys when you push to the `main` branch:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Render will automatically detect the push and redeploy both services

To disable auto-deploy:
- Go to service settings → **Build & Deploy**
- Toggle off "Auto-Deploy"

---

## Upgrading from Free Tier

Consider upgrading if you need:
- Zero downtime (no cold starts)
- Custom domains
- More CPU/memory
- Background workers
- Priority support

Pricing starts at $7/month per service.

---

## Security Best Practices

✅ **Do**:
- Keep `.env` in `.gitignore` (already done)
- Use environment variables for all secrets
- Regularly rotate JWT_SECRET
- Monitor logs for suspicious activity
- Keep dependencies updated

❌ **Don't**:
- Commit secrets to GitHub
- Share service role keys publicly
- Use the same JWT_SECRET in dev and prod
- Expose database URL in frontend code

---

## Next Steps

1. Set up a custom domain (optional)
2. Configure email templates in Supabase
3. Set up monitoring/alerting
4. Create staging environment
5. Set up automated backups
6. Configure CDN for static assets

---

## Support

- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

Need help? Check the logs first, then review this guide.
