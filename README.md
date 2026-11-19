# TVET e-ASSESS — Digital Practical Assessment Platform

**Assess Digitally. Verify Competence. Preserve Evidence.**

A comprehensive digital platform for managing practical assessments in TVET (Technical and Vocational Education and Training) institutions.

## 🚀 Quick Deploy (20 Minutes)

**Architecture: Vercel (Frontend) + Render (Backend) + Supabase (Database)**

```
Frontend (Vercel) → Backend (Render) → Database (Supabase)
     FREE             FREE/$7           FREE
```

### 📖 Deployment Guide

**[DEPLOY-RENDER-VERCEL.md](./DEPLOY-RENDER-VERCEL.md)** ⭐ - Complete step-by-step deployment

**Total Cost**: 
- Free tier: $0/month (with cold starts)
- Production: $7/month (Render Starter - no cold starts)

## 📋 Features

- **Assessment Management**: Create and manage competency-based assessments
- **Digital Evidence**: Upload, store, and verify evidence files
- **Marking Interface**: Real-time marking with checklist-based criteria
- **Marksheet Generation**: Automated PDF and Excel marksheet generation
- **Verification Workflow**: Multi-level verification and moderation
- **Role-Based Access**: Super admin, admin, assessor, verifier roles
- **Audit Trail**: Complete audit logging of all actions

## 🛠 Tech Stack

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + Radix UI
- Zustand (state management)
- React Router
- Axios

### Backend
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- Pydantic (validation)
- JWT authentication
- ReportLab & FPDF2 (PDF generation)
- OpenPyXL (Excel generation)

### Infrastructure
- **Authentication**: Supabase Auth
- **Database**: PostgreSQL (Supabase)
- **Storage**: Supabase Storage
- **Hosting**: Render (Blueprint deployment)

## 📁 Project Structure

```
TVET@2026/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── models/      # SQLAlchemy models
│   │   ├── routers/     # API endpoints
│   │   ├── services/    # Business logic
│   │   ├── auth/        # Authentication
│   │   └── utils/       # Helpers
│   └── requirements.txt
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Route pages
│   │   ├── api/         # API client
│   │   ├── store/       # State management
│   │   └── types/       # TypeScript types
│   └── package.json
├── database/            # SQL schemas
├── render.yaml          # Render Blueprint
└── .env                 # Local environment (not committed)
```

## 🚀 Deployment

### Recommended Setup: Render + Vercel + Supabase

- **Frontend**: Vercel (Fast CDN, auto-deploy, FREE)
- **Backend**: Render (Easy setup, FREE or $7/mo Starter)
- **Database**: Supabase (PostgreSQL + Auth + Storage, FREE)

**Total Time**: ~20 minutes  
**Total Cost**: $0/month (free) or $7/month (no cold starts)

See [DEPLOY-RENDER-VERCEL.md](./DEPLOY-RENDER-VERCEL.md) for complete step-by-step guide.

### Quick Deploy Steps

1. **Setup Supabase**: Deploy database schema and create storage bucket
2. **Deploy Backend to Render**: Connect GitHub, configure environment variables
3. **Deploy Frontend to Vercel**: Import repo, set frontend folder, add env vars
4. **Configure**: Update CORS and Supabase redirect URLs

### Cost Options

**Free Tier** ($0/mo):
- Good for development and testing
- ⚠️ Backend has cold starts (30-60s after 15min inactivity)

**Production** ($7/mo):
- Upgrade Render to Starter plan
- ✅ Always-on backend, no cold starts
- Same fast frontend and database

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Supabase account)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alexfreed254/tvet2026.git
   cd tvet2026
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Start Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
   API will be available at: `http://localhost:8000`
   API Docs: `http://localhost:8000/docs`

4. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   App will be available at: `http://localhost:5173`

### Environment Variables

See `.env.example` for all required variables. Key variables:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_DB_URL=postgresql://...

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=480

# App
APP_NAME=TVET e-ASSESS
DEBUG=true
ALLOWED_ORIGINS=http://localhost:5173
```

## 🗄 Database Setup

1. **Run the schema**
   ```bash
   # In Supabase SQL Editor
   # Execute: database/schema.sql
   ```

2. **Create Storage Bucket**
   - Go to Supabase Storage
   - Create bucket: `evidence-files`
   - Set to private

3. **Create Admin User**
   - Use Supabase Auth to create user
   - Insert into `public.users` table with role `super_admin`

## 📚 Documentation

- **[Deploy Guide](./DEPLOY-RENDER-VERCEL.md)** ⭐ - Deploy in 20 minutes (Render + Vercel + Supabase)
- **[Deployment Options](./DEPLOYMENT-OPTIONS.md)** - Platform comparison
- **[Implementation Notes](./IMPLEMENTATION-NOTES.md)** - Technical details
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running locally)

## 🔒 Security

- Environment variables for all secrets
- JWT-based authentication
- Role-based access control (RBAC)
- Supabase Row Level Security (RLS)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Assessments
- `GET /api/assessments` - List assessments
- `POST /api/assessments` - Create assessment
- `GET /api/assessments/{id}` - Get assessment details
- `PUT /api/assessments/{id}` - Update assessment

### Marking
- `POST /api/marking/start` - Start marking session
- `POST /api/marking/submit` - Submit marks
- `GET /api/marking/session/{id}` - Get marking session

### Evidence
- `POST /api/evidence/upload` - Upload evidence file
- `GET /api/evidence/{id}` - Get evidence details
- `DELETE /api/evidence/{id}` - Delete evidence

See full API documentation at `/docs` when backend is running.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open Pull Request

## ⚠️ Important Notes

- This is a deployment-configured platform, not production-certified
- Complete acceptance testing before using with real trainee data
- Never commit `.env` file (already in `.gitignore`)
- Keep Supabase service role key secure (server-side only)
- Review [IMPLEMENTATION-NOTES.md](./IMPLEMENTATION-NOTES.md) for known limitations

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Check [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) for troubleshooting
- Review logs in Render dashboard
- Check Supabase logs for database issues
- Open an issue on GitHub

## 🔗 Links

- **Repository**: https://github.com/alexfreed254/tvet2026
- **Render Dashboard**: https://dashboard.render.com
- **Supabase Dashboard**: https://supabase.com/dashboard

---

**Built for TVET@2026 Initiative**
