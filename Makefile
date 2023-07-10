# start: install-prod run
start: run-lint run
default: start

# Freezing the dependencies
freeze:
	@echo "Freezing all dependencies"
	pipenv requirements --dev > requirements/common.txt
dev:
	@echo "Freezing dependencies for development"
	pipenv requirements --dev-only > requirements/dev.txt
prod:
	@echo "Freezing dependencies for production"
	pipenv requirements > requirements/prod.txt

# Running server
run:
	@echo "Running server with gunicorn"
	pipenv run gunicorn --bind 0.0.0.0:8000 --workers=5 --threads=2 main:app
run-dev:
	pipenv run python main.py
run-docs:
	pipenv run streamlit run labs/streamlit.py

# Running linter with pylint
run-lint:
	@echo "Running linter..."
	pipenv run pylint ./**/*.py
run-lint-git:
	@echo "Running linter in all git files..."
	pipenv run pylint $(git ls-files '*.py')

# Installing required dependencies
install:
	@echo "Installing all dependencies"
	pipenv install -r requirements/common.txt
install-dev:
	@echo "Installing dependencies for development"
	pipenv install -r requirements/dev.txt
install-prod:
	@echo "Installing dependencies for production"
	pipenv install -r requirements/prod.txt

# Database migration
migration:
	@echo "Migrating database"
	pipenv run python migration.py
