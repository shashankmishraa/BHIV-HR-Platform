-- BHIV HR Platform - Essential DBeaver Queries
-- Quick reference queries for database exploration and monitoring
-- Version: 4.1.0 with Phase 3 Features
-- Updated: October 14, 2025

-- ============================================================================
-- 🔍 SCHEMA VERIFICATION QUERIES
-- ============================================================================

-- Check current schema version
SELECT 
    version,
    applied_at,
    description
FROM schema_version 
ORDER BY applied_at DESC;

-- List all tables with row counts
SELECT 
    schemaname,
    tablename,
    n_live_tup as row_count,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as table_size
FROM pg_stat_user_tables 
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;

-- Verify all expected tables exist
SELECT 
    table_name,
    table_type,
    CASE 
        WHEN table_name IN ('candidates', 'jobs', 'feedback', 'interviews', 'offers', 
                           'users', 'clients', 'matching_cache', 'audit_logs', 
                           'rate_limits', 'csp_violations', 'company_scoring_preferences', 
                           'schema_version') 
        THEN '✅ Core Table'
        ELSE '❓ Additional Table'
    END as table_category
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- ============================================================================
-- 📊 DATA OVERVIEW QUERIES
-- ============================================================================

-- Quick data counts across all tables
SELECT 
    'candidates' as table_name, COUNT(*) as record_count, 
    MAX(created_at) as latest_record FROM candidates
UNION ALL
SELECT 'jobs', COUNT(*), MAX(created_at) FROM jobs
UNION ALL
SELECT 'feedback', COUNT(*), MAX(created_at) FROM feedback
UNION ALL
SELECT 'interviews', COUNT(*), MAX(created_at) FROM interviews
UNION ALL
SELECT 'offers', COUNT(*), MAX(created_at) FROM offers
UNION ALL
SELECT 'users', COUNT(*), MAX(created_at) FROM users
UNION ALL
SELECT 'clients', COUNT(*), MAX(created_at) FROM clients
UNION ALL
SELECT 'audit_logs', COUNT(*), MAX(timestamp) FROM audit_logs
UNION ALL
SELECT 'matching_cache', COUNT(*), MAX(created_at) FROM matching_cache
UNION ALL
SELECT 'rate_limits', COUNT(*), MAX(window_start) FROM rate_limits
ORDER BY record_count DESC;

-- Database health summary
SELECT 
    pg_database.datname as database_name,
    pg_size_pretty(pg_database_size(pg_database.datname)) as database_size,
    (SELECT count(*) FROM pg_stat_activity WHERE datname = pg_database.datname) as active_connections
FROM pg_database 
WHERE datname IN ('bhiv_hr', 'bhiv_hr_jcuu');

-- ============================================================================
-- 👥 CANDIDATES DATA EXPLORATION
-- ============================================================================

-- Recent candidates with complete profile
SELECT 
    c.id,
    c.name,
    c.email,
    c.location,
    c.experience_years,
    c.seniority_level,
    c.average_score,
    c.status,
    c.created_at,
    COUNT(f.id) as feedback_count,
    COUNT(i.id) as interview_count,
    COUNT(o.id) as offer_count
FROM candidates c
LEFT JOIN feedback f ON c.id = f.candidate_id
LEFT JOIN interviews i ON c.id = i.candidate_id
LEFT JOIN offers o ON c.id = o.candidate_id
GROUP BY c.id, c.name, c.email, c.location, c.experience_years, c.seniority_level, c.average_score, c.status, c.created_at
ORDER BY c.created_at DESC
LIMIT 20;

-- Top candidates by average score
SELECT 
    c.name,
    c.email,
    c.location,
    c.experience_years,
    c.technical_skills,
    c.average_score,
    COUNT(f.id) as total_feedback
FROM candidates c
LEFT JOIN feedback f ON c.id = f.candidate_id
WHERE c.average_score > 0
GROUP BY c.id, c.name, c.email, c.location, c.experience_years, c.technical_skills, c.average_score
ORDER BY c.average_score DESC, total_feedback DESC
LIMIT 15;

-- Candidates by location distribution
SELECT 
    location,
    COUNT(*) as candidate_count,
    AVG(experience_years) as avg_experience,
    AVG(average_score) as avg_score
