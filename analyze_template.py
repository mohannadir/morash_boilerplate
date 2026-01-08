import os
import subprocess
import tempfile
import shutil

# Simulate what cookiecutter sees
print("=" * 70)
print("CookieCutter Template Analysis")
print("=" * 70)

# Check what's in git
result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
files = result.stdout.strip().split('\n')

# Group by top-level directory
dirs = set()
for file in files:
    if file:
        top_dir = file.split('/')[0]
        if not top_dir.startswith('.'):
            dirs.add(top_dir)

print("\n📁 Directories cookiecutter will see from git:")
for d in sorted(dirs):
    if d == 'main':
        print(f"  ⚠️  {d}/ (CONFLICTS - should be removed!)")
    elif 'cookiecutter' in d:
        print(f"  ✓ {d}/ (template variable)")
    elif d in ['hooks', 'locale', 'logs', 'demo']:
        print(f"  - {d}/ (ignored/excluded)")
    else:
        print(f"  ✓ {d}/")

# Check for main/ specifically
main_files = [f for f in files if f.startswith('main/')]
if main_files:
    print(f"\n⚠️  PROBLEM: {len(main_files)} files in main/ are still in git!")
    print("   These need to be removed and committed.")
else:
    print("\n✅ main/ is NOT in git repository")
