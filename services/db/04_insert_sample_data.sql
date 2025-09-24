-- BHIV HR Platform - Sample Data
-- Production-quality sample data for testing and development

-- Insert system configuration
INSERT INTO system_config (key, value, description, updated_by) VALUES
('app_version', '3.2.0', 'Current application version', 'system'),
('maintenance_mode', 'false', 'Application maintenance mode flag', 'system'),
('max_file_upload_size', '10485760', 'Maximum file upload size in bytes (10MB)', 'system'),
('session_timeout_hours', '24', 'Session timeout in hours', 'system'),
('api_rate_limit_per_minute', '1000', 'API rate limit per minute', 'system'),
('email_notifications_enabled', 'true', 'Enable email notifications', 'system'),
('ai_matching_enabled', 'true', 'Enable AI matching features', 'system'),
('audit_log_retention_days', '365', 'Audit log retention period in days', 'system')
ON CONFLICT (key) DO UPDATE SET 
    value = EXCLUDED.value,
    updated_at = CURRENT_TIMESTAMP,
    updated_by = EXCLUDED.updated_by;

-- Insert client authentication data
INSERT INTO client_auth (
    client_id, company_name, industry, company_size, website, email, phone, address,
    password_hash, subscription_tier, api_rate_limit, created_by
) VALUES
(
    'TECH001', 
    'Tech Solutions Inc', 
    'Technology', 
    'medium', 
    'https://techsolutions.com',
    'admin@techsolutions.com', 
    '+1-555-0100', 
    '123 Tech Street, San Francisco, CA 94105',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcQjyPHSS',
    'premium',
    2000,
    'system'
),
(
    'STARTUP001', 
    'InnovateCorp', 
    'Software', 
    'startup', 
    'https://innovatecorp.io',
    'hr@innovatecorp.io', 
    '+1-555-0200', 
    '456 Innovation Ave, Austin, TX 78701',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcQjyPHSS',
    'basic',
    1000,
    'system'
),
(
    'ENTERPRISE001', 
    'Global Systems Corp', 
    'Enterprise Software', 
    'enterprise', 
    'https://globalsystems.com',
    'talent@globalsystems.com', 
    '+1-555-0300', 
    '789 Enterprise Blvd, New York, NY 10001',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcQjyPHSS',
    'enterprise',
    5000,
    'system'
)
ON CONFLICT (client_id) DO UPDATE SET 
    company_name = EXCLUDED.company_name,
    updated_at = CURRENT_TIMESTAMP;

