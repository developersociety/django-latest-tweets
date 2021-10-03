SHELL=/bin/bash
.DEFAULT_GOAL := help


# ---------------------------------
# Project specific targets
# ---------------------------------
#
# Add any targets specific to the current project in here.



# -------------------------------
# Common targets for DEV projects
# -------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

clean: ## Remove unneeded files generated from the various build tasks.
clean: build-clean

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check

format: ## Run this project's code formatters.
format: black-format isort-format

lint: ## Lint the project.
lint: black-lint isort-lint flake8-lint

test: ## Run unit and integration tests.
test: django-test

test-report: ## Run and report on unit and integration tests.
test-report: coverage-clean test coverage-report

dist: ## Builds source and wheel package
dist: clean build-dist

release: ## Package and release this project to PyPI.
release: dist build-release


# ---------------
# Utility targets
# ---------------
#
# Targets which are used by the common targets. You likely want to customise these per project,
# to ensure they're pointing at the correct directories, etc.

# Build
build-clean:
	rm -rf build
	rm -rf dist
	rm -rf .eggs
	find . -maxdepth 1 -name '*.egg-info' -exec rm -rf {} +

build-release:
	@echo
	@echo "This will package and release this project to PyPI."
	@echo
	@echo "A checklist before you continue:"
	@echo
	@echo " - have you ran 'bumpversion'?"
	@echo " - have you pushed the commit and tag created by 'bumpversion'?"
	@echo " - are you sure the project is in a state to be released?"
	@echo
	@read -p "Press <enter> to continue. Or <ctrl>-c to quit and address the above points."
	twine upload dist/*

build-dist:
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist


# Virtual Environments
venv-check:
ifndef VIRTUAL_ENV
	$(error Must be in a virtualenv)
endif

venv-wipe: venv-check
	if ! pip list --format=freeze | grep -v "^pip=\|^setuptools=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


# Installs
install-local: pip-install-local


# Pip
pip-install-local: venv-check
	pip install -r requirements/local.txt


# ISort
isort-lint:
	isort --check-only --diff latest_tweets tests

isort-format:
	isort latest_tweets tests


# Flake8
flake8-lint:
	flake8 latest_tweets


# Coverage
coverage-report: coverage-combine coverage-html coverage-xml
	coverage report --show-missing

coverage-combine:
	coverage combine

coverage-html:
	coverage html

coverage-xml:
	coverage xml

coverage-clean:
	rm -rf htmlcov
	rm -f coverage.xml
	rm -f .coverage


# Black
black-lint:
	black --check latest_tweets tests setup.py

black-format:
	black latest_tweets tests setup.py


#pipdeptree
pipdeptree-check:
	@pipdeptree --warn fail > /dev/null


# Project testing
django-test:
	PYTHONWARNINGS=all coverage run $$(which django-admin) test --pythonpath $$(pwd) --settings tests.settings tests


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