FROM candidates 
WHERE location IS NOT NULL
GROUP BY location
ORDER BY candidate_count DESC;

-- ============================================================================
-- 💼 JOBS AND CLIENT DATA
-- ============================================================================

-- Active jobs with client information
SELECT 
    j.id,
    j.title,
    j.department,
    j.location,
    j.experience_level,
    j.employment_type,
    c.company_name,
    c.client_id,
    j.status,
    j.created_at,
    (SELECT COUNT(*) FROM feedback f WHERE f.job_id = j.id) as applications
FROM jobs j
LEFT JOIN clients c ON j.client_id = c.client_id
WHERE j.status = 'active'
ORDER BY j.created_at DESC;

-- Jobs by department and status
SELECT 
    department,
    status,
    COUNT(*) as job_count,
    AVG(CASE WHEN created_at > CURRENT_DATE - INTERVAL '30 days' THEN 1 ELSE 0 END) * 100 as recent_percentage
FROM jobs
GROUP BY department, status
ORDER BY department, status;

-- Client activity summary
SELECT 
    c.client_id,
    c.company_name,
    c.status as client_status,
    COUNT(j.id) as total_jobs,
    COUNT(CASE WHEN j.status = 'active' THEN 1 END) as active_jobs,
    MAX(j.created_at) as latest_job_posted
FROM clients c
LEFT JOIN jobs j ON c.client_id = j.client_id
GROUP BY c.client_id, c.company_name, c.status
ORDER BY total_jobs DESC;

-- ============================================================================
-- 📝 FEEDBACK AND VALUES ASSESSMENT
-- ============================================================================

-- Values assessment overview
SELECT 
    AVG(integrity) as avg_integrity,
    AVG(honesty) as avg_honesty,
    AVG(discipline) as avg_discipline,
    AVG(hard_work) as avg_hard_work,
    AVG(gratitude) as avg_gratitude,
    AVG(average_score) as overall_avg_score,
    COUNT(*) as total_assessments
FROM feedback;

-- Top performers by BHIV values
SELECT 
    c.name,
    c.email,
    f.integrity,
    f.honesty,
    f.discipline,
    f.hard_work,
    f.gratitude,
    f.average_score,
    j.title as job_title,
    f.reviewer_name,
    f.created_at
FROM feedback f
JOIN candidates c ON f.candidate_id = c.id
JOIN jobs j ON f.job_id = j.id
WHERE f.average_score >= 4.0
ORDER BY f.average_score DESC, f.created_at DESC
LIMIT 20;

-- Feedback distribution by score ranges
SELECT 
    CASE 
        WHEN average_score >= 4.5 THEN '⭐ Excellent (4.5-5.0)'
        WHEN average_score >= 4.0 THEN '🌟 Very Good (4.0-4.4)'
        WHEN average_score >= 3.5 THEN '✨ Good (3.5-3.9)'
        WHEN average_score >= 3.0 THEN '📈 Average (3.0-3.4)'
        ELSE '📉 Below Average (<3.0)'
    END as score_range,
    COUNT(*) as feedback_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM feedback), 2) as percentage
FROM feedback
GROUP BY 
    CASE 
        WHEN average_score >= 4.5 THEN '⭐ Excellent (4.5-5.0)'
        WHEN average_score >= 4.0 THEN '🌟 Very Good (4.0-4.4)'
        WHEN average_score >= 3.5 THEN '✨ Good (3.5-3.9)'
        WHEN average_score >= 3.0 THEN '📈 Average (3.0-3.4)'
        ELSE '📉 Below Average (<3.0)'
    END
ORDER BY MIN(average_score) DESC;

-- ============================================================================
-- 🤖 AI MATCHING AND PERFORMANCE
-- ============================================================================

-- AI matching cache performance
SELECT 
    algorithm_version,
    COUNT(*) as cached_matches,
    AVG(match_score) as avg_match_score,
    MAX(match_score) as best_match_score,
    MIN(created_at) as first_cached,
    MAX(created_at) as last_cached
FROM matching_cache
GROUP BY algorithm_version
ORDER BY last_cached DESC;

-- Top AI matches by job
SELECT 
    j.title as job_title,
    c.name as candidate_name,
    c.email,
    mc.match_score,
    mc.skills_match_score,
    mc.experience_match_score,
    mc.location_match_score,
    mc.algorithm_version,
    mc.created_at
