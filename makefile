PYTHON_VERSION=3
PACKAGE=handles

VENV=.venv
SHELL=/bin/bash
PIP=$(VENV)/bin/pip3

# Utility scripts to prettify echo outputs
bold := \033[1m
clr := \033[0m


.PHONY: bootstrap
bootstrap: venv develop


.PHONY: clean
clean:
	@echo '$(bold)Clean up old virtualenv and cache$(sgr0)'
	rm -rf $(VENV) $(PACKAGE).egg-info .pytest_cache

.PHONY: venv
venv: clean
	@echo '$(bold)Create virtualenv$(sgr0)'
	virtualenv -p /usr/bin/python$(PYTHON_VERSION) $(VENV)
	$(PIP) install --upgrade pip setuptools

.PHONY: develop
develop:
	@echo '$(bold)Install and update requirements$(sgr0)'
	$(PIP) install --upgrade .[develop]
	$(PIP) install --upgrade .[testing]
	$(PIP) install -e .


.PHONT: help
help: 
	$(VENV)/bin/python -m $(PACKAGE) --help


.PHONY: run
run:
	$(VENV)/bin/python -m $(PACKAGE) 

	
.PHONY: test
test:
	$(VENV)/bin/pytest 