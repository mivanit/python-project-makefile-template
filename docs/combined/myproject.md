> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.3.4


## Contents
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

The whole idea behind this is rather than having a bunch of stuff in your readme describing what commands you need to run to do X, you have those commands in your makefile -- rather than just being human-readable, they are machine-readable.

# How to use this:

- `make` should already be on your system, unless you are on windows
  - I recommend using [gitforwindows.org](https://gitforwindows.org), or just using WSL
- you will need [uv](https://docs.astral.sh/uv/) and some form of python installed.
- run `uv init` or otherwise set up a `pyproject.toml` file
  - the `pyproject.toml` of this repo has dev dependencies that you might need, you may want to copy those
  - it's also got some configuration that is worth looking at
- copy `makefile` from this repo into the root of your repo
- modify `PACKAGE_NAME := myproject` at the top of the makefile to match your package name
  - there are also a variety of other variables you can modify -- most are at the top of the makefile
- if you want automatic documentation generation, copy `docs/resources/`. it contains:
  - `docs/resources/make_docs.py` script to generate the docs using pdoc. reads everything it needs from your `pyproject.toml`
  - `docs/resources/templates/`: jinja2 templates for the docs, template for the todolist
  - `docs/resources/css/`, `docs/resources/svg/`: some css and icons for the docs


# docs

you can see the generated docs for this repo at [`miv.name/python-project-makefile-template`](https://miv.name/python-project-makefile-template), or the generated docs for the notebooks at [`miv.name/python-project-makefile-template/notebooks`](https://miv.name/python-project-makefile-template/notebooks)

# Makefile

`make help` Displays the help message listing all available make targets and variables. running just `make` will also display this message.

```sh
$ make help
# make targets:
    make build                build the package
    make check                run format checks, tests, and typing checks
    make clean                clean up temporary files
    make clean-all            clean up all temporary files, dep files, venv, and generated docs
    make cov                  generate coverage reports
    make dep                  Exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
    make dep-check            Checking that exported requirements are up to date
    make dep-check-torch      see if torch is installed, and which CUDA version and devices it sees
    make dep-clean            clean up lock files, .venv, and requirements files
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs
    make docs-combined        generate combined (single-file) docs in markdown and convert to other formats
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         check if the source code is formatted correctly
    make help
    make info                 # makefile variables
    make info-long            # other variables
    make lmcat                write the lmcat full output to pyproject.toml:[tool.lmcat.output]
    make lmcat-tree           show in console the lmcat tree view
    make publish              run all checks, build, and then publish
    make setup                install and update via uv
    make test                 running tests
    make todo                 get all TODO's from the code
    make typing               running type checks
    make verify-git           checking git status
    make version              Current version is $(PROJ_VERSION), last auto-uploaded version is $(LAST_VERSION)
# makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.12.0 
    PACKAGE_NAME = myproject
    PROJ_VERSION = v0.0.6 
    LAST_VERSION = v0.0.5
    PYTEST_OPTIONS =  --cov=.
```

# Development

`makefile.template` is the template file for the makefile, which contains everything except python scripts which will be inserted into the makefile.

the scripts used to generate the makefile are located in `scripts/`, with the exception of `scripts/assemble_make.py` which is the script used to populate the makefile.

If developing, modify the `makefile.template` file or scripts in `scripts/`, and then run
```sh
python scripts/assemble_make.py
```


## Submodules

- [`helloworld`](#helloworld)
- [`other`](#other)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject.py)

# `myproject` { #myproject }

### Makefile Template for Python Projects

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

The whole idea behind this is rather than having a bunch of stuff in your readme describing what commands you need to run to do X, you have those commands in your makefile -- rather than just being human-readable, they are machine-readable.

### How to use this:

- `make` should already be on your system, unless you are on windows
  - I recommend using [gitforwindows.org](https://gitforwindows.org), or just using WSL
- you will need [uv](https://docs.astral.sh/uv/) and some form of python installed.
- run `uv init` or otherwise set up a `pyproject.toml` file
  - the `pyproject.toml` of this repo has dev dependencies that you might need, you may want to copy those
  - it's also got some configuration that is worth looking at
- copy `makefile` from this repo into the root of your repo
- modify `PACKAGE_NAME := myproject` at the top of the makefile to match your package name
  - there are also a variety of other variables you can modify -- most are at the top of the makefile
- if you want automatic documentation generation, copy `docs/resources/`. it contains:
  - `docs/resources/make_docs.py` script to generate the docs using pdoc. reads everything it needs from your `pyproject.toml`
  - `docs/resources/templates/`: jinja2 templates for the docs, template for the todolist
  - `docs/resources/css/`, `docs/resources/svg/`: some css and icons for the docs


### docs

you can see the generated docs for this repo at [`miv.name/python-project-makefile-template`](https://miv.name/python-project-makefile-template), or the generated docs for the notebooks at [`miv.name/python-project-makefile-template/notebooks`](https://miv.name/python-project-makefile-template/notebooks)

### Makefile

`make help` Displays the help message listing all available make targets and variables. running just `make` will also display this message.

```sh
$ make help
### make targets:
    make build                build the package
    make check                run format checks, tests, and typing checks
    make clean                clean up temporary files
    make clean-all            clean up all temporary files, dep files, venv, and generated docs
    make cov                  generate coverage reports
    make dep                  Exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
    make dep-check            Checking that exported requirements are up to date
    make dep-check-torch      see if torch is installed, and which CUDA version and devices it sees
    make dep-clean            clean up lock files, .venv, and requirements files
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs
    make docs-combined        generate combined (single-file) docs in markdown and convert to other formats
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         check if the source code is formatted correctly
    make help
    make info                 # makefile variables
    make info-long            # other variables
    make lmcat                write the lmcat full output to pyproject.toml:[tool.lmcat.output]
    make lmcat-tree           show in console the lmcat tree view
    make publish              run all checks, build, and then publish
    make setup                install and update via uv
    make test                 running tests
    make todo                 get all TODO's from the code
    make typing               running type checks
    make verify-git           checking git status
    make version              Current version is $(PROJ_VERSION), last auto-uploaded version is $(LAST_VERSION)
### makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.12.0 
    PACKAGE_NAME = myproject
    PROJ_VERSION = v0.0.6 
    LAST_VERSION = v0.0.5
    PYTEST_OPTIONS =  --cov=.
```

### Development

`makefile.template` is the template file for the makefile, which contains everything except python scripts which will be inserted into the makefile.

the scripts used to generate the makefile are located in `scripts/`, with the exception of `scripts/assemble_make.py` which is the script used to populate the makefile.

If developing, modify the `makefile.template` file or scripts in `scripts/`, and then run
```sh
python scripts/assemble_make.py
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject.py#L0-L0)





> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.3.4


## Contents
dummy module


## API Documentation

 - [`some_function`](#some_function)
 - [`critical_function`](#critical_function)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/helloworld.py)

# `myproject.helloworld` { #myproject.helloworld }

dummy module

[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/helloworld.py#L0-L15)



### `def some_function` { #some_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/helloworld.py#L8-L10)


dummy docstring


### `def critical_function` { #critical_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/helloworld.py#L14-L16)


dummy docstring




> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.3.4


## Contents
a module


## API Documentation

 - [`another_function`](#another_function)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/other.py)

# `myproject.other` { #myproject.other }

a module

[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/other.py#L0-L6)



### `def another_function` { #another_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.3.4myproject/other.py#L5-L7)


dummy docstring



