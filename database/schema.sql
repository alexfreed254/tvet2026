-- ============================================================
-- TVET e-ASSESS — COMPLETE DATABASE SCHEMA
-- Run this in Supabase SQL Editor
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. INSTITUTIONS
CREATE TABLE IF NOT EXISTS institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(100),
    logo_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. DEPARTMENTS
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID REFERENCES institutions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    hod_user_id UUID,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(institution_id, code)
);

-- 3. COURSES
CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID REFERENCES departments(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    qualification_level VARCHAR(50),
    duration_months INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(department_id, code)
);

-- 4. CLASSES
CREATE TABLE IF NOT EXISTS classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    intake_year INTEGER,
    cycle INTEGER,
    level INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(course_id, name)
);

-- 5. UNITS
CREATE TABLE IF NOT EXISTS units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    code VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    credit_hours INTEGER,
    level INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(course_id, code)
);

-- 6. USERS
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    institution_id UUID REFERENCES institutions(id),
    department_id UUID REFERENCES departments(id),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    staff_number VARCHAR(50),
    role VARCHAR(50) NOT NULL CHECK (role IN (
        'super_admin', 'hod', 'trainer', 'assessor',
        'internal_verifier', 'external_verifier', 'trainee', 'management'
    )),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. TRAINEES
CREATE TABLE IF NOT EXISTS trainees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    class_id UUID REFERENCES classes(id) ON DELETE CASCADE,
    admission_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    national_id VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(255),
    enrollment_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'graduated', 'dropped', 'transferred')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. TRAINER ALLOCATIONS
CREATE TABLE IF NOT EXISTS trainer_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trainer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    class_id UUID REFERENCES classes(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES units(id) ON DELETE CASCADE,
    academic_year INTEGER NOT NULL,
    term INTEGER NOT NULL CHECK (term IN (1, 2, 3)),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(trainer_id, class_id, unit_id, academic_year, term)
);

-- 9. ACADEMIC PERIODS
CREATE TABLE IF NOT EXISTS academic_periods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID REFERENCES institutions(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    term INTEGER NOT NULL CHECK (term IN (1, 2, 3)),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(institution_id, year, term)
);

-- 10. ASSESSMENTS
CREATE TABLE IF NOT EXISTS assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID REFERENCES institutions(id) ON DELETE CASCADE,
    department_id UUID REFERENCES departments(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    class_id UUID REFERENCES classes(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES units(id) ON DELETE CASCADE,
    academic_period_id UUID REFERENCES academic_periods(id),
    title VARCHAR(255) NOT NULL,
    assessment_number VARCHAR(50) NOT NULL,
    assessment_type VARCHAR(20) NOT NULL CHECK (assessment_type IN ('oral', 'practical')),
    assessment_level VARCHAR(20),
    instructions TEXT,
    duration_minutes INTEGER,
    total_marks INTEGER,
    passing_percentage DECIMAL(5,2) DEFAULT 50.00,
    required_tools TEXT,
    required_equipment TEXT,
    required_materials TEXT,
    safety_precautions TEXT,
    ppe_requirements TEXT,
    marking_guidelines TEXT,
    reference_documents TEXT,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN (
        'draft', 'preview', 'published', 'withdrawn', 'archived'
    )),
    version INTEGER DEFAULT 1,
    published_at TIMESTAMPTZ,
    deadline TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(class_id, unit_id, assessment_number, academic_period_id, version)
);

