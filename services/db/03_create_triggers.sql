-- BHIV HR Platform - Database Triggers
-- Automated triggers for audit logging and data consistency

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, changed_by, ip_address)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, row_to_json(OLD), 
                COALESCE(current_setting('app.current_user', true), 'system'),
                COALESCE(current_setting('app.client_ip', true)::inet, NULL));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by, ip_address)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW),
                COALESCE(current_setting('app.current_user', true), 'system'),
                COALESCE(current_setting('app.client_ip', true)::inet, NULL));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values, changed_by, ip_address)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW),
                COALESCE(current_setting('app.current_user', true), 'system'),
                COALESCE(current_setting('app.client_ip', true)::inet, NULL));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Function to validate email format
CREATE OR REPLACE FUNCTION validate_email(email_address TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN email_address ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
END;
$$ LANGUAGE plpgsql;

-- Function to validate phone format
CREATE OR REPLACE FUNCTION validate_phone(phone_number TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN phone_number ~ '^\+?[1-9]\d{1,14}$';
END;
$$ LANGUAGE plpgsql;

-- Function to clean and normalize text fields
CREATE OR REPLACE FUNCTION normalize_text(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    IF input_text IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN trim(regexp_replace(input_text, '\s+', ' ', 'g'));
END;
$$ LANGUAGE plpgsql;

-- Trigger to normalize candidate data
CREATE OR REPLACE FUNCTION normalize_candidate_data()
RETURNS TRIGGER AS $$
BEGIN
    NEW.name = normalize_text(NEW.name);
    NEW.location = normalize_text(NEW.location);
    NEW.technical_skills = normalize_text(NEW.technical_skills);
    NEW.soft_skills = normalize_text(NEW.soft_skills);
    NEW.education_level = normalize_text(NEW.education_level);
    
    -- Validate email if provided
    IF NEW.email IS NOT NULL AND NOT validate_email(NEW.email) THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    
    -- Validate phone if provided
    IF NEW.phone IS NOT NULL AND NOT validate_phone(NEW.phone) THEN
        RAISE EXCEPTION 'Invalid phone format: %', NEW.phone;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to normalize job data
CREATE OR REPLACE FUNCTION normalize_job_data()
RETURNS TRIGGER AS $$
BEGIN
    NEW.title = normalize_text(NEW.title);
    NEW.department = normalize_text(NEW.department);
    NEW.location = normalize_text(NEW.location);
    NEW.requirements = normalize_text(NEW.requirements);
    NEW.description = normalize_text(NEW.description);
    NEW.responsibilities = normalize_text(NEW.responsibilities);
    NEW.benefits = normalize_text(NEW.benefits);
    NEW.hiring_manager = normalize_text(NEW.hiring_manager);
    NEW.hr_contact = normalize_text(NEW.hr_contact);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to validate interview scheduling
CREATE OR REPLACE FUNCTION validate_interview_scheduling()
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure interview date is in the future for new interviews
    IF TG_OP = 'INSERT' AND NEW.interview_date <= CURRENT_TIMESTAMP THEN
        RAISE EXCEPTION 'Interview date must be in the future';
    END IF;
    
    -- Normalize interviewer data
    NEW.interviewer_name = normalize_text(NEW.interviewer_name);
    NEW.interviewer_role = normalize_text(NEW.interviewer_role);
    NEW.location = normalize_text(NEW.location);
    
    -- Validate interviewer email if provided
    IF NEW.interviewer_email IS NOT NULL AND NOT validate_email(NEW.interviewer_email) THEN
        RAISE EXCEPTION 'Invalid interviewer email format: %', NEW.interviewer_email;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to validate feedback scores
CREATE OR REPLACE FUNCTION validate_feedback_scores()
RETURNS TRIGGER AS $$
BEGIN
    -- Normalize evaluator data
    NEW.evaluator_name = normalize_text(NEW.evaluator_name);
    NEW.evaluator_role = normalize_text(NEW.evaluator_role);
    NEW.strengths = normalize_text(NEW.strengths);
    NEW.areas_for_improvement = normalize_text(NEW.areas_for_improvement);
    NEW.additional_comments = normalize_text(NEW.additional_comments);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to manage client authentication
CREATE OR REPLACE FUNCTION manage_client_auth()
RETURNS TRIGGER AS $$
BEGIN
    -- Normalize company data
    NEW.company_name = normalize_text(NEW.company_name);
    NEW.industry = normalize_text(NEW.industry);
    
    -- Validate email
    IF NOT validate_email(NEW.email) THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    
    -- Validate phone if provided
    IF NEW.phone IS NOT NULL AND NOT validate_phone(NEW.phone) THEN
        RAISE EXCEPTION 'Invalid phone format: %', NEW.phone;
    END IF;
    
    -- Reset login attempts on successful login
    IF TG_OP = 'UPDATE' AND OLD.last_login IS DISTINCT FROM NEW.last_login THEN
        NEW.login_attempts = 0;
        NEW.locked_until = NULL;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create updated_at triggers for all tables
CREATE TRIGGER update_candidates_updated_at BEFORE UPDATE ON candidates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_applications_updated_at BEFORE UPDATE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_interviews_updated_at BEFORE UPDATE ON interviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feedback_updated_at BEFORE UPDATE ON feedback
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_client_auth_updated_at BEFORE UPDATE ON client_auth
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_config_updated_at BEFORE UPDATE ON system_config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create audit triggers for all main tables
CREATE TRIGGER audit_candidates_trigger
    AFTER INSERT OR UPDATE OR DELETE ON candidates
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_jobs_trigger
    AFTER INSERT OR UPDATE OR DELETE ON jobs
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_job_applications_trigger
    AFTER INSERT OR UPDATE OR DELETE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_interviews_trigger
    AFTER INSERT OR UPDATE OR DELETE ON interviews
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_feedback_trigger
    AFTER INSERT OR UPDATE OR DELETE ON feedback
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_client_auth_trigger
    AFTER INSERT OR UPDATE OR DELETE ON client_auth
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Create data validation triggers
CREATE TRIGGER normalize_candidate_data_trigger
    BEFORE INSERT OR UPDATE ON candidates
    FOR EACH ROW EXECUTE FUNCTION normalize_candidate_data();

CREATE TRIGGER normalize_job_data_trigger
    BEFORE INSERT OR UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION normalize_job_data();

CREATE TRIGGER validate_interview_scheduling_trigger
    BEFORE INSERT OR UPDATE ON interviews
    FOR EACH ROW EXECUTE FUNCTION validate_interview_scheduling();

CREATE TRIGGER validate_feedback_scores_trigger
    BEFORE INSERT OR UPDATE ON feedback
    FOR EACH ROW EXECUTE FUNCTION validate_feedback_scores();

CREATE TRIGGER manage_client_auth_trigger
    BEFORE INSERT OR UPDATE ON client_auth
    FOR EACH ROW EXECUTE FUNCTION manage_client_auth();