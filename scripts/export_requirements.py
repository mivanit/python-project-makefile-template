import sys

if sys.version_info >= (3, 11):
	import tomllib
else:
	import tomli as tomllib
from pathlib import Path
from typing import Union, List

pyproject_path: Path = Path(sys.argv[1])
output_dir: Path = Path(sys.argv[2])

with open(pyproject_path, "rb") as f:
	pyproject_data: dict = tomllib.load(f)

# all available groups
all_groups: List[str] = list(pyproject_data.get("dependency-groups", {}).keys())
all_extras: List[str] = list(
	pyproject_data.get("project", {}).get("optional-dependencies", {}).keys()
)

# options for exporting
export_opts: dict = pyproject_data.get("tool", {}).get("uv-exports", {})

# what are we exporting?
exports: List[str] = export_opts.get("exports", [])
if not exports:
	exports = [{"name": "all", "groups": [], "extras": [], "options": []}]

# export each configuration
for export in exports:
	# get name and validate
	name = export.get("name")
	if not name or not name.isalnum():
		print(
			f"Export configuration missing valid 'name' field {export}", file=sys.stderr
		)
		continue

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

	cmd.extend(options)

	output_path = output_dir / filename
	print(f"{' '.join(cmd)} > {output_path.as_posix()}")
