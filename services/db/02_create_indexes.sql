-- BHIV HR Platform - Database Indexes
-- Performance optimization indexes for all tables

-- Candidates table indexes
CREATE INDEX CONCURRENTLY idx_candidates_email ON candidates(email) WHERE email IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_candidates_status ON candidates(status);
CREATE INDEX CONCURRENTLY idx_candidates_experience ON candidates(experience_years);
CREATE INDEX CONCURRENTLY idx_candidates_location ON candidates(location) WHERE location IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_candidates_skills_gin ON candidates USING gin(to_tsvector('english', technical_skills));
CREATE INDEX CONCURRENTLY idx_candidates_created_at ON candidates(created_at);
CREATE INDEX CONCURRENTLY idx_candidates_updated_at ON candidates(updated_at);
CREATE INDEX CONCURRENTLY idx_candidates_uuid ON candidates(uuid);

-- Jobs table indexes
CREATE INDEX CONCURRENTLY idx_jobs_status ON jobs(status);
CREATE INDEX CONCURRENTLY idx_jobs_client_id ON jobs(client_id);
CREATE INDEX CONCURRENTLY idx_jobs_department ON jobs(department);
CREATE INDEX CONCURRENTLY idx_jobs_location ON jobs(location) WHERE location IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX CONCURRENTLY idx_jobs_employment_type ON jobs(employment_type);
CREATE INDEX CONCURRENTLY idx_jobs_salary_range ON jobs(salary_min, salary_max) WHERE salary_min IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_jobs_deadline ON jobs(application_deadline) WHERE application_deadline IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_jobs_created_at ON jobs(created_at);
CREATE INDEX CONCURRENTLY idx_jobs_title_gin ON jobs USING gin(to_tsvector('english', title));
CREATE INDEX CONCURRENTLY idx_jobs_description_gin ON jobs USING gin(to_tsvector('english', description));
CREATE INDEX CONCURRENTLY idx_jobs_skills_gin ON jobs USING gin(skills_required);
CREATE INDEX CONCURRENTLY idx_jobs_uuid ON jobs(uuid);

-- Job applications table indexes
CREATE INDEX CONCURRENTLY idx_job_applications_candidate_id ON job_applications(candidate_id);
CREATE INDEX CONCURRENTLY idx_job_applications_job_id ON job_applications(job_id);
CREATE INDEX CONCURRENTLY idx_job_applications_status ON job_applications(status);
CREATE INDEX CONCURRENTLY idx_job_applications_date ON job_applications(application_date);
CREATE INDEX CONCURRENTLY idx_job_applications_candidate_job ON job_applications(candidate_id, job_id);
CREATE INDEX CONCURRENTLY idx_job_applications_uuid ON job_applications(uuid);

-- Interviews table indexes
CREATE INDEX CONCURRENTLY idx_interviews_candidate_id ON interviews(candidate_id);
CREATE INDEX CONCURRENTLY idx_interviews_job_id ON interviews(job_id);
CREATE INDEX CONCURRENTLY idx_interviews_application_id ON interviews(application_id) WHERE application_id IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_interviews_date ON interviews(interview_date);
CREATE INDEX CONCURRENTLY idx_interviews_status ON interviews(status);
CREATE INDEX CONCURRENTLY idx_interviews_type ON interviews(interview_type);
CREATE INDEX CONCURRENTLY idx_interviews_interviewer ON interviews(interviewer_name);
CREATE INDEX CONCURRENTLY idx_interviews_candidate_job ON interviews(candidate_id, job_id);
CREATE INDEX CONCURRENTLY idx_interviews_upcoming ON interviews(interview_date, status) WHERE status IN ('scheduled', 'in_progress');
CREATE INDEX CONCURRENTLY idx_interviews_uuid ON interviews(uuid);

