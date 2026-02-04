"add scripts and version to the makefile -- this one isnt put in the makefile"

from __future__ import annotations

from pathlib import Path
from typing import Dict

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

SCRIPTS_MAKE_DIR: Path = SCRIPTS_DIR / "make"
"path to scripts which go in the makefile"

TEMPLATE_SYNTAX: str = "##[[{var}]]##"
"template syntax in the makefile and make_docs templates"

IGNORE_SCRIPTS: set[str] = set()
"scripts from `SCRIPTS_MAKE_DIR` to ignore"

DOCS_MAKE_PATH: Path = SCRIPTS_DIR / "make_docs.py"
"path to the make_docs script template"

DOCS_MAKE_PATH_OUT: Path = Path("docs/resources/make_docs.py")
"path to the make_docs script output"

with open("pyproject.toml", "rb") as f_pyproject:
	VERSION: str = tomllib.load(f_pyproject)["project"]["version"]


def read_scripts(scripts_dir: Path = SCRIPTS_MAKE_DIR) -> Dict[str, str]:
	"read script contents into a dict"
	scripts: Dict[str, str] = {}
	for script in scripts_dir.iterdir():
		if script.is_file() and script.suffix == ".py":
			script_text: str = script.read_text()
			# add a link to the script
			script_text = f"# source: https://github.com/mivanit/python-project-makefile-template/tree/main/{script.as_posix()}\n\n{script_text}"
			scripts[script.stem] = script_text
	return scripts


def assemble_make() -> None:
	"assemble the makefile"
	contents: str = MAKEFILE_TEMPLATE_PATH.read_text()
	scripts: Dict[str, str] = read_scripts()

	# inline each script
	for script_name, script_contents in scripts.items():
		if script_name in IGNORE_SCRIPTS:
			continue

		template_replace: str = TEMPLATE_SYNTAX.format(
			var=f"SCRIPT_{script_name.upper()}",
		)
		if template_replace not in contents:
			msg = f"Template syntax not found in {MAKEFILE_TEMPLATE_PATH}:\n{template_replace}"
			raise ValueError(msg)

		contents = contents.replace(
			template_replace,
			script_contents,
		)

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