-- Insert comprehensive candidate data
INSERT INTO candidates (
    name, email, phone, location, experience_years, technical_skills, soft_skills,
    seniority_level, education_level, portfolio_url, linkedin_url, github_url,
    salary_expectation_min, salary_expectation_max, remote_preference, source, created_by
) VALUES
(
    'John Doe', 
    'john.doe@email.com', 
    '+1-555-1001', 
    'New York, NY', 
    5, 
    'Python, Django, FastAPI, PostgreSQL, Docker, AWS, Redis, Celery',
    'Leadership, Communication, Problem Solving, Team Collaboration',
    'senior', 
    'Bachelor of Computer Science',
    'https://johndoe.dev',
    'https://linkedin.com/in/johndoe',
    'https://github.com/johndoe',
    120000, 
    150000, 
    true,
    'linkedin',
    'system'
),
(
    'Jane Smith', 
    'jane.smith@email.com', 
    '+1-555-1002', 
    'San Francisco, CA', 
    3, 
    'JavaScript, React, Node.js, TypeScript, MongoDB, GraphQL, Jest',
    'Creativity, Adaptability, Critical Thinking, Time Management',
    'mid_level', 
    'Master of Software Engineering',
    'https://janesmith.io',
    'https://linkedin.com/in/janesmith',
    'https://github.com/janesmith',
    90000, 
    120000, 
    true,
    'referral',
    'system'
),
(
    'Bob Johnson', 
    'bob.johnson@email.com', 
    '+1-555-1003', 
    'Austin, TX', 
    7, 
    'Java, Spring Boot, Microservices, Kubernetes, MySQL, Apache Kafka',
    'Mentoring, Strategic Thinking, Project Management, Conflict Resolution',
    'senior', 
    'Bachelor of Information Technology',
    'https://bobjohnson.tech',
    'https://linkedin.com/in/bobjohnson',
    'https://github.com/bobjohnson',
    130000, 
    160000, 
    false,
    'job_board',
    'system'
),
(
    'Alice Brown', 
    'alice.brown@email.com', 
    '+1-555-1004', 
    'Remote', 
    2, 
    'Python, Machine Learning, TensorFlow, Pandas, Scikit-learn, Jupyter',
    'Analytical Thinking, Attention to Detail, Curiosity, Presentation Skills',
    'junior', 
    'Master of Data Science',
    'https://alicebrown.ai',
    'https://linkedin.com/in/alicebrown',
    'https://github.com/alicebrown',
    70000, 
    90000, 
    true,
    'university',
    'system'
),
(
    'Charlie Wilson', 
    'charlie.wilson@email.com', 
    '+1-555-1005', 
    'Seattle, WA', 
    4, 
    'Go, Kubernetes, Docker, Terraform, AWS, CI/CD, Prometheus, Grafana',
    'Automation Mindset, Reliability Focus, Collaboration, Documentation',
    'mid_level', 
    'Bachelor of Computer Engineering',
    'https://charliewilson.dev',
    'https://linkedin.com/in/charliewilson',
    'https://github.com/charliewilson',
    100000, 
    130000, 
    true,
    'direct_application',
    'system'
),
(
    'Diana Martinez', 
    'diana.martinez@email.com', 
    '+1-555-1006', 
    'Miami, FL', 
    6, 
    'C#, .NET Core, Azure, SQL Server, Entity Framework, SignalR',
    'Client Relations, Requirements Gathering, Solution Architecture, Training',
    'senior', 
    'Bachelor of Software Engineering',
    'https://dianamart.dev',
    'https://linkedin.com/in/dianamart',
    'https://github.com/dianamart',
    115000, 
    145000, 
    false,
    'headhunter',
    'system'
)
ON CONFLICT (email) DO UPDATE SET 
    name = EXCLUDED.name,
    updated_at = CURRENT_TIMESTAMP;

-- Insert comprehensive job postings
INSERT INTO jobs (
    title, department, location, remote_allowed, employment_type, experience_level,
    salary_min, salary_max, requirements, description, responsibilities, benefits,
    skills_required, skills_preferred, positions_available, application_deadline,
    client_id, hiring_manager, hr_contact, created_by
) VALUES
(
    'Senior Python Developer', 
    'Engineering', 
    'New York, NY', 
    true, 
    'full_time', 
    'senior',
    120000, 
    150000,
    'Bachelor''s degree in Computer Science or related field. 5+ years of Python development experience. Strong knowledge of Django/FastAPI, PostgreSQL, and cloud platforms.',
    'We are seeking a Senior Python Developer to join our growing engineering team. You will be responsible for designing and implementing scalable backend services, mentoring junior developers, and contributing to architectural decisions.',
    'Design and develop high-performance backend services; Mentor junior developers; Participate in code reviews; Collaborate with product and design teams; Optimize application performance; Maintain code quality standards',
    'Competitive salary, Health insurance, 401k matching, Flexible PTO, Remote work options, Professional development budget',
    ARRAY['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Docker', 'AWS'],
    ARRAY['Redis', 'Celery', 'Kubernetes', 'GraphQL', 'Machine Learning'],
    2,
    '2025-02-15',
    'TECH001',
    'Sarah Johnson',
    'hr@techsolutions.com',
    'system'
),
(
    'Frontend Developer', 
    'Engineering', 
    'San Francisco, CA', 
    true, 
    'full_time', 
    'mid_level',
    90000, 
    120000,
    'Bachelor''s degree preferred. 3+ years of frontend development experience. Proficiency in React, TypeScript, and modern CSS frameworks.',
    'Join our frontend team to build beautiful, responsive user interfaces. You will work closely with designers and backend developers to create exceptional user experiences.',
    'Develop responsive web applications; Implement pixel-perfect designs; Optimize for performance and accessibility; Write comprehensive tests; Collaborate with UX/UI designers',
    'Health insurance, Dental and vision, Stock options, Flexible hours, Learning stipend, Catered meals',
    ARRAY['JavaScript', 'React', 'TypeScript', 'CSS', 'HTML'],
    ARRAY['Next.js', 'GraphQL', 'Jest', 'Cypress', 'Figma'],
    1,
    '2025-02-20',
    'TECH001',
    'Mike Chen',
    'hr@techsolutions.com',
    'system'
),
(
    'DevOps Engineer', 
    'Infrastructure', 
    'Austin, TX', 
    false, 
    'full_time', 
    'mid_level',
    100000, 
    130000,
    'Bachelor''s degree in Computer Science or related field. 3+ years of DevOps experience. Strong knowledge of containerization, orchestration, and cloud platforms.',
    'We need a DevOps Engineer to help scale our infrastructure and improve our deployment processes. You will work on automation, monitoring, and ensuring high availability of our services.',
    'Manage CI/CD pipelines; Monitor system performance; Automate infrastructure provisioning; Ensure security compliance; Troubleshoot production issues; Implement disaster recovery',
    'Competitive salary, Health benefits, 401k, Professional certifications, Conference attendance, Flexible schedule',
    ARRAY['Docker', 'Kubernetes', 'AWS', 'Terraform', 'CI/CD'],
    ARRAY['Prometheus', 'Grafana', 'ELK Stack', 'Ansible', 'Go'],
    1,
    '2025-02-25',
    'STARTUP001',
    'Alex Rodriguez',
    'hr@innovatecorp.io',
    'system'
),
(
    'Data Scientist', 
    'Analytics', 
    'Remote', 
    true, 
    'full_time', 
    'junior',
    70000, 
    90000,
    'Master''s degree in Data Science, Statistics, or related field. 1-3 years of experience. Strong Python and SQL skills. Experience with machine learning frameworks.',
    'Join our data science team to build predictive models and extract insights from large datasets. You will work on exciting projects involving customer behavior analysis and business optimization.',
    'Develop machine learning models; Analyze large datasets; Create data visualizations; Collaborate with business stakeholders; Present findings to leadership; Maintain data pipelines',
    'Health insurance, Learning budget, Remote work, Flexible hours, Stock options, Mentorship program',
    ARRAY['Python', 'SQL', 'Machine Learning', 'Statistics'],
    ARRAY['TensorFlow', 'PyTorch', 'Spark', 'Tableau', 'R'],
    1,
    '2025-03-01',
    'ENTERPRISE001',
    'Dr. Lisa Wang',
    'talent@globalsystems.com',
    'system'
),
(
    'Full Stack Developer', 
    'Engineering', 
    'Remote', 
    true, 
    'contract', 
    'mid_level',
    80000, 
    110000,
    'Bachelor''s degree preferred. 3+ years of full-stack development experience. Proficiency in both frontend and backend technologies.',
    'We are looking for a versatile Full Stack Developer to work on various client projects. You will be responsible for both frontend and backend development using modern technologies.',
    'Develop end-to-end web applications; Work with multiple technology stacks; Collaborate with cross-functional teams; Ensure code quality and best practices; Participate in project planning',
    'Competitive hourly rate, Flexible schedule, Remote work, Project bonuses, Professional development',
    ARRAY['JavaScript', 'Node.js', 'React', 'MongoDB', 'Express'],
    ARRAY['TypeScript', 'GraphQL', 'Docker', 'AWS', 'Vue.js'],
    3,
    '2025-02-28',
    'TECH001',
    'Tom Anderson',
    'hr@techsolutions.com',
    'system'
)
ON CONFLICT DO NOTHING;

