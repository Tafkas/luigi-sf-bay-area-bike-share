create-virtualenv: ## Creates a Python virtual environment and installs all dependencies
	@echo "Create virtalenv"
	@rm -rf .venv
	@virtualenv -p /usr/local/bin/python2 .venv
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install -r requirements.txt

create-postgres-db: ## Creates a PostgreSQL database with necessary structure
	@echo "Create PostgreSQL sfbike database"
	@echo "select pg_terminate_backend(pid) from pg_stat_activity where pid <> pg_backend_pid() AND datname='sfbike';" | psql postgres
	@echo "drop database sfbike; create database sfbike" | psql postgres

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
