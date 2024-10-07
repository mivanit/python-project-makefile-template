# ==================================================
# configuration & variables
# ==================================================
# MODIFY THIS FILE TO SUIT YOUR PROJECT
# it assumes that the source is in a directory named the same as the package name
PACKAGE_NAME := myproject

# for checking you are on the right branch when publishing
PUBLISH_BRANCH := main
# where to put docs
DOCS_DIR := docs
# where to put the coverage reports
COVERAGE_REPORTS_DIR := docs/coverage
# where the tests are (assumes pytest)
TESTS_DIR := tests/
# temp directory to clean up
TESTS_TEMP_DIR := tests/_temp
# requirements.txt files for base package, all extras, and dev
REQ_BASE := .github/requirements.txt
REQ_EXTRAS := .github/requirements-extras.txt
REQ_DEV := .github/requirements-dev.txt

# probably don't change these:
# --------------------------------------------------
# local files, don't push
LOCAL_DIR := .github/local
# will print this token when publishing
PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token
# the last version that was auto-uploaded. will use this to create a commit log for version tag
LAST_VERSION_FILE := .github/.lastversion
# where the pyproject.toml file is
PYPROJECT := pyproject.toml
# base python to use. Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1
PYTHON_BASE := python
# where the commit log will be stored
COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log
# pandoc commands (for docs)
PANDOC ?= pandoc

# version vars
# --------------------------------------------------
# assuming your pyproject.toml has a line that looks like `version = "0.0.1"`, will get the version
VERSION := NULL
# read last auto-uploaded version from file
LAST_VERSION := NULL
# get the python version, now that we have picked the python command
PYTHON_VERSION := NULL


# ==================================================
# reading command line options
# ==================================================

# RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `uv run $(PYTHON_BASE)`
# --------------------------------------------------
# for formatting, we might want to run python without setting uv
RUN_GLOBAL ?= 0
ifeq ($(RUN_GLOBAL),0)
	PYTHON = uv run $(PYTHON_BASE)
else
	PYTHON = $(PYTHON_BASE)
endif

# if you want different behavior for different python versions
# --------------------------------------------------
# COMPATIBILITY_MODE := $(shell $(PYTHON) -c "import sys; print(1 if sys.version_info < (3, 10) else 0)")

# options we might want to pass to pytest
# --------------------------------------------------
PYTEST_OPTIONS ?=
COV ?= 1
VERBOSE ?= 0

ifeq ($(VERBOSE),1)
	PYTEST_OPTIONS += --verbose
endif

ifeq ($(COV),1)
    PYTEST_OPTIONS += --cov=.
endif

# ==================================================
# default target (help)
# ==================================================

.PHONY: default
default: help

# ==================================================
# getting version info
# we do this in a separate target because it takes a bit of time
# ==================================================

.PHONY: gen-version-info
gen-version-info:
	@mkdir -p $(LOCAL_DIR)
	$(eval VERSION := $(shell python -c "import re; print('v'+re.search(r'^version\s*=\s*\"(.+?)\"', open('$(PYPROJECT)').read(), re.MULTILINE).group(1))") )
	$(eval LAST_VERSION := $(shell [ -f $(LAST_VERSION_FILE) ] && cat $(LAST_VERSION_FILE) || echo NULL) )
	$(eval PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')") )

# getting commit log
.PHONY: gen-commit-log
gen-commit-log: gen-version-info
	@if [ "$(LAST_VERSION)" = "NULL" ]; then \
		echo "LAST_VERSION is NULL, cant get commit log!"; \
		exit 1; \
	fi
	@mkdir -p $(LOCAL_DIR)
	@python -c "import subprocess; open('$(COMMIT_LOG_FILE)', 'w').write('\n'.join(reversed(subprocess.check_output(['git', 'log', '$(LAST_VERSION)'.strip() + '..HEAD', '--pretty=format:- %s (%h)']).decode('utf-8').strip().split('\n'))))"


.PHONY: version
version: gen-commit-log
	@echo "Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)"
	@echo "Commit log since last version from '$(COMMIT_LOG_FILE)':"
	@cat $(COMMIT_LOG_FILE)
	@if [ "$(VERSION)" = "$(LAST_VERSION)" ]; then \
		echo "Python package $(VERSION) is the same as last published version $(LAST_VERSION), exiting!"; \
		exit 1; \
	fi


# ==================================================
# dependencies and setup
# ==================================================

.PHONY: setup
setup:
	@echo "install and update via uv"
	uv sync --all-extras
	@echo "To activate the virtual environment, run one of:"
	@echo "  source .venv/bin/activate"
	@echo "  source .venv/Scripts/activate"

.PHONY: dep
dep:
	@echo "sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)"
	uv sync
	uv export --no-dev --no-hashes > $(REQ_BASE)
	uv export --all-extras --no-dev --no-hashes > $(REQ_EXTRAS)
	uv export --all-extras --no-hashes > $(REQ_DEV)

.PHONY: dep-check
dep-check:
	@echo "checking uv.lock is good, exported requirements up to date"
	uv sync --locked
	uv export --no-dev --no-hashes | diff - $(REQ_BASE)
	uv export --all-extras --no-dev --no-hashes | diff - $(REQ_EXTRAS)
	uv export --all-extras --no-hashes | diff - $(REQ_DEV)


# ==================================================
# checks (formatting/linting, typing, tests)
# ==================================================
.PHONY: format
format:
	@echo "format the source code"
	$(PYTHON) -m ruff format --config $(PYPROJECT) .
	$(PYTHON) -m ruff check --fix --config $(PYPROJECT) .
	$(PYTHON) -m pycln --config $(PYPROJECT) --all .

.PHONY: format-check
format-check:
	@echo "run format check"
	$(PYTHON) -m ruff check --config $(PYPROJECT) .
	$(PYTHON) -m pycln --check --config $(PYPROJECT) .

# at some point, need to add back --check-untyped-defs to mypy call
# but it complains when we specify arguments by keyword where positional is fine
# not sure how to fix this
# python -m pylint $(PACKAGE_NAME)/
# python -m pylint tests/
.PHONY: typing
typing: clean gen-extra-tests
	@echo "running type checks"
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) $(PACKAGE_NAME)/
	$(PYTHON) -m mypy --config-file $(PYPROJECT) $(TYPECHECK_ARGS) tests/

