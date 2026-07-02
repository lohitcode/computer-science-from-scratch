# Python Basics Makefile
# Easy commands to run lessons and tests

.PHONY: all test lesson clean help

# Default: show menu
all:
	@python3 main.py

# Run interactive course
test:
	@python3 main.py

# Run specific lesson (usage: make lesson N=1)
lesson:
	@python3 lesson$(N)_*.py

# Run lesson 1
l1:
	@python3 lesson1_variables.py

# Run lesson 2
l2:
	@python3 lesson2_functions.py

# Run lesson 3
l3:
	@python3 lesson3_data_structures.py

# Run lesson 4
l4:
	@python3 lesson4_classes.py

# Run lesson 5
l5:
	@python3 lesson5_async.py

# Progress checklist
progress:
	@cat PROGRESS.md

# Quick reference
cheat:
	@cat CHEATSHEET.md

# Help
help:
	@echo "Python Basics - Quick Commands"
	@echo ""
	@echo "  make          - Start interactive course"
	@echo "  make test     - Same as make"
	@echo "  make l1       - Run lesson 1"
	@echo "  make l2       - Run lesson 2"
	@echo "  make l3       - Run lesson 3"
	@echo "  make l4       - Run lesson 4"
	@echo "  make l5       - Run lesson 5"
	@echo "  make progress - Show progress checklist"
	@echo "  make cheat    - Show quick reference"
	@echo ""
	@echo "Example: make l1"
