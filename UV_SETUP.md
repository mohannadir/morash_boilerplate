# UV Setup Guide

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

## What is UV?

UV is an extremely fast Python package installer and resolver written in Rust. It's a drop-in replacement for pip that's 10-100x faster.

## Installation

### macOS and Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Via pip
```bash
pip install uv
```

### Via Homebrew (macOS)
```bash
brew install uv
```

## Usage

### Installing Dependencies

**Option 1: Using pyproject.toml (Recommended)**
```bash
uv sync
```

This will:
- Create a virtual environment (if needed)
- Install all dependencies from `pyproject.toml`
- Install the project in editable mode

**Option 2: Using requirements.txt**
```bash
uv pip install -r requirements.txt
```

**Option 3: Install into existing virtual environment**
```bash
uv pip install --system -r requirements.txt
```

### Running Commands

You can run Python commands through uv:
```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

Or activate the virtual environment:
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Adding Dependencies

**Add a new dependency:**
```bash
uv add package-name
```

**Add a development dependency:**
```bash
uv add --dev package-name
```

**Add with version:**
```bash
uv add "package-name==1.2.3"
```

### Updating Dependencies

```bash
uv sync --upgrade
```

### Exporting to requirements.txt

If you need to generate requirements.txt from pyproject.toml:
```bash
uv pip compile pyproject.toml -o requirements.txt
```

## Docker Usage

The Dockerfiles are already configured to use uv. They will:
1. Install uv automatically
2. Use `uv pip install --system` to install dependencies

## Benefits of UV

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 📦 **Better caching** for faster subsequent installs
- 🎯 **Drop-in replacement** for pip commands
- 🔄 **Compatible** with existing pip workflows

## Migration from pip

If you're already using pip, you can switch to uv seamlessly:

1. Install uv (see above)
2. Replace `pip install` with `uv pip install`
3. Or use `uv sync` for projects with `pyproject.toml`

All your existing commands work the same way!

## Troubleshooting

### Virtual Environment Location

UV creates virtual environments in `.venv/` by default. To use a different location:
```bash
uv venv /path/to/venv
```

### System-wide Installation

For Docker or system-wide installations:
```bash
uv pip install --system -r requirements.txt
```

### Compatibility

UV is fully compatible with:
- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `Pipfile`

You can use uv alongside pip without any issues.

## More Information

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV GitHub](https://github.com/astral-sh/uv)