.PHONY: test
test: clean
	@echo "running tests"
	$(PYTHON) -m pytest $(PYTEST_OPTIONS) $(TESTS_DIR)

.PHONY: check
check: clean format-check test typing
	@echo "run format and lint checks, tests, and typing checks"

# ==================================================
# coverage & docs
# ==================================================

.PHONY: docs-html
docs-html:
	@echo "generate html docs"
	$(PYTHON) docs/make_docs.py

.PHONY: docs-md
docs-md:
	@echo "generate combined (single-file) docs in markdown"
	mkdir $(DOCS_DIR)/combined -p
	$(PYTHON) docs/make_docs.py --combined


.PHONY: docs-combined
docs-combined: docs-md
	@echo "generate combined (single-file) docs in markdown and convert to other formats"
	@echo "requires pandoc in path"
	$(PANDOC) -f markdown -t gfm $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME)_gfm.md
	$(PANDOC) -f markdown -t plain $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).txt
	$(PANDOC) -f markdown -t html $(DOCS_DIR)/combined/$(PACKAGE_NAME).md -o $(DOCS_DIR)/combined/$(PACKAGE_NAME).html

.PHONY: cov
cov:
	@echo "generate coverage reports"
	@if [ ! -f .coverage ]; then \
		echo ".coverage not found, running tests first..."; \
		$(MAKE) test; \
	fi
	mkdir $(COVERAGE_REPORTS_DIR) -p
	$(PYTHON) -m coverage report -m > $(COVERAGE_REPORTS_DIR)/coverage.txt
	$(PYTHON) -m coverage_badge -f -o $(COVERAGE_REPORTS_DIR)/coverage.svg
	$(PYTHON) -m coverage html --directory=$(COVERAGE_REPORTS_DIR)/html/
	rm -rf $(COVERAGE_REPORTS_DIR)/html/.gitignore

.PHONY: docs
docs: cov docs-html docs-combined
	@echo "generate all documentation and coverage reports"

.PHONY: docs-clean
docs-clean:
	@echo "clean up docs"
	rm -rf $(DOCS_DIR)/combined/
	rm -rf $(DOCS_DIR)/$(PACKAGE_NAME)/
	rm -rf $(COVERAGE_REPORTS_DIR)/
	rm $(DOCS_DIR)/$(PACKAGE_NAME).html
	rm $(DOCS_DIR)/index.html
	rm $(DOCS_DIR)/search.js


# ==================================================
# build and publish
# ==================================================

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
	uv build

.PHONY: publish
publish: gen-commit-log check build verify-git version gen-version-info
	@echo "run all checks, build, and then publish"

	@echo "Enter the new version number if you want to upload to pypi and create a new tag"
	@echo "Now would also be the time to edit $(COMMIT_LOG_FILE), as that will be used as the tag description"
	@read -p "Confirm: " NEW_VERSION; \
	if [ "$$NEW_VERSION" = $(VERSION) ]; then \
		echo "Version confirmed. Proceeding with publish."; \
	else \
		echo "Version mismatch, exiting: you gave $$NEW_VERSION but expected $(VERSION)"; \
		exit 1; \
	fi;

	@echo "pypi username: __token__"
	@echo "pypi token from '$(PYPI_TOKEN_FILE)' :"
	echo $$(cat $(PYPI_TOKEN_FILE))

	echo "Uploading!"; \
	echo $(VERSION) > $(LAST_VERSION_FILE); \
	git add $(LAST_VERSION_FILE); \
	git commit -m "Auto update to $(VERSION)"; \
	git tag -a $(VERSION) -F $(COMMIT_LOG_FILE); \
	git push origin $(VERSION); \
	twine upload dist/* --verbose

# cleanup
# ==================================================

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


# smart help command
# ==================================================
# listing targets, from stackoverflow
# https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
# no .PHONY because this will only be run before `make help`
# it's a separate command because getting the versions takes a bit of time
help-targets:
	@echo -n "# make targets"
	@echo ":"
	@cat Makefile | sed -n '/^\.PHONY: / h; /\(^\t@*echo\|^\t:\)/ {H; x; /PHONY/ s/.PHONY: \(.*\)\n.*"\(.*\)"/    make \1\t\2/p; d; x}'| sort -k2,2 |expand -t 30

.PHONY: help
help: help-targets gen-version-info
	@echo -n ""
	@echo "# makefile variables"
	@echo "    PYTHON = $(PYTHON)"
	@echo "    PYTHON_VERSION = $(PYTHON_VERSION)"
	@echo "    PACKAGE_NAME = $(PACKAGE_NAME)"
	@echo "    VERSION = $(VERSION)"
	@echo "    LAST_VERSION = $(LAST_VERSION)"
	@echo "    PYTEST_OPTIONS = $(PYTEST_OPTIONS)"