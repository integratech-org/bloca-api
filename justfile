set dotenv-load := true
set shell := ["bash", "-uc"]

py := "uv run python manage.py"

# List all recipes
default:
  @just --list


# ==========================================
# Setup commands
# ==========================================

# Run setup script
setup:
  ./scripts/setup.sh


# ==========================================
# Dev commands
# ==========================================

# Run dev server (just run 3000)
run port="8000":
  {{py}} runserver {{port}}

# Django shell
shell:
  {{py}} shell

# Catch-all (just manage showmigrations)
manage *args:
  {{py}} {{args}}


# ==========================================
# Database commands
# ==========================================

# Make migrations (just makemigrations blog)
makemigrations *args:
  {{py}} makemigrations {{args}}

# Apply migrations
migrate *args:
  {{py}} migrate {{args}}

# Show migrations
showmigrations *args:
  {{py}} showmigrations {{args}}

# ==========================================
# Test and quality commands
# ==========================================

# Run tests (just test blog --keepdb)
test *args:
  {{py}} test {{args}}

# Format and autofix
fmt:
  uv run ruff format .
  uv run ruff check --fix .

# Lint only
lint:
  uv run ruff check .


# ===========================================
# Pre-commit Hooks
# ===========================================

# Install pre-commit hooks
pre-commit-install:
  uv run pre-commit install

# Update pre-commit hooks to latest versions
pre-commit-update:
  uv run pre-commit autoupdate

# Run pre-commit on all files
pre-commit-all:
  uv run pre-commit run --all-files