-- Insert job applications
INSERT INTO job_applications (candidate_id, job_id, status, cover_letter, source, created_by) VALUES
(1, 1, 'interviewing', 'I am excited to apply for the Senior Python Developer position. My 5 years of experience with Python and Django make me a perfect fit for this role.', 'direct', 'system'),
(2, 2, 'screening', 'As a passionate frontend developer with 3 years of React experience, I would love to contribute to your team.', 'linkedin', 'system'),
(3, 3, 'applied', 'My DevOps background and experience with Kubernetes align perfectly with your infrastructure needs.', 'job_board', 'system'),
(4, 4, 'offered', 'I am thrilled to apply my data science skills to solve complex business problems at your company.', 'university', 'system'),
(5, 5, 'interviewing', 'My full-stack experience and ability to work with multiple technologies make me ideal for this position.', 'referral', 'system'),
(6, 1, 'screening', 'With my .NET background and willingness to learn Python, I believe I can contribute significantly to your team.', 'headhunter', 'system')
ON CONFLICT (candidate_id, job_id) DO NOTHING;

-- Insert interview schedules
INSERT INTO interviews (
    candidate_id, job_id, application_id, interview_type, interview_date, duration_minutes,
    location, interviewer_name, interviewer_email, interviewer_role, status, notes, created_by
) VALUES
(1, 1, 1, 'technical', '2025-01-25 10:00:00+00', 90, 'Video Call', 'Sarah Johnson', 'sarah.johnson@techsolutions.com', 'Engineering Manager', 'scheduled', 'Technical interview focusing on Python and system design', 'system'),
(1, 1, 1, 'panel', '2025-01-26 14:00:00+00', 60, 'Office - Conference Room A', 'Mike Chen', 'mike.chen@techsolutions.com', 'Senior Developer', 'scheduled', 'Panel interview with team members', 'system'),
(2, 2, 2, 'phone', '2025-01-24 15:00:00+00', 45, 'Phone Call', 'Lisa Park', 'lisa.park@techsolutions.com', 'HR Manager', 'completed', 'Initial screening call completed successfully', 'system'),
(4, 4, 4, 'final', '2025-01-23 11:00:00+00', 60, 'Video Call', 'Dr. Lisa Wang', 'lisa.wang@globalsystems.com', 'Data Science Director', 'completed', 'Final interview with director', 'system'),
(5, 5, 5, 'technical', '2025-01-27 13:00:00+00', 120, 'Video Call', 'Tom Anderson', 'tom.anderson@techsolutions.com', 'Lead Developer', 'scheduled', 'Full-stack technical assessment', 'system')
ON CONFLICT DO NOTHING;

-- Insert comprehensive feedback
INSERT INTO feedback (
    candidate_id, job_id, interview_id, evaluator_name, evaluator_role,
    technical_skills, problem_solving, code_quality, system_design,
    communication, teamwork, leadership, adaptability,
    integrity, honesty, discipline, hard_work, gratitude,
    strengths, areas_for_improvement, additional_comments, recommendation, created_by
) VALUES
(1, 1, 1, 'Sarah Johnson', 'Engineering Manager',
    5, 5, 4, 5,
    5, 4, 4, 5,
    5, 5, 4, 5, 4,
    'Excellent Python skills, strong system design knowledge, great communication',
    'Could improve code documentation practices',
    'Very impressed with the candidate''s technical depth and problem-solving approach',
    'strong_hire', 'system'),
(2, 2, 2, 'Lisa Park', 'HR Manager',
    4, 4, NULL, NULL,
    5, 5, 3, 4,
    4, 5, 5, 4, 5,
    'Strong React skills, excellent communication, team player',
    'Limited experience with testing frameworks',
    'Great cultural fit, enthusiastic about learning',
    'hire', 'system'),
(4, 4, 4, 'Dr. Lisa Wang', 'Data Science Director',
    4, 5, 4, 3,
    4, 4, 3, 5,
    5, 4, 5, 5, 4,
    'Strong analytical skills, quick learner, good statistical foundation',
    'Needs more experience with production ML systems',
    'Shows great potential for growth in our data science team',
    'hire', 'system')
ON CONFLICT DO NOTHING;