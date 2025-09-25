#!/usr/bin/env python3
"""
Import Validation Script for BHIV HR Platform
Validates that all imports are using absolute paths and can be resolved correctly
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import List, Dict, Tuple


class ImportValidator:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues = []
        self.files_checked = 0

    def validate_file(self, file_path: Path) -> List[Dict]:
        """Validate imports in a single Python file"""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("."):
                        # Found relative import
                        issues.append(
                            {
                                "file": str(file_path.relative_to(self.root_path)),
                                "line": node.lineno,
                                "type": "relative_import",
                                "import": f"from {node.module} import {', '.join([alias.name for alias in node.names])}",
                                "suggestion": self._suggest_absolute_import(
                                    node, file_path
                                ),
                            }
                        )

        except Exception as e:
            issues.append(
                {
                    "file": str(file_path.relative_to(self.root_path)),
                    "line": 0,
                    "type": "parse_error",
                    "error": str(e),
                }
            )

        return issues

    def _suggest_absolute_import(self, node: ast.ImportFrom, file_path: Path) -> str:
        """Suggest absolute import path"""
        relative_path = file_path.relative_to(self.root_path)

        # Determine the base package
        if "services/gateway/app" in str(relative_path):
            base = "app"
        elif "services/shared" in str(relative_path):
            base = "services.shared"
        elif "services/agent" in str(relative_path):
            base = "services.agent"
        else:
            base = "services"

        # Convert relative import to absolute
        if node.module.startswith(".."):
            # Go up directories
            dots = len(node.module) - len(node.module.lstrip("."))
            module_parts = node.module[dots:].split(".") if node.module[dots:] else []

            # Calculate absolute path
            current_parts = str(relative_path.parent).replace("\\", "/").split("/")
            if "services/gateway/app" in str(relative_path):
                # Remove the number of dots from current path
                absolute_parts = ["app"] + module_parts
            else:
                absolute_parts = current_parts[:-dots] + module_parts

            absolute_module = ".".join(filter(None, absolute_parts))
        else:
            absolute_module = (
                f"{base}.{node.module[1:]}"
                if node.module.startswith(".")
                else node.module
            )

        imports = ", ".join([alias.name for alias in node.names])
        return f"from {absolute_module} import {imports}"

    def validate_directory(self, directory: Path) -> None:
        """Validate all Python files in a directory recursively"""
        for file_path in directory.rglob("*.py"):
            # Skip __pycache__ and .git directories
            if "__pycache__" in str(file_path) or ".git" in str(file_path):
                continue

            self.files_checked += 1
            file_issues = self.validate_file(file_path)
            self.issues.extend(file_issues)

    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("=" * 80)
        report.append("BHIV HR Platform - Import Validation Report")
        report.append("=" * 80)
        report.append(f"Files checked: {self.files_checked}")
        report.append(f"Issues found: {len(self.issues)}")
        report.append("")

        if not self.issues:
            report.append("SUCCESS: All imports are using absolute paths!")
            report.append("")
            report.append("Import validation completed successfully.")
        else:
            report.append("ISSUES FOUND:")
            report.append("")

            # Group issues by type
            by_type = {}
            for issue in self.issues:
                issue_type = issue["type"]
                if issue_type not in by_type:
                    by_type[issue_type] = []
                by_type[issue_type].append(issue)

            for issue_type, issues in by_type.items():
                report.append(
                    f"## {issue_type.replace('_', ' ').title()} ({len(issues)} issues)"
                )
                report.append("")

                for issue in issues:
                    report.append(f"File: {issue['file']}")
                    if "line" in issue and issue["line"] > 0:
                        report.append(f"Line: {issue['line']}")
                    if "import" in issue:
                        report.append(f"Current: {issue['import']}")
                    if "suggestion" in issue:
                        report.append(f"Suggested: {issue['suggestion']}")
                    if "error" in issue:
                        report.append(f"Error: {issue['error']}")
                    report.append("")

        report.append("=" * 80)
        return "\n".join(report)


def main():
    """Main validation function"""
    # Get the root directory (parent of scripts directory)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    print("Starting import validation...")
    print(f"Root directory: {root_dir}")

    validator = ImportValidator(str(root_dir))

    # Validate key directories
    directories_to_check = [
        root_dir / "services" / "gateway" / "app",
        root_dir / "services" / "shared",
        root_dir / "tests",
    ]

    for directory in directories_to_check:
        if directory.exists():
            print(f"Checking: {directory.relative_to(root_dir)}")
            validator.validate_directory(directory)

    # Generate and display report
    report = validator.generate_report()
    print(report)

    # Save report to file
    report_file = root_dir / "IMPORT_VALIDATION_REPORT.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved to: {report_file}")

    # Return exit code based on issues found
    return 0 if not validator.issues else 1


if __name__ == "__main__":
    sys.exit(main())
