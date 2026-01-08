# Testing the CookieCutter Template

## Quick Test Commands

### 1. Commit and Push (if not done)
```bash
git add -A
git commit -m "Complete fix: Restore main/ and ensure full template generation"
git push
```

### 2. Clear Cache
```bash
Remove-Item -Recurse -Force C:\Users\mohan\.cookiecutters\morash_boilerplate
```

### 3. Test from Demo Folder
```bash
cd C:\Users\mohan\PycharmProjects\demo
cookiecutter https://github.com/mohannadir/morash_boilerplate.git
```

## What Should Happen

1. CookieCutter prompts for variables:
   - project_name
   - project_slug
   - platform_name
   - main_app_name
   - etc.

2. After answering prompts, cookiecutter should generate:
   - ✅ `{project_slug}/` directory
   - ✅ `{main_app_name}/` directory
   - ✅ `api/` directory
   - ✅ `CONFIG/` directory
   - ✅ `modules/` directory
   - ✅ `theme/` directory
   - ✅ `websockets/` directory
   - ✅ All root files (manage.py, requirements.txt, etc.)
   - ❌ NO `main/` directory (excluded)

## Verification

After generation, check the created project:
```bash
cd {project_name}  # or whatever you named it
ls  # or dir on Windows
```

You should see all directories listed above.

## Troubleshooting

### If only main/ is generated:
1. Check that `.cookiecutterignore` is in GitHub
2. Verify `main/` is listed in `.cookiecutterignore`
3. Clear cache and try again
4. Check cookiecutter version: `cookiecutter --version` (should be 2.0+)

### If TemplateSyntaxError occurs:
1. Verify `_copy_without_render` is in `cookiecutter.json`
2. Check that HTML files are listed in the patterns
3. Clear cache and try again

### If directories are missing:
1. Verify all directories are in GitHub repository
2. Check that they're not in `.cookiecutterignore`
3. Verify template directories use correct syntax: `{{cookiecutter.variable}}`
