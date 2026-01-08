# CookieCutter Troubleshooting Guide

## Issue: TemplateSyntaxError with Django Templates

### Problem
When running `cookiecutter`, you may encounter an error like:
```
jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'load'.
```

This happens because cookiecutter uses Jinja2 to process template files, but Django template files (`.html`) use Django's own template syntax which is incompatible with Jinja2.

### Solution
The `.cookiecutterignore` file has been created to exclude Django template files from cookiecutter processing. This file tells cookiecutter to skip:
- All `.html` files (Django templates)
- Migration files (auto-generated)
- Other build artifacts

### Verification
Make sure `.cookiecutterignore` exists in the template root directory and contains:
```
*.html
**/*.html
**/templates/**/*.html
```

### How It Works
- Cookiecutter will still process directory names with `{{cookiecutter.variable}}` syntax
- Cookiecutter will process Python files and other text files
- Cookiecutter will skip HTML files, so Django can process them with its own template engine

### If Issues Persist

1. **Check cookiecutter version:**
   ```bash
   cookiecutter --version
   ```
   Make sure you're using a recent version (2.0+)

2. **Verify .cookiecutterignore location:**
   The file must be in the template root directory (same level as `cookiecutter.json`)

3. **Try explicit ignore:**
   If patterns don't work, you can also rename template files temporarily or use a different approach

4. **Check for cookiecutter variables in HTML:**
   HTML files should NOT contain `{{cookiecutter.*}}` variables. If they do, you'll need to escape them or use a different approach.

## Other Common Issues

### Directory Names Not Renaming
If directories with `{{cookiecutter.variable}}` syntax aren't being renamed:
- Make sure cookiecutter version is 2.0+
- Check that directory names use the exact syntax: `{{cookiecutter.variable_name}}`
- Verify the variable exists in `cookiecutter.json`

### Variables Not Replacing
If `{{cookiecutter.variable}}` isn't being replaced:
- Check `cookiecutter.json` has the variable defined
- Verify the syntax is correct (no spaces: `{{cookiecutter.var}}` not `{{ cookiecutter.var }}`)
- Make sure the file isn't in `.cookiecutterignore`

### Permission Errors
If you get permission errors:
- Check file/directory permissions
- On Windows, make sure you're not running from a protected directory
- Try running as administrator if needed

## Getting Help

If you continue to experience issues:
1. Check the [CookieCutter documentation](https://cookiecutter.readthedocs.io/)
2. Review the error message carefully
3. Verify all files are in the correct locations
4. Test with a minimal template first
