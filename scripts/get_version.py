import sys

try:
	try:
		import tomllib  # Python 3.11+
	except ImportError:
		import tomli as tomllib # type: ignore

	pyproject_path: str = sys.argv[1].strip()

	with open(pyproject_path, "rb") as f:
		pyproject_data: dict = tomllib.load(f)

	print("v" + pyproject_data["project"]["version"], end="")
except Exception:
	print("NULL", end="")
	sys.exit(1)
