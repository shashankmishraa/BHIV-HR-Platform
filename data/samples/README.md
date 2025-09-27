# Sample Data v4.1.0

**Updated**: January 18, 2025 | **Status**: ✅ Optimized & Secure

## 📊 Sample Datasets

### **candidates.csv**
- **Purpose**: Sample candidate data for development and testing
- **Size**: Optimized for quick loading
- **Security**: Anonymized data only, no personal information
- **Format**: CSV with standardized columns

### **Usage Guidelines**
- Use only for development and testing
- Never commit personal or sensitive data
- Keep files under 1MB for performance
- Update samples when schema changes

### **Data Structure**
```csv
id,name,email,skills,experience_years,location
1,"Sample Candidate","sample@example.com","Python,React",5,"Remote"
```

### **Integration**
- **Database**: PostgreSQL 17 schema compatible
- **Services**: Used by Gateway and Agent services
- **Testing**: Automated test data generation
- **Validation**: Schema validation included
