#!/usr/bin/env python3
"""
BHIV HR Platform - Data Management System
Organize and optimize data files, resume storage, and sample datasets
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any
import json
import hashlib

class DataManager:
    """Comprehensive data organization and management"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        self.resume_dir = self.project_root / "resume"
        
    def organize_data_structure(self) -> Dict[str, Any]:
        """Organize data directory with proper structure"""
        print("Organizing data directory structure...")
        
        # Create organized structure
        new_structure = {
            "data/samples": "Small sample datasets for development",
            "data/schemas": "Database schemas and migrations",
            "data/fixtures": "Test fixtures and mock data",
            "data/archive": "Archived or deprecated data"
        }
        
        results = {"created_dirs": [], "moved_files": []}
        
        # Create directories
        for dir_path, description in new_structure.items():
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                results["created_dirs"].append(dir_path)
                
                # Create README
                readme_path = full_path / "README.md"
                readme_content = f"# {dir_path.split('/')[-1].title()}\n\n{description}\n"
                readme_path.write_text(readme_content)
        
        # Move existing data files to appropriate locations
        if self.data_dir.exists():
            for item in self.data_dir.iterdir():
                if item.is_file() and item.name != "README.md":
                    # Move to samples directory
                    target = self.data_dir / "samples" / item.name
                    if not target.exists():
                        shutil.move(str(item), str(target))
                        results["moved_files"].append(f"{item.name} -> samples/")
        
        return results
    
    def optimize_resume_storage(self) -> Dict[str, Any]:
        """Optimize resume file storage and organization"""
        print("Optimizing resume storage...")
        
        if not self.resume_dir.exists():
            return {"status": "no_resume_directory"}
        
        optimization = {
            "total_files": 0,
            "total_size": 0,
            "duplicates_found": [],
            "large_files": [],
            "organized_files": []
        }
        
        # Analyze files
        file_hashes = {}
        for resume_file in self.resume_dir.iterdir():
            if resume_file.is_file():
                optimization["total_files"] += 1
                size = resume_file.stat().st_size
                optimization["total_size"] += size
                
                # Check for duplicates by content hash
                file_hash = self._calculate_file_hash(resume_file)
                if file_hash in file_hashes:
                    optimization["duplicates_found"].append({
                        "original": file_hashes[file_hash],
                        "duplicate": resume_file.name
                    })
                else:
                    file_hashes[file_hash] = resume_file.name
                
                # Identify large files
                if size > 1024 * 1024:  # >1MB
                    optimization["large_files"].append({
                        "name": resume_file.name,
                        "size_mb": round(size / (1024 * 1024), 2)
                    })
        
        return optimization
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return ""
    
    def create_data_documentation(self) -> str:
        """Create comprehensive data documentation"""
        print("Creating data documentation...")
        
        doc_content = """# BHIV HR Platform - Data Management

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
"""
        
        doc_path = self.data_dir / "README.md"
        doc_path.write_text(doc_content)
        return str(doc_path)
    
    def execute_data_optimization(self) -> Dict[str, Any]:
        """Execute comprehensive data optimization"""
        print("BHIV HR Platform - Data Optimization")
        print("=" * 40)
        
        results = {
            "data_organization": self.organize_data_structure(),
            "resume_optimization": self.optimize_resume_storage(),
            "documentation": self.create_data_documentation()
        }
        
        return results

def main():
    """Main data management interface"""
    data_manager = DataManager()
    results = data_manager.execute_data_optimization()
    
    print("\nData optimization completed:")
    print(f"  Created directories: {len(results['data_organization']['created_dirs'])}")
    print(f"  Moved files: {len(results['data_organization']['moved_files'])}")
    
    if results['resume_optimization'].get('duplicates_found'):
        print(f"  Duplicate resumes found: {len(results['resume_optimization']['duplicates_found'])}")
    
    print(f"  Documentation created: {results['documentation']}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())