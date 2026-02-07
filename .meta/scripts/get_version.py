# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.4.0
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Extract version from pyproject.toml and print to stdout.

Usage: python get_version.py <pyproject_path>
Prints 'v<version>' on success, 'NULL' on failure.
"""

from __future__ import annotations

import sys

try:
	try:
		import tomllib  # type: ignore[import-not-found]
	except ImportError:
		import tomli as tomllib  # type: ignore

	pyproject_path: str = sys.argv[1].strip()

	with open(pyproject_path, "rb") as f:
		pyproject_data: dict = tomllib.load(f)

	print("v" + pyproject_data["project"]["version"], end="")
except Exception:  # noqa: BLE001
	print("NULL", end="")
	sys.exit(1)
