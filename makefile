PACKAGE_NAME := myproject

PUBLISH_BRANCH := main
PYPI_TOKEN_FILE := .pypi-token
LAST_VERSION_FILE := .lastversion
COVERAGE_REPORTS_DIR := docs/coverage
TESTS_DIR := tests/
TESTS_TEMP_DIR := tests/_temp
PYPROJECT := pyproject.toml

VERSION := $(shell python -c "import re; print(re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))")
LAST_VERSION := $(shell [ -f $(LAST_VERSION_FILE) ] && cat $(LAST_VERSION_FILE) || echo NONE)
PYTHON_BASE := python

# note that the commands at the end:
# 1) format the git log
# 2) replace backticks with single quotes, to avoid funny business
# 3) add a final newline, to make tac happy
# 4) reverse the order of the lines, so that the oldest commit is first
# 5) replace newlines with tabs, to prevent the newlines from being lost
COMMIT_LOG_FILE := .commit_log
ifeq ($(LAST_VERSION),NONE)
	COMMIT_LOG_SINCE_LAST_VERSION := "No last version found, cannot generate commit log"
else
	COMMIT_LOG_SINCE_LAST_VERSION := $(shell (git log $(LAST_VERSION)..HEAD --pretty=format:"- %s (%h)" | tr '`' "'" ; echo) | tac | tr '\n' '\t')
#                                                                                    1                2            3       4     5
endif


# command line options
# --------------------------------------------------
# for formatting, we might want to run python without setting up all of poetry
RUN_GLOBAL ?= 0
ifeq ($(RUN_GLOBAL),0)
	PYTHON = poetry run $(PYTHON_BASE)
else
	PYTHON = $(PYTHON_BASE)
endif

# options we might want to pass to pytest
PYTEST_OPTIONS ?=
COV ?= 1
ifdef VERBOSE
	PYTEST_OPTIONS += --verbose
endif

ifeq ($(COV),1)
    PYTEST_OPTIONS += --cov=.
endif

USE_SHELL ?= 1
ifdef NO_SHELL
	USE_SHELL = 0
endif

# default target
# --------------------------------------------------

.PHONY: default
default: help

.PHONY: version
version:
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version:"
	@echo "$(COMMIT_LOG_SINCE_LAST_VERSION)" | tr '\t' '\n' > $(COMMIT_LOG_FILE)
	@cat $(COMMIT_LOG_FILE)
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi

# installation and setup
# --------------------------------------------------
.PHONY: setup
setup:
	@echo "install and update via poetry and setup shell"
	poetry update
	@if [ "$(USE_SHELL)" = "1" ]; then \
		poetry shell; \
	fi

.PHONY: setup-format
setup-format:
	@echo "install only packages needed for formatting, direct via pip (useful for CI)"
	$(PYTHON_BASE) -c 'import re,tomllib; cfg = tomllib.load(open("$(PYPROJECT)", "rb")); deps = [(pkg, re.match(r"^\D*(\d.*)", ver).group(1)) for pkg, ver in cfg["tool"]["poetry"]["group"]["dev"]["dependencies"].items() if pkg in ["ruff", "pycln"]]; print(" ".join([f"{pkg}=={ver}" for pkg,ver in deps]))' | xargs $(PYTHON) -m pip install

# formatting
# --------------------------------------------------
.PHONY: format
format:
	$(PYTHON) -m ruff format
	$(PYTHON) -m pycln --config $(PYPROJECT) --all .

.PHONY: check-format
check-format:
	@echo "run format check"
	$(PYTHON) -m ruff check
	$(PYTHON) -m pycln --check --config $(PYPROJECT) .

# tests
# --------------------------------------------------

.PHONY: lint
lint: clean
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(PACKAGE_NAME)/
	$(PYTHON) -m mypy --config-file $(PYPROJECT) tests/

.PHONY: test
test: clean
	@echo "running tests"
	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)

.PHONY: check
check: clean check-format clean test lint
	@echo "run format check, test, and lint"

# coverage reports
# --------------------------------------------------
# whether to run pytest with coverage report generation

.PHONY: cov
cov:
	@echo "generate coverage reports"
	@echo "requires tests to have been run"
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html	


# build and publish
# --------------------------------------------------

.PHONY: verify-git
verify-git: 
	@echo "checking git status"
	if [ "$(shell git branch --show-current)" != $(PUBLISH_BRANCH) ]; then \
		echo "Git is not on the $(PUBLISH_BRANCH) branch, exiting!"; \
		exit 1; \
	fi; \
	if [ -n "$(shell git status --porcelain)" ]; then \
		echo "Git is not clean, exiting!"; \
		exit 1; \
	fi; \

.PHONY: build
build: 
	@echo "build via poetry, assumes checks have been run"
	poetry build

.PHONY: publish
publish: check build verify-git version
	@echo "run all checks, build, and then publish"

	@echo "# Enter the new version number if you want to upload to pypi and create a new tag"
	@read -p "Confirm: " NEW_VERSION; \
	if [ "$$NEW_VERSION" != "$(VERSION)" ]; then \
		echo "Confirmation failed, exiting!"; \
		exit 1; \
	fi; \

	@echo "# pypi username: __token__"
	@echo "# pypi token from '$(PYPI_TOKEN_FILE)' :"
	echo $$(cat $(PYPI_TOKEN_FILE))

	echo "# Uploading!"; \
	echo $(VERSION) > $(LAST_VERSION_FILE); \
	git add $(LAST_VERSION_FILE); \
	git commit -m "Auto update to $(VERSION)"; \
	git tag -a $(VERSION) -F $(COMMIT_LOG_FILE); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# cleanup
# --------------------------------------------------

.PHONY: clean
clean:
	@echo "cleaning up"
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf $(PACKAGE_NAME).egg-info
	rm -rf $(TESTS_TEMP_DIR)
	$(PYTHON_BASE) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON_BASE) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.PHONY: help
help:
	@echo -n "# list make targets and variables"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 25
	@echo "# makefile variables:"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    VERSION = $(VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"