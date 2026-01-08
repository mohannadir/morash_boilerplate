# CookieCutter Template Setup Instructions

This document explains how to properly set up this codebase as a cookiecutter template.

## Important Note About Directory Names

Cookiecutter supports variable substitution in directory names, but you need to manually rename directories in the template to use the `{{cookiecutter.variable}}` syntax.

## Setup Steps

### 1. Rename Directories

You need to rename the following directories to use cookiecutter variables:

1. **Rename `base/` to `{{cookiecutter.project_slug}}/`**
   - This is the main Django project directory
   - On Windows, you may need to use a script or rename manually after creating the template

2. **Rename `main/` to `{{cookiecutter.main_app_name}}/`**
   - This is the main Django app directory
   - Same note about Windows applies

### 2. How to Rename on Windows

Since Windows doesn't allow `{{` in directory names directly, you have two options:

#### Option A: Use a Script
Create a script that renames directories after you've set up the template structure.

#### Option B: Manual Process
1. Create the template in a location where you can work with it
2. Use a tool that supports the `{{` syntax, or
3. After someone generates a project from the template, they can manually rename if needed

### 3. Template Structure

The final template structure should look like:

```
cookiecutter-template/
├── cookiecutter.json
├── hooks/
│   └── post_gen_project.py
├── {{cookiecutter.project_slug}}/    # Renamed from 'base'
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── {{cookiecutter.main_app_name}}/   # Renamed from 'main'
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── ...
├── CONFIG/
├── modules/
├── requirements.txt
└── ...
```

### 4. Using the Template

Once set up, users can generate a new project with:

```bash
cookiecutter /path/to/this/template
```

Or if published:

```bash
cookiecutter https://github.com/yourusername/your-template-repo
```

## Alternative: Directory Renaming Script

If you can't rename directories with `{{` syntax, you can use this approach:

1. Keep directories as `base/` and `main/` in the template
2. In the post-generation hook, rename them programmatically
3. Update the hook script to read cookiecutter context and rename accordingly

The hook script (`hooks/post_gen_project.py`) includes logic to handle this, but cookiecutter's directory renaming should work automatically if the directories are properly named in the template.

## Testing the Template

To test your template:

1. Create a test directory outside your template
2. Run: `cookiecutter /path/to/template`
3. Answer the prompts
4. Verify that:
   - All `{{cookiecutter.variable}}` references were replaced
   - Directories were renamed correctly
   - The project runs without errors

## Publishing the Template

If you want to publish this template:

1. Create a GitHub repository
2. Push your template code
3. Users can then use:
   ```bash
   cookiecutter https://github.com/yourusername/your-template-repo
   ```

Or for a specific branch/tag:
```bash
cookiecutter https://github.com/yourusername/your-template-repo --checkout v1.0.0
```
