# TVET e-ASSESS — DIGITAL PRACTICAL ASSESSMENT PLATFORM

**Assess Digitally. Verify Competence. Preserve Evidence.**

This repository follows the uploaded `tvet-eassess/` folder structure and includes the code blocks supplied in the 19 November 2026 implementation uploads. Files absent from the supplied code were added only where necessary to make the project structure buildable; see `IMPLEMENTATION-NOTES.md`.

## Stack
- React 18 + TypeScript + Vite + Tailwind CSS
- FastAPI + SQLAlchemy
- Supabase Auth, PostgreSQL and Storage
- Render Blueprint (`render.yaml`)

## Deploy on Render
1. Push this project to a GitHub repository. The repository root must contain `render.yaml`.
2. In Render, choose **New + → Blueprint** and connect the repository.
3. In the Render dashboard, set the API service secrets: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_URL`, and a strong `JWT_SECRET` (Render generates one by default).
4. Set the frontend service `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`. The API host is linked from the API service.
5. After the frontend deploys, copy its `https://...onrender.com` URL into the API service's `ALLOWED_ORIGINS` (comma-separated if adding more than one origin), save, and redeploy the API.
6. In Supabase SQL Editor, run `database/schema.sql`. Create a private Storage bucket named `evidence-files`.
7. In Supabase Auth, create the initial admin user, then create the matching profile in `public.users` with role `super_admin` (the SQL schema requires the auth user ID).

## Local development
- API: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`
- UI: `cd frontend && npm install && npm run dev`
- API docs: `http://localhost:8000/api/docs`

## Important
This package is **deployment-configured, not production-certified**. The supplied implementation contains incomplete modules and some integration inconsistencies; check `IMPLEMENTATION-NOTES.md` and complete the acceptance tests before using real trainee records. Do not expose the Supabase service-role key in frontend variables.
# tvet2026
