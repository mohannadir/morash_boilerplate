import os
import json
from pathlib import Path

# Read cookiecutter.json
with open('cookiecutter.json') as f:
    config = json.load(f)

print("CookieCutter Configuration:")
print(f"  Project name: {config.get('project_name')}")
print(f"  Main app name: {config.get('main_app_name')}")
print(f"\nCopy without render patterns:")
for pattern in config.get('_copy_without_render', []):
    print(f"  - {pattern}")

# Check template directories
template_dirs = [
    '{{cookiecutter.project_slug}}',
    '{{cookiecutter.main_app_name}}',
    'api',
    'CONFIG',
    'modules',
    'theme',
    'websockets'
]

print("\nTemplate Directories:")
for dir_name in template_dirs:
    if os.path.exists(dir_name):
        print(f"  ✓ {dir_name}/")
    else:
        print(f"  ✗ {dir_name}/ MISSING")

# Check excluded directories
excluded_dirs = ['main', 'base', 'demo']
print("\nExcluded Directories (should not be in template):")
for dir_name in excluded_dirs:
    if os.path.exists(dir_name):
        print(f"  ⚠️  {dir_name}/ EXISTS (should be excluded)")
    else:
        print(f"  ✓ {dir_name}/ not present")
