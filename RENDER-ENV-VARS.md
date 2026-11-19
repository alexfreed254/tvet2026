# 🔐 Render Environment Variables

## Copy these EXACT values into Render Dashboard

Go to: https://dashboard.render.com → Your Service → Environment

---

## ✅ Required Environment Variables

### 1. SUPABASE_URL
```
https://psdxitqfusfmkutxsojc.supabase.co
```

### 2. SUPABASE_ANON_KEY
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwNzY2NTcsImV4cCI6MjExMDY1MjY1N30.yAeKBvZKtMPfgvb1dQiHRlyC9FH6TBDVwcaZYnrIZi8
```

### 3. SUPABASE_SERVICE_ROLE_KEY
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzZHhpdHFmdXNmbWt1dHhzb2pjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA3NjY1NywiZXhwIjoyMTEwNjUyNjU3fQ.yMFpBWeqDQzc0wqWz-tva7DvfoUex0hLFZn0r0Aqcdk
```

### 4. SUPABASE_DB_URL ⚠️ IMPORTANT
```
postgresql://postgres:SxQnTCatCQ2mvJxH@db.psdxitqfusfmkutxsojc.supabase.co:5432/postgres
```

### 5. JWT_SECRET ⚠️ IMPORTANT
```
II+wY04cO0Q6z4YiWOIxMqCVwpP/rYwb+xgP6jShzK7Ji4OKW65os17hms/zBGGzzZOXVE1RlGq6YDzlzPeG6Q==
```

### 6. JWT_ALGORITHM
```
HS256
```

### 7. JWT_EXPIRATION_MINUTES
```
480
```

### 8. SUPABASE_STORAGE_BUCKET
```
evidence-files
```

### 9. MAX_FILE_SIZE_MB
```
100
```

### 10. APP_NAME
```
TVET e-ASSESS
```

### 11. DEBUG
```
false
```

---

## 📋 Step-by-Step Instructions

### In Render Dashboard:

1. **Go to your service**: https://dashboard.render.com
2. **Click on**: `tvet-eassess-api`
3. **Click**: **Environment** (left sidebar)
4. **For each variable above**:
   - Click **Add Environment Variable**
   - Copy the **Key** (e.g., `SUPABASE_URL`)
   - Copy the **Value** (the long string below it)
   - Click **Add**
5. **After adding all 11 variables**:
   - Click **Save Changes**
   - Render will automatically redeploy

---

## 📝 Note about ALLOWED_ORIGINS

**ALLOWED_ORIGINS is NOT set as an environment variable.**

It uses the default value from `backend/app/config.py`:
```python
ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]
```

After deploying your frontend to Vercel, update this line in the code to add your Vercel URL:
```python
ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173", "https://your-app.vercel.app"]
```

---

## ⚠️ Critical Variables

These two were MISSING and caused the deployment to fail:

1. ✅ **SUPABASE_DB_URL** - Now added
2. ✅ **JWT_SECRET** - Now added

---

## 🔍 Verification Checklist

After adding all variables, you should have:

- [ ] SUPABASE_URL
- [ ] SUPABASE_ANON_KEY
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] SUPABASE_DB_URL ⚠️
- [ ] JWT_SECRET ⚠️
- [ ] JWT_ALGORITHM
- [ ] JWT_EXPIRATION_MINUTES
- [ ] SUPABASE_STORAGE_BUCKET
- [ ] MAX_FILE_SIZE_MB
- [ ] APP_NAME
- [ ] DEBUG

**Total: 11 environment variables**

(ALLOWED_ORIGINS is not needed - it uses the default from code)

---

## 🚀 After Saving

1. Render will automatically redeploy (2-3 minutes)
2. Watch the logs for success
3. Test health endpoint: `https://your-service.onrender.com/api/health`

---

## 🎯 Expected Success

Once all variables are set, you should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

And visiting `/api/health` should return:
```json
{
  "status": "healthy",
  "service": "TVET e-ASSESS API",
  "version": "1.0.0"
}
```

---

## 🔐 Security Note

⚠️ **NEVER commit this file to Git!**

This file contains sensitive credentials and is for reference only.
The `.env` file in the project root is already in `.gitignore`.

---

**Your Database Password**: `SxQnTCatCQ2mvJxH`  
**Keep this secure!**
