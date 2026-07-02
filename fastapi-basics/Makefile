# FastAPI Basics Makefile

.PHONY: all install run help venv-check

# Check if venv exists
VENV_PATH = .venv
VENV_BIN = $(VENV_PATH)/bin

# Check if we're in venv
IN_VENV = $(shell echo $(VIRTUAL_ENV))

# Default: show menu
all: help

# Create venv if not exists
venv-check:
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "🔧 Creating virtual environment..."; \
		python3 -m venv $(VENV_PATH); \
		echo "✅ Virtual environment created!"; \
	fi

# Install dependencies (auto-creates venv if needed)
install: venv-check
	@echo "📦 Installing packages to $(VENV_PATH)..."
	@$(VENV_BIN)/pip install --upgrade pip
	@$(VENV_BIN)/pip install fastapi uvicorn
	@$(VENV_BIN)/pip freeze > requirements.txt
	@echo "✅ Done! Installed:"
	@$(VENV_BIN)/pip list | grep -E "fastapi|uvicorn"

# Run the server (auto-creates venv if needed)
run: venv-check
	@echo "🚀 Starting server..."
	@$(VENV_BIN)/uvicorn main:app --reload

# Help
help:
	@echo "FastAPI Basics - Quick Commands"
	@echo ""
	@echo "  make install   - Create venv + install FastAPI"
	@echo "  make run       - Start server with reload"
	@echo "  make help      - Show this help"
	@echo ""
	@echo "Note: venv is auto-managed by Makefile"
	@echo ""
	@echo "After starting server:"
	@echo "  - API:   http://localhost:8000"
	@echo "  - Docs:  http://localhost:8000/docs"
