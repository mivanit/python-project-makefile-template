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
# list make targets and variables:
	make build           build via poetry, assumes checks have been run
	make check           run format check, test, and lint
	make check-format    run format check
	make clean           cleaning up
	make cov             generate coverage reports
	make help            # list make targets and variables
	make publish         run all checks, build, and then publish
	make setup           install and update via poetry and setup shell
	make setup-format    install only packages needed for formatting, direct via pip (useful for CI)
	make test            running tests
	make verify-git      checking git status
	make version         Current version is $(VERSION), last auto-uploaded version is $(LAST_VERSION)
# makefile variables:
	PACKAGE_NAME = myproject
	VERSION = 0.0.1
	LAST_VERSION = NONE
	PYTEST_OPTIONS =  --cov=.
```

- `make` does the same as `make help`

- `make version` Displays the current version of the project and the last auto-uploaded version (via tag). It also generates a commit log since the last version (and uses this for tag descriptions when publishing)

### Setup

- `make setup` install and update via poetry and setup shell (from `pyproject.toml`)
- `make setup-format` install only packages needed for formatting, direct via pip (useful for CI)
	- this is most useful for a separate format check in CI (see `checks.yml`), and used as `make setup-format RUN_GLOBAL=1`
	- This means you can avoid installing poetry and other dependencies for a quick format check

### Formatting

- `make format` formats the code using `ruff` and `pycln`
  
- `make check-format` checks the code formatting using `ruff` and `pycln

### Testing and Linting

  
- `make test` runs tests using `pytest`, with data for coverage reports
	- you can pass `COV=0` to disable coverage reports
- `make lint` runs linting using `mypy`
  
- `make check` runs format check, test, and lint

- `make cov` generates coverage reports in text and html, as well as an svg badge. requires tests to have been run with coverage data

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
