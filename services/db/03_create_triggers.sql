-- BHIV HR Platform - Database Triggers
-- Audit trails and automatic updates for all tables

-- Function to update the updated_at timestamp
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
                COALESCE(inet_client_addr(), '127.0.0.1'));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by, ip_address)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW),
                COALESCE(current_setting('app.current_user', true), 'system'),
                COALESCE(inet_client_addr(), '127.0.0.1'));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_values, changed_by, ip_address)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW),
                COALESCE(current_setting('app.current_user', true), 'system'),
                COALESCE(inet_client_addr(), '127.0.0.1'));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Updated_at triggers for all tables with updated_at column
CREATE TRIGGER update_candidates_updated_at 
    BEFORE UPDATE ON candidates 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at 
    BEFORE UPDATE ON jobs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_applications_updated_at 
    BEFORE UPDATE ON job_applications 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_interviews_updated_at 
    BEFORE UPDATE ON interviews 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_feedback_updated_at 
    BEFORE UPDATE ON feedback 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_client_auth_updated_at 
    BEFORE UPDATE ON client_auth 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_config_updated_at 
    BEFORE UPDATE ON system_config 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Audit triggers for all main tables
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

-- Function to clean up expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM client_sessions 
    WHERE expires_at < CURRENT_TIMESTAMP 
    OR is_revoked = true;
END;
$$ LANGUAGE plpgsql;

-- Function to handle failed login attempts
CREATE OR REPLACE FUNCTION handle_failed_login()
RETURNS TRIGGER AS $$
BEGIN
    -- Increment login attempts
    NEW.login_attempts = COALESCE(OLD.login_attempts, 0) + 1;
    
    -- Lock account after 5 failed attempts for 30 minutes
    IF NEW.login_attempts >= 5 THEN
        NEW.locked_until = CURRENT_TIMESTAMP + INTERVAL '30 minutes';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to handle successful login
CREATE OR REPLACE FUNCTION handle_successful_login()
RETURNS TRIGGER AS $$
BEGIN
    -- Reset login attempts and unlock account
    NEW.login_attempts = 0;
    NEW.locked_until = NULL;
    NEW.last_login = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to validate email format
CREATE OR REPLACE FUNCTION validate_email_format()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email IS NOT NULL AND NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Email validation triggers
CREATE TRIGGER validate_candidate_email
    BEFORE INSERT OR UPDATE ON candidates
    FOR EACH ROW EXECUTE FUNCTION validate_email_format();

CREATE TRIGGER validate_client_email
    BEFORE INSERT OR UPDATE ON client_auth
    FOR EACH ROW EXECUTE FUNCTION validate_email_format();

-- Function to update job application status based on interview results
CREATE OR REPLACE FUNCTION update_application_status_from_interview()
RETURNS TRIGGER AS $$
BEGIN
    -- Update application status based on interview status
    IF NEW.status = 'completed' AND NEW.recommendation IN ('strong_hire', 'hire') THEN
        UPDATE job_applications 
        SET status = 'offered' 
        WHERE candidate_id = NEW.candidate_id AND job_id = NEW.job_id;
    ELSIF NEW.status = 'completed' AND NEW.recommendation IN ('no_hire', 'strong_no_hire') THEN
        UPDATE job_applications 
        SET status = 'rejected' 
        WHERE candidate_id = NEW.candidate_id AND job_id = NEW.job_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update application status from interview results
CREATE TRIGGER update_application_from_interview
    AFTER UPDATE ON interviews
    FOR EACH ROW 
    WHEN (NEW.status = 'completed' AND NEW.recommendation IS NOT NULL)
    EXECUTE FUNCTION update_application_status_from_interview();

-- Function to prevent deletion of active records
CREATE OR REPLACE FUNCTION prevent_active_record_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status = 'active' THEN
        RAISE EXCEPTION 'Cannot delete active record. Please set status to inactive first.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Prevent deletion of active candidates and jobs
CREATE TRIGGER prevent_active_candidate_deletion
    BEFORE DELETE ON candidates
    FOR EACH ROW EXECUTE FUNCTION prevent_active_record_deletion();

CREATE TRIGGER prevent_active_job_deletion
    BEFORE DELETE ON jobs
    FOR EACH ROW EXECUTE FUNCTION prevent_active_record_deletion();

-- Function to validate salary ranges
CREATE OR REPLACE FUNCTION validate_salary_range()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary_min IS NOT NULL AND NEW.salary_max IS NOT NULL THEN
        IF NEW.salary_min > NEW.salary_max THEN
            RAISE EXCEPTION 'Minimum salary cannot be greater than maximum salary';
        END IF;
        IF NEW.salary_min < 0 OR NEW.salary_max < 0 THEN
            RAISE EXCEPTION 'Salary values cannot be negative';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Salary validation triggers
CREATE TRIGGER validate_job_salary_range
    BEFORE INSERT OR UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION validate_salary_range();

CREATE TRIGGER validate_candidate_salary_range
    BEFORE INSERT OR UPDATE ON candidates
    FOR EACH ROW 
    WHEN (NEW.salary_expectation_min IS NOT NULL OR NEW.salary_expectation_max IS NOT NULL)
    EXECUTE FUNCTION validate_salary_range();

-- Function to automatically set interview application_id
CREATE OR REPLACE FUNCTION set_interview_application_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Automatically set application_id if not provided
    IF NEW.application_id IS NULL THEN
        SELECT id INTO NEW.application_id 
        FROM job_applications 
        WHERE candidate_id = NEW.candidate_id AND job_id = NEW.job_id
        LIMIT 1;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set interview application_id
CREATE TRIGGER set_interview_application_id_trigger
    BEFORE INSERT ON interviews
    FOR EACH ROW EXECUTE FUNCTION set_interview_application_id();

-- Function to validate interview scheduling
CREATE OR REPLACE FUNCTION validate_interview_scheduling()
RETURNS TRIGGER AS $$
BEGIN
    -- Prevent scheduling interviews in the past
    IF NEW.interview_date < CURRENT_TIMESTAMP THEN
        RAISE EXCEPTION 'Cannot schedule interview in the past';
    END IF;
    
    -- Prevent double-booking (same interviewer, overlapping time)
    IF EXISTS (
        SELECT 1 FROM interviews 
        WHERE interviewer_name = NEW.interviewer_name 
        AND status IN ('scheduled', 'in_progress')
        AND id != COALESCE(NEW.id, 0)
        AND (
            (interview_date <= NEW.interview_date AND 
             interview_date + INTERVAL '1 minute' * duration_minutes > NEW.interview_date)
            OR
            (NEW.interview_date <= interview_date AND 
             NEW.interview_date + INTERVAL '1 minute' * COALESCE(NEW.duration_minutes, 60) > interview_date)
        )
    ) THEN
        RAISE EXCEPTION 'Interviewer % is already scheduled for an overlapping time slot', NEW.interviewer_name;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Interview scheduling validation trigger
CREATE TRIGGER validate_interview_scheduling_trigger
    BEFORE INSERT OR UPDATE ON interviews
    FOR EACH ROW EXECUTE FUNCTION validate_interview_scheduling();