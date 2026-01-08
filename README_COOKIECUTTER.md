# CookieCutter Template - Complete Setup Guide

## ✅ Current Status

The template is now fully configured:

- ✅ `main/` directory restored in repository (for your reference)
- ✅ `main/` excluded from cookiecutter generation (via `.cookiecutterignore`)
- ✅ `{{cookiecutter.main_app_name}}/` - Template directory (will be renamed)
- ✅ `{{cookiecutter.project_slug}}/` - Template directory (will be renamed)
- ✅ All other directories included (api/, CONFIG/, modules/, theme/, websockets/)
- ✅ HTML files handled via `_copy_without_render`
- ✅ All configuration files in place

## How to Use

### For Template Users

1. **Install cookiecutter:**
   ```bash
   pip install cookiecutter
   # or
   uv pip install cookiecutter
   ```

2. **Generate a project:**
   ```bash
   cookiecutter https://github.com/mohannadir/morash_boilerplate.git
   ```

3. **Follow the prompts:**
   - Enter your project name
   - Enter your main app name
   - Configure other settings

4. **Result:**
   - Full Django project with all modules
   - Customized with your project/app names
   - Ready to use!

### For Template Maintainer

1. **Keep `main/` in repository:**
   - It's excluded from cookiecutter via `.cookiecutterignore`
   - Useful for reference or local development

2. **Template directories:**
   - `{{cookiecutter.main_app_name}}/` - Gets renamed to user's app name
   - `{{cookiecutter.project_slug}}/` - Gets renamed to user's project name

3. **To update template:**
   - Edit files in template directories
   - Update `cookiecutter.json` for new variables
   - Commit and push changes

## What Gets Generated

When someone uses the template, they get:

✅ **Directories:**
- `{project_slug}/` - Main Django project directory
- `{main_app_name}/` - Main Django app
- `api/` - API endpoints
- `CONFIG/` - Configuration files
- `modules/` - Reusable modules
- `theme/` - Tailwind CSS theme
- `websockets/` - WebSocket support

✅ **Files:**
- `manage.py`
- `requirements.txt`
- `pyproject.toml`
- `Dockerfile`
- `docker-compose.yml`
- All other template files

❌ **NOT Generated:**
- `main/` - Excluded (user gets `{main_app_name}/` instead)
- `demo/` - Excluded
- `base/` - Excluded

## Troubleshooting

### Issue: Only main/ is generated
**Solution:** 
1. Verify `.cookiecutterignore` is in GitHub
2. Check that `main/` is listed in ignore patterns
3. Clear cache: `Remove-Item -Recurse -Force C:\Users\mohan\.cookiecutters\morash_boilerplate`
4. Try again

### Issue: TemplateSyntaxError
**Solution:**
1. Verify `_copy_without_render` is in `cookiecutter.json`
2. Check HTML files are in the patterns
3. This should already be fixed ✅

### Issue: Missing directories
**Solution:**
1. Verify all directories are in GitHub
2. Check they're not in `.cookiecutterignore`
3. Ensure template directories use `{{cookiecutter.variable}}` syntax

## Configuration Files

- **`cookiecutter.json`** - Template variables and `_copy_without_render`
- **`.cookiecutterignore`** - Excludes `main/`, `demo/`, `base/`, and HTML files
- **`hooks/post_gen_project.py`** - Post-generation instructions

## Next Steps

1. **Push commits:**
   ```bash
   git push
   ```

2. **Test the template:**
   ```bash
   cd C:\Users\mohan\PycharmProjects\demo
   Remove-Item -Recurse -Force C:\Users\mohan\.cookiecutters\morash_boilerplate
   cookiecutter https://github.com/mohannadir/morash_boilerplate.git
   ```

3. **Verify:**
   - Full template is generated
   - No `main/` directory in generated project
   - All directories present
   - No errors
