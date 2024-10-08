- `PACKAGE_NAME`: !!! MODIFY AT LEAST THIS PART TO SUIT YOUR PROJECT !!!  
  it assumes that the source is in a directory named the same as the package name  
  this also gets passed to some other places      `PACKAGE_NAME := myproject`  

- `PUBLISH_BRANCH`: for checking you are on the right branch when publishing  
  `PUBLISH_BRANCH := main`  

- `DOCS_DIR`: where to put docs  
  `DOCS_DIR := docs`  

- `COVERAGE_REPORTS_DIR`: where to put the coverage reports  
  note that this will be published with the docs!  
  modify the `docs` targets and `.gitignore` if you don't want that      `COVERAGE_REPORTS_DIR := docs/coverage`  

- `TESTS_DIR`: where the tests are, for pytest  
  `TESTS_DIR := tests/`  

- `TESTS_TEMP_DIR`: tests temp directory to clean up. will remove this in `make clean`  
  `TESTS_TEMP_DIR := tests/_temp`  

- `PYPROJECT`: where the pyproject.toml file is. no idea why you would change this but just in case  
  `PYPROJECT := pyproject.toml`  

- `REQ_BASE`: requirements.txt files for base package, all extras, and dev  
  `REQ_BASE := .github/requirements.txt`  

- `REQ_EXTRAS`: *(No description available)*  
  `REQ_EXTRAS := .github/requirements-extras.txt`  

- `REQ_DEV`: *(No description available)*  
  `REQ_DEV := .github/requirements-dev.txt`  

- `LOCAL_DIR`: local files (don't push this to git)  
  `LOCAL_DIR := .github/local`  

- `PYPI_TOKEN_FILE`: will print this token when publishing. make sure not to commit this file!!!  
  `PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token`  

- `LAST_VERSION_FILE`: the last version that was auto-uploaded. will use this to create a commit log for version tag  
  see `gen-commit-log` target      `LAST_VERSION_FILE := .github/.lastversion`  

- `PYTHON_BASE`: base python to use. Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1  
  `PYTHON_BASE := python`  

- `COMMIT_LOG_FILE`: where the commit log will be stored  
  `COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log`  

- `PANDOC`: pandoc commands (for docs)  
  `PANDOC ?= pandoc`  

- `VERSION`: assuming your `pyproject.toml` has a line that looks like `version = "0.0.1"`, `gen-version-info` will extract this  
  `VERSION := NULL`  

- `LAST_VERSION`: `gen-version-info` will read the last version from `$(LAST_VERSION_FILE)`, or `NULL` if it doesn't exist  
  `LAST_VERSION := NULL`  

- `PYTHON_VERSION`: get the python version, now that we have picked the python command  
  `PYTHON_VERSION := NULL`  

- `RUN_GLOBAL`: for formatting or something, we might want to run python without uv  
  RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `uv run $(PYTHON_BASE)`      `RUN_GLOBAL ?= 0`  

- `PYTHON`: *(No description available)*  
  `PYTHON = uv run $(PYTHON_BASE)`  

- `PYTHON`: *(No description available)*  
  `PYTHON = $(PYTHON_BASE)`  

- `PYTEST_OPTIONS`: base options for pytest, will be appended to if `COV` or `VERBOSE` are 1.  
  user can also set this when running make to add more options      `PYTEST_OPTIONS ?=`  

- `COV`: set to `1` to run pytest with `--cov=.` to get coverage reports in a `.coverage` file  
  `COV ?= 1`  

- `VERBOSE`: set to `1` to run pytest with `--verbose`  
  `VERBOSE ?= 0`  

- `default`: No description available  
  

# getting version info

- `gen-version-info`: No description available  
  

- `gen-commit-log`: LAST_VERSION is NULL, cant get commit log!"; \  
  

- `version`: Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)  
  

- `setup`: install and update via uv  
  

- `dep`: sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)  
  

- `dep-check`: checking uv.lock is good, exported requirements up to date  
  

- `format`: format the source code  
  

- `format-check`: check if the source code is formatted correctly  
  

- `typing`: running type checks  
  

- `test`: running tests  
  

- `check`: run format checks, tests, and typing checks  
  

- `docs-html`: generate html docs  
  

- `docs-md`: generate combined (single-file) docs in markdown  
  

- `docs-combined`: generate combined (single-file) docs in markdown and convert to other formats  
  

- `cov`: generate coverage reports  
  

- `docs`: generate all documentation and coverage reports  
  

- `docs-clean`: remove generated docs  
  

- `verify-git`: checking git status  
  

- `build`: build the package  
  

- `publish`: run all checks, build, and then publish  
  

- `clean`: clean up temporary files  
  

- `help-targets`: -n "# make targets  
    https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile  
  no .PHONY because this will only be run before `make help`  
  it's a separate command because getting the versions takes a bit of time    

- `help`: -n "  
  


