> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.0.2


## Contents
# Makefile Template for Python Projects

I've ended up using the same makefile template for multiple Python projects, so I've decided to create a template repository for it.

Relevant ideological decisions:

- **github actions should be minimal, and mostly consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`mypy`](https://github.com/python/mypy) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) and [`pycln`](https://github.com/hadialqattan/pycln) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation (I know there are better build tools out there and it's overkill, but `make` is universal)
- [`git`](https://github.com/git) for version control (a spicy take, I know)

## Targets

### Help & info

- `make help` Displays the help message listing all available make targets and variables.
```sh
$ make help
# list make targets:
    make check                run format and lint checks, tests, and typing checks
    make clean                cleaning up
    make cov                  generate coverage reports
    make dep                  sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)
    make dep-check            checking uv.lock is good, exported requirements up to date
    make docs                 generate all documentation
    make docs-clean           clean up docs
    make docs-combined        generate combined docs in markdown and other formats
    make docs-html            generate html docs
    make docs-md              generate combined docs in markdown
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

- `make` does the same as `make help`

- `make version` Displays the current version of the project and the last auto-uploaded version (via tag). It also generates a commit log since the last version (and uses this for tag descriptions when publishing)

### Setup/deps

- `make setup` install and update via poetry and setup shell (from `pyproject.toml`)

- `make dep` export dependencies for the base package, all extras, and dev requirements into `.github/requirements.txt`, `.github/requirements-extras.txt`, and `.github/requirements-dev.txt` respectively

- `make dep-check` checks that the `uv.lock` file is up to date and that the exported requirements are up to date

### Formatting

- `make format` formats the code using `ruff` and `pycln`
  
- `make format-check` checks the code formatting using `ruff` and `pycln

### Testing and Linting

  
- `make test` runs tests using `pytest`, with data for coverage reports
	- you can pass `COV=0` to disable coverage reports
- `make typing` runs type checking using `mypy`
  
- `make check` runs format check, test, and type checks


### Docs

Provided files for pdoc usage are:

- `docs/make_docs.py` which generates documentation with a slightly custom style, automatically adding metadata read from your `pyproject.toml` file
- `docs/templates/` containing template files for both html and markdown docs
- `docs/resources/` containing some of the base `pdoc` resources as well as some custom icons for admonitions

Provided recipes:

- `make cov` generates coverage reports in text and html, as well as an svg badge. Will run tests if `.coverage` doesn't exist.
- `make docs-html` generates html documentation using pdoc
- `make docs-md` generates markdown documentation using pdoc
- `make docs-combined` generates single-file docs by using `pandoc` to process the `docs-md` output into other formats
- `make docs` generates all documentation
- `make docs-clean` cleans up the documentation generated files (keeps templates, resources, and `make_docs.py` script)

### Build and Publish

- `make publish` runs all checks, builds the project, and then publishes it. It also prompts for the new version number and handles tagging and pushing to the repository. Will also print your pypi token to the console, so you can copy and paste it into the prompt.
- `make build` builds the project using Poetry, assuming checks have been run
- `make verify-git` verifies the git status to ensure the repository is on the correct branch and is completely synced up and clean.
- `clean` Cleans up the build artifacts, caches, and temporary files.

## Makefile Variables

- `PACKAGE_NAME` Name of the package (default is `myproject`, change this).
- `PUBLISH_BRANCH` Branch to publish from (default is `main`).
- `PYPI_TOKEN_FILE` File containing the PyPI token (default is `.pypi-token`).
- `LAST_VERSION_FILE` File containing the last version (default is `.lastversion`).
- `COVERAGE_REPORTS_DIR` Directory for coverage reports (default is `docs/coverage`).
- `TESTS_DIR` Directory containing tests (default is `tests/`).
- `TESTS_TEMP_DIR` Temporary directory for tests (default is `tests/_temp`), which will be cleaned up.
- `PYPROJECT` Path to project config (default is `pyproject.toml`).
- `VERSION` Extracted automatically from `pyproject.toml`.
- `LAST_VERSION` Extracted from `.lastversion`, `NONE` if the file doesn't exist.
- `PYTHON_BASE` Base Python command (default is `python`). 
- `RUN_GLOBAL` Flag to determine whether to run Python globally or via Poetry (default is `0`).
- `PYTHON` Python command determined by `RUN_GLOBAL`. Will have `poetry run` prepended if `RUN_GLOBAL` is `0`.
- `PYTEST_OPTIONS` Optional parameters to pass to `pytest`.
- `COV` Determines if coverage should be reported (`1` by default), prepends `--cov=.` to `PYTEST_OPTIONS` if `1`.
- `VERBOSE` If defined, will append `--verbose` to `PYTEST_OPTIONS`.



## Submodules

- [`helloworld`](#helloworld)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.2/__init__.py)

# `myproject` { #myproject }

### Makefile Template for Python Projects

I've ended up using the same makefile template for multiple Python projects, so I've decided to create a template repository for it.

Relevant ideological decisions:

- **github actions should be minimal, and mostly consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`mypy`](https://github.com/python/mypy) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) and [`pycln`](https://github.com/hadialqattan/pycln) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation (I know there are better build tools out there and it's overkill, but `make` is universal)
- [`git`](https://github.com/git) for version control (a spicy take, I know)

#### Targets

##### Help & info

- `make help` Displays the help message listing all available make targets and variables.
```sh
$ make help
### list make targets:
    make check                run format and lint checks, tests, and typing checks
    make clean                cleaning up
    make cov                  generate coverage reports
    make dep                  sync and export deps to $(REQ_BASE), $(REQ_EXTRAS), and $(REQ_DEV)
    make dep-check            checking uv.lock is good, exported requirements up to date
    make docs                 generate all documentation
    make docs-clean           clean up docs
    make docs-combined        generate combined docs in markdown and other formats
    make docs-html            generate html docs
    make docs-md              generate combined docs in markdown
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

- `make` does the same as `make help`

- `make version` Displays the current version of the project and the last auto-uploaded version (via tag). It also generates a commit log since the last version (and uses this for tag descriptions when publishing)

##### Setup/deps

- `make setup` install and update via poetry and setup shell (from `pyproject.toml`)

- `make dep` export dependencies for the base package, all extras, and dev requirements into `.github/requirements.txt`, `.github/requirements-extras.txt`, and `.github/requirements-dev.txt` respectively

- `make dep-check` checks that the `uv.lock` file is up to date and that the exported requirements are up to date

##### Formatting

- `make format` formats the code using `ruff` and `pycln`
  
- `make format-check` checks the code formatting using `ruff` and `pycln

##### Testing and Linting

  
- `make test` runs tests using `pytest`, with data for coverage reports
	- you can pass `COV=0` to disable coverage reports
- `make typing` runs type checking using `mypy`
  
- `make check` runs format check, test, and type checks


##### Docs

Provided files for pdoc usage are:

- `docs/make_docs.py` which generates documentation with a slightly custom style, automatically adding metadata read from your `pyproject.toml` file
- `docs/templates/` containing template files for both html and markdown docs
- `docs/resources/` containing some of the base `pdoc` resources as well as some custom icons for admonitions

Provided recipes:

- `make cov` generates coverage reports in text and html, as well as an svg badge. Will run tests if `.coverage` doesn't exist.
- `make docs-html` generates html documentation using pdoc
- `make docs-md` generates markdown documentation using pdoc
- `make docs-combined` generates single-file docs by using `pandoc` to process the `docs-md` output into other formats
- `make docs` generates all documentation
- `make docs-clean` cleans up the documentation generated files (keeps templates, resources, and `make_docs.py` script)

##### Build and Publish

- `make publish` runs all checks, builds the project, and then publishes it. It also prompts for the new version number and handles tagging and pushing to the repository. Will also print your pypi token to the console, so you can copy and paste it into the prompt.
- `make build` builds the project using Poetry, assuming checks have been run
- `make verify-git` verifies the git status to ensure the repository is on the correct branch and is completely synced up and clean.
- `clean` Cleans up the build artifacts, caches, and temporary files.

#### Makefile Variables

- `PACKAGE_NAME` Name of the package (default is `myproject`, change this).
- `PUBLISH_BRANCH` Branch to publish from (default is `main`).
- `PYPI_TOKEN_FILE` File containing the PyPI token (default is `.pypi-token`).
- `LAST_VERSION_FILE` File containing the last version (default is `.lastversion`).
- `COVERAGE_REPORTS_DIR` Directory for coverage reports (default is `docs/coverage`).
- `TESTS_DIR` Directory containing tests (default is `tests/`).
- `TESTS_TEMP_DIR` Temporary directory for tests (default is `tests/_temp`), which will be cleaned up.
- `PYPROJECT` Path to project config (default is `pyproject.toml`).
- `VERSION` Extracted automatically from `pyproject.toml`.
- `LAST_VERSION` Extracted from `.lastversion`, `NONE` if the file doesn't exist.
- `PYTHON_BASE` Base Python command (default is `python`). 
- `RUN_GLOBAL` Flag to determine whether to run Python globally or via Poetry (default is `0`).
- `PYTHON` Python command determined by `RUN_GLOBAL`. Will have `poetry run` prepended if `RUN_GLOBAL` is `0`.
- `PYTEST_OPTIONS` Optional parameters to pass to `pytest`.
- `COV` Determines if coverage should be reported (`1` by default), prepends `--cov=.` to `PYTEST_OPTIONS` if `1`.
- `VERBOSE` If defined, will append `--verbose` to `PYTEST_OPTIONS`.



[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.2/__init__.py#L0-L2)





> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.0.2







[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.2/helloworld.py)

# `myproject.helloworld` { #myproject.helloworld }


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.0.2/helloworld.py#L0-L0)




