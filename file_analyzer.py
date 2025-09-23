import os
import json
from pathlib import Path
from datetime import datetime

def analyze_project_files():
    """Analyze all project files and categorize them"""
    
    project_root = Path(".")
    
    # File categories
    categories = {
        "critical": [],
        "important": [],
        "unused": [],
        "redundant": [],
        "needs_update": [],
        "needs_more_info": [],
        "generated": [],
        "config": [],
        "documentation": []
    }
    
    # Define patterns
    critical_patterns = [
        "main.py", "app.py", "__init__.py", "requirements.txt", 
        "docker-compose", "Dockerfile", ".env"
    ]
    
    config_patterns = [
        ".env", ".gitignore", "docker-compose", "requirements.txt",
        "config", "settings", ".yml", ".yaml", ".json"
    ]
    
    doc_patterns = [
        ".md", ".txt", "README", "CHANGELOG", "LICENSE"
    ]
    
    generated_patterns = [
        ".pyc", "__pycache__", ".git", "node_modules", 
        ".pytest_cache", "logs", "endpoint_test_results"
    ]
    
    # Walk through all files
    for root, dirs, files in os.walk(project_root):
        # Skip hidden and generated directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(project_root)
            
            # Skip hidden files
            if file.startswith('.') and file not in ['.env', '.gitignore']:
                continue
                
            file_info = {
                "path": str(rel_path),
                "size": file_path.stat().st_size if file_path.exists() else 0,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if file_path.exists() else "Unknown"
            }
            
            # Categorize files
            if any(pattern in file.lower() for pattern in generated_patterns):
                categories["generated"].append(file_info)
            elif any(pattern in file.lower() for pattern in critical_patterns):
                categories["critical"].append(file_info)
            elif any(file.endswith(pattern) for pattern in config_patterns):
                categories["config"].append(file_info)
            elif any(file.endswith(pattern) for pattern in doc_patterns):
                categories["documentation"].append(file_info)
            elif file.endswith('.py'):
                categories["important"].append(file_info)
            else:
                categories["needs_more_info"].append(file_info)
    
    return categories

def generate_report(categories):
    """Generate detailed file analysis report"""
    
    print("="*80)
    print("BHIV HR PLATFORM - PROJECT FILE ANALYSIS")
    print("="*80)
    
    # Critical Files
    print(f"\nCRITICAL FILES ({len(categories['critical'])})")
    print("-" * 50)
    for file in sorted(categories['critical'], key=lambda x: x['path']):
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    
    # Important Python Files
    print(f"\nIMPORTANT PYTHON FILES ({len(categories['important'])})")
    print("-" * 50)
    for file in sorted(categories['important'], key=lambda x: x['path'])[:20]:
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    if len(categories['important']) > 20:
        print(f"  ... and {len(categories['important']) - 20} more Python files")
    
    # Configuration Files
    print(f"\nCONFIGURATION FILES ({len(categories['config'])})")
    print("-" * 50)
    for file in sorted(categories['config'], key=lambda x: x['path']):
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    
    # Documentation Files
    print(f"\nDOCUMENTATION FILES ({len(categories['documentation'])})")
    print("-" * 50)
    for file in sorted(categories['documentation'], key=lambda x: x['path']):
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    
    # Files needing attention
    print(f"\nFILES NEEDING MORE INFO ({len(categories['needs_more_info'])})")
    print("-" * 50)
    for file in sorted(categories['needs_more_info'], key=lambda x: x['path']):
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    
    # Generated/Temporary Files
    print(f"\nGENERATED/TEMPORARY FILES ({len(categories['generated'])})")
    print("-" * 50)
    for file in sorted(categories['generated'], key=lambda x: x['path'])[:10]:
        print(f"  {file['path']} ({file['size']} bytes, {file['modified']})")
    if len(categories['generated']) > 10:
        print(f"  ... and {len(categories['generated']) - 10} more generated files")

def analyze_specific_issues():
    """Analyze specific file issues"""
    
    issues = {
        "missing_critical": [],
        "outdated": [],
        "redundant": [],
        "unused": []
    }
    
    # Check for missing critical files
    critical_files = [
        "requirements.txt",
        "docker-compose.yml",
        "README.md",
        ".env.example",
        ".gitignore"
    ]
    
    for file in critical_files:
        if not Path(file).exists():
            issues["missing_critical"].append(file)
    
    # Check for potentially redundant files
    redundant_patterns = [
        ("endpoint_tester.py", "comprehensive_endpoint_tester.py"),
        ("test_", "comprehensive_test_"),
    ]
    
    # Check for unused files (files not imported or referenced)
    python_files = list(Path(".").rglob("*.py"))
    
    print(f"\nSPECIFIC ISSUES ANALYSIS")
    print("-" * 50)
    
    if issues["missing_critical"]:
        print(f"Missing Critical Files: {', '.join(issues['missing_critical'])}")
    
    # Check for large files that might need attention
    large_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = Path(root) / file
            if file_path.stat().st_size > 100000:  # > 100KB
                large_files.append((str(file_path), file_path.stat().st_size))
    
    if large_files:
        print(f"\nLARGE FILES (>100KB):")
        for file, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {file} ({size:,} bytes)")

def main():
    categories = analyze_project_files()
    generate_report(categories)
    analyze_specific_issues()
    
    # Summary
    total_files = sum(len(files) for files in categories.values())
    print(f"\nSUMMARY")
    print("-" * 50)
    print(f"Total Files Analyzed: {total_files}")
    print(f"Critical Files: {len(categories['critical'])}")
    print(f"Important Python Files: {len(categories['important'])}")
    print(f"Configuration Files: {len(categories['config'])}")
    print(f"Documentation Files: {len(categories['documentation'])}")
    print(f"Generated/Temp Files: {len(categories['generated'])}")

if __name__ == "__main__":
    main()