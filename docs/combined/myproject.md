> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.5.1


## Contents
# Makefile Template for Python Projects

I've ended up using the same style of makefile for multiple Python projects, so I've decided to create a repository with a template. The idea is to have a makefile that can be easily copied into any python project, and that provides a standard set of commands for common tasks like testing, formatting, type checking, documentation generation, and dependency management.

Relevant ideological decisions:

- **everything contained in github actions should be minimal, and mostly consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`ty`](https://github.com/astral-sh/ty), [`mypy`](https://github.com/python/mypy), and [`basedpyright`](https://github.com/DetachHead/basedpyright) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation
  - I know there are better build tools out there and it's overkill, but `make` is universal. you can think of this as a bunch of hacky additions to `make` to make it a tad more like a modern build tool for python projects
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
- run `make setup` to download helper scripts and sync dependencies
- modify `PACKAGE_NAME := myproject` at the top of the makefile to match your package name
  - there are also a variety of other variables you can modify -- most are at the top of the makefile
- if you want automatic documentation generation, copy `docs/resources/`. it contains:
  - `docs/resources/templates/`: jinja2 templates for the docs, template for the todolist
  - `docs/resources/css/`, `docs/resources/svg/`: some css and icons for the docs


# docs

you can see the generated docs for this repo at [`miv.name/python-project-makefile-template`](https://miv.name/python-project-makefile-template), or the generated docs for the notebooks at [`miv.name/python-project-makefile-template/notebooks`](https://miv.name/python-project-makefile-template/notebooks)

# Makefile

## General Help

`make help` Displays the help message listing all available make targets and variables. Running just `make` will also display this message.

```sh
$ make help
# make targets:
    make build                build the package
    make check                run format checks, tests, and typing checks
    make clean                clean up temporary files
    make clean-all            clean up all temporary files, dep files, venv, and generated docs
    make cov                  generate coverage reports
    make dep                  syncing and exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
    make dep-check            Checking that exported requirements are up to date
    make dep-check-torch      see if torch is installed, and which CUDA version and devices it sees
    make dep-clean            clean up lock files, .venv, and requirements files
    make dep-compile          syncing dependencies with bytecode compilation
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs except resources
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         check if the source code is formatted correctly
    make info                 # makefile variables
    make info-long            # other variables
    make lmcat                write the lmcat full output to pyproject.toml:[tool.lmcat.output]
    make lmcat-tree           show in console the lmcat tree view
    make publish              Ready to publish $(PROJ_VERSION) to PyPI
    make self-setup-scripts   downloading makefile scripts (version: $(SCRIPTS_VERSION))
    make setup                download scripts and sync dependencies
    make test                 running tests
    make todo                 get all TODO's from the code
    make typing               running type checks
    make typing-summary       running type checks and saving to $(TYPE_ERRORS_DIR)/
    make verify-git           checking git status
    make version              Current version is $(PROJ_VERSION), last auto-uploaded version is $(LAST_VERSION)
# makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.9.23 
    PACKAGE_NAME = myproject
    PROJ_VERSION = v0.5.0 
    LAST_VERSION = v0.0.1 
    PYTEST_OPTIONS = 

To get detailed info about specific make targets or variables, use:
  make help=TARGET    or    make HELP="TARGET1 TARGET2"
  make help=VARIABLE  - shows variable values (case-insensitive)
  make H=*            or    make h=--all
```

## Detailed Help for Specific Targets

You can get detailed information about specific make targets using the `help` variable:

```sh
# Get detailed info about a single target
$ make help=test
test:
  running tests
  depends-on: clean

# Get info about multiple targets
$ make HELP="test clean"
test:
  running tests
  depends-on: clean
clean:
  clean up temporary files
  comments:
    cleans up temp files from formatter, type checking, tests, coverage
    removes all built files
    removes $(TESTS_TEMP_DIR) to remove temporary test files
    ...

# Get info about all targets (wildcard expansion)
$ make h=*
# or
$ make H=--all

# Pattern matching - all targets starting with "dep"
$ make help="dep*"
dep-check-torch:
  see if torch is installed, and which CUDA version and devices it sees
dep:
  Exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
dep-check:
  Checking that exported requirements are up to date
dep-clean:
  clean up lock files, .venv, and requirements files
```

All these variations work:
- `make help=TARGET` or `make HELP=TARGET`
- `make h=TARGET` or `make H=TARGET`
- `make help="TARGET1 TARGET2"` (multiple targets)
- `make help=*` or `make h=--all` (all targets)
- `make help="dep*"` (pattern matching with wildcards)
- `make HELP="*clean"` (any target ending in "clean")

Pattern matching supports shell-style wildcards:
- `*` - matches any characters
- `?` - matches any single character
- `[abc]` - matches any character in brackets





# Configuration Reference

The `pyproject.toml` file contains custom configuration sections for this makefile system. All options have sensible defaults.

## `[tool.makefile.docs]` - Documentation Generation

Settings for `make docs`, `make docs-html`, `make docs-md`, and `make docs-clean`:

```toml
[tool.makefile.docs]
    # Base directory for all generated documentation
    # Default: "docs"
    output_dir = "docs"

    # Files/directories preserved during `make docs-clean`
    # Paths are relative to output_dir
    # Default: []
    no_clean = [".nojekyll"]

    # Shifts heading levels in combined markdown output (make docs-md)
    # With increment=2: # H1 → ### H3, ## H2 → #### H4
    # Useful when embedding generated docs in a larger document
    # Default: 2
    markdown_headings_increment = 2

    # Regex patterns for pdoc warnings to suppress
    # Matched against warning messages; use ".*pattern.*" for partial matches
    # Default: [] (show all warnings)
    warnings_ignore = [
        ".*No docstring.*",
        ".*Private member.*",
    ]

    # Jupyter notebook conversion settings
    [tool.makefile.docs.notebooks]
        # Master switch - set to true to convert .ipynb files to HTML
        # Requires nbformat and nbconvert packages
        # Default: false
        enabled = true

        # Directory containing source .ipynb files
        # Default: "notebooks"
        source_path = "notebooks"

        # Output subdirectory relative to output_dir
        # Default: "notebooks"
        output_path_relative = "notebooks"

        # Custom Jinja2 template for notebooks index page
        # Available variables: notebooks (list of dicts with ipynb, html, desc)
        # Default: built-in template
        # index_template = "..."

        # Map notebook filename (without .ipynb) to description
        # Shown on the notebooks index page
        # Notebooks not listed here appear with no description
        [tool.makefile.docs.notebooks.descriptions]
            "example" = "Example notebook showing basic usage"
            "advanced" = "Advanced usage patterns"
```

## `[tool.makefile.uv-exports]` - Dependency Export

Settings for `make dep` which exports dependencies to `.meta/requirements/`:

```toml
[tool.makefile.uv-exports]
    # Global args passed to ALL uv export commands
    # Default: []
    args = ["--no-hashes"]

    # Each entry generates a requirements file in .meta/requirements/
    # Default: [{ name = "all" }] (just base dependencies)
    exports = [
        # name (required): identifier for this export
        #   - must be alphanumeric
        #   - generates filename "requirements-{name}.txt" by default
        #
        # groups: which dependency groups to include
        #   - true: include ALL groups from [dependency-groups]
        #   - false: exclude ALL groups (base dependencies only)
        #   - ["dev", "lint"]: include only these specific groups
        #   - omitted/null: no group filtering
        #
        # extras: which optional dependencies to include
        #   - true: include ALL extras from [project.optional-dependencies]
        #   - false or []: no extras
        #   - ["cli"]: include only these specific extras
        #
        # filename: override the output filename
        #
        # options: raw args passed directly to uv export

        # Base dependencies only (from [project.dependencies])
        { name = "base", groups = false, extras = false },

        # All dependency groups, no extras
        { name = "groups", groups = true, extras = false },

        # Only the lint group - using raw uv options
        { name = "lint", options = ["--only-group", "lint"] },

        # Everything with custom filename
        { name = "all", filename = "requirements.txt", groups = true, extras = true },
    ]
```

## `[tool.makefile.inline-todo]` - TODO Extraction

Settings for `make todo` which finds TODO/FIXME/BUG comments and generates reports:

```toml
[tool.makefile.inline-todo]
    # Root directory to search for TODOs
    # Default: "."
    search_dir = "."

    # Base path for output files (without extension)
    # Generates multiple files:
    #   - {base}.jsonl: raw data, one JSON object per line
    #   - {base}-standard.md: grouped by tag, then by file
    #   - {base}-table.md: flat table format
    #   - {base}.html: interactive HTML viewer
    # Default: "docs/todo-inline"
    out_file_base = "docs/other/todo-inline"

    # Lines of context to include before/after each TODO
    # Default: 2
    context_lines = 2

    # File extensions to scan (without dots)
    # Default: ["py", "md"]
    extensions = ["py", "md"]

    # Comment tags to search for (case-sensitive, exact match)
    # Must be surrounded by valid boundary characters (space, colon, brackets, etc.)
    # Default: ["CRIT", "TODO", "FIXME", "HACK", "BUG"]
    tags = ["CRIT", "TODO", "FIXME", "HACK", "BUG", "DOC"]

    # Glob patterns to exclude from search
    # Default: ["docs/**", ".venv/**"]
    exclude = ["docs/**", ".venv/**", "scripts/get_todos.py"]

    # Git branch for GitHub code links
    # Links point to: {repo_url}/blob/{branch}/{file}#L{line}
    # Default: "main"
    branch = "main"

    # Repository URL for GitHub links
    # Auto-detected from [project.urls.Repository] or [project.urls.github]
    # Only set this to override auto-detection
    # repo_url = "https://github.com/user/repo"

    # Map comment tags to GitHub issue labels
    # Used when generating "create issue" links
    # Tags not in this map use the tag name as the label
    # Defaults: CRIT/FIXME/BUG → "bug", TODO/HACK → "enhancement"
    [tool.makefile.inline-todo.tag_label_map]
        "CRIT" = "bug"
        "BUG" = "bug"
        "FIXME" = "bug"
        "TODO" = "enhancement"
        "HACK" = "enhancement"
        "DOC" = "documentation"
```




# Development

`makefile.template` is the template file for the makefile. Helper scripts are in `scripts/make/` and are downloaded from GitHub via `make self-setup-scripts`.

If developing, modify `makefile.template` or scripts in `scripts/make/`, then run:
```sh
python scripts/assemble.py
```

## Project Structure

```
python-project-makefile-template/
├── .github/workflows/       # CI/CD workflows (minimal, just call makefile recipes)
├── .meta/
│   ├── scripts/             # Runtime scripts (used by makefile)
│   ├── requirements/        # Generated requirements.txt files
│   ├── versions/            # Version tracking files (.version, .lastversion)
│   └── local/               # Local files (tokens, logs) - not in git
├── scripts/
│   ├── assemble.py          # Assembles makefile and scripts from templates
│   ├── make/                # Source scripts (templates with version placeholders)
│   └── out/                 # Assembled scripts (generated, with version replaced)
├── docs/                    # Generated documentation (via `make docs`)
│   ├── resources/           # Templates, CSS, SVG (not auto-cleaned)
│   └── ...                  # Generated HTML, markdown, coverage reports
├── myproject/               # Example Python package (replace with your package)
├── tests/                   # pytest test directory
├── notebooks/               # Jupyter notebooks (optional, for docs generation)
├── makefile                 # Generated makefile (from makefile.template)
├── makefile.template        # Makefile source with version placeholders
└── pyproject.toml           # Project configuration
```

## Scripts System

There are three script directories that serve different purposes:

| Directory        | Purpose                                                            | When Modified                                                                   |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `scripts/make/`  | **Source templates** - edit these when developing                  | Manual edits                                                                    |
| `scripts/out/`   | **Assembled output** - generated from `scripts/make/` for download | `python scripts/assemble.py`                                                    |
| `.meta/scripts/` | **Runtime scripts** - used by makefile at runtime                  | `make self-setup-scripts` -- this is what projects using this template will use |
|                  |                                                                    |                                                                                 |

**For users of this template:** You don't need to modify scripts. Just run `make self-setup-scripts` to download the latest versions.

**For developers of this template:**
1. Edit scripts in `scripts/make/`
2. Run `python scripts/assemble.py` to generate `scripts/out/` and `.meta/scripts/`
3. The `##[[VERSION]]##` placeholder gets replaced with the version from `pyproject.toml`

# Version System

The makefile tracks two versions:

| File                          | Variable       | Purpose                        |
| ----------------------------- | -------------- | ------------------------------ |
| `pyproject.toml`              | `PROJ_VERSION` | Current version of the package |
| `.meta/versions/.lastversion` | `LAST_VERSION` | Last version published to PyPI |

**The `scripts/assemble.py` script:**
- Reads version from `pyproject.toml`
- Replaces `##[[VERSION]]##` placeholders in `makefile.template` → `makefile`
- Replaces `##[[VERSION]]##` placeholders in `scripts/make/*.py` → `scripts/out/*.py` and `.meta/scripts/*.py`


## Submodules

- [`helloworld`](#helloworld)
- [`other`](#other)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject.py)

# `myproject` { #myproject }

### Makefile Template for Python Projects

I've ended up using the same style of makefile for multiple Python projects, so I've decided to create a repository with a template. The idea is to have a makefile that can be easily copied into any python project, and that provides a standard set of commands for common tasks like testing, formatting, type checking, documentation generation, and dependency management.

Relevant ideological decisions:

- **everything contained in github actions should be minimal, and mostly consist of calling makefile recipes**
- [`uv`](https://docs.astral.sh/uv/) for dependency management and packaging
- [`pytest`](https://docs.pytest.org) for testing
- [`ty`](https://github.com/astral-sh/ty), [`mypy`](https://github.com/python/mypy), and [`basedpyright`](https://github.com/DetachHead/basedpyright) for static type checking
- [`ruff`](https://docs.astral.sh/ruff/) for formatting
- [`pdoc`](https://pdoc.dev) for documentation generation
- [`make`](https://en.wikipedia.org/wiki/Make_(software)) for automation
  - I know there are better build tools out there and it's overkill, but `make` is universal. you can think of this as a bunch of hacky additions to `make` to make it a tad more like a modern build tool for python projects
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
- run `make setup` to download helper scripts and sync dependencies
- modify `PACKAGE_NAME := myproject` at the top of the makefile to match your package name
  - there are also a variety of other variables you can modify -- most are at the top of the makefile
- if you want automatic documentation generation, copy `docs/resources/`. it contains:
  - `docs/resources/templates/`: jinja2 templates for the docs, template for the todolist
  - `docs/resources/css/`, `docs/resources/svg/`: some css and icons for the docs


### docs

you can see the generated docs for this repo at [`miv.name/python-project-makefile-template`](https://miv.name/python-project-makefile-template), or the generated docs for the notebooks at [`miv.name/python-project-makefile-template/notebooks`](https://miv.name/python-project-makefile-template/notebooks)

### Makefile

#### General Help

`make help` Displays the help message listing all available make targets and variables. Running just `make` will also display this message.

```sh
$ make help
### make targets:
    make build                build the package
    make check                run format checks, tests, and typing checks
    make clean                clean up temporary files
    make clean-all            clean up all temporary files, dep files, venv, and generated docs
    make cov                  generate coverage reports
    make dep                  syncing and exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
    make dep-check            Checking that exported requirements are up to date
    make dep-check-torch      see if torch is installed, and which CUDA version and devices it sees
    make dep-clean            clean up lock files, .venv, and requirements files
    make dep-compile          syncing dependencies with bytecode compilation
    make docs                 generate all documentation and coverage reports
    make docs-clean           remove generated docs except resources
    make docs-html            generate html docs
    make docs-md              generate combined (single-file) docs in markdown
    make format               format the source code
    make format-check         check if the source code is formatted correctly
    make info                 # makefile variables
    make info-long            # other variables
    make lmcat                write the lmcat full output to pyproject.toml:[tool.lmcat.output]
    make lmcat-tree           show in console the lmcat tree view
    make publish              Ready to publish $(PROJ_VERSION) to PyPI
    make self-setup-scripts   downloading makefile scripts (version: $(SCRIPTS_VERSION))
    make setup                download scripts and sync dependencies
    make test                 running tests
    make todo                 get all TODO's from the code
    make typing               running type checks
    make typing-summary       running type checks and saving to $(TYPE_ERRORS_DIR)/
    make verify-git           checking git status
    make version              Current version is $(PROJ_VERSION), last auto-uploaded version is $(LAST_VERSION)
### makefile variables
    PYTHON = uv run python
    PYTHON_VERSION = 3.9.23 
    PACKAGE_NAME = myproject
    PROJ_VERSION = v0.5.0 
    LAST_VERSION = v0.0.1 
    PYTEST_OPTIONS = 

To get detailed info about specific make targets or variables, use:
  make help=TARGET    or    make HELP="TARGET1 TARGET2"
  make help=VARIABLE  - shows variable values (case-insensitive)
  make H=*            or    make h=--all
```

#### Detailed Help for Specific Targets

You can get detailed information about specific make targets using the `help` variable:

```sh
### Get detailed info about a single target
$ make help=test
test:
  running tests
  depends-on: clean

### Get info about multiple targets
$ make HELP="test clean"
test:
  running tests
  depends-on: clean
clean:
  clean up temporary files
  comments:
    cleans up temp files from formatter, type checking, tests, coverage
    removes all built files
    removes $(TESTS_TEMP_DIR) to remove temporary test files
    ...

### Get info about all targets (wildcard expansion)
$ make h=*
### or
$ make H=--all

### Pattern matching - all targets starting with "dep"
$ make help="dep*"
dep-check-torch:
  see if torch is installed, and which CUDA version and devices it sees
dep:
  Exporting dependencies as per $(PYPROJECT) section 'tool.uv-exports.exports'
dep-check:
  Checking that exported requirements are up to date
dep-clean:
  clean up lock files, .venv, and requirements files
```

All these variations work:
- `make help=TARGET` or `make HELP=TARGET`
- `make h=TARGET` or `make H=TARGET`
- `make help="TARGET1 TARGET2"` (multiple targets)
- `make help=*` or `make h=--all` (all targets)
- `make help="dep*"` (pattern matching with wildcards)
- `make HELP="*clean"` (any target ending in "clean")

Pattern matching supports shell-style wildcards:
- `*` - matches any characters
- `?` - matches any single character
- `[abc]` - matches any character in brackets





### Configuration Reference

The `pyproject.toml` file contains custom configuration sections for this makefile system. All options have sensible defaults.

#### `[tool.makefile.docs]` - Documentation Generation

Settings for `make docs`, `make docs-html`, `make docs-md`, and `make docs-clean`:

```toml
[tool.makefile.docs]
    # Base directory for all generated documentation
    # Default: "docs"
    output_dir = "docs"

    # Files/directories preserved during `make docs-clean`
    # Paths are relative to output_dir
    # Default: []
    no_clean = [".nojekyll"]

    # Shifts heading levels in combined markdown output (make docs-md)
    # With increment=2: # H1 → ### H3, ## H2 → #### H4
    # Useful when embedding generated docs in a larger document
    # Default: 2
    markdown_headings_increment = 2

    # Regex patterns for pdoc warnings to suppress
    # Matched against warning messages; use ".*pattern.*" for partial matches
    # Default: [] (show all warnings)
    warnings_ignore = [
        ".*No docstring.*",
        ".*Private member.*",
    ]

    # Jupyter notebook conversion settings
    [tool.makefile.docs.notebooks]
        # Master switch - set to true to convert .ipynb files to HTML
        # Requires nbformat and nbconvert packages
        # Default: false
        enabled = true

        # Directory containing source .ipynb files
        # Default: "notebooks"
        source_path = "notebooks"

        # Output subdirectory relative to output_dir
        # Default: "notebooks"
        output_path_relative = "notebooks"

        # Custom Jinja2 template for notebooks index page
        # Available variables: notebooks (list of dicts with ipynb, html, desc)
        # Default: built-in template
        # index_template = "..."

        # Map notebook filename (without .ipynb) to description
        # Shown on the notebooks index page
        # Notebooks not listed here appear with no description
        [tool.makefile.docs.notebooks.descriptions]
            "example" = "Example notebook showing basic usage"
            "advanced" = "Advanced usage patterns"
```

#### `[tool.makefile.uv-exports]` - Dependency Export

Settings for `make dep` which exports dependencies to `.meta/requirements/`:

```toml
[tool.makefile.uv-exports]
    # Global args passed to ALL uv export commands
    # Default: []
    args = ["--no-hashes"]

    # Each entry generates a requirements file in .meta/requirements/
    # Default: [{ name = "all" }] (just base dependencies)
    exports = [
        # name (required): identifier for this export
        #   - must be alphanumeric
        #   - generates filename "requirements-{name}.txt" by default
        #
        # groups: which dependency groups to include
        #   - true: include ALL groups from [dependency-groups]
        #   - false: exclude ALL groups (base dependencies only)
        #   - ["dev", "lint"]: include only these specific groups
        #   - omitted/null: no group filtering
        #
        # extras: which optional dependencies to include
        #   - true: include ALL extras from [project.optional-dependencies]
        #   - false or []: no extras
        #   - ["cli"]: include only these specific extras
        #
        # filename: override the output filename
        #
        # options: raw args passed directly to uv export

        # Base dependencies only (from [project.dependencies])
        { name = "base", groups = false, extras = false },

        # All dependency groups, no extras
        { name = "groups", groups = true, extras = false },

        # Only the lint group - using raw uv options
        { name = "lint", options = ["--only-group", "lint"] },

        # Everything with custom filename
        { name = "all", filename = "requirements.txt", groups = true, extras = true },
    ]
```

#### `[tool.makefile.inline-todo]` - TODO Extraction

Settings for `make todo` which finds TODO/FIXME/BUG comments and generates reports:

```toml
[tool.makefile.inline-todo]
    # Root directory to search for TODOs
    # Default: "."
    search_dir = "."

    # Base path for output files (without extension)
    # Generates multiple files:
    #   - {base}.jsonl: raw data, one JSON object per line
    #   - {base}-standard.md: grouped by tag, then by file
    #   - {base}-table.md: flat table format
    #   - {base}.html: interactive HTML viewer
    # Default: "docs/todo-inline"
    out_file_base = "docs/other/todo-inline"

    # Lines of context to include before/after each TODO
    # Default: 2
    context_lines = 2

    # File extensions to scan (without dots)
    # Default: ["py", "md"]
    extensions = ["py", "md"]

    # Comment tags to search for (case-sensitive, exact match)
    # Must be surrounded by valid boundary characters (space, colon, brackets, etc.)
    # Default: ["CRIT", "TODO", "FIXME", "HACK", "BUG"]
    tags = ["CRIT", "TODO", "FIXME", "HACK", "BUG", "DOC"]

    # Glob patterns to exclude from search
    # Default: ["docs/**", ".venv/**"]
    exclude = ["docs/**", ".venv/**", "scripts/get_todos.py"]

    # Git branch for GitHub code links
    # Links point to: {repo_url}/blob/{branch}/{file}#L{line}
    # Default: "main"
    branch = "main"

    # Repository URL for GitHub links
    # Auto-detected from [project.urls.Repository] or [project.urls.github]
    # Only set this to override auto-detection
    # repo_url = "https://github.com/user/repo"

    # Map comment tags to GitHub issue labels
    # Used when generating "create issue" links
    # Tags not in this map use the tag name as the label
    # Defaults: CRIT/FIXME/BUG → "bug", TODO/HACK → "enhancement"
    [tool.makefile.inline-todo.tag_label_map]
        "CRIT" = "bug"
        "BUG" = "bug"
        "FIXME" = "bug"
        "TODO" = "enhancement"
        "HACK" = "enhancement"
        "DOC" = "documentation"
```




### Development

`makefile.template` is the template file for the makefile. Helper scripts are in `scripts/make/` and are downloaded from GitHub via `make self-setup-scripts`.

If developing, modify `makefile.template` or scripts in `scripts/make/`, then run:
```sh
python scripts/assemble.py
```

#### Project Structure

```
python-project-makefile-template/
├── .github/workflows/       # CI/CD workflows (minimal, just call makefile recipes)
├── .meta/
│   ├── scripts/             # Runtime scripts (used by makefile)
│   ├── requirements/        # Generated requirements.txt files
│   ├── versions/            # Version tracking files (.version, .lastversion)
│   └── local/               # Local files (tokens, logs) - not in git
├── scripts/
│   ├── assemble.py          # Assembles makefile and scripts from templates
│   ├── make/                # Source scripts (templates with version placeholders)
│   └── out/                 # Assembled scripts (generated, with version replaced)
├── docs/                    # Generated documentation (via `make docs`)
│   ├── resources/           # Templates, CSS, SVG (not auto-cleaned)
│   └── ...                  # Generated HTML, markdown, coverage reports
├── myproject/               # Example Python package (replace with your package)
├── tests/                   # pytest test directory
├── notebooks/               # Jupyter notebooks (optional, for docs generation)
├── makefile                 # Generated makefile (from makefile.template)
├── makefile.template        # Makefile source with version placeholders
└── pyproject.toml           # Project configuration
```

#### Scripts System

There are three script directories that serve different purposes:

| Directory        | Purpose                                                            | When Modified                                                                   |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `scripts/make/`  | **Source templates** - edit these when developing                  | Manual edits                                                                    |
| `scripts/out/`   | **Assembled output** - generated from `scripts/make/` for download | `python scripts/assemble.py`                                                    |
| `.meta/scripts/` | **Runtime scripts** - used by makefile at runtime                  | `make self-setup-scripts` -- this is what projects using this template will use |
|                  |                                                                    |                                                                                 |

**For users of this template:** You don't need to modify scripts. Just run `make self-setup-scripts` to download the latest versions.

**For developers of this template:**
1. Edit scripts in `scripts/make/`
2. Run `python scripts/assemble.py` to generate `scripts/out/` and `.meta/scripts/`
3. The `##[[VERSION]]##` placeholder gets replaced with the version from `pyproject.toml`

### Version System

The makefile tracks two versions:

| File                          | Variable       | Purpose                        |
| ----------------------------- | -------------- | ------------------------------ |
| `pyproject.toml`              | `PROJ_VERSION` | Current version of the package |
| `.meta/versions/.lastversion` | `LAST_VERSION` | Last version published to PyPI |

**The `scripts/assemble.py` script:**
- Reads version from `pyproject.toml`
- Replaces `##[[VERSION]]##` placeholders in `makefile.template` → `makefile`
- Replaces `##[[VERSION]]##` placeholders in `scripts/make/*.py` → `scripts/out/*.py` and `.meta/scripts/*.py`


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject.py#L0-L0)





> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.5.1


## Contents
dummy module


## API Documentation

 - [`some_function`](#some_function)
 - [`critical_function`](#critical_function)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/helloworld.py)

# `myproject.helloworld` { #myproject.helloworld }

dummy module

[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/helloworld.py#L0-L15)



### `def some_function` { #some_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/helloworld.py#L8-L10)


dummy docstring


### `def critical_function` { #critical_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/helloworld.py#L14-L16)


dummy docstring




> docs for [`myproject`](https://github.com/mivanit/python-project-makefile-template) v0.5.1


## Contents
a module


## API Documentation

 - [`another_function`](#another_function)




[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/other.py)

# `myproject.other` { #myproject.other }

a module

[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/other.py#L0-L6)



### `def another_function` { #another_function }
```python
() -> None
```


[View Source on GitHub](https://github.com/mivanit/python-project-makefile-template/blob/0.5.1myproject/other.py#L5-L7)


dummy docstring



