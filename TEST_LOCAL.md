# Testing CookieCutter Template Locally

## Quick Test Commands

### 1. Test from Local Directory

```bash
# Create a test directory
cd C:\Users\mohan\PycharmProjects
mkdir test_cookiecutter
cd test_cookiecutter

# Run cookiecutter from local template
cookiecutter C:\Users\mohan\PycharmProjects\codebase
```

### 2. Verify Generated Structure

After generation, check that you have:
- ✅ `{project_slug}/` directory (not `base/`)
- ✅ `{main_app_name}/` directory (not `main/`)
- ✅ `api/` directory
- ✅ `CONFIG/` directory
- ✅ `modules/` directory
- ✅ `theme/` directory
- ✅ `websockets/` directory
- ✅ `manage.py`
- ✅ `requirements.txt`
- ✅ `pyproject.toml`
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`

### 3. Test from GitHub (After Pushing)

```bash
# Clear cache first
Remove-Item -Recurse -Force C:\Users\mohan\.cookiecutters\morash_boilerplate

# Test from GitHub
cookiecutter https://github.com/mohannadir/morash_boilerplate.git
```

## Expected Behavior

When you run cookiecutter:
1. It should prompt for all variables
2. It should generate the full project structure
3. It should NOT include `main/`, `base/`, or `demo/` directories
4. HTML files should be copied without errors (no TemplateSyntaxError)

## Troubleshooting

If only `main/` is generated:
- Check that `main/` is removed from git: `git ls-files | grep "^main/"`
- Verify `.cookiecutterignore` includes `main/`
- Clear cookiecutter cache and try again

If TemplateSyntaxError occurs:
- Verify `_copy_without_render` is in `cookiecutter.json`
- Check that HTML files are listed in the patterns
