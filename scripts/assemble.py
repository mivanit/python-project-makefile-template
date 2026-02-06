"add version to the makefile template"

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
"path to all scripts, including this one and make docs"

TEMPLATE_SYNTAX: str = "##[[{var}]]##"
"template syntax in the makefile and make_docs templates"

DOCS_MAKE_PATH: Path = SCRIPTS_DIR / "make_docs.py"
"path to the make_docs script template"

DOCS_MAKE_PATH_OUT: Path = Path("docs/resources/make_docs.py")
"path to the make_docs script output"

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


def assemble_make_docs() -> None:
	"assemble the make_docs script"
	make_docs_base: str = DOCS_MAKE_PATH.read_text()
	make_docs_base = make_docs_base.replace(
		TEMPLATE_SYNTAX.format(var="VERSION"),
		VERSION,
	)
	DOCS_MAKE_PATH_OUT.write_text(make_docs_base)


if __name__ == "__main__":
	assemble_make()
	assemble_make_docs()
