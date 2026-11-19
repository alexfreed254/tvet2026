# Implementation and deployment notes

## Source coverage
- Extracted all explicitly labelled code blocks from the latest uploaded `Pasted text(20261119-091715).txt`.
- Preserved the latest complete uploaded source as `SOURCE-IMPLEMENTATION.txt` and the earlier 08:44 upload as `SOURCE-ORIGINAL-084418.txt`. The 09:16 and 09:17 uploads are identical copies.
- Added small missing files needed for imports and page routing, and a Render Blueprint. These additions are labelled in this document.

## Added or corrected to support build/deploy
- Added minimal frontend route pages where the uploaded `App.tsx` imports pages that were not included as code blocks.
- Added `backend/app/routers/auth.py` as a bridge to the provided authentication router.
- Added the missing SQLAlchemy `AcademicPeriod` model referenced by assessments.
- Fixed `ChecklistCriterion` import in `assessment_service.py` and ensured models are registered before metadata creation.
- Added comma-separated CORS environment parsing and Render static-site API host normalization.
- Added SPA rewrite and Render `render.yaml`.

## Known items requiring completion before production
- The source code references ORM relationships such as `assessment.unit`, `assessment.department`, `assessment.institution`, and `assessment.academic_period` that are not consistently declared in all models. PDF generation and related endpoints need relationship integration tests.
- Some UI controls in the supplied source are demo-level (for example task/checklist editor callbacks); connect them to their API endpoints and validate all required IDs before production.
- Verify every router's permissions and institution/department data isolation. The included SQL RLS policies are a starter set, not a complete security review.
- Test evidence uploads, signed URL downloads, PDF generation, Excel/CSV exports, reassessment/versioning, verification, and marksheet calculations against a real Supabase project.
- Confirm database schema and ORM models remain aligned. Avoid relying on `Base.metadata.create_all()` for production migrations; use controlled SQL migrations.
- The uploaded implementation does not provide a complete admin onboarding workflow. Create the first Supabase Auth user and matching `public.users` row securely.

## Render environment variables
API service: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_URL`, `JWT_SECRET`, `ALLOWED_ORIGINS`, `SUPABASE_STORAGE_BUCKET`, `MAX_FILE_SIZE_MB`, `DEBUG=false`.
Frontend static site: `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_API_BASE_URL` (linked to API service host by `render.yaml`).
