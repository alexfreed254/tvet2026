# TVET e-ASSESS — Digital Practical Assessment Platform

**Assess Digitally. Verify Competence. Preserve Evidence.**

A comprehensive digital platform for managing practical assessments in TVET (Technical and Vocational Education and Training) institutions.

## 🚀 Quick Deploy (25 Minutes) - FREE!

**Architecture: Vercel (Frontend) + Fly.io (Backend) + Supabase (Database)**

```
Frontend (Vercel) → Backend (Fly.io) → Database (Supabase)
    FREE              FREE                FREE
```

### 📖 Deployment Guides

1. **[DEPLOY-NOW.md](./DEPLOY-NOW.md)** ⭐ - Complete deployment in 25 minutes (with Supabase)
2. **[SUPABASE-BACKEND.md](./SUPABASE-BACKEND.md)** - Detailed Supabase + Fly.io guide
3. **[DEPLOYMENT-OPTIONS.md](./DEPLOYMENT-OPTIONS.md)** - Compare all platforms

**Total Cost**: $0/month (All free tiers!)

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

### Recommended Setup: All Free Tiers! 🎉

- **Frontend**: Vercel (Fast CDN, auto-deploy)
- **Backend**: Fly.io (Always-on, no cold starts)
- **Database**: Supabase (PostgreSQL + Auth + Storage)

**Total Time**: ~25 minutes  
**Total Cost**: $0/month (All free tiers!)

See [DEPLOY-NOW.md](./DEPLOY-NOW.md) for step-by-step deployment.

### Quick Deploy

1. **Setup Supabase**: [Guide](./DEPLOY-NOW.md#step-1-setup-supabase-database-5-min)
2. **Deploy Backend to Fly.io**: [Guide](./DEPLOY-NOW.md#step-2-deploy-backend-to-flyio-10-min)
3. **Deploy Frontend to Vercel**: [Guide](./DEPLOY-NOW.md#step-3-deploy-frontend-to-vercel-5-min)
4. Configure CORS and Supabase

### Alternative Platforms

- **Railway**: Backend alternative ($5/mo credit)
- **Render**: Full-stack (free tier with cold starts)
- See [DEPLOYMENT-OPTIONS.md](./DEPLOYMENT-OPTIONS.md) for comparison

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

- **[Deploy Now](./DEPLOY-NOW.md)** ⭐ - Deploy in 25 minutes (FREE - Vercel + Fly.io + Supabase)
- **[Supabase Backend Guide](./SUPABASE-BACKEND.md)** - Using Supabase as your data layer
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
