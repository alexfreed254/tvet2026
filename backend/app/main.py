from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import app.models  # register all SQLAlchemy models before metadata creation
from app.routers import (
    auth, institutions, departments, courses, classes,
    units, users, trainees, assessments, sessions,
    marking, evidence, verification, marksheet, reports, documents
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TVET e-ASSESS API",
    description="Digital Practical Assessment Platform for TVET Institutions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(institutions.router, prefix="/api/v1/institutions", tags=["Institutions"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["Departments"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(classes.router, prefix="/api/v1/classes", tags=["Classes"])
app.include_router(units.router, prefix="/api/v1/units", tags=["Units"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(trainees.router, prefix="/api/v1/trainees", tags=["Trainees"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["Assessment Sessions"])
app.include_router(marking.router, prefix="/api/v1/marking", tags=["Marking"])
app.include_router(evidence.router, prefix="/api/v1/evidence", tags=["Evidence"])
app.include_router(verification.router, prefix="/api/v1/verification", tags=["Verification"])
app.include_router(marksheet.router, prefix="/api/v1/marksheet", tags=["Marksheet"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "TVET e-ASSESS API", "version": "1.0.0"}


@app.get("/")
def root():
    return {"message": "TVET e-ASSESS — Digital Practical Assessment Platform", "docs": "/api/docs"}
