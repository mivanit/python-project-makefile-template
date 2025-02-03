import sys

try:
	if sys.version_info >= (3, 11):
		import tomllib
	else:
		import tomli as tomllib

	pyproject_path = "$(PYPROJECT)"

	with open(pyproject_path, "rb") as f:
		pyproject_data = tomllib.load(f)

	print("v" + pyproject_data["project"]["version"], end="")
except Exception:
	print("NULL", end="")
	sys.exit(1)
