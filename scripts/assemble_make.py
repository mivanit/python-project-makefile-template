from pathlib import Path

TEMPLATE_PATH: Path = Path("makefile.template")
MAKEFILE_PATH: Path = Path("Makefile")
SCRIPTS_DIR: Path = Path("scripts")
TEMPLATE_SYNTAX: str = "#{{SCRIPT_{script_name}}}#"
IGNORE_SCRIPTS: set[str] = {"assemble_make"}


def read_scripts(scripts_dir: Path = SCRIPTS_DIR) -> dict[str, str]:
	scripts: dict[str, str] = {}
	for script in scripts_dir.iterdir():
		if script.is_file() and script.suffix == ".py":
			scripts[script.stem] = script.read_text()
	return scripts

def main():
	template_contents: str = TEMPLATE_PATH.read_text()
	scripts: dict[str, str] = read_scripts()
	for script_name, script_contents in scripts.items():
		if script_name in IGNORE_SCRIPTS:
			continue

		template_replace: str = TEMPLATE_SYNTAX.format(script_name=script_name.upper())
		assert template_replace in template_contents, f"Template syntax not found in {TEMPLATE_PATH}:\n{template_replace}"

		template_contents = template_contents.replace(
			template_replace,
			script_contents,
		)

	MAKEFILE_PATH.write_text(template_contents)


if __name__ == "__main__":
	main()

