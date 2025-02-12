import sys
import warnings

if sys.version_info >= (3, 11):
	import tomllib
else:
	import tomli as tomllib
from pathlib import Path
from typing import Any, Union, List
from functools import reduce

TOOL_PATH: str = "tool.makefile.uv-exports"


def deep_get(d: dict, path: str, default: Any = None, sep: str = ".") -> Any:
	return reduce(
		lambda x, y: x.get(y, default) if isinstance(x, dict) else default,  # function
		path.split(sep) if isinstance(path, str) else path,  # sequence
		d,  # initial
	)


def export_configuration(
	export: dict,
	all_groups: List[str],
	all_extras: List[str],
	export_opts: dict,
	output_dir: Path,
):
	# get name and validate
	name = export.get("name")
	if not name or not name.isalnum():
		warnings.warn(
			f"Export configuration missing valid 'name' field {export}",
			file=sys.stderr,
		)
		return

	# get other options with default fallbacks
	filename: str = export.get("filename") or f"requirements-{name}.txt"
	groups: Union[List[str], bool, None] = export.get("groups", None)
	extras: Union[List[str], bool] = export.get("extras", [])
	options: List[str] = export.get("options", [])

	# init command
	cmd: List[str] = ["uv", "export"] + export_opts.get("args", [])

	# handle groups
	if groups is not None:
		groups_list: List[str] = []
		if isinstance(groups, bool):
			if groups:
				groups_list = all_groups.copy()
		else:
			groups_list = groups

		for group in all_groups:
			if group in groups_list:
				cmd.extend(["--group", group])
			else:
				cmd.extend(["--no-group", group])

	# handle extras
	extras_list: List[str] = []
	if isinstance(extras, bool):
		if extras:
			extras_list = all_extras.copy()
	else:
		extras_list = extras

	for extra in extras_list:
		cmd.extend(["--extra", extra])

	# add extra options
	cmd.extend(options)

	# assemble the command and print to console -- makefile will run it
	output_path = output_dir / filename
	print(f"{' '.join(cmd)} > {output_path.as_posix()}")


def main(
	pyproject_path: Path,
	output_dir: Path,
):
	# read pyproject.toml
	with open(pyproject_path, "rb") as f:
		pyproject_data: dict = tomllib.load(f)

	# all available groups
	all_groups: List[str] = list(pyproject_data.get("dependency-groups", {}).keys())
	all_extras: List[str] = list(
		deep_get(pyproject_data, "project.optional-dependencies", {}).keys()
	)

	# options for exporting
	export_opts: dict = deep_get(pyproject_data, TOOL_PATH, {})

	# what are we exporting?
	exports: List[str] = export_opts.get("exports", [])
	if not exports:
		exports = [{"name": "all", "groups": [], "extras": [], "options": []}]

	# export each configuration
	for export in exports:
		export_configuration(
			export=export,
			all_groups=all_groups,
			all_extras=all_extras,
			export_opts=export_opts,
			output_dir=output_dir,
		)


if __name__ == "__main__":
	main(
		pyproject_path=Path(sys.argv[1]),
		output_dir=Path(sys.argv[2]),
	)
