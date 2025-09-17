#!/usr/bin/env python3
"""
BHIV HR Platform - Repository Cleanup Management
Comprehensive cleanup of redundant directories, cache files, and stale data
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Set
import json
from datetime import datetime

class RepositoryCleanupManager:
    """Comprehensive repository cleanup and maintenance"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cleanup_results = {
            "pycache_removed": [],
            "stale_files_removed": [],
            "empty_dirs_removed": [],
            "large_files_identified": [],
            "space_saved": 0
        }
        
        # Define cleanup patterns
        self.cache_patterns = [
            "__pycache__",
            "*.pyc",
            "*.pyo", 
            ".pytest_cache",
            ".coverage",
            "htmlcov"
        ]
        
        self.stale_patterns = [
            "*.tmp",
            "*.temp",
            "*.bak",
            "*.backup",
            "*~",
            ".DS_Store",
            "Thumbs.db"
        ]
    
    def analyze_repository_structure(self) -> Dict[str, Any]:
        """Analyze current repository structure and identify issues"""
        print("Analyzing repository structure...")
        
        analysis = {
            "total_files": 0,
            "total_size": 0,
            "pycache_dirs": [],
            "large_files": [],
            "stale_files": [],
            "empty_dirs": [],
            "resume_files": [],
            "data_files": []
        }
        
        # Scan all files
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                analysis["total_files"] += 1
                try:
                    size = file_path.stat().st_size
                    analysis["total_size"] += size
                    
                    # Identify large files (>1MB)
                    if size > 1024 * 1024:
                        analysis["large_files"].append({
                            "path": str(file_path.relative_to(self.project_root)),
                            "size": size,
                            "size_mb": round(size / (1024 * 1024), 2)
                        })
                    
                    # Identify resume files
                    if file_path.parent.name == "resume":
                        analysis["resume_files"].append({
                            "path": str(file_path.relative_to(self.project_root)),
                            "size": size
                        })
                    
                    # Identify data files
                    if file_path.parent.name == "data":
                        analysis["data_files"].append({
                            "path": str(file_path.relative_to(self.project_root)),
                            "size": size
                        })
                    
                    # Check for stale files
                    if any(file_path.name.endswith(pattern.replace("*", "")) 
                          for pattern in self.stale_patterns if not pattern.startswith("*")):
                        analysis["stale_files"].append(str(file_path.relative_to(self.project_root)))
                
                except:
                    continue
            
            elif file_path.is_dir():
                # Identify __pycache__ directories
                if file_path.name == "__pycache__":
                    analysis["pycache_dirs"].append(str(file_path.relative_to(self.project_root)))
                
                # Check for empty directories
                try:
                    if not any(file_path.iterdir()):
                        analysis["empty_dirs"].append(str(file_path.relative_to(self.project_root)))
                except:
                    continue
        
        return analysis
    
    def cleanup_pycache_directories(self) -> List[str]:
        """Remove all __pycache__ directories"""
        print("Cleaning up __pycache__ directories...")
        
        removed_dirs = []
        for pycache_dir in self.project_root.rglob("__pycache__"):
            if pycache_dir.is_dir():
                try:
                    # Calculate size before removal
                    size = sum(f.stat().st_size for f in pycache_dir.rglob("*") if f.is_file())
                    
                    shutil.rmtree(pycache_dir)
                    removed_dirs.append(str(pycache_dir.relative_to(self.project_root)))
                    self.cleanup_results["space_saved"] += size
                    
                except Exception as e:
                    print(f"Failed to remove {pycache_dir}: {e}")
        
        self.cleanup_results["pycache_removed"] = removed_dirs
        return removed_dirs
    
    def cleanup_stale_files(self) -> List[str]:
        """Remove stale and temporary files"""
        print("Cleaning up stale files...")
        
        removed_files = []
        
        # Remove files matching stale patterns
        for pattern in self.stale_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        file_path.unlink()
                        removed_files.append(str(file_path.relative_to(self.project_root)))
                        self.cleanup_results["space_saved"] += size
                    except Exception as e:
                        print(f"Failed to remove {file_path}: {e}")
        
        self.cleanup_results["stale_files_removed"] = removed_files
        return removed_files
    
    def cleanup_empty_directories(self) -> List[str]:
        """Remove empty directories"""
        print("Cleaning up empty directories...")
        
        removed_dirs = []
        
        # Multiple passes to handle nested empty directories
        for _ in range(3):
            for dir_path in list(self.project_root.rglob("*")):
                if dir_path.is_dir() and dir_path != self.project_root:
                    try:
                        # Check if directory is empty
                        if not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            removed_dirs.append(str(dir_path.relative_to(self.project_root)))
                    except:
                        continue
        
        self.cleanup_results["empty_dirs_removed"] = removed_dirs
        return removed_dirs
    
    def analyze_resume_files(self) -> Dict[str, Any]:
        """Analyze resume files for optimization"""
        print("Analyzing resume files...")
        
        resume_dir = self.project_root / "resume"
        if not resume_dir.exists():
            return {"status": "no_resume_directory"}
        
        analysis = {
            "total_files": 0,
            "total_size": 0,
            "file_types": {},
            "large_files": [],
            "recommendations": []
        }
        
        for resume_file in resume_dir.iterdir():
            if resume_file.is_file():
                analysis["total_files"] += 1
                size = resume_file.stat().st_size
                analysis["total_size"] += size
                
                # Count file types
                ext = resume_file.suffix.lower()
                analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
                
                # Identify large files
                if size > 500 * 1024:  # >500KB
                    analysis["large_files"].append({
                        "name": resume_file.name,
                        "size": size,
                        "size_kb": round(size / 1024, 2)
                    })
        
        # Generate recommendations
        if analysis["total_files"] > 30:
            analysis["recommendations"].append("Consider archiving older resume files")
        
        if analysis["total_size"] > 10 * 1024 * 1024:  # >10MB
            analysis["recommendations"].append("Resume directory is large - consider compression")
        
        return analysis
    
    def optimize_data_structure(self) -> Dict[str, Any]:
        """Optimize data directory structure"""
        print("Optimizing data structure...")
        
        data_dir = self.project_root / "data"
        optimization = {
            "current_structure": [],
            "recommendations": [],
            "proposed_structure": []
        }
        
        if data_dir.exists():
            # Analyze current structure
            for item in data_dir.iterdir():
                if item.is_file():
                    size = item.stat().st_size
                    optimization["current_structure"].append({
                        "name": item.name,
                        "type": "file",
                        "size": size
                    })
        
        # Recommendations for better structure
        optimization["recommendations"] = [
            "Separate sample data from production data",
            "Use compressed formats for large datasets",
            "Implement data versioning for samples",
            "Move large files to external storage"
        ]
        
        optimization["proposed_structure"] = [
            "data/samples/ - Small sample datasets",
            "data/schemas/ - Database schemas and migrations", 
            "data/fixtures/ - Test fixtures and mock data",
            "data/README.md - Data documentation"
        ]
        
        return optimization
    
    def generate_cleanup_report(self) -> Dict[str, Any]:
        """Generate comprehensive cleanup report"""
        analysis = self.analyze_repository_structure()
        resume_analysis = self.analyze_resume_files()
        data_optimization = self.optimize_data_structure()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "repository_analysis": analysis,
            "resume_analysis": resume_analysis,
            "data_optimization": data_optimization,
            "cleanup_results": self.cleanup_results,
            "recommendations": self._generate_recommendations(analysis)
        }
        
        return report
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate cleanup recommendations"""
        recommendations = []
        
        if analysis["pycache_dirs"]:
            recommendations.append(f"Remove {len(analysis['pycache_dirs'])} __pycache__ directories")
        
        if analysis["large_files"]:
            recommendations.append(f"Review {len(analysis['large_files'])} large files for optimization")
        
        if analysis["resume_files"] and len(analysis["resume_files"]) > 25:
            recommendations.append("Archive older resume files to reduce repository size")
        
        if analysis["total_size"] > 50 * 1024 * 1024:  # >50MB
            recommendations.append("Repository is large - consider using Git LFS for binary files")
        
        recommendations.extend([
            "Implement automated cleanup in CI/CD pipeline",
            "Add pre-commit hooks to prevent cache file commits",
            "Regular repository maintenance schedule"
        ])
        
        return recommendations
    
    def execute_comprehensive_cleanup(self) -> Dict[str, Any]:
        """Execute comprehensive repository cleanup"""
        print("BHIV HR Platform - Repository Cleanup")
        print("=" * 40)
        
        # Generate initial analysis
        initial_analysis = self.analyze_repository_structure()
        initial_size = initial_analysis["total_size"]
        
        print(f"Initial repository analysis:")
        print(f"  Total files: {initial_analysis['total_files']}")
        print(f"  Total size: {initial_size / (1024*1024):.2f} MB")
        print(f"  __pycache__ directories: {len(initial_analysis['pycache_dirs'])}")
        print(f"  Large files: {len(initial_analysis['large_files'])}")
        
        # Execute cleanup operations
        self.cleanup_pycache_directories()
        self.cleanup_stale_files()
        self.cleanup_empty_directories()
        
        # Generate final report
        final_report = self.generate_cleanup_report()
        space_saved = self.cleanup_results["space_saved"]
        
        print(f"\nCleanup completed:")
        print(f"  __pycache__ dirs removed: {len(self.cleanup_results['pycache_removed'])}")
        print(f"  Stale files removed: {len(self.cleanup_results['stale_files_removed'])}")
        print(f"  Empty dirs removed: {len(self.cleanup_results['empty_dirs_removed'])}")
        print(f"  Space saved: {space_saved / (1024*1024):.2f} MB")
        
        return final_report

def main():
    """Main cleanup interface"""
    cleanup_manager = RepositoryCleanupManager()
    
    # Execute comprehensive cleanup
    report = cleanup_manager.execute_comprehensive_cleanup()
    
    # Save report
    report_file = cleanup_manager.project_root / "CLEANUP_REPORT.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    # Print recommendations
    if report["recommendations"]:
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())