#!/usr/bin/env python
"""
Test script to verify the cookiecutter template structure.
This simulates what cookiecutter will include/exclude.
"""
import os
import json
from pathlib import Path

def read_ignore_patterns(ignore_file):
    """Read and parse .cookiecutterignore patterns."""
    patterns = []
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    return patterns

def matches_pattern(path, pattern):
    """Simple pattern matching (supports * and **)."""
    import fnmatch
    # Convert pattern to regex-like matching
    if '**' in pattern:
        # Handle ** patterns
        parts = pattern.split('**')
        if len(parts) == 2:
            if path.startswith(parts[0]) or path.endswith(parts[1]):
                return True
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern)

def should_include(path, ignore_patterns):
    """Check if a path should be included in the template."""
    # Normalize path
    path = path.replace('\\', '/')
    
    for pattern in ignore_patterns:
        if matches_pattern(path, pattern) or matches_pattern(path + '/', pattern):
            return False
    return True

def scan_template_directory(root_dir, ignore_patterns):
    """Scan directory and list what would be included."""
    included = []
    excluded = []
    
    for root, dirs, files in os.walk(root_dir):
        # Filter dirs based on ignore patterns
        dirs[:] = [d for d in dirs if should_include(os.path.join(root, d).replace('\\', '/'), ignore_patterns)]
        
        for file in files:
            file_path = os.path.join(root, file).replace('\\', '/')
            rel_path = os.path.relpath(file_path, root_dir).replace('\\', '/')
            
            if should_include(rel_path, ignore_patterns):
                included.append(rel_path)
            else:
                excluded.append(rel_path)
    
    return included, excluded

def main():
    """Main test function."""
    print("=" * 70)
    print("CookieCutter Template Structure Test")
    print("=" * 70)
    
    # Read configuration
    with open('cookiecutter.json') as f:
        config = json.load(f)
    
    print("\n✓ CookieCutter Configuration:")
    print(f"  Project name: {config.get('project_name')}")
    print(f"  Main app name: {config.get('main_app_name')}")
    print(f"  Copy without render: {len(config.get('_copy_without_render', []))} patterns")
    
    # Read ignore patterns
    ignore_patterns = read_ignore_patterns('.cookiecutterignore')
    print(f"\n✓ Ignore patterns: {len(ignore_patterns)} patterns loaded")
    
    # Scan template
    print("\n" + "=" * 70)
    print("Scanning Template Directory...")
    print("=" * 70)
    
    included, excluded = scan_template_directory('.', ignore_patterns)
    
    # Group by directory
    dirs_included = set()
    dirs_excluded = set()
    
    for path in included:
        parts = path.split('/')
        if len(parts) > 1:
            dirs_included.add(parts[0])
    
    for path in excluded:
        parts = path.split('/')
        if len(parts) > 1:
            dirs_excluded.add(parts[0])
    
    print(f"\n📁 Directories that WILL be included ({len(dirs_included)}):")
    for d in sorted(dirs_included):
        if d not in ['.git', '.idea', '.secrets', 'locale', 'logs']:
            print(f"  ✓ {d}/")
    
    print(f"\n📁 Directories that WILL be excluded ({len(dirs_excluded)}):")
    for d in sorted(dirs_excluded):
        print(f"  ✗ {d}/")
    
    # Check critical directories
    print("\n" + "=" * 70)
    print("Critical Template Directories Check:")
    print("=" * 70)
    
    critical_dirs = [
        '{{cookiecutter.project_slug}}',
        '{{cookiecutter.main_app_name}}',
        'api',
        'CONFIG',
        'modules',
        'theme',
        'websockets',
        'manage.py',
        'requirements.txt',
        'pyproject.toml',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    missing = []
    for item in critical_dirs:
        if os.path.exists(item):
            # Check if it would be included
            if should_include(item, ignore_patterns):
                print(f"  ✓ {item}")
            else:
                print(f"  ⚠️  {item} (EXISTS but EXCLUDED by ignore patterns)")
                missing.append(item)
        else:
            print(f"  ✗ {item} (MISSING)")
            missing.append(item)
    
    if missing:
        print(f"\n⚠️  Warning: {len(missing)} critical items are missing or excluded!")
    else:
        print(f"\n✅ All critical template items are present and will be included!")
    
    # Check for conflicts
    print("\n" + "=" * 70)
    print("Conflict Check:")
    print("=" * 70)
    
    conflicts = []
    if os.path.exists('main') and should_include('main', ignore_patterns):
        conflicts.append('main/ (conflicts with {{cookiecutter.main_app_name}}/)')
    if os.path.exists('base') and should_include('base', ignore_patterns):
        conflicts.append('base/ (conflicts with {{cookiecutter.project_slug}}/)')
    if os.path.exists('demo'):
        conflicts.append('demo/ (test directory, should be excluded)')
    
    if conflicts:
        print("  ⚠️  Conflicts found:")
        for conflict in conflicts:
            print(f"    - {conflict}")
    else:
        print("  ✅ No conflicts detected!")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
