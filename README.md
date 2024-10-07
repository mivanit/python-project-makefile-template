# Makefile Template for Python Projects

I've ended up using the same style of makefile for multiple Python projects, so I've decided to create a repository with a template.

Relevant ideological decisions:

- **everything contained in github actions should be minimal, and mostly consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`mypy`](https://github.com/python/mypy) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) and [`pycln`](https://github.com/hadialqattan/pycln) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation (I know there are better build tools out there and it's overkill, but `make` is universal)
- [`git`](https://github.com/git) for version control (a spicy take, I know)

# Targets

## Help & info

- `make help` Displays the help message listing all available make targets and variables. running just `make` will also display this message.
```sh
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


### Docs

Provided files for pdoc usage are:

- `docs/make_docs.py` which generates documentation with a slightly custom style, automatically adding metadata read from your `pyproject.toml` file
- `docs/templates/` containing template files for both html and markdown docs
- `docs/resources/` containing some of the base `pdoc` resources as well as some custom icons for admonitions
