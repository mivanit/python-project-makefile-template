from pathlib import Path
from typing import Dict

try:
	import tomllib  # Python 3.11+
except ImportError:
	import tomli as tomllib # type: ignore

TEMPLATE_PATH: Path = Path("makefile.template")
MAKEFILE_PATH: Path = Path("Makefile")
SCRIPTS_DIR: Path = Path("scripts")
TEMPLATE_SYNTAX: str = "##[[{var}]]##"
IGNORE_SCRIPTS: set[str] = {"assemble_make"}

with open("pyproject.toml", "rb") as f_pyproject:
	VERSION: str = tomllib.load(f_pyproject)["project"]["version"]


def read_scripts(scripts_dir: Path = SCRIPTS_DIR) -> Dict[str, str]:
	scripts: Dict[str, str] = {}
	for script in scripts_dir.iterdir():
		if script.is_file() and script.suffix == ".py":
			scripts[script.stem] = script.read_text()
	return scripts


def main() -> None:
	contents: str = TEMPLATE_PATH.read_text()
	scripts: Dict[str, str] = read_scripts()

	# inline each script
	for script_name, script_contents in scripts.items():
		if script_name in IGNORE_SCRIPTS:
			continue

		template_replace: str = TEMPLATE_SYNTAX.format(
			var=f"SCRIPT_{script_name.upper()}"
		)
		assert template_replace in contents, (
			f"Template syntax not found in {TEMPLATE_PATH}:\n{template_replace}"
		)

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


if __name__ == "__main__":
	main()
