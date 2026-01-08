# Fix: Template Only Including "main" App

## Problem
When using the cookiecutter template, only the `main/` directory is being generated, not the full template.

## Root Cause
The old `main/` directory is still tracked in git and conflicts with `{{cookiecutter.main_app_name}}/`. CookieCutter is seeing both and may be prioritizing the regular `main/` directory.

## Solution Applied

### 1. Updated `.cookiecutterignore`
Added patterns to exclude old directories:
```
main/
demo/
base/
```

### 2. Updated `.gitignore`
Added patterns to prevent committing old directories:
```
main/
base/
demo/
```

## What Needs to Be Done

### Option A: Remove from Git (Recommended)
If `main/`, `base/`, and `demo/` are old directories that shouldn't be in the template:

```bash
# Remove from git tracking (but keep locally)
git rm -r --cached main/ base/ demo/

# Commit the removal
git commit -m "Remove old directories from template (use cookiecutter variables instead)"

# Push
git push
```

### Option B: Keep but Exclude
If you want to keep them locally but exclude from template:

1. Ensure they're in `.cookiecutterignore` ✅ (already done)
2. Ensure they're in `.gitignore` ✅ (already done)
3. They won't be included in the template

## Verification

After fixing, test the template:

```bash
# Clear cache
Remove-Item -Recurse -Force C:\Users\mohan\.cookiecutters\morash_boilerplate

# Test locally
cookiecutter C:\Users\mohan\PycharmProjects\codebase

# Or test from GitHub
cookiecutter https://github.com/mohannadir/morash_boilerplate.git
```

## Expected Result

The generated project should include:
- ✅ `{project_slug}/` (renamed from `{{cookiecutter.project_slug}}`)
- ✅ `{main_app_name}/` (renamed from `{{cookiecutter.main_app_name}}`)
- ✅ `api/`
- ✅ `CONFIG/`
- ✅ `modules/`
- ✅ `theme/`
- ✅ `websockets/`
- ✅ `manage.py`
- ✅ `requirements.txt`
- ✅ `pyproject.toml`
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ All other template files

And should NOT include:
- ❌ `main/` (old directory)
- ❌ `base/` (old directory)
- ❌ `demo/` (test directory)
