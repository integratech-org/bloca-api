SHELL := /bin/bash
.SHELLFLAGS := -uc
.DEFAULT_GOAL := help

PY := uv run python manage.py
PORT ?= 8000

.PHONY: help
help: ## List all targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-22s %s\n", $$1, $$2}'


# ==========================================
# Setup commands
# ==========================================

.PHONY: setup
setup: ## Run setup script
	@./scripts/setup.sh


# ==========================================
# Dev commands
# ==========================================

.PHONY: run shell manage
run: ## Run dev server (make run PORT=3000)
	$(PY) runserver $(PORT)

shell: ## Django shell
	$(PY) shell

manage: ## Catch-all (make manage ARGS="showmigrations")
	$(PY) $(ARGS)


# ==========================================
# Database commands
# ==========================================

.PHONY: makemigrations migrate showmigrations
makemigrations: ## Make migrations (make makemigrations ARGS="blog")
	$(PY) makemigrations $(ARGS)

migrate: ## Apply migrations
	$(PY) migrate $(ARGS)

showmigrations: ## Show migrations
	$(PY) showmigrations $(ARGS)


# ==========================================
# Test and quality commands
# ==========================================

.PHONY: test fmt lint
test: ## Run tests (make test ARGS="blog --keepdb")
	$(PY) test $(ARGS)

fmt: ## Format and autofix
	uv run ruff format .
	uv run ruff check --fix .

lint: ## Lint only
	uv run ruff check .


# ===========================================
# Pre-commit Hooks
# ===========================================

.PHONY: pre-commit-install pre-commit-update pre-commit-all
pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install

pre-commit-update: ## Update pre-commit hooks to latest versions
	uv run pre-commit autoupdate

pre-commit-all: ## Run pre-commit on all files
	uv run pre-commit run --all-files
