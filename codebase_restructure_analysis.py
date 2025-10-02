#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Codebase Restructure Analysis
Step-by-step analysis to detect outdated code and restructure project
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class CodebaseAnalyzer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.analysis = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "outdated_files": [],
            "files_to_update": [],
            "files_to_keep": [],
            "files_to_eliminate": [],
            "restructure_recommendations": [],
            "critical_updates": []
        }
    
    def analyze_file_status(self, file_path: Path) -> Dict[str, Any]:
        """Analyze individual file for outdated code and structure"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_info = {
                "path": str(file_path.relative_to(self.project_root)),
                "size": len(content),
                "lines": len(content.splitlines()),
                "status": "keep",
                "issues": [],
                "recommendations": []
            }
            
            # Check for outdated patterns
            if "hardcoded" in content.lower() or "mock" in content.lower():
                file_info["issues"].append("Contains hardcoded/mock data")
            
            if "TODO" in content or "FIXME" in content:
                file_info["issues"].append("Contains TODO/FIXME comments")
            
            if "deprecated" in content.lower():
                file_info["issues"].append("Contains deprecated code")
            
            # Check for duplicate functionality
            if file_path.name in ["auth_service.py"] and file_path.parent.name == "client_portal":
                file_info["status"] = "eliminate"
                file_info["issues"].append("Redundant authentication service")
            
            # Check for unused semantic engine
            if "semantic_engine" in str(file_path) and not any(x in content for x in ["import", "from"]):
                file_info["status"] = "eliminate"
                file_info["issues"].append("Unused semantic engine files")
            
            return file_info
            
        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.project_root)),
                "status": "error",
                "issues": [f"Analysis error: {str(e)}"]
            }
    
    def analyze_services_structure(self):
        """Analyze services directory structure"""
        services_dir = self.project_root / "services"
        
        for service_dir in services_dir.iterdir():
            if service_dir.is_dir():
                service_analysis = {
                    "service": service_dir.name,
                    "files": [],
                    "structure_issues": [],
                    "recommendations": []
                }
                
                # Check for proper structure
                expected_files = ["Dockerfile", "requirements.txt"]
                for expected in expected_files:
                    if not (service_dir / expected).exists():
                        service_analysis["structure_issues"].append(f"Missing {expected}")
                
                # Analyze service files
                for file_path in service_dir.rglob("*"):
                    if file_path.is_file():
                        file_info = self.analyze_file_status(file_path)
                        service_analysis["files"].append(file_info)
                
                self.analysis["services_analysis"] = service_analysis
    
    def identify_elimination_candidates(self):
        """Identify files that should be eliminated"""
        elimination_candidates = [
            {
                "path": "services/client_portal/auth_service.py",
                "reason": "Redundant 300+ line authentication service for simple login",
                "action": "eliminate",
                "replacement": "Use gateway authentication endpoints"
            },
            {
                "path": "services/semantic_engine/",
                "reason": "Unused semantic engine directory - not integrated",
                "action": "eliminate",
                "replacement": "AI matching handled by agent service"
            },
            {
                "path": "*.pyc files",
                "reason": "Compiled Python files should not be in repository",
                "action": "eliminate",
                "replacement": "Add to .gitignore"
            },
            {
                "path": "logs/*.log",
                "reason": "Log files should not be committed",
                "action": "eliminate", 
                "replacement": "Add to .gitignore"
            }
        ]
        
        self.analysis["files_to_eliminate"] = elimination_candidates
    
    def recommend_restructure(self):
        """Recommend project restructuring"""
        restructure_plan = [
            {
                "action": "create_directory",
                "path": "src/",
                "reason": "Standard Python project structure"
            },
            {
                "action": "move_services",
                "from": "services/",
                "to": "src/services/",
                "reason": "Follow Python packaging standards"
            },
            {
                "action": "create_directory", 
                "path": "deployment/",
                "reason": "Centralize deployment configurations"
            },
            {
                "action": "move_configs",
                "files": ["docker-compose.*.yml", "*.env*"],
                "to": "deployment/",
                "reason": "Organize deployment files"
            },
            {
                "action": "create_directory",
                "path": "docs/api/",
                "reason": "Separate API documentation"
            }
        ]
        
        self.analysis["restructure_recommendations"] = restructure_plan
    
    def identify_critical_updates(self):
        """Identify files needing critical updates"""
        critical_updates = [
            {
                "file": "services/agent/app.py",
                "issue": "Incomplete skills_score calculation at line 130",
                "action": "fix_calculation",
                "priority": "high"
            },
            {
                "file": "services/gateway/app/main.py", 
                "issue": "API endpoint count mismatch (44 vs 46 claimed)",
                "action": "verify_endpoints",
                "priority": "medium"
            },
            {
                "file": ".gitignore",
                "issue": "Missing entries for logs, cache, compiled files",
                "action": "update_gitignore",
                "priority": "high"
            }
        ]
        
        self.analysis["critical_updates"] = critical_updates
    
    def run_analysis(self):
        """Run complete codebase analysis"""
        print("Starting comprehensive codebase analysis...")
        
        # Analyze all files
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not any(x in str(file_path) for x in [".git", "__pycache__", ".pyc"]):
                self.analysis["files_analyzed"] += 1
                file_info = self.analyze_file_status(file_path)
                
                if file_info["status"] == "eliminate":
                    self.analysis["outdated_files"].append(file_info)
                elif file_info["issues"]:
                    self.analysis["files_to_update"].append(file_info)
                else:
                    self.analysis["files_to_keep"].append(file_info)
        
        # Run specific analyses
        self.analyze_services_structure()
        self.identify_elimination_candidates()
        self.recommend_restructure()
        self.identify_critical_updates()
        
        # Save analysis
        with open(self.project_root / "codebase_analysis_report.json", "w") as f:
            json.dump(self.analysis, f, indent=2)
        
        return self.analysis

if __name__ == "__main__":
    analyzer = CodebaseAnalyzer()
    results = analyzer.run_analysis()
    
    print(f"\nAnalysis Complete:")
    print(f"Files analyzed: {results['files_analyzed']}")
    print(f"Files to eliminate: {len(results['files_to_eliminate'])}")
    print(f"Files needing updates: {len(results['files_to_update'])}")
    print(f"Critical updates needed: {len(results['critical_updates'])}")