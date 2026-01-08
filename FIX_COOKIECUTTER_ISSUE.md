# Fix for CookieCutter TemplateSyntaxError

## Problem
When running cookiecutter from a Git repository, you get:
```
jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'load'.
```

This happens because cookiecutter tries to process Django template files (`.html`) with Jinja2, but Django templates use different syntax.

## Solution

### Step 1: Ensure `.cookiecutterignore` is Committed

The `.cookiecutterignore` file **must be committed to your Git repository** for it to work when someone clones the repo.

```bash
git add .cookiecutterignore
git commit -m "Add .cookiecutterignore to exclude Django templates"
git push
```

### Step 2: Verify the File is in the Repository

After committing, verify the file exists in your GitHub repository:
- Go to: `https://github.com/mohannadir/morash_boilerplate`
- Check that `.cookiecutterignore` is visible in the root directory

### Step 3: Clear CookieCutter Cache

If you've already tried to use the template, clear the cached version:

```bash
# On Windows
rmdir /s C:\Users\mohan\.cookiecutters\morash_boilerplate

# On Linux/Mac
rm -rf ~/.cookiecutters/morash_boilerplate
```

### Step 4: Try Again

After committing and pushing, try again:

```bash
cookiecutter https://github.com/mohannadir/morash_boilerplate.git
```

## Alternative Solution: Use `_copy_without_render`

If `.cookiecutterignore` still doesn't work, you can use cookiecutter's `_copy_without_render` feature by creating a directory structure like:

```
{{cookiecutter.main_app_name}}/
  _templates/  # Files here are copied without rendering
    {{cookiecutter.main_app_name}}/
      dashboard.html
      landing.html
```

Then in a post-generation hook, move the files to the correct location. However, this is more complex and the `.cookiecutterignore` approach should work.

## Verification

To verify `.cookiecutterignore` is working:

1. Check it's in the repo root (same level as `cookiecutter.json`)
2. Check it contains `*.html` patterns
3. Clear cookiecutter cache
4. Try generating a project

## Current Status

✅ `.cookiecutterignore` file created with comprehensive patterns
⚠️ **Needs to be committed to Git repository**
⚠️ **Cache needs to be cleared after committing**

## Next Steps

1. **Commit the file:**
   ```bash
   git add .cookiecutterignore
   git commit -m "Add .cookiecutterignore to fix Django template processing"
   git push
   ```

2. **Clear cache and test:**
   ```bash
   rmdir /s C:\Users\mohan\.cookiecutters\morash_boilerplate
   cookiecutter https://github.com/mohannadir/morash_boilerplate.git
   ```
