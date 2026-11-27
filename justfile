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

# Run dev server on localhost (just run 3000)
[group('dev')]
run port="8000":
  {{py}} runserver 127.0.0.1:{{port}}

# Run dev server exposed on the network/LAN (just run-lan 3000)
[group('dev')]
run-lan port="8000":
  {{py}} runserver 0.0.0.0:{{port}}

# Run with Werkzeug debugger (django-extensions)
[group('dev')]
runplus port="8000":
  {{py}} runserver_plus 127.0.0.1:{{port}}

# Run with Werkzeug debugger, exposed on the network/LAN
[group('dev')]
runplus-lan port="8000":
  {{py}} runserver_plus 0.0.0.0:{{port}}

# Django shell (shell_plus auto-imports all models)
[group('dev')]
shell:
  {{py}} shell_plus

# Plain Django shell
[group('dev')]
shell-plain:
  {{py}} shell

# Open the database shell (psql/sqlite3)
[group('dev')]
dbshell:
  {{py}} dbshell

# Create a superuser
[group('dev')]
superuser:
  {{py}} createsuperuser

# Collect static files
[group('dev')]
collectstatic:
  {{py}} collectstatic --noinput

# Check the project for problems (just check --deploy)
[group('dev')]
check *args:
  {{py}} check {{args}}

# Catch-all (just manage showmigrations)
[group('dev')]
manage *args:
  {{py}} {{args}}


# ==========================================
# Database commands
# ==========================================

# Make migrations (just makemigrations blog)
[group('db')]
makemigrations *args:
  {{py}} makemigrations {{args}}

# Apply migrations
[group('db')]
migrate *args:
  {{py}} migrate {{args}}

# Show migrations
[group('db')]
showmigrations *args:
  {{py}} showmigrations {{args}}

# Check for missing migrations (good for CI)
[group('db')]
migrations-check:
  {{py}} makemigrations --check --dry-run

# Drop and recreate the schema, then migrate (Postgres) - DESTRUCTIVE
[group('db')]
[confirm("This will DELETE ALL data in the database schema. Continue?")]
reset-db:
  {{py}} reset_schema --noinput
  {{py}} migrate


# ==========================================
# django-extensions goodies
# ==========================================

# List all URLs
[group('extensions')]
urls:
  {{py}} show_urls

# Print effective settings (just settings DATABASES)
[group('extensions')]
settings *args:
  {{py}} diffsettings {{args}}

# Generate an ER diagram (needs graphviz + pydot)
[group('extensions')]
graph-models app="":
  {{py}} graph_models {{app}} -o models.png

# Validate templates
[group('extensions')]
validate-templates:
  {{py}} validate_templates

# Clear all Python cache files
[group('extensions')]
clean-pyc:
  {{py}} clean_pyc


# ==========================================
# Dependencies
# ==========================================

# Add a dependency (just add requests / just add --dev pytest)
[group('deps')]
add *args:
  uv add {{args}}

# Remove a dependency
[group('deps')]
remove *args:
  uv remove {{args}}

# Sync the environment from the lockfile
[group('deps')]
sync:
  uv sync

# Upgrade all dependencies
[group('deps')]
upgrade:
  uv lock --upgrade
  uv sync


# ==========================================
# Test and quality commands
# ==========================================

# Run tests (just test blog --keepdb)
[group('quality')]
test *args:
  {{py}} test {{args}}

# Run tests with coverage
[group('quality')]
cov *args:
  uv run coverage run manage.py test {{args}}
  uv run coverage report

# Format and autofix
[group('quality')]
fmt:
  uv run ruff format .
  uv run ruff check --fix .

# Lint only
[group('quality')]
lint:
  uv run ruff check .

# Full CI check: lint + format check + migrations + tests
[group('quality')]
ci:
  uv run ruff check .
  uv run ruff format --check .
  {{py}} makemigrations --check --dry-run
  {{py}} test --parallel


# ===========================================
# Pre-commit Hooks
# ===========================================

# Install pre-commit hooks
[group('hooks')]
pre-commit-install:
  uv run pre-commit install

# Update pre-commit hooks to latest versions
[group('hooks')]
pre-commit-update:
  uv run pre-commit autoupdate

# Run pre-commit on all files
[group('hooks')]
pre-commit-all:
  uv run pre-commit run --all-files
