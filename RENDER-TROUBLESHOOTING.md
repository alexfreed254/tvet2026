# Render Deployment Troubleshooting Guide

## ✅ FIXED: Dockerfile Error

### Issue
```
error: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory
```

### Cause
Render was auto-detecting the `Dockerfile` in the `backend/` directory and trying to use Docker instead of the Blueprint configuration from `render.yaml`.

### Solution Applied
1. Renamed `backend/Dockerfile` to `backend/Dockerfile.docker-compose`
2. Updated `render.yaml` to explicitly use `env: python` (native build)
3. Pushed changes to GitHub

### Result
Render will now use the native Python environment as specified in `render.yaml` instead of trying to build with Docker.

---

## Common Render Deployment Issues

### 1. Build Fails - Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
- Check `backend/requirements.txt` exists and is complete
- Verify build command in render.yaml: `pip install -r requirements.txt`
- Check Render logs for specific missing packages

---

### 2. Environment Variables Not Set

**Error:**
```
ValidationError: SUPABASE_URL field required
```

**Solution:**
1. Go to Render dashboard → Your service
2. Click **Environment** tab
3. Add all required variables:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `SUPABASE_DB_URL`
4. Save and redeploy

---

### 3. CORS Errors in Browser

**Error (in browser console):**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Go to backend service → Environment
2. Update `ALLOWED_ORIGINS` to include your frontend URL:
   ```
   http://localhost:5173,https://your-frontend.onrender.com
   ```
3. Save (will auto-redeploy)

---

### 4. Frontend Build Fails

**Error:**
```
npm ERR! missing script: build
```

**Solution:**
- Verify `frontend/package.json` has build script:
  ```json
  "scripts": {
    "build": "tsc && vite build"
  }
  ```
- Check that `frontend/vite.config.ts` exists

---

### 5. Backend Won't Start

**Error:**
```
uvicorn: command not found
```

**Solution:**
- Ensure `uvicorn[standard]` is in `backend/requirements.txt`
- Verify start command in render.yaml:
  ```yaml
  startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

---

### 6. Database Connection Error

**Error:**
```
OperationalError: could not connect to server
```

**Solution:**
1. Verify `SUPABASE_DB_URL` format:
   ```
   postgresql://postgres.xxx:[PASSWORD]@xxx.supabase.co:6543/postgres
   ```
2. Check password is correct (no brackets)
3. Ensure database is accessible from Render IPs
4. Verify Supabase project is not paused

---

### 7. Authentication Fails

**Error:**
```
Invalid login credentials
```

**Solution:**
1. Check Supabase → Authentication → URL Configuration
2. Add your Render frontend URL to:
   - Site URL
   - Redirect URLs (with `/**`)
3. Verify JWT_SECRET is set in backend environment
4. Check that user exists in Supabase Auth

---

### 8. File Upload Fails

**Error:**
```
Storage bucket not found
```

**Solution:**
1. Go to Supabase → Storage
2. Create bucket: `evidence-files`
3. Set to **Private**
4. Configure RLS policies if needed
5. Verify `SUPABASE_STORAGE_BUCKET=evidence-files` in backend env

---

### 9. Service in "Build Failed" State

**Symptoms:**
- Red status indicator
- Service won't start

**Solutions:**
1. **Check Build Logs**:
   - Click service → Logs tab
   - Look for specific error messages

2. **Common Fixes**:
   - Clear cache: Manual Deploy → Clear build cache
   - Check all env vars are set
   - Verify branch is correct (main)
   - Check file paths in render.yaml

3. **If Still Failing**:
   - Delete service and recreate
   - Check GitHub repo is accessible
   - Try manual deployment from specific commit

---

### 10. Cold Starts (Free Tier)

**Symptoms:**
- First request takes 30-60 seconds
- "Service is starting" message

**This is Normal for Free Tier:**
- Services spin down after 15 min inactivity
- First request wakes up the service
- Subsequent requests are fast

**Solutions:**
- Upgrade to paid plan for 24/7 uptime
- Use uptime monitoring to ping periodically
- Inform users about potential wait time

---

## Debugging Tips

### 1. Check Logs
```
Render Dashboard → Service → Logs
```
- Build logs: Show dependency installation
- Deploy logs: Show service startup
- Runtime logs: Show application errors

### 2. Check Health Endpoint
```
https://your-backend.onrender.com/api/health
```
Should return: `{"status": "healthy"}`

### 3. Test API Docs
```
https://your-backend.onrender.com/docs
```
FastAPI interactive documentation

### 4. Browser Console
```
F12 → Console tab
```
Check for JavaScript errors and CORS issues

### 5. Network Tab
```
F12 → Network tab
```
- Check API request/response
- Verify status codes
- Check request headers

---

## Emergency Rollback

If deployment breaks:

1. **Via Git:**
   ```bash
   git log --oneline -5
   git revert HEAD
   git push origin main
   ```

2. **Via Render:**
   - Go to service → Deploys
   - Find last working deploy
   - Click "Redeploy"

---

## Getting More Help

### Check Documentation
1. [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md)
2. [RENDER-QUICK-START.md](./RENDER-QUICK-START.md)
3. [DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md)

### External Resources
- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

### Support Channels
- Render Support: https://render.com/support
- Supabase Discord: https://discord.supabase.com
- GitHub Issues: https://github.com/alexfreed254/tvet2026/issues

---

## Verification Checklist

After fixing any issue, verify:

- [ ] Service shows "Live" status (green)
- [ ] Health endpoint responds: `/api/health`
- [ ] Frontend loads without errors
- [ ] Can login/register users
- [ ] No CORS errors in console
- [ ] API requests work from frontend
- [ ] File uploads work (if applicable)

---

## Prevention Tips

### Before Each Deployment
1. Test locally first
2. Run `.\verify-env.ps1`
3. Check all environment variables
4. Review recent code changes
5. Test critical features

### Regular Maintenance
- Monitor service logs weekly
- Check for dependency updates monthly
- Rotate secrets quarterly
- Review error rates
- Monitor disk usage

---

## Current Status

✅ **Dockerfile Issue**: FIXED (commit ba677fd)
- Renamed to `Dockerfile.docker-compose`
- Updated `render.yaml` to use native Python
- Deployment should now work correctly

---

**Last Updated**: January 2025 (after Dockerfile fix)
**Commit**: ba677fd
