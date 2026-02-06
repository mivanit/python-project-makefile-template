# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Assemble the makefile and helper scripts by replacing version placeholders.

Reads version from pyproject.toml and replaces ##[[VERSION]]## placeholders in:
- makefile.template -> makefile
- scripts/make/*.py -> scripts/out/*.py
"""

from __future__ import annotations

from pathlib import Path

try:
	import tomllib  # type: ignore[import-not-found]
except ImportError:
	import tomli as tomllib  # type: ignore

MAKEFILE_TEMPLATE_PATH: Path = Path("makefile.template")
"path of the makefile template which we read"

MAKEFILE_PATH: Path = Path("makefile")
"path of the assembled makefile which we write"

SCRIPTS_DIR: Path = Path("scripts")
"path to all scripts, including this one"

SCRIPTS_MAKE_DIR: Path = SCRIPTS_DIR / "make"
"path to template scripts (with version placeholders)"

SCRIPTS_OUT_DIR: Path = SCRIPTS_DIR / "out"
"path to assembled scripts (with version replaced)"

TEMPLATE_SYNTAX: str = "##[[{var}]]##"
"template syntax in the makefile and script templates"

with open("pyproject.toml", "rb") as f_pyproject:
	VERSION: str = tomllib.load(f_pyproject)["project"]["version"]


def assemble_make() -> None:
	"assemble the makefile (just version replacement)"
	contents: str = MAKEFILE_TEMPLATE_PATH.read_text()

	# version
	version_str: str = f"#| version: v{VERSION}"
	contents = contents.replace(
		TEMPLATE_SYNTAX.format(var="VERSION"),
		f"{version_str:<68}|",
	)

	MAKEFILE_PATH.write_text(contents)


def assemble_scripts() -> None:
	"read template scripts from scripts/make/, replace version, write to scripts/out/"
	SCRIPTS_OUT_DIR.mkdir(exist_ok=True)
	for script_path in SCRIPTS_MAKE_DIR.glob("*.py"):
		contents: str = script_path.read_text()
		contents = contents.replace(
			TEMPLATE_SYNTAX.format(var="VERSION"),
			VERSION,
		)
		(SCRIPTS_OUT_DIR / script_path.name).write_text(contents)


if __name__ == "__main__":
	assemble_make()
	assemble_scripts()
