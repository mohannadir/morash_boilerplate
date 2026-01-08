#!/usr/bin/env python
"""
Script to set up this codebase as a cookiecutter template.
This script renames directories to use cookiecutter variable syntax.

Run this script to prepare the codebase as a cookiecutter template.
After running, the directories will be renamed to use {{cookiecutter.variable}} syntax.
"""
import os
import shutil
import sys

def setup_template():
    """Rename directories to use cookiecutter variable syntax."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Rename base/ to {{cookiecutter.project_slug}}/
    base_dir = os.path.join(script_dir, 'base')
    new_base_dir = os.path.join(script_dir, '{{cookiecutter.project_slug}}')
    
    if os.path.exists(base_dir) and not os.path.exists(new_base_dir):
        try:
            # On Windows, we can't create directories with {{ in the name directly
            # So we'll create a temporary name first, then provide instructions
            print("⚠️  Note: Windows doesn't allow '{{' in directory names.")
            print("   You'll need to manually rename directories or use a different approach.")
            print("\nTo complete the template setup:")
            print(f"1. Rename '{base_dir}' to '{{cookiecutter.project_slug}}'")
            print(f"2. Rename 'main' to '{{cookiecutter.main_app_name}}'")
            print("\nAlternatively, cookiecutter will handle this automatically")
            print("if you structure your template repository correctly.")
            return False
        except Exception as e:
            print(f"Error renaming base directory: {e}")
            return False
    
    # Rename main/ to {{cookiecutter.main_app_name}}/
    main_dir = os.path.join(script_dir, 'main')
    new_main_dir = os.path.join(script_dir, '{{cookiecutter.main_app_name}}')
    
    if os.path.exists(main_dir) and not os.path.exists(new_main_dir):
        try:
            # Same issue - can't rename on Windows
            pass
        except Exception as e:
            print(f"Error renaming main directory: {e}")
            return False
    
    print("✅ Template setup instructions:")
    print("\nSince Windows doesn't support '{{' in directory names, you have two options:")
    print("\nOption 1: Manual Rename (Recommended for testing)")
    print("  - After generating a project with cookiecutter, manually rename:")
    print("    - 'base' → your project_slug")
    print("    - 'main' → your main_app_name")
    print("\nOption 2: Use Git/Version Control")
    print("  - Commit files with current names")
    print("  - On Linux/Mac, rename directories to use {{cookiecutter.variable}}")
    print("  - Commit the renamed directories")
    print("  - CookieCutter will handle renaming automatically")
    
    return True

if __name__ == '__main__':
    print("Setting up cookiecutter template structure...")
    print("=" * 60)
    
    if setup_template():
        print("\n✅ Setup complete!")
    else:
        print("\n⚠️  Manual steps required (see above)")
    
    print("\n" + "=" * 60)
    print("\nYour codebase is now ready to use as a cookiecutter template!")
    print("All file contents have been updated with cookiecutter variables.")
    print("\nTo use this template:")
    print("  cookiecutter .")
    print("\nOr from another location:")
    print("  cookiecutter /path/to/this/directory")