-- 11. ASSESSMENT TASKS
CREATE TABLE IF NOT EXISTS assessment_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    task_number INTEGER NOT NULL,
    task_title VARCHAR(255) NOT NULL,
    task_description TEXT,
    max_marks INTEGER NOT NULL DEFAULT 0,
    task_type VARCHAR(30) DEFAULT 'practical' CHECK (task_type IN (
        'practical', 'oral', 'theory', 'observation', 'continuous_test'
    )),
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. CHECKLIST CRITERIA
CREATE TABLE IF NOT EXISTS checklist_criteria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    task_id UUID REFERENCES assessment_tasks(id) ON DELETE CASCADE,
    criterion_number VARCHAR(20),
    criterion_text TEXT NOT NULL,
    sub_criterion_text TEXT,
    max_marks INTEGER NOT NULL DEFAULT 0,
    scoring_type VARCHAR(20) DEFAULT 'numerical' CHECK (scoring_type IN (
        'binary', 'numerical', 'award_max'
    )),
    award_max INTEGER,
    binary_pass_mark INTEGER DEFAULT 1,
    display_order INTEGER DEFAULT 0,
    is_sub_total BOOLEAN DEFAULT FALSE,
    is_grand_total BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. ASSESSMENT SESSIONS
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    trainee_id UUID REFERENCES trainees(id) ON DELETE CASCADE,
    assessor_id UUID REFERENCES users(id),
    session_number INTEGER DEFAULT 1,
    assessment_date DATE,
    assessment_venue VARCHAR(255),
    academic_period_id UUID REFERENCES academic_periods(id),
    total_marks_available INTEGER DEFAULT 0,
    total_marks_obtained DECIMAL(10,2) DEFAULT 0,
    percentage_score DECIMAL(5,2) DEFAULT 0,
    competency_outcome VARCHAR(30) CHECK (competency_outcome IN (
        'competent', 'not_yet_competent', 'proficient', 'mastery', 'pending'
    )) DEFAULT 'pending',
    assessor_comments TEXT,
    feedback_to_candidate TEXT,
    status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN (
        'in_progress', 'submitted', 'verified', 'returned', 'rejected', 'approved'
    )),
    submitted_at TIMESTAMPTZ,
    verified_at TIMESTAMPTZ,
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(assessment_id, trainee_id, session_number)
);

-- 14. CRITERION RESULTS
CREATE TABLE IF NOT EXISTS criterion_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    criterion_id UUID REFERENCES checklist_criteria(id) ON DELETE CASCADE,
    marks_available INTEGER NOT NULL,
    marks_obtained DECIMAL(10,2) DEFAULT 0,
    is_competent BOOLEAN,
    assessor_comment TEXT,
    evidence_attached BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_id, criterion_id)
);

-- 15. EVIDENCE FILES
CREATE TABLE IF NOT EXISTS evidence_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    criterion_id UUID REFERENCES checklist_criteria(id),
    uploaded_by UUID REFERENCES users(id),
    original_filename VARCHAR(500) NOT NULL,
    system_filename VARCHAR(500) NOT NULL,
    storage_path TEXT NOT NULL,
    file_type VARCHAR(20) NOT NULL CHECK (file_type IN (
        'photo', 'video', 'audio', 'document', 'scanned'
    )),
    mime_type VARCHAR(100),
    file_size_bytes BIGINT,
    admission_number VARCHAR(50),
    unit_code VARCHAR(50),
    document_type VARCHAR(50),
    assessment_number VARCHAR(50),
    term INTEGER,
    year INTEGER,
    assessed_by_name VARCHAR(200),
    item_reference VARCHAR(50),
    version INTEGER DEFAULT 1,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 16. VERIFICATION RECORDS
CREATE TABLE IF NOT EXISTS verification_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    verifier_id UUID REFERENCES users(id),
    verifier_type VARCHAR(20) NOT NULL CHECK (verifier_type IN ('internal', 'external')),
    decision VARCHAR(20) NOT NULL CHECK (decision IN (
        'approved', 'returned_for_correction', 'rejected'
    )),
    comments TEXT,
    rejection_reasons TEXT,
    verified_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 17. GENERATED DOCUMENTS
CREATE TABLE IF NOT EXISTS generated_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    document_type VARCHAR(30) NOT NULL CHECK (document_type IN (
        'completed_assessment_pdf', 'marksheet_pdf', 'marksheet_excel',
        'marksheet_csv', 'report_pdf'
    )),
    storage_path TEXT NOT NULL,
    system_filename VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 18. AUDIT LOGS
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 19. REASSESSMENT RECORDS
CREATE TABLE IF NOT EXISTS reassessment_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    reassessment_session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    reason TEXT NOT NULL,
    authorized_by UUID REFERENCES users(id),
    authorized_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 20. RESULT CORRECTIONS
CREATE TABLE IF NOT EXISTS result_corrections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    criterion_result_id UUID REFERENCES criterion_results(id),
    old_marks_obtained DECIMAL(10,2),
    new_marks_obtained DECIMAL(10,2),
    reason TEXT NOT NULL,
    requested_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    decided_at TIMESTAMPTZ
);

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_trainees_admission ON trainees(admission_number);
CREATE INDEX IF NOT EXISTS idx_assessments_class ON assessments(class_id);
CREATE INDEX IF NOT EXISTS idx_assessments_unit ON assessments(unit_id);
CREATE INDEX IF NOT EXISTS idx_assessments_status ON assessments(status);
CREATE INDEX IF NOT EXISTS idx_sessions_assessment ON assessment_sessions(assessment_id);
CREATE INDEX IF NOT EXISTS idx_sessions_trainee ON assessment_sessions(trainee_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON assessment_sessions(status);
CREATE INDEX IF NOT EXISTS idx_evidence_session ON evidence_files(session_id);
CREATE INDEX IF NOT EXISTS idx_evidence_trainee ON evidence_files(admission_number);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_trainer_allocations ON trainer_allocations(trainer_id, class_id, unit_id);
CREATE INDEX IF NOT EXISTS idx_verification_session ON verification_records(session_id);

-- AUTO-UPDATE TRIGGER FUNCTION
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_institutions_updated BEFORE UPDATE ON institutions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_departments_updated BEFORE UPDATE ON departments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_users_updated BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_trainees_updated BEFORE UPDATE ON trainees FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_assessments_updated BEFORE UPDATE ON assessments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_sessions_updated BEFORE UPDATE ON assessment_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_criterion_results_updated BEFORE UPDATE ON criterion_results FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ROW LEVEL SECURITY
ALTER TABLE institutions ENABLE ROW LEVEL SECURITY;
ALTER TABLE departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainees ENABLE ROW LEVEL SECURITY;
ALTER TABLE trainer_allocations ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE checklist_criteria ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE criterion_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE verification_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE reassessment_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE result_corrections ENABLE ROW LEVEL SECURITY;

-- RLS POLICIES
CREATE POLICY "institutions_select" ON institutions FOR SELECT TO authenticated USING (is_active = TRUE);
CREATE POLICY "users_select_own" ON users FOR SELECT TO authenticated USING (id = auth.uid());

CREATE POLICY "trainees_select" ON trainees FOR SELECT TO authenticated USING (
    EXISTS (SELECT 1 FROM trainer_allocations ta WHERE ta.class_id = trainees.class_id AND ta.trainer_id = auth.uid())
    OR EXISTS (SELECT 1 FROM users u WHERE u.id = auth.uid() AND u.role IN ('super_admin', 'hod', 'management'))
);

CREATE POLICY "sessions_insert" ON assessment_sessions FOR INSERT TO authenticated WITH CHECK (assessor_id = auth.uid());
CREATE POLICY "sessions_update_own" ON assessment_sessions FOR UPDATE TO authenticated USING (assessor_id = auth.uid());
CREATE POLICY "sessions_select" ON assessment_sessions FOR SELECT TO authenticated USING (
    assessor_id = auth.uid()
    OR EXISTS (SELECT 1 FROM users u WHERE u.id = auth.uid() AND u.role IN ('super_admin', 'hod', 'internal_verifier', 'external_verifier', 'management'))
);

CREATE POLICY "evidence_insert" ON evidence_files FOR INSERT TO authenticated WITH CHECK (uploaded_by = auth.uid());
CREATE POLICY "evidence_select" ON evidence_files FOR SELECT TO authenticated USING (TRUE);

CREATE POLICY "audit_select_admin" ON audit_logs FOR SELECT TO authenticated USING (
    EXISTS (SELECT 1 FROM users u WHERE u.id = auth.uid() AND u.role IN ('super_admin', 'management'))
);

CREATE POLICY "verification_insert" ON verification_records FOR INSERT TO authenticated WITH CHECK (verifier_id = auth.uid());
CREATE POLICY "verification_select" ON verification_records FOR SELECT TO authenticated USING (TRUE);
🐍 BACKEND
