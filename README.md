# Django Platform CookieCutter Template

A comprehensive Django project template with authentication, billing, payments, websockets, and more.

## Features

- 🔐 Authentication (email-based, social login, MFA)
- 💳 Billing system (subscriptions, credits, or both)
- 💰 Stripe integration for payments
- 📧 Email system with task queue support
- 🌐 WebSockets support
- 🎨 Modern admin panel with Unfold
- 🌍 Internationalization (i18n) support
- 📱 Responsive UI with Tailwind CSS
- 🐳 Docker support
- 🔄 Task queue with Huey
- 📊 API with JWT authentication
- ⚡ **UV** for fast Python package management

## Prerequisites

- Python 3.10+
- **uv** (recommended) - Fast Python package installer. Install with:
  ```bash
  # On macOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # On Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  
  # Or via pip
  pip install uv
  ```
- Docker and Docker Compose (optional, for containerized setup)
- Node.js and npm (for Tailwind CSS)

## Usage

### Using This Template

1. Install cookiecutter if you haven't already:
   ```bash
   # Using uv (recommended)
   uv pip install cookiecutter
   
   # Or using pip
   pip install cookiecutter
   ```

2. Generate a new project from this template:
   ```bash
   cookiecutter .
   ```
   
   Or if this template is in a repository:
   ```bash
   cookiecutter https://github.com/yourusername/your-template-repo
   ```

3. Follow the prompts to configure your project:
   - `project_name`: Your project name (e.g., "myproject")
   - `platform_name`: Display name for your platform
   - `platform_tagline`: Tagline for your platform
   - `platform_version`: Initial version number
   - `platform_url`: Base URL for your platform
   - `main_app_name`: Name of your main Django app
   - `database_name`: PostgreSQL database name
   - `author_name`: Your name
   - `author_email`: Your email

   **Note:** If you encounter a `TemplateSyntaxError` about Django templates, this is normal. The `.cookiecutterignore` file excludes Django template files (`.html`) from cookiecutter processing since they use Django's template syntax, not Jinja2. See `COOKIECUTTER_TROUBLESHOOTING.md` for more details.

4. **Important**: After generation, if directories weren't automatically renamed:
   - Rename the `base` directory to your `project_slug` (from cookiecutter prompt)
   - Rename the `main` directory to your `main_app_name` (from cookiecutter prompt)
   
   Note: Modern cookiecutter versions should handle directory renaming automatically if the template directories are named with `{{cookiecutter.variable}}` syntax. See `TEMPLATE_SETUP.md` for template setup instructions.

### Manual Setup

If cookiecutter doesn't automatically rename directories, you can manually:

1. Rename `base/` to `{{your_project_slug}}/`
2. Rename `main/` to `{{your_main_app_name}}/`

### Post-Generation Setup

After generating your project:

1. **Set up environment variables:**
   - Copy `.env.example` to `.env` (if available)
   - Configure your secrets in `CONFIG/secrets.py` or use environment variables

2. **Install dependencies:**
   ```bash
   # Using uv (recommended - faster)
   uv pip install -r requirements.txt
   
   # Or using uv with pyproject.toml
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Set up Tailwind CSS:**
   ```bash
   python manage.py tailwind install
   python manage.py tailwind start
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Build and start containers:**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations:**
   ```bash
   docker-compose exec django python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

## Configuration

### Platform Settings

Edit `CONFIG/platform.py` to customize:
- Platform name and tagline
- Platform version
- Platform URL

### Billing Configuration

Edit `CONFIG/billing.py` to configure:
- Billing model (subscriptions, credits, both, or none)
- Subscription plans
- Credit packages

### Authentication Settings

Edit `CONFIG/authentication.py` to configure:
- Social login providers (GitHub, LinkedIn)
- Registration settings
- MFA settings

### Email Configuration

Edit `CONFIG/emails.py` to configure:
- Email provider (SMTP, SendGrid, etc.)
- Email settings

### Secrets Management

The project uses a secrets manager that supports:
- Environment variables
- AWS Secrets Manager
- Azure Key Vault
- Infisical

Configure in `CONFIG/secrets.py`.

## Project Structure

```
{{cookiecutter.project_slug}}/
├── {{cookiecutter.main_app_name}}/          # Main Django app
├── api/                                      # API endpoints
├── CONFIG/                                   # Configuration files
├── modules/                                  # Reusable modules
│   ├── authentication/                      # Auth module
│   ├── billing/                             # Billing module
│   ├── payments/                            # Payments module
│   ├── emails/                              # Email module
│   └── ...
├── theme/                                    # Tailwind CSS theme
├── static/                                   # Static files
├── media/                                    # Media files
├── locale/                                   # Translation files
├── pyproject.toml                            # Python project configuration (uv/pip)
└── requirements.txt                          # Python dependencies (backward compatibility)
```

## Modules

### Authentication Module
- Email-based authentication
- Social login (GitHub, LinkedIn)
- Multi-factor authentication (MFA)
- Password reset and change

### Billing Module
- Subscription management
- Credit system
- Stripe integration

### Payments Module
- Stripe checkout
- Webhook handling
- Payment processing

### Examples Module
- Example views and templates
- Can be removed if not needed

## Development

### Running Tests
```bash
# Using uv (recommended)
uv run python manage.py test

# Or activate virtual environment first
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
python manage.py test
```

### Making Migrations
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Collecting Static Files
```bash
uv run python manage.py collectstatic
```

### Translations
```bash
python manage.py makemessages -l <language_code>
python manage.py compilemessages
```

## License

[Your License Here]

## Support

[Your Support Information Here]