FROM matching_cache mc
JOIN jobs j ON mc.job_id = j.id
JOIN candidates c ON mc.candidate_id = c.id
WHERE mc.match_score >= 80
ORDER BY mc.match_score DESC, mc.created_at DESC
LIMIT 25;

-- Phase 3 learning engine data
SELECT 
    cl.company_name,
    csp.scoring_weights,
    csp.avg_satisfaction,
    csp.feedback_count,
    csp.preferred_experience,
    csp.updated_at
FROM company_scoring_preferences csp
JOIN clients cl ON csp.client_id = cl.client_id
ORDER BY csp.updated_at DESC;

-- ============================================================================
-- 🔒 SECURITY AND AUDIT QUERIES
-- ============================================================================

-- Recent audit activity
SELECT 
    al.action,
    al.resource,
    al.resource_id,
    COALESCE(u.username, al.client_id) as actor,
    al.ip_address,
    al.success,
    al.error_message,
    al.timestamp
FROM audit_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.timestamp DESC
LIMIT 50;

-- Security events summary
SELECT 
    DATE(timestamp) as date,
    action,
    success,
    COUNT(*) as event_count
FROM audit_logs
WHERE timestamp >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(timestamp), action, success
ORDER BY date DESC, event_count DESC;

-- Rate limiting status
SELECT 
    ip_address,
    endpoint,
    user_tier,
    request_count,
    window_start,
    blocked_until,
    CASE 
        WHEN blocked_until > CURRENT_TIMESTAMP THEN '🚫 Blocked'
        WHEN request_count > 50 THEN '⚠️ High Usage'
        ELSE '✅ Normal'
    END as status
FROM rate_limits
ORDER BY request_count DESC, window_start DESC;

-- User authentication status
SELECT 
    username,
    email,
    role,
    is_2fa_enabled,
    status,
    last_login,
    failed_login_attempts,
    CASE 
        WHEN locked_until > CURRENT_TIMESTAMP THEN '🔒 Locked'
        WHEN failed_login_attempts > 3 THEN '⚠️ Multiple Failures'
        WHEN last_login < CURRENT_DATE - INTERVAL '30 days' THEN '😴 Inactive'
        ELSE '✅ Active'
    END as account_status
FROM users
ORDER BY last_login DESC NULLS LAST;

-- ============================================================================
-- 📈 PERFORMANCE AND MONITORING
-- ============================================================================

-- Database performance metrics
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    CASE 
        WHEN idx_scan = 0 THEN '❌ Unused'
        WHEN idx_scan < 100 THEN '⚠️ Low Usage'
        ELSE '✅ Active'
    END as usage_status
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Connection and activity monitoring
SELECT 
    datname as database,
    state,
    COUNT(*) as connection_count,
    MAX(state_change) as last_state_change
FROM pg_stat_activity
WHERE datname IN ('bhiv_hr', 'bhiv_hr_jcuu')
GROUP BY datname, state
ORDER BY datname, connection_count DESC;

-- ============================================================================
-- 🎯 BUSINESS INTELLIGENCE QUERIES
-- ============================================================================

-- Recruitment funnel analysis
WITH funnel_data AS (
    SELECT 
        c.id as candidate_id,
        c.name,
        c.created_at as applied_date,
        CASE WHEN EXISTS (SELECT 1 FROM feedback f WHERE f.candidate_id = c.id) THEN 1 ELSE 0 END as has_feedback,
        CASE WHEN EXISTS (SELECT 1 FROM interviews i WHERE i.candidate_id = c.id) THEN 1 ELSE 0 END as has_interview,
        CASE WHEN EXISTS (SELECT 1 FROM offers o WHERE o.candidate_id = c.id) THEN 1 ELSE 0 END as has_offer
    FROM candidates c
)
SELECT 
    'Applied' as stage, COUNT(*) as count, 100.0 as percentage FROM funnel_data
UNION ALL
SELECT 'Feedback Given', SUM(has_feedback), ROUND(SUM(has_feedback) * 100.0 / COUNT(*), 2) FROM funnel_data
UNION ALL
SELECT 'Interviewed', SUM(has_interview), ROUND(SUM(has_interview) * 100.0 / COUNT(*), 2) FROM funnel_data
UNION ALL
SELECT 'Offered', SUM(has_offer), ROUND(SUM(has_offer) * 100.0 / COUNT(*), 2) FROM funnel_data;

