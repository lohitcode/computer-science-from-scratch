# FastAPI CRUD Makefile

.PHONY: all install run db-up db-down db-logs db-shell clean help

# Default: show menu
all: help

# Install dependencies
install:
	@pip install -r requirements.txt

# Run the app
run:
	@uvicorn app.main:app --reload

# Start PostgreSQL
db-up:
	@docker-compose up -d

# Stop PostgreSQL
db-down:
	@docker-compose down

# View PostgreSQL logs
db-logs:
	@docker-compose logs -f db

# Connect to PostgreSQL shell
db-shell:
	@docker exec -it fastapi_postgres psql -U myuser -d mydb

# Reset database (WARNING: deletes all data)
db-reset:
	@docker-compose down -v
	@docker-compose up -d

# Help
help:
	@echo "FastAPI CRUD - Quick Commands"
	@echo ""
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Start the server"
	@echo "  make db-up    - Start PostgreSQL"
	@echo "  make db-down  - Stop PostgreSQL"
	@echo "  make db-logs  - View PostgreSQL logs"
	@echo "  make db-shell - Connect to PostgreSQL"
	@echo "  make db-reset - Reset database (deletes data)"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make db-up"
	@echo "  2. make install"
	@echo "  3. make run"