-- Feedback table indexes
CREATE INDEX CONCURRENTLY idx_feedback_candidate_id ON feedback(candidate_id);
CREATE INDEX CONCURRENTLY idx_feedback_job_id ON feedback(job_id);
CREATE INDEX CONCURRENTLY idx_feedback_interview_id ON feedback(interview_id) WHERE interview_id IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_feedback_overall_score ON feedback(overall_score) WHERE overall_score IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_feedback_recommendation ON feedback(recommendation) WHERE recommendation IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_feedback_evaluator ON feedback(evaluator_name);
CREATE INDEX CONCURRENTLY idx_feedback_created_at ON feedback(created_at);
CREATE INDEX CONCURRENTLY idx_feedback_candidate_job ON feedback(candidate_id, job_id);
CREATE INDEX CONCURRENTLY idx_feedback_uuid ON feedback(uuid);

-- Client auth table indexes
CREATE INDEX CONCURRENTLY idx_client_auth_client_id ON client_auth(client_id);
CREATE INDEX CONCURRENTLY idx_client_auth_email ON client_auth(email);
CREATE INDEX CONCURRENTLY idx_client_auth_active ON client_auth(is_active);
CREATE INDEX CONCURRENTLY idx_client_auth_subscription ON client_auth(subscription_tier);
CREATE INDEX CONCURRENTLY idx_client_auth_company ON client_auth(company_name);
CREATE INDEX CONCURRENTLY idx_client_auth_last_login ON client_auth(last_login) WHERE last_login IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_client_auth_locked ON client_auth(locked_until) WHERE locked_until IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_client_auth_uuid ON client_auth(uuid);

-- Client sessions table indexes
CREATE INDEX CONCURRENTLY idx_client_sessions_client_id ON client_sessions(client_id);
CREATE INDEX CONCURRENTLY idx_client_sessions_token ON client_sessions(token_hash);
CREATE INDEX CONCURRENTLY idx_client_sessions_expires ON client_sessions(expires_at);
CREATE INDEX CONCURRENTLY idx_client_sessions_active ON client_sessions(client_id, expires_at, is_revoked) WHERE is_revoked = false;
CREATE INDEX CONCURRENTLY idx_client_sessions_ip ON client_sessions(ip_address) WHERE ip_address IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_client_sessions_uuid ON client_sessions(uuid);

-- Audit log table indexes
CREATE INDEX CONCURRENTLY idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX CONCURRENTLY idx_audit_log_action ON audit_log(action);
CREATE INDEX CONCURRENTLY idx_audit_log_changed_by ON audit_log(changed_by) WHERE changed_by IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX CONCURRENTLY idx_audit_log_ip ON audit_log(ip_address) WHERE ip_address IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_audit_log_uuid ON audit_log(uuid);

-- System config table indexes
CREATE INDEX CONCURRENTLY idx_system_config_key ON system_config(key);
CREATE INDEX CONCURRENTLY idx_system_config_encrypted ON system_config(is_encrypted);

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY idx_candidates_active_experience ON candidates(status, experience_years) WHERE status = 'active';
CREATE INDEX CONCURRENTLY idx_jobs_active_client ON jobs(status, client_id) WHERE status = 'active';
CREATE INDEX CONCURRENTLY idx_interviews_upcoming_by_date ON interviews(interview_date, status, candidate_id) WHERE status IN ('scheduled', 'in_progress');
CREATE INDEX CONCURRENTLY idx_feedback_high_scores ON feedback(overall_score DESC, candidate_id) WHERE overall_score >= 4.0;

-- Partial indexes for performance
CREATE INDEX CONCURRENTLY idx_candidates_with_resume ON candidates(id) WHERE resume_path IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_jobs_with_salary ON jobs(id, salary_min, salary_max) WHERE salary_min IS NOT NULL;
CREATE INDEX CONCURRENTLY idx_interviews_with_assessment ON interviews(id, assessment_score) WHERE technical_assessment = true;

-- Full-text search indexes
CREATE INDEX CONCURRENTLY idx_candidates_fulltext ON candidates USING gin(
    to_tsvector('english', 
        COALESCE(name, '') || ' ' || 
        COALESCE(technical_skills, '') || ' ' || 
        COALESCE(soft_skills, '') || ' ' ||
        COALESCE(education_level, '')
    )
);

CREATE INDEX CONCURRENTLY idx_jobs_fulltext ON jobs USING gin(
    to_tsvector('english', 
        COALESCE(title, '') || ' ' || 
        COALESCE(description, '') || ' ' || 
        COALESCE(requirements, '') || ' ' ||
        COALESCE(responsibilities, '')
    )
);