#!/usr/bin/env python
"""
Post-generation hook for cookiecutter.
This script handles any post-generation tasks and verifies the setup.
"""
import os
import sys

def main():
    """Post-generation tasks."""
    # Get the project directory
    # In cookiecutter hooks, the current directory is the generated project root
    project_dir = os.getcwd()
    
    print("=" * 60)
    print("CookieCutter Post-Generation Setup")
    print("=" * 60)
    
    # Verify critical directories exist
    print("\n✓ Verifying project structure...")
    
    # Check for project settings directory (should be renamed from base)
    settings_files = [f for f in os.listdir(project_dir) 
                     if os.path.isdir(os.path.join(project_dir, f)) 
                     and os.path.exists(os.path.join(project_dir, f, 'settings.py'))]
    
    if settings_files:
        settings_dir = settings_files[0]
        print(f"  ✓ Found settings directory: {settings_dir}")
    else:
        print("  ⚠️  Warning: Could not find settings directory")
    
    # Check for main app directory (should be renamed from main)
    app_dirs = [f for f in os.listdir(project_dir) 
               if os.path.isdir(os.path.join(project_dir, f)) 
               and os.path.exists(os.path.join(project_dir, f, 'models.py'))
               and os.path.exists(os.path.join(project_dir, f, 'views.py'))]
    
    if app_dirs:
        main_app = app_dirs[0]
        print(f"  ✓ Found main app directory: {main_app}")
    else:
        print("  ⚠️  Warning: Could not find main app directory")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("\n1. Review and update configuration files in CONFIG/")
    print("   - CONFIG/platform.py - Platform name and settings")
    print("   - CONFIG/billing.py - Billing configuration")
    print("   - CONFIG/authentication.py - Auth settings")
    print("   - CONFIG/secrets.py - Secret management setup")
    print("\n2. Set up your environment variables or secrets")
    print("   - Configure database credentials")
    print("   - Set up API keys (Stripe, OpenAI, etc.)")
    print("\n3. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n4. Set up the database:")
    print("   python manage.py migrate")
    print("\n5. Create a superuser:")
    print("   python manage.py createsuperuser")
    print("\n6. Set up Tailwind CSS:")
    print("   python manage.py tailwind install")
    print("   python manage.py tailwind start  # In a separate terminal")
    print("\n7. Run the development server:")
    print("   python manage.py runserver")
    print("\n" + "=" * 60)
    print("For Docker setup, see README.md")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n⚠️  Error during post-generation: {e}", file=sys.stderr)
        print("You can continue with manual setup. See README.md for instructions.")
        sys.exit(0)  # Don't fail the generation, just warn
