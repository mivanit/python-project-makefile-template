"cli to convert markdown files to HTML using pdoc's markdown2"

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from pdoc.markdown2 import Markdown, _safe_mode  # type: ignore[import]


def convert_file(
	input_path: Path,
	output_path: Path,
	safe_mode: Optional[_safe_mode] = None,
	encoding: str = "utf-8",
) -> None:
	"""Convert a markdown file to HTML"""
	# Read markdown input
	text: str = input_path.read_text(encoding=encoding)

	# Convert to HTML using markdown2
	markdown: Markdown = Markdown(
		extras=["fenced-code-blocks", "header-ids", "markdown-in-html", "tables"],
		safe_mode=safe_mode,
	)
	html: str = markdown.convert(text)

	# Write HTML output
	output_path.write_text(str(html), encoding=encoding)


def main() -> None:
	"cli entry point"
	parser: argparse.ArgumentParser = argparse.ArgumentParser(
		description="Convert markdown files to HTML using pdoc's markdown2",
	)
	parser.add_argument("input", type=Path, help="Input markdown file path")
	parser.add_argument("output", type=Path, help="Output HTML file path")
	parser.add_argument(
		"--safe-mode",
		choices=["escape", "replace"],
		help="Sanitize literal HTML: 'escape' escapes HTML meta chars, 'replace' replaces with [HTML_REMOVED]",
	)
	parser.add_argument(
		"--encoding",
		default="utf-8",
		help="Character encoding for reading/writing files (default: utf-8)",
	)

	args: argparse.Namespace = parser.parse_args()

	convert_file(
		args.input,
		args.output,
		safe_mode=args.safe_mode,
		encoding=args.encoding,
	)


if __name__ == "__main__":
	main()
