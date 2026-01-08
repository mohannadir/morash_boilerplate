#!/usr/bin/env python
"""
Verification script to check if the cookiecutter template is properly set up.
This script checks for:
1. Directory structure with cookiecutter variables
2. File contents with cookiecutter variables
3. Missing or incorrect references
"""
import os
import re
from pathlib import Path

def check_directories():
    """Check if directories are properly named with cookiecutter variables."""
    print("Checking directory structure...")
    issues = []
    
    base_dir = Path("{{cookiecutter.project_slug}}")
    main_dir = Path("{{cookiecutter.main_app_name}}")
    
    if not base_dir.exists():
        issues.append(f"❌ Missing: {base_dir}")
    else:
        print(f"  ✓ Found: {base_dir}")
        if not (base_dir / "settings.py").exists():
            issues.append(f"❌ Missing settings.py in {base_dir}")
    
    if not main_dir.exists():
        issues.append(f"❌ Missing: {main_dir}")
    else:
        print(f"  ✓ Found: {main_dir}")
        if not (main_dir / "models.py").exists():
            issues.append(f"❌ Missing models.py in {main_dir}")
    
    # Check templates directory
    templates_dir = main_dir / "templates" / "{{cookiecutter.main_app_name}}"
    if templates_dir.exists():
        print(f"  ✓ Found templates directory: {templates_dir}")
    else:
        issues.append(f"❌ Missing templates directory: {templates_dir}")
    
    return issues

def check_cookiecutter_json():
    """Check if cookiecutter.json exists and has required fields."""
    print("\nChecking cookiecutter.json...")
    issues = []
    
    json_file = Path("cookiecutter.json")
    if not json_file.exists():
        issues.append("❌ Missing cookiecutter.json")
        return issues
    
    print("  ✓ Found cookiecutter.json")
    
    # Check for required variables
    import json
    with open(json_file) as f:
        data = json.load(f)
    
    required_vars = ['project_name', 'project_slug', 'platform_name', 'main_app_name']
    for var in required_vars:
        if var not in data:
            issues.append(f"❌ Missing variable in cookiecutter.json: {var}")
        else:
            print(f"  ✓ Variable found: {var}")
    
    return issues

def check_file_references():
    """Check if files have proper cookiecutter variable references."""
    print("\nChecking file references...")
    issues = []
    
    # Check settings.py
    settings_file = Path("{{cookiecutter.project_slug}}") / "settings.py"
    if settings_file.exists():
        content = settings_file.read_text()
        if "{{ cookiecutter.project_slug }}" in content:
            print("  ✓ settings.py has cookiecutter variables")
        else:
            issues.append("❌ settings.py missing cookiecutter variables")
        
        if "{{ cookiecutter.main_app_name }}" in content:
            print("  ✓ settings.py references main app correctly")
        else:
            issues.append("❌ settings.py missing main app reference")
    
    # Check manage.py
    manage_file = Path("manage.py")
    if manage_file.exists():
        content = manage_file.read_text()
        if "{{ cookiecutter.project_slug }}" in content:
            print("  ✓ manage.py has cookiecutter variables")
        else:
            issues.append("❌ manage.py missing cookiecutter variables")
    
    return issues

def main():
    """Run all checks."""
    print("=" * 60)
    print("CookieCutter Template Verification")
    print("=" * 60)
    
    all_issues = []
    
    # Run checks
    all_issues.extend(check_directories())
    all_issues.extend(check_cookiecutter_json())
    all_issues.extend(check_file_references())
    
    # Summary
    print("\n" + "=" * 60)
    if all_issues:
        print("Issues found:")
        for issue in all_issues:
            print(f"  {issue}")
        print("\n⚠️  Please fix the issues above before using the template.")
        return 1
    else:
        print("✅ All checks passed! Template is ready to use.")
        print("\nTo test the template:")
        print("  cookiecutter .")
        return 0

if __name__ == '__main__':
    exit(main())