-- Monthly recruitment trends
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as new_candidates,
    AVG(experience_years) as avg_experience,
    COUNT(CASE WHEN average_score > 0 THEN 1 END) as assessed_candidates
FROM candidates
WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- Client satisfaction analysis
SELECT 
    cl.company_name,
    COUNT(DISTINCT j.id) as total_jobs,
    COUNT(DISTINCT f.candidate_id) as candidates_assessed,
    AVG(f.average_score) as avg_candidate_score,
    COUNT(DISTINCT o.candidate_id) as offers_made,
    ROUND(COUNT(DISTINCT o.candidate_id) * 100.0 / NULLIF(COUNT(DISTINCT f.candidate_id), 0), 2) as offer_rate
FROM clients cl
LEFT JOIN jobs j ON cl.client_id = j.client_id
LEFT JOIN feedback f ON j.id = f.job_id
LEFT JOIN offers o ON j.id = o.job_id
GROUP BY cl.client_id, cl.company_name
HAVING COUNT(DISTINCT j.id) > 0
ORDER BY avg_candidate_score DESC NULLS LAST;

-- ============================================================================
-- 🔧 MAINTENANCE AND CLEANUP QUERIES
-- ============================================================================

-- Find potential data quality issues
SELECT 'Candidates without email' as issue, COUNT(*) as count FROM candidates WHERE email IS NULL OR email = ''
UNION ALL
SELECT 'Jobs without requirements', COUNT(*) FROM jobs WHERE requirements IS NULL OR requirements = ''
UNION ALL
SELECT 'Feedback without comments', COUNT(*) FROM feedback WHERE comments IS NULL OR comments = ''
UNION ALL
SELECT 'Old audit logs (>90 days)', COUNT(*) FROM audit_logs WHERE timestamp < CURRENT_DATE - INTERVAL '90 days'
UNION ALL
SELECT 'Stale matching cache (>7 days)', COUNT(*) FROM matching_cache WHERE created_at < CURRENT_DATE - INTERVAL '7 days';

-- Disk space usage by table
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as total_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) as table_size,
    pg_size_pretty(pg_total_relation_size(tablename::regclass) - pg_relation_size(tablename::regclass)) as index_size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- ============================================================================
-- 📊 CUSTOM VIEWS FOR DASHBOARDS
-- ============================================================================

-- Create a comprehensive candidate summary view
-- (Run this to create a reusable view for reporting)
/*
CREATE OR REPLACE VIEW candidate_dashboard AS
SELECT 
    c.id,
    c.name,
    c.email,
    c.location,
    c.experience_years,
    c.technical_skills,
    c.seniority_level,
    c.average_score,
    c.status,
    c.created_at,
    COUNT(DISTINCT f.id) as feedback_count,
    AVG(f.average_score) as avg_feedback_score,
    COUNT(DISTINCT i.id) as interview_count,
    COUNT(DISTINCT o.id) as offer_count,
    MAX(mc.match_score) as best_match_score,
    STRING_AGG(DISTINCT j.title, ', ') as applied_positions
FROM candidates c
LEFT JOIN feedback f ON c.id = f.candidate_id
LEFT JOIN interviews i ON c.id = i.candidate_id
LEFT JOIN offers o ON c.id = o.candidate_id
LEFT JOIN matching_cache mc ON c.id = mc.candidate_id
LEFT JOIN jobs j ON f.job_id = j.id
GROUP BY c.id, c.name, c.email, c.location, c.experience_years, 
         c.technical_skills, c.seniority_level, c.average_score, c.status, c.created_at;
*/

-- Query the dashboard view (after creating it)
-- SELECT * FROM candidate_dashboard ORDER BY created_at DESC LIMIT 20;

-- ============================================================================
-- END OF QUERIES
-- ============================================================================

-- 🎉 Query Collection Complete
-- Total Queries: 25+ essential queries for database exploration
-- Categories: Schema, Data Overview, Business Intelligence, Security, Performance
-- Usage: Copy and paste individual queries into DBeaver SQL Editor
-- 
-- Built with Integrity, Honesty, Discipline, Hard Work & Gratitude
-- BHIV HR Platform v4.1.0 - Production Ready