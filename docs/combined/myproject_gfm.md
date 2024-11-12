> docs for
> [`myproject`](https://github.com/mivanit/python-project-makefile-template)
> v0.0.3

## Contents

# Makefile Template for Python Projects

I’ve ended up using the same style of makefile for multiple Python
projects, so I’ve decided to create a repository with a template.

Relevant ideological decisions:

- **everything contained in github actions should be minimal, and mostly
  consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and
  packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`mypy`](https://github.com/python/mypy) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) and
  [`pycln`](https://github.com/hadialqattan/pycln) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation
  (I know there are better build tools out there and it’s overkill, but
  `make` is universal)
- [`git`](https://github.com/git) for version control (a spicy take, I
  know)

# Makefile

`make help` Displays the help message listing all available make targets
and variables. running just `make` will also display this message.

``` sh
$ make help
# make targets:
    make build                build the package
    make check                run format and lint checks, tests, and typing checks
    make clean                clean up temporary files
    make cov                  generate coverage reports
    make dep                  sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)
    make dep-check            checking uv.lock is good, exported requirements up to date
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs
    make docs-combined        generate combined (single-file) docs in markdown and convert to other formats
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         run format check
    make help
    make publish              run all checks, build, and then publish
    make setup                install and update via uv
    make test                 running tests
    make typing               running type checks
    make verify-git           checking git status
    make version              Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)
# makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.12.0 
    PACKAGE_NAME = myproject
    VERSION = v0.0.2 
    LAST_VERSION = v0.0.1 
    PYTEST_OPTIONS =  --cov=.
```

## Configuration & Variables

- `PACKAGE_NAME`: The name of the package  
  `PACKAGE_NAME := myproject`

- `PUBLISH_BRANCH`: The branch to check when publishing  
  `PUBLISH_BRANCH := main`

- `DOCS_DIR`: Where to put docs  
  `DOCS_DIR := docs`

- `COVERAGE_REPORTS_DIR`: Where to put the coverage reports  
  This will be published with the docs. Modify the `docs` targets and
  `.gitignore` if you don’t want that  
  `COVERAGE_REPORTS_DIR := docs/coverage`

- `TESTS_DIR`: Where the tests are, for pytest  
  `TESTS_DIR := tests/`

- `TESTS_TEMP_DIR`: Tests temp directory to clean up  
  Will remove this in `make clean`  
  `TESTS_TEMP_DIR := tests/_temp`

### probably don’t change these:

- `PYPROJECT`: Where the pyproject.toml file is  
  `PYPROJECT := pyproject.toml`

- `REQ_BASE`: Requirements.txt file for base package  
  `REQ_BASE := .github/requirements.txt`

- `REQ_EXTRAS`: Requirements.txt file for all extras  
  `REQ_EXTRAS := .github/requirements-extras.txt`

- `REQ_DEV`: Requirements.txt file for dev  
  `REQ_DEV := .github/requirements-dev.txt`

- `LOCAL_DIR`: Local files (don’t push this to git)  
  `LOCAL_DIR := .github/local`

- `PYPI_TOKEN_FILE`: Will print this token when publishing  
  Make sure not to commit this file!  
  `PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token`

- `LAST_VERSION_FILE`: The last version that was auto-uploaded  
  Will use this to create a commit log for version tag  
  `LAST_VERSION_FILE := .github/.lastversion`

- `PYTHON_BASE`: Base python to use  
  Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1  
  `PYTHON_BASE := python`

- `COMMIT_LOG_FILE`: Where the commit log will be stored  
  `COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log`

- `PANDOC`: Pandoc commands (for docs)  
  `PANDOC ?= pandoc`

### version vars - extracted automatically from `pyproject.toml`, `$(LAST_VERSION_FILE)`, and \$(PYTHON)

- `VERSION`: Extracted automatically from `pyproject.toml`  
  `VERSION := NULL`

- `LAST_VERSION`: Read from `$(LAST_VERSION_FILE)`, or `NULL` if it
  doesn’t exist  
  `LAST_VERSION := NULL`

- `PYTHON_VERSION`: Get the python version, now that we have picked the
  python command  
  `PYTHON_VERSION := NULL`

- `RUN_GLOBAL`: For formatting or something, we might want to run python
  without uv  
  RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of
  `uv run $(PYTHON_BASE)`  
  `RUN_GLOBAL ?= 0`

- `PYTEST_OPTIONS`: Base options for pytest, will be appended to if
  `COV` or `VERBOSE` are 1  
  User can also set this when running make to add more options  
  `PYTEST_OPTIONS ?=`

- `COV`: Set to `1` to run pytest with `--cov=.` to get coverage reports
  in a `.coverage` file  
  `COV ?= 1`

- `VERBOSE`: Set to `1` to run pytest with `--verbose`  
  `VERBOSE ?= 0`

## Default Target (Help)

- `default`: First/default target is help

## Getting Version Info

- `gen-version-info`: Gets version info from \$(PYPROJECT), last version
  from \$(LAST_VERSION_FILE), and python version  
  Uses just `python` for everything except getting the python version.
  No echo here, because this is “private”

- `gen-commit-log`: Getting commit log since the tag specified in
  \$(LAST_VERSION_FILE)  
  Will write to \$(COMMIT_LOG_FILE)  
  When publishing, the contents of \$(COMMIT_LOG_FILE) will be used as
  the tag description (but can be edited during the process)  
  Uses just `python`. No echo here, because this is “private”

- `version`: Force the version info to be read, printing it out  
  Also force the commit log to be generated, and cat it out

## Dependencies and Setup

- `setup`: Install and update via uv

- `dep`: Sync and export deps to \$(REQ_BASE), \$(REQ_EXTRAS), and
  \$(REQ_DEV)

- `dep-check`: Checking uv.lock is good, exported requirements up to
  date

## Checks (Formatting/Linting, Typing, Tests)

- `format`: Format the source code  
  Runs ruff and pycln to format the code

- `format-check`: Check if the source code is formatted correctly  
  Runs ruff and pycln to check if the code is formatted correctly

- `typing`: Running type checks  
  Runs type checks with mypy  
  At some point, need to add back –check-untyped-defs to mypy call  
  But it complains when we specify arguments by keyword where positional
  is fine  
  Not sure how to fix this

- `test`: Running tests

- `check`: Run format checks, tests, and typing checks

## Coverage & Docs

- `docs-html`: Generate html docs  
  Generates a whole tree of documentation in html format.  
  See `docs/make_docs.py` and the templates in `docs/templates/html/`
  for more info

- `docs-md`: Generate combined (single-file) docs in markdown  
  Instead of a whole website, generates a single markdown file with all
  docs using the templates in `docs/templates/markdown/`.  
  This is useful if you want to have a copy that you can grep/search,
  but those docs are much messier.  
  docs-combined will use pandoc to convert them to other formats.

- `docs-combined`: Generate combined (single-file) docs in markdown and
  convert to other formats  
  After running docs-md, this will convert the combined markdown file to
  other formats:  
  gfm (github-flavored markdown), plain text, and html  
  Requires pandoc in path, pointed to by \$(PANDOC)  
  pdf output would be nice but requires other deps

- `cov`: Generate coverage reports  
  Generates coverage reports as html and text with `pytest-cov`, and a
  badge with `coverage-badge`  
  If `.coverage` is not found, will run tests first  
  Also removes the `.gitignore` file that `coverage html` creates, since
  we count that as part of the docs

- `docs`: Generate all documentation and coverage reports  
  Runs the coverage report, then the docs, then the combined docs

- `docs-clean`: Remove generated docs  
  Removed all generated documentation files, but leaves the templates
  and the `docs/make_docs.py` script  
  Distinct from `make clean`

## Build and Publish

- `verify-git`: Checking git status  
  Verifies that the current branch is \$(PUBLISH_BRANCH) and that git is
  clean  
  Used before publishing

- `build`: Build the package

- `publish`: Run all checks, build, and then publish  
  Gets the commit log, checks everything, builds, and then publishes
  with twine  
  Will ask the user to confirm the new version number (and this allows
  for editing the tag info)  
  Will also print the contents of \$(PYPI_TOKEN_FILE) to the console for
  the user to copy and paste in when prompted by twine

## Cleanup of Temp Files

- `clean`: Clean up temporary files  
  Cleans up temp files from formatter, type checking, tests, coverage  
  Removes all built files  
  Removes \$(TESTS_TEMP_DIR) to remove temporary test files  
  Recursively removes all `__pycache__` directories and `*.pyc` or
  `*.pyo` files  
  Distinct from `make docs-clean`, which only removes generated
  documentation files

## Smart Help Command

- `help-targets`: List make targets  
  Listing targets is from stackoverflow  
  https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile  
  No .PHONY because this will only be run before `make help`  
  It’s a separate command because getting the versions takes a bit of
  time

- `help`: Print out the help targets, and then local variables (but
  those take a bit longer)  
  Immediately print out the help targets, and then local variables (but
  those take a bit longer)

## Docs generation

Provided files for pdoc usage are:

- `docs/make_docs.py` which generates documentation with a slightly
  custom style, automatically adding metadata read from your
  `pyproject.toml` file
- `docs/templates/` containing template files for both html and markdown
  docs
- `docs/resources/` containing some of the base `pdoc` resources as well
  as some custom icons for admonitions

## Submodules

- [`helloworld`](#helloworld)

[View Source on
GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.3/__init__.py)

# `myproject`

### Makefile Template for Python Projects

I’ve ended up using the same style of makefile for multiple Python
projects, so I’ve decided to create a repository with a template.

Relevant ideological decisions:

- **everything contained in github actions should be minimal, and mostly
  consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and
  packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`mypy`](https://github.com/python/mypy) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) and
  [`pycln`](https://github.com/hadialqattan/pycln) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation
  (I know there are better build tools out there and it’s overkill, but
  `make` is universal)
- [`git`](https://github.com/git) for version control (a spicy take, I
  know)

### Makefile

`make help` Displays the help message listing all available make targets
and variables. running just `make` will also display this message.

``` sh
$ make help
### make targets:
    make build                build the package
    make check                run format and lint checks, tests, and typing checks
    make clean                clean up temporary files
    make cov                  generate coverage reports
    make dep                  sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)
    make dep-check            checking uv.lock is good, exported requirements up to date
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs
    make docs-combined        generate combined (single-file) docs in markdown and convert to other formats
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         run format check
    make help
    make publish              run all checks, build, and then publish
    make setup                install and update via uv
    make test                 running tests
    make typing               running type checks
    make verify-git           checking git status
    make version              Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)
### makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.12.0 
    PACKAGE_NAME = myproject
    VERSION = v0.0.2 
    LAST_VERSION = v0.0.1 
    PYTEST_OPTIONS =  --cov=.
```

#### Configuration & Variables

- `PACKAGE_NAME`: The name of the package  
  `PACKAGE_NAME := myproject`

- `PUBLISH_BRANCH`: The branch to check when publishing  
  `PUBLISH_BRANCH := main`

- `DOCS_DIR`: Where to put docs  
  `DOCS_DIR := docs`

- `COVERAGE_REPORTS_DIR`: Where to put the coverage reports  
  This will be published with the docs. Modify the `docs` targets and
  `.gitignore` if you don’t want that  
  `COVERAGE_REPORTS_DIR := docs/coverage`

- `TESTS_DIR`: Where the tests are, for pytest  
  `TESTS_DIR := tests/`

- `TESTS_TEMP_DIR`: Tests temp directory to clean up  
  Will remove this in `make clean`  
  `TESTS_TEMP_DIR := tests/_temp`

##### probably don’t change these:

- `PYPROJECT`: Where the pyproject.toml file is  
  `PYPROJECT := pyproject.toml`

- `REQ_BASE`: Requirements.txt file for base package  
  `REQ_BASE := .github/requirements.txt`

- `REQ_EXTRAS`: Requirements.txt file for all extras  
  `REQ_EXTRAS := .github/requirements-extras.txt`

- `REQ_DEV`: Requirements.txt file for dev  
  `REQ_DEV := .github/requirements-dev.txt`

- `LOCAL_DIR`: Local files (don’t push this to git)  
  `LOCAL_DIR := .github/local`

- `PYPI_TOKEN_FILE`: Will print this token when publishing  
  Make sure not to commit this file!  
  `PYPI_TOKEN_FILE := $(LOCAL_DIR)/.pypi-token`

- `LAST_VERSION_FILE`: The last version that was auto-uploaded  
  Will use this to create a commit log for version tag  
  `LAST_VERSION_FILE := .github/.lastversion`

- `PYTHON_BASE`: Base python to use  
  Will add `uv run` in front of this if `RUN_GLOBAL` is not set to 1  
  `PYTHON_BASE := python`

- `COMMIT_LOG_FILE`: Where the commit log will be stored  
  `COMMIT_LOG_FILE := $(LOCAL_DIR)/.commit_log`

- `PANDOC`: Pandoc commands (for docs)  
  `PANDOC ?= pandoc`

##### version vars - extracted automatically from `pyproject.toml`, `$(LAST_VERSION_FILE)`, and \$(PYTHON)

- `VERSION`: Extracted automatically from `pyproject.toml`  
  `VERSION := NULL`

- `LAST_VERSION`: Read from `$(LAST_VERSION_FILE)`, or `NULL` if it
  doesn’t exist  
  `LAST_VERSION := NULL`

- `PYTHON_VERSION`: Get the python version, now that we have picked the
  python command  
  `PYTHON_VERSION := NULL`

- `RUN_GLOBAL`: For formatting or something, we might want to run python
  without uv  
  RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of
  `uv run $(PYTHON_BASE)`  
  `RUN_GLOBAL ?= 0`

- `PYTEST_OPTIONS`: Base options for pytest, will be appended to if
  `COV` or `VERBOSE` are 1  
  User can also set this when running make to add more options  
  `PYTEST_OPTIONS ?=`

- `COV`: Set to `1` to run pytest with `--cov=.` to get coverage reports
  in a `.coverage` file  
  `COV ?= 1`

- `VERBOSE`: Set to `1` to run pytest with `--verbose`  
  `VERBOSE ?= 0`

#### Default Target (Help)

- `default`: First/default target is help

#### Getting Version Info

- `gen-version-info`: Gets version info from \$(PYPROJECT), last version
  from \$(LAST_VERSION_FILE), and python version  
  Uses just `python` for everything except getting the python version.
  No echo here, because this is “private”

- `gen-commit-log`: Getting commit log since the tag specified in
  \$(LAST_VERSION_FILE)  
  Will write to \$(COMMIT_LOG_FILE)  
  When publishing, the contents of \$(COMMIT_LOG_FILE) will be used as
  the tag description (but can be edited during the process)  
  Uses just `python`. No echo here, because this is “private”

- `version`: Force the version info to be read, printing it out  
  Also force the commit log to be generated, and cat it out

#### Dependencies and Setup

- `setup`: Install and update via uv

- `dep`: Sync and export deps to \$(REQ_BASE), \$(REQ_EXTRAS), and
  \$(REQ_DEV)

- `dep-check`: Checking uv.lock is good, exported requirements up to
  date

#### Checks (Formatting/Linting, Typing, Tests)

- `format`: Format the source code  
  Runs ruff and pycln to format the code

- `format-check`: Check if the source code is formatted correctly  
  Runs ruff and pycln to check if the code is formatted correctly

- `typing`: Running type checks  
  Runs type checks with mypy  
  At some point, need to add back –check-untyped-defs to mypy call  
  But it complains when we specify arguments by keyword where positional
  is fine  
  Not sure how to fix this

- `test`: Running tests

- `check`: Run format checks, tests, and typing checks

#### Coverage & Docs

- `docs-html`: Generate html docs  
  Generates a whole tree of documentation in html format.  
  See `docs/make_docs.py` and the templates in `docs/templates/html/`
  for more info

- `docs-md`: Generate combined (single-file) docs in markdown  
  Instead of a whole website, generates a single markdown file with all
  docs using the templates in `docs/templates/markdown/`.  
  This is useful if you want to have a copy that you can grep/search,
  but those docs are much messier.  
  docs-combined will use pandoc to convert them to other formats.

- `docs-combined`: Generate combined (single-file) docs in markdown and
  convert to other formats  
  After running docs-md, this will convert the combined markdown file to
  other formats:  
  gfm (github-flavored markdown), plain text, and html  
  Requires pandoc in path, pointed to by \$(PANDOC)  
  pdf output would be nice but requires other deps

- `cov`: Generate coverage reports  
  Generates coverage reports as html and text with `pytest-cov`, and a
  badge with `coverage-badge`  
  If `.coverage` is not found, will run tests first  
  Also removes the `.gitignore` file that `coverage html` creates, since
  we count that as part of the docs

- `docs`: Generate all documentation and coverage reports  
  Runs the coverage report, then the docs, then the combined docs

- `docs-clean`: Remove generated docs  
  Removed all generated documentation files, but leaves the templates
  and the `docs/make_docs.py` script  
  Distinct from `make clean`

#### Build and Publish

- `verify-git`: Checking git status  
  Verifies that the current branch is \$(PUBLISH_BRANCH) and that git is
  clean  
  Used before publishing

- `build`: Build the package

- `publish`: Run all checks, build, and then publish  
  Gets the commit log, checks everything, builds, and then publishes
  with twine  
  Will ask the user to confirm the new version number (and this allows
  for editing the tag info)  
  Will also print the contents of \$(PYPI_TOKEN_FILE) to the console for
  the user to copy and paste in when prompted by twine

#### Cleanup of Temp Files

- `clean`: Clean up temporary files  
  Cleans up temp files from formatter, type checking, tests, coverage  
  Removes all built files  
  Removes \$(TESTS_TEMP_DIR) to remove temporary test files  
  Recursively removes all `__pycache__` directories and `*.pyc` or
  `*.pyo` files  
  Distinct from `make docs-clean`, which only removes generated
  documentation files

#### Smart Help Command

- `help-targets`: List make targets  
  Listing targets is from stackoverflow  
  https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile  
  No .PHONY because this will only be run before `make help`  
  It’s a separate command because getting the versions takes a bit of
  time

- `help`: Print out the help targets, and then local variables (but
  those take a bit longer)  
  Immediately print out the help targets, and then local variables (but
  those take a bit longer)

#### Docs generation

Provided files for pdoc usage are:

- `docs/make_docs.py` which generates documentation with a slightly
  custom style, automatically adding metadata read from your
  `pyproject.toml` file
- `docs/templates/` containing template files for both html and markdown
  docs
- `docs/resources/` containing some of the base `pdoc` resources as well
  as some custom icons for admonitions

[View Source on
GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.3/__init__.py#L0-L2)

> docs for
> [`myproject`](https://github.com/mivanit/python-project-makefile-template)
> v0.0.3

[View Source on
GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.3/helloworld.py)

# `myproject.helloworld`

[View Source on
GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.3/helloworld.py#L0-L0)
