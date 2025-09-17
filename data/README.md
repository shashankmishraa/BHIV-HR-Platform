# BHIV HR Platform - Data Management

## Directory Structure

### data/samples/
Small sample datasets for development and testing.
- Keep files under 1MB
- Use representative but anonymized data
- Include data format documentation

### data/schemas/
Database schemas, migrations, and structure definitions.
- SQL schema files
- Migration scripts
- Database documentation

### data/fixtures/
Test fixtures and mock data for automated testing.
- JSON fixtures for unit tests
- Mock API responses
- Test data generators

### data/archive/
Archived or deprecated data files.
- Old data formats
- Deprecated samples
- Historical datasets

## Resume Files Management

### Guidelines
- Store only necessary sample resumes
- Remove personal information from samples
- Use compressed formats when possible
- Archive older files regularly

### File Naming Convention
```
resume/samples/sample_[role]_[level].pdf
resume/archive/[date]_archived_resumes/
```

## Best Practices

### Data Security
- Never commit personal data
- Use anonymized samples only
- Implement data retention policies
- Regular cleanup of temporary files

### Performance
- Keep sample files small (<1MB)
- Use compressed formats
- Implement lazy loading for large datasets
- Cache frequently accessed data

### Maintenance
- Regular cleanup of unused files
- Archive old data periodically
- Monitor directory sizes
- Update documentation when structure changes

## Tools

### Data Management
```bash
# Organize data structure
python tools/data_manager.py --organize

# Optimize resume storage
python tools/data_manager.py --optimize-resumes

# Clean up redundant files
python tools/repo_cleanup.py
```

### Monitoring
```bash
# Check data directory sizes
python tools/data_manager.py --analyze

# Generate data report
python tools/data_manager.py --report
```
