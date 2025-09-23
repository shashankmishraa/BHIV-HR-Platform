import os
from pathlib import Path

def get_all_files():
    """Get complete list of all files in project"""
    all_files = []
    excluded_dirs = {'.git', '__pycache__', 'node_modules', '.pytest_cache'}
    
    for root, dirs, files in os.walk('.'):
        # Remove excluded directories from dirs list
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to('.')
            all_files.append(str(rel_path))
    
    return sorted(all_files)

def compare_with_analyzer():
    """Compare with file_analyzer.py results"""
    all_files = get_all_files()
    
    print(f"COMPLETE FILE COUNT ANALYSIS")
    print("="*50)
    print(f"Total files found: {len(all_files)}")
    print(f"File analyzer reported: 264 files")
    print(f"Difference: {len(all_files) - 264} files")
    
    # Show file breakdown by extension
    extensions = {}
    for file in all_files:
        ext = Path(file).suffix.lower() or 'no_extension'
        extensions[ext] = extensions.get(ext, 0) + 1
    
    print(f"\nFILE BREAKDOWN BY EXTENSION:")
    print("-" * 30)
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext}: {count} files")
    
    # Show first 50 files for verification
    print(f"\nFIRST 50 FILES:")
    print("-" * 30)
    for i, file in enumerate(all_files[:50]):
        print(f"  {file}")
    
    if len(all_files) > 50:
        print(f"  ... and {len(all_files) - 50} more files")
    
    return all_files

if __name__ == "__main__":
    files = compare_with_analyzer()