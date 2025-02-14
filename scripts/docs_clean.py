import sys
import shutil
from functools import reduce
from pathlib import Path
from typing import Any, List, Set

try:
	import tomllib  # Python 3.11+
except ImportError:
	import tomli as tomllib # type: ignore

TOOL_PATH: str = "tool.makefile.docs"
DEFAULT_DOCS_DIR: str = "docs"


def deep_get(d: dict, path: str, default: Any = None, sep: str = ".") -> Any:
	"""Get nested dictionary value via separated path with default."""
	return reduce(
		lambda x, y: x.get(y, default) if isinstance(x, dict) else default,  # function
		path.split(sep) if isinstance(path, str) else path,  # sequence
		d,  # initial
	)


def read_config(pyproject_path: Path) -> tuple[Path, Set[Path]]:
	if not pyproject_path.is_file():
		return Path(DEFAULT_DOCS_DIR), set()

	with pyproject_path.open("rb") as f:
		config = tomllib.load(f)

	preserved: List[str] = deep_get(config, f"{TOOL_PATH}.no_clean", [])
	docs_dir: Path = Path(deep_get(config, f"{TOOL_PATH}.output_dir", DEFAULT_DOCS_DIR))

	# Convert to absolute paths and validate
	preserve_set: Set[Path] = set()
	for p in preserved:
		full_path = (docs_dir / p).resolve()
		if not full_path.as_posix().startswith(docs_dir.resolve().as_posix()):
			raise ValueError(f"Preserved path '{p}' must be within docs directory")
		preserve_set.add(docs_dir / p)

	return docs_dir, preserve_set


def clean_docs(docs_dir: Path, preserved: Set[Path]) -> None:
	for path in docs_dir.iterdir():
		if path.is_file() and path not in preserved:
			path.unlink()
		elif path.is_dir() and path not in preserved:
			shutil.rmtree(path)


def main(
	pyproject_path: str,
	docs_dir_cli: str,
	extra_preserve: list[str],
) -> None:
	docs_dir: Path
	preserved: Set[Path]
	docs_dir, preserved = read_config(Path(pyproject_path))

	assert docs_dir.is_dir(), f"Docs directory '{docs_dir}' not found"
	assert docs_dir == Path(docs_dir_cli), (
		f"Docs directory mismatch: {docs_dir = } != {docs_dir_cli = }. this is probably because you changed one of `pyproject.toml:{TOOL_PATH}.output_dir` (the former) or `makefile:DOCS_DIR` (the latter) without updating the other."
	)

	for x in extra_preserve:
		preserved.add(Path(x))
	clean_docs(docs_dir, preserved)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3:])
