import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path
from datetime import datetime

class SimpleEnhancedProcessor:
    def __init__(self):
        self.resume_folder = "resume"
        self.output_file = "data/enhanced_candidates.csv"
        
    def extract_text_from_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def extract_enhanced_info(self, text, filename):
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        # Basic extraction
        name = self.extract_name(text, filename)
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        location = self.extract_location(text)
        skills = self.extract_skills(text)
        experience = self.estimate_experience(text)
        education = self.extract_education(text)
        
        # Validate and clean extracted data
        name = name if name != 'Name Not Found' else f"Candidate_{filename[:10]}"
        email = email if '@' in email and 'placeholder' not in email else f"candidate_{filename[:5]}@email.com"
        phone = phone if phone != 'Not provided' else 'Phone not available'
        location = location if location != 'Location Not Specified' else 'India'
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'experience_years': experience,
            'education_level': education,
            'technical_skills': skills,
            'seniority_level': self.determine_seniority(experience),
            'cv_url': f"/resumes/{filename}",
            'status': 'applied',
            'job_id': 1,
            'summary': self.generate_summary(name, experience, skills, education),
            'availability': self.determine_availability(experience),
            'expected_salary': self.estimate_salary(experience, skills),
            'processed_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def extract_name(self, text, filename):
        # Try to extract name from text first
        text_lines = text.split('\n')[:10]  # Check first 10 lines
        
        # Pattern 1: Look for "Name:" or similar labels
        name_patterns = [
            r'(?i)name\s*:?\s*([A-Za-z\s]{2,30})',
            r'(?i)candidate\s*name\s*:?\s*([A-Za-z\s]{2,30})',
            r'^([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$'  # Title case names
        ]
        
        for line in text_lines:
            line = line.strip()
            for pattern in name_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1).strip()
                    if len(name.split()) >= 2 and len(name) <= 50:
                        return name.title()
        
        # Pattern 2: Look for standalone names in first few lines
        for line in text_lines[:5]:
            line = line.strip()
            if len(line.split()) == 2 and all(word.isalpha() for word in line.split()):
                if len(line) > 5 and len(line) < 30:
                    return line.title()
        
        # Fallback: Extract from filename
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv|\d+|\(\d+\))', '', name_from_file).strip()
        
        # Clean up filename-based name
        if name_from_file:
            words = name_from_file.split()
            if len(words) >= 1:
                return ' '.join(words[:3]).title()  # Max 3 words
        
        return "Name Not Found"
    
    def extract_email(self, text):
        # Enhanced email patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Standard
            r'(?i)email\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',  # With label
            r'(?i)e-mail\s*:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'   # With e-mail label
        ]
        
        all_emails = []
        for pattern in email_patterns:
            matches = re.findall(pattern, text)
            all_emails.extend(matches)
        
        # Filter out common fake/template emails
        fake_emails = ['example.com', 'test.com', 'sample.com', 'dummy.com']
        valid_emails = []
        
        for email in all_emails:
            email = email.lower().strip()
            if not any(fake in email for fake in fake_emails) and len(email) > 5:
                valid_emails.append(email)
        
        return valid_emails[0] if valid_emails else "email-not-found@placeholder.com"
    
    def extract_phone(self, text):
        # Multiple phone patterns for better extraction
        patterns = [
            r'\+91[-.\s]?\d{10}',  # Indian format +91-9876543210
            r'\+91\s?\d{5}\s?\d{5}',  # Indian format +91 98765 43210
            r'\d{10}',  # 10 digit number
            r'\+\d{1,3}[-.\s]?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}',  # International
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'  # US format
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                phone = phones[0].strip()
                # Clean up the phone number
                phone = re.sub(r'[()\s-]', '', phone)
                if phone.startswith('+91'):
                    return phone
                elif len(phone) == 10 and phone.isdigit():
                    return f'+91-{phone}'
                else:
                    return phone
        return "Not provided"
    
    def extract_location(self, text):
        # Enhanced location extraction with patterns
        location_patterns = [
            r'(?i)(?:address|location|city|based in|residing in)\s*:?\s*([A-Za-z\s,]+)',
            r'(?i)current\s*(?:location|address)\s*:?\s*([A-Za-z\s,]+)',
            r'(?i)(?:from|in)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?),?\s*(?:India|IN)?'
        ]
        
        # Try pattern-based extraction first
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                location = match.strip().replace(',', '').strip()
                if len(location) > 2 and len(location) < 30:
                    return location.title()
        
        # Expanded city database with states
        locations = {
            'Mumbai': ['mumbai', 'bombay', 'mumbai maharashtra'],
            'Delhi': ['delhi', 'new delhi', 'delhi ncr', 'ncr'],
            'Bangalore': ['bangalore', 'bengaluru', 'bangalore karnataka'],
            'Hyderabad': ['hyderabad', 'hyderabad telangana'],
            'Chennai': ['chennai', 'madras', 'chennai tamil nadu'],
            'Pune': ['pune', 'pune maharashtra'],
            'Kolkata': ['kolkata', 'calcutta', 'kolkata west bengal'],
            'Ahmedabad': ['ahmedabad', 'ahmedabad gujarat'],
            'Jaipur': ['jaipur', 'jaipur rajasthan'],
            'Surat': ['surat', 'surat gujarat'],
            'Lucknow': ['lucknow', 'lucknow uttar pradesh'],
            'Kanpur': ['kanpur', 'kanpur uttar pradesh'],
            'Nagpur': ['nagpur', 'nagpur maharashtra'],
            'Indore': ['indore', 'indore madhya pradesh'],
            'Thane': ['thane', 'thane maharashtra'],
            'Bhopal': ['bhopal', 'bhopal madhya pradesh'],
            'Visakhapatnam': ['visakhapatnam', 'vizag', 'vishakhapatnam'],
            'Pimpri-Chinchwad': ['pimpri', 'chinchwad', 'pimpri chinchwad'],
            'Patna': ['patna', 'patna bihar'],
            'Vadodara': ['vadodara', 'baroda', 'vadodara gujarat'],
            'Ghaziabad': ['ghaziabad', 'ghaziabad uttar pradesh'],
            'Ludhiana': ['ludhiana', 'ludhiana punjab'],
            'Agra': ['agra', 'agra uttar pradesh'],
            'Nashik': ['nashik', 'nashik maharashtra'],
            'Faridabad': ['faridabad', 'faridabad haryana'],
            'Meerut': ['meerut', 'meerut uttar pradesh'],
            'Rajkot': ['rajkot', 'rajkot gujarat'],
            'Kalyan-Dombivli': ['kalyan', 'dombivli'],
            'Vasai-Virar': ['vasai', 'virar'],
            'Varanasi': ['varanasi', 'banaras'],
            'Srinagar': ['srinagar'],
            'Aurangabad': ['aurangabad'],
            'Dhanbad': ['dhanbad'],
            'Amritsar': ['amritsar'],
            'Navi Mumbai': ['navi mumbai', 'new mumbai'],
            'Allahabad': ['allahabad', 'prayagraj'],
            'Ranchi': ['ranchi'],
            'Howrah': ['howrah'],
            'Coimbatore': ['coimbatore'],
            'Jabalpur': ['jabalpur'],
            'Gwalior': ['gwalior'],
            'Vijayawada': ['vijayawada'],
            'Jodhpur': ['jodhpur'],
            'Madurai': ['madurai'],
            'Raipur': ['raipur'],
            'Kota': ['kota'],
            'Guwahati': ['guwahati'],
            'Chandigarh': ['chandigarh'],
            'Solapur': ['solapur'],
            'Hubli-Dharwad': ['hubli', 'dharwad'],
            'Bareilly': ['bareilly'],
            'Moradabad': ['moradabad'],
            'Mysore': ['mysore', 'mysuru'],
            'Gurgaon': ['gurgaon', 'gurugram'],
            'Aligarh': ['aligarh'],
            'Jalandhar': ['jalandhar'],
            'Tiruchirappalli': ['tiruchirappalli', 'trichy'],
            'Bhubaneswar': ['bhubaneswar'],
            'Salem': ['salem'],
            'Mira-Bhayandar': ['mira bhayandar'],
            'Warangal': ['warangal'],
            'Thiruvananthapuram': ['thiruvananthapuram', 'trivandrum'],
            'Guntur': ['guntur'],
            'Bhiwandi': ['bhiwandi'],
            'Saharanpur': ['saharanpur'],
            'Gorakhpur': ['gorakhpur'],
            'Bikaner': ['bikaner'],
            'Amravati': ['amravati'],
            'Noida': ['noida'],
            'Jamshedpur': ['jamshedpur'],
            'Bhilai': ['bhilai'],
            'Cuttack': ['cuttack'],
            'Firozabad': ['firozabad'],
            'Kochi': ['kochi', 'cochin'],
            'Nellore': ['nellore'],
            'Bhavnagar': ['bhavnagar'],
            'Dehradun': ['dehradun'],
            'Durgapur': ['durgapur'],
            'Asansol': ['asansol'],
            'Rourkela': ['rourkela'],
            'Nanded': ['nanded'],
            'Kolhapur': ['kolhapur'],
            'Ajmer': ['ajmer'],
            'Akola': ['akola'],
            'Gulbarga': ['gulbarga'],
            'Jamnagar': ['jamnagar'],
            'Ujjain': ['ujjain'],
            'Loni': ['loni'],
            'Siliguri': ['siliguri'],
            'Jhansi': ['jhansi'],
            'Ulhasnagar': ['ulhasnagar'],
            'Jammu': ['jammu'],
            'Sangli-Miraj & Kupwad': ['sangli', 'miraj', 'kupwad'],
            'Mangalore': ['mangalore', 'mangaluru'],
            'Erode': ['erode'],
            'Belgaum': ['belgaum'],
            'Ambattur': ['ambattur'],
            'Tirunelveli': ['tirunelveli'],
            'Malegaon': ['malegaon'],
            'Gaya': ['gaya'],
            'Jalgaon': ['jalgaon'],
            'Udaipur': ['udaipur'],
            'Maheshtala': ['maheshtala']
        }
        
        text_lower = text.lower()
        # Score-based matching for better accuracy
        location_scores = {}
        
        for city, variations in locations.items():
            for variation in variations:
                if variation in text_lower:
                    # Give higher score to exact matches
                    score = len(variation) if variation == city.lower() else len(variation) * 0.8
                    if city not in location_scores or location_scores[city] < score:
                        location_scores[city] = score
        
        if location_scores:
            # Return the city with highest score
            best_city = max(location_scores.items(), key=lambda x: x[1])[0]
            return best_city
        
        return "Location Not Specified"
    
    def extract_skills(self, text):
        # Look for skills sections first
        skills_sections = re.findall(r'(?i)(?:skills?|technologies?|technical\s+skills?)\s*:?\s*([^\n]{50,200})', text)
        
        skills = set()
        text_lower = text.lower()
        
        # Comprehensive skill database with variations
        skill_database = {
            # Programming Languages
            'Python': ['python', 'py', 'python3'],
            'Java': ['java', 'java8', 'java 8', 'java11', 'java 11'],
            'JavaScript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015'],
            'TypeScript': ['typescript', 'ts'],
            'C++': ['c++', 'cpp', 'c plus plus'],
            'C#': ['c#', 'csharp', 'c sharp'],
            'PHP': ['php', 'php7', 'php8'],
            'Ruby': ['ruby', 'ruby on rails'],
            'Go': ['golang', 'go lang'],
            'Kotlin': ['kotlin'],
            'Swift': ['swift', 'swift ui'],
            'Scala': ['scala'],
            'R': ['r programming', 'r language'],
            'MATLAB': ['matlab'],
            'Perl': ['perl'],
            'Shell': ['shell', 'bash', 'zsh', 'shell scripting'],
            
            # Web Technologies
            'React': ['react', 'reactjs', 'react.js'],
            'Angular': ['angular', 'angularjs', 'angular2', 'angular 2'],
            'Vue.js': ['vue', 'vuejs', 'vue.js'],
            'HTML': ['html', 'html5'],
            'CSS': ['css', 'css3'],
            'SASS': ['sass', 'scss'],
            'Bootstrap': ['bootstrap'],
            'jQuery': ['jquery'],
            'Node.js': ['node', 'nodejs', 'node.js'],
            'Express': ['express', 'expressjs', 'express.js'],
            'Django': ['django'],
            'Flask': ['flask'],
            'Spring': ['spring', 'spring boot', 'springboot'],
            'Laravel': ['laravel'],
            'CodeIgniter': ['codeigniter'],
            'ASP.NET': ['asp.net', 'aspnet', 'asp net'],
            
            # Databases
            'SQL': ['sql', 'structured query language'],
            'MySQL': ['mysql'],
            'PostgreSQL': ['postgresql', 'postgres'],
            'MongoDB': ['mongodb', 'mongo'],
            'Redis': ['redis'],
            'Oracle': ['oracle', 'oracle db'],
            'SQLite': ['sqlite'],
            'Cassandra': ['cassandra'],
            'DynamoDB': ['dynamodb'],
            'Firebase': ['firebase'],
            
            # Cloud & DevOps
            'AWS': ['aws', 'amazon web services'],
            'Azure': ['azure', 'microsoft azure'],
            'GCP': ['gcp', 'google cloud', 'google cloud platform'],
            'Docker': ['docker', 'containerization'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'Jenkins': ['jenkins'],
            'GitLab CI': ['gitlab', 'gitlab ci'],
            'Terraform': ['terraform'],
            'Ansible': ['ansible'],
            
            # Data Science & Analytics
            'Pandas': ['pandas'],
            'NumPy': ['numpy'],
            'Matplotlib': ['matplotlib'],
            'Seaborn': ['seaborn'],
            'Scikit-learn': ['scikit-learn', 'sklearn'],
            'TensorFlow': ['tensorflow'],
            'PyTorch': ['pytorch'],
            'Keras': ['keras'],
            'Tableau': ['tableau'],
            'Power BI': ['power bi', 'powerbi'],
            'Excel': ['excel', 'ms excel', 'microsoft excel'],
            'Jupyter': ['jupyter', 'jupyter notebook'],
            'Apache Spark': ['spark', 'apache spark'],
            'Hadoop': ['hadoop'],
            
            # Mobile Development
            'Android': ['android', 'android development'],
            'iOS': ['ios', 'ios development'],
            'React Native': ['react native'],
            'Flutter': ['flutter'],
            'Xamarin': ['xamarin'],
            
            # Tools & IDEs
            'Git': ['git', 'version control'],
            'GitHub': ['github'],
            'GitLab': ['gitlab'],
            'Jira': ['jira'],
            'Postman': ['postman'],
            'VS Code': ['vs code', 'visual studio code'],
            'IntelliJ': ['intellij', 'intellij idea'],
            'Eclipse': ['eclipse'],
            'Sublime Text': ['sublime', 'sublime text'],
            'Vim': ['vim'],
            
            # Testing
            'Selenium': ['selenium'],
            'Jest': ['jest'],
            'JUnit': ['junit'],
            'PyTest': ['pytest'],
            'Cypress': ['cypress'],
            
            # Other Technologies
            'REST API': ['rest', 'rest api', 'restful'],
            'GraphQL': ['graphql'],
            'Microservices': ['microservices'],
            'Machine Learning': ['machine learning', 'ml'],
            'Artificial Intelligence': ['artificial intelligence', 'ai'],
            'Deep Learning': ['deep learning'],
            'Data Mining': ['data mining'],
            'Big Data': ['big data'],
            'Blockchain': ['blockchain'],
            'IoT': ['iot', 'internet of things'],
            'Agile': ['agile', 'scrum'],
            'DevOps': ['devops'],
            'CI/CD': ['ci/cd', 'continuous integration'],
            'Linux': ['linux', 'ubuntu', 'centos'],
            'Windows': ['windows'],
            'macOS': ['macos', 'mac os']
        }
        
        # Extract from skills sections first
        for section in skills_sections:
            section_lower = section.lower()
            for skill, variations in skill_database.items():
                for variation in variations:
                    if variation in section_lower:
                        skills.add(skill)
        
        # If no skills section found, search entire text
        if not skills:
            for skill, variations in skill_database.items():
                for variation in variations:
                    # Use word boundaries for better matching
                    pattern = r'\b' + re.escape(variation) + r'\b'
                    if re.search(pattern, text_lower):
                        skills.add(skill)
        
        # Convert to list and sort by relevance (length of skill name)
        skills_list = sorted(list(skills), key=len, reverse=True)[:12]  # Top 12 skills
        return ', '.join(skills_list) if skills_list else 'Skills Not Specified'
    
    def extract_education(self, text):
        text_lower = text.lower()
        
        # Enhanced education patterns with specific degrees
        education_patterns = {
            'PhD': [
                'phd', 'ph.d', 'doctorate', 'doctoral', 'doctor of philosophy',
                'ph d', 'postdoctoral', 'post doctoral'
            ],
            'Masters': [
                'master', 'masters', 'm.tech', 'mtech', 'mba', 'm.b.a',
                'ms', 'm.s', 'msc', 'm.sc', 'ma', 'm.a', 'mca', 'm.c.a',
                'me', 'm.e', 'master of', 'post graduate', 'postgraduate',
                'pg diploma', 'pgdm'
            ],
            'Bachelors': [
                'bachelor', 'bachelors', 'b.tech', 'btech', 'be', 'b.e',
                'bs', 'b.s', 'bsc', 'b.sc', 'ba', 'b.a', 'bca', 'b.c.a',
                'bcom', 'b.com', 'bachelor of', 'undergraduate', 'graduate',
                'engineering degree', 'degree in'
            ],
            'Diploma': [
                'diploma', 'polytechnic', 'certificate', 'advanced diploma'
            ],
            '12th/Higher Secondary': [
                '12th', 'xii', 'higher secondary', 'intermediate', 'hsc',
                'plus two', '+2', 'senior secondary'
            ],
            '10th/Secondary': [
                '10th', 'x', 'secondary', 'ssc', 'matriculation', 'high school'
            ]
        }
        
        # Look for education section first
        education_sections = re.findall(r'(?i)(?:education|qualification|academic)\s*:?\s*([^\n]{20,100})', text)
        
        found_education = []
        search_text = ' '.join(education_sections) if education_sections else text_lower
        
        for level, keywords in education_patterns.items():
            for keyword in keywords:
                if keyword in search_text:
                    found_education.append(level)
                    break
        
        # Return highest education level found
        education_hierarchy = ['PhD', 'Masters', 'Bachelors', 'Diploma', '12th/Higher Secondary', '10th/Secondary']
        
        for level in education_hierarchy:
            if level in found_education:
                return level
        
        # Try to extract specific degree names
        degree_patterns = [
            r'(?i)(b\.?tech|bachelor of technology)',
            r'(?i)(m\.?tech|master of technology)',
            r'(?i)(mba|master of business administration)',
            r'(?i)(bca|bachelor of computer applications)',
            r'(?i)(mca|master of computer applications)',
            r'(?i)(be|bachelor of engineering)',
            r'(?i)(me|master of engineering)'
        ]
        
        for pattern in degree_patterns:
            if re.search(pattern, text_lower):
                match = re.search(pattern, text_lower)
                degree = match.group(1).upper()
                if degree in ['B.TECH', 'BE', 'BCA']:
                    return f'Bachelors ({degree})'
                elif degree in ['M.TECH', 'ME', 'MBA', 'MCA']:
                    return f'Masters ({degree})'
        
        return 'Education Not Specified'
    
    def estimate_experience(self, text):
        text_lower = text.lower()
        
        # Look for explicit experience mentions first
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)(?:ience)?',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)',
            r'total\s*(?:experience|exp)\s*:?\s*(\d+)\+?\s*years?',
            r'work\s*experience\s*:?\s*(\d+)\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                exp_years = int(matches[0])
                # Be more conservative - cap at 15 years and validate
                if exp_years <= 15:
                    return exp_years
                elif exp_years <= 25:
                    return min(exp_years, 10)  # Reduce inflated numbers
        
        # Look for work history with company names and dates
        current_year = datetime.now().year
        
        # Find graduation year patterns
        grad_patterns = [
            r'(?:graduated|graduation|passed).*?(20\d{2})',
            r'(20\d{2}).*?(?:graduate|graduation|passed)',
            r'(?:b\.?tech|be|bachelor).*?(20\d{2})',
            r'(20\d{2}).*?(?:b\.?tech|be|bachelor)'
        ]
        
        graduation_year = None
        for pattern in grad_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                year = int(matches[0])
                if 2000 <= year <= current_year:
                    graduation_year = year
                    break
        
        # Calculate experience from graduation year
        if graduation_year:
            calculated_exp = current_year - graduation_year - 1  # Subtract 1 for graduation delay
            return max(0, min(calculated_exp, 12))  # Cap at 12 years
        
        # Look for work dates in format "2020-2023" or "2020 to 2023"
        work_date_patterns = [
            r'(20\d{2})\s*[-to]+\s*(20\d{2})',
            r'(20\d{2})\s*-\s*present',
            r'(20\d{2})\s*to\s*present'
        ]
        
        work_years = []
        for pattern in work_date_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    start_year = int(match[0])
                    end_year = current_year if 'present' in str(match[1]) else int(match[1])
                    work_years.append(end_year - start_year)
        
        if work_years:
            total_exp = sum(work_years)
            return min(total_exp, 10)  # Cap at 10 years
        
        # Keyword-based estimation (more conservative)
        if any(word in text_lower for word in ['fresher', 'fresh graduate', 'entry level', 'trainee']):
            return 0
        elif any(word in text_lower for word in ['intern', 'internship']):
            return 0
        elif any(word in text_lower for word in ['junior', '1 year', 'one year']):
            return 1
        elif any(word in text_lower for word in ['senior', 'lead', 'team lead']):
            return 4
        elif any(word in text_lower for word in ['manager', 'principal', 'architect']):
            return 6
        
        # Default conservative estimate
        return 2
    
    def determine_seniority(self, experience):
        if experience >= 8:
            return 'Senior'
        elif experience >= 5:
            return 'Mid-level'
        elif experience >= 2:
            return 'Junior'
        elif experience >= 1:
            return 'Associate'
        else:
            return 'Entry-level'
    
    def generate_summary(self, name, experience, skills, education):
        # Create more personalized summaries
        skills_list = skills.split(', ') if skills != 'Skills Not Specified' else []
        primary_skills = skills_list[:3] if skills_list else ['various technologies']
        
        if experience == 0:
            if 'fresher' in name.lower() or any(word in education.lower() for word in ['recent', 'fresh']):
                return f"Recent {education} graduate seeking opportunities in {', '.join(primary_skills)}"
            else:
                return f"{education} graduate with foundational knowledge in {', '.join(primary_skills)}"
        elif experience == 1:
            return f"Early-career professional with 1 year experience in {', '.join(primary_skills)}"
        elif experience <= 3:
            return f"Developing professional with {experience} years experience specializing in {', '.join(primary_skills)}"
        elif experience <= 6:
            return f"Experienced professional with {experience} years expertise in {', '.join(primary_skills)} and team collaboration"
        else:
            return f"Senior professional with {experience}+ years leadership experience in {', '.join(primary_skills)} and project management"
    
    def estimate_salary(self, experience, skills):
        # More realistic salary estimation for Indian market
        if experience == 0:
            base_salary = 250000  # Entry level
        elif experience <= 2:
            base_salary = 350000  # Junior
        elif experience <= 5:
            base_salary = 550000  # Mid-level
        else:
            base_salary = 800000  # Senior
        
        # Skills-based adjustment (more conservative)
        high_value_skills = ['AWS', 'React', 'Python', 'Machine Learning', 'Docker', 'Kubernetes', 'Java']
        skill_count = sum(1 for skill in high_value_skills if skill in skills)
        skill_multiplier = 1 + (skill_count * 0.1)  # 10% per high-value skill
        
        # Location adjustment (if in major cities)
        estimated = int(base_salary * skill_multiplier)
        
        # Cap the salary to realistic ranges
        if experience == 0:
            estimated = min(estimated, 400000)
        elif experience <= 2:
            estimated = min(estimated, 600000)
        elif experience <= 5:
            estimated = min(estimated, 1000000)
        else:
            estimated = min(estimated, 1500000)
        
        return f"{estimated:,} INR"
    
    def determine_availability(self, experience):
        # More realistic availability based on experience
        if experience == 0:
            return 'Immediate'
        elif experience <= 2:
            return 'Within 2 weeks'
        elif experience <= 5:
            return '30 days notice'
        else:
            return '60 days notice'
    
    def process_resumes(self):
        candidates = []
        resume_files = list(Path(self.resume_folder).glob('*.pdf'))
        
        print(f"Processing {len(resume_files)} resumes...")
        
        for file_path in resume_files:
            filename = file_path.name
            print(f"Processing: {filename}")
            
            text = self.extract_text_from_pdf(file_path)
            if text.strip():
                candidate_info = self.extract_enhanced_info(text, filename)
                candidates.append(candidate_info)
                print(f"  -> {candidate_info['name']} ({candidate_info['seniority_level']})")
        
        if candidates:
            df = pd.DataFrame(candidates)
            # Reorder columns for better readability
            column_order = [
                'name', 'email', 'phone', 'location', 'experience_years', 
                'seniority_level', 'education_level', 'technical_skills', 
                'expected_salary', 'summary', 'availability', 'cv_url', 
                'status', 'job_id', 'processed_date'
            ]
            df = df[column_order]
            df.to_csv(self.output_file, index=False)
            print(f"\nSaved {len(candidates)} candidates to {self.output_file}")
            print(f"Skills extracted: {len(set([skill for candidate in candidates for skill in candidate['technical_skills'].split(', ') if skill != 'Skills Not Specified']))} unique skills")
            print(f"Locations found: {len(set([c['location'] for c in candidates if c['location'] != 'Location Not Specified']))} cities")
            return df
        return None

if __name__ == "__main__":
    processor = SimpleEnhancedProcessor()
    processor.process_resumes()