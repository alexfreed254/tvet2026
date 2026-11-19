COMPETENCY_LEVELS = {
    'not_yet_competent': {'label': 'Not Yet Competent', 'min_percentage': 0, 'color': 'red'},
    'competent': {'label': 'Competent', 'min_percentage': 50, 'color': 'green'},
    'proficient': {'label': 'Proficient', 'min_percentage': 70, 'color': 'blue'},
    'mastery': {'label': 'Mastery', 'min_percentage': 80, 'color': 'purple'},
}

ASSESSMENT_TYPES = ['oral', 'practical']
ASSESSMENT_STATUSES = ['draft', 'preview', 'published', 'withdrawn', 'archived']
SESSION_STATUSES = ['in_progress', 'submitted', 'verified', 'returned', 'rejected', 'approved']
USER_ROLES = ['super_admin', 'hod', 'trainer', 'assessor', 'internal_verifier', 'external_verifier', 'trainee', 'management']
