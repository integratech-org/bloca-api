# Setup Guide — Bloca Backend API (`bloca-api`)

Follow these instructions to set up, configure, and run `bloca-api` locally.

## Prerequisites

- **Python**: Version 3.14 or higher
- **Package Manager**: `uv`
- **Database**: PostgreSQL (running locally or via Docker Compose)
- **Make**: (optional) For running Makefile shortcuts

## Installation & Configuration

1. Navigate to the project directory:
   ```bash
   cd bloca-api
   ```

2. Run the development environment setup. This installs pre-commit hooks and checks system requirements:
   ```bash
   make setup
   # or run the script directly:
   ./scripts/setup.sh
   ```

3. Copy the environment configuration template:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to configure your database credentials and environment variables.*

4. Install python dependencies using `uv`:
   ```bash
   uv sync
   ```

## Database Migration

Run database migrations to set up the schema:

```bash
uv run python manage.py migrate
```

## Running the Development Server

Start the API development server:

```bash
uv run python manage.py runserver
# or via uvicorn/main
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` (with interactive API docs at `/docs`).

## Code Quality, Linting & Pre-commit

- **Pre-commit Hooks Management (via Makefile):**
  - Install pre-commit hooks:
    ```bash
    make pre-commit-install
    ```
  - Run pre-commit checks on all files:
    ```bash
    make pre-commit-all
    ```
  - Update pre-commit hooks to their latest versions:
    ```bash
    make pre-commit-update
    ```

- **Manual Code Quality Checks:**
  - **Linting (Ruff):**
    ```bash
    uv run ruff check .
    ```
  - **Type Checking (Mypy):**
    ```bash
    uv run mypy .
    ```
  - **Running Tests:**
    ```bash
    uv run python manage.py test
    ```
