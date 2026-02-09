# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: ##[[VERSION]]##
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Generate GitHub-style SVG badges for coverage, tests, or arbitrary label/value pairs.

Usage:
    python generate_badge.py [OPTIONS]

Examples:
    # Generic badge
    python generate_badge.py --label "version" --value "1.2.3" -o version.svg
    python generate_badge.py --label "license" --value "MIT" --color blue -o license.svg

    # Coverage badge (reads from .coverage sqlite db)
    python generate_badge.py --coverage .coverage -o coverage.svg

    # Tests badge (parses pytest output)
    python generate_badge.py --pytest-results .pytest_results.txt -o tests.svg

"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

# Color presets (GitHub badge style)
COLORS: dict[str, str] = {
	"brightgreen": "#4c1",
	"green": "#97ca00",
	"yellowgreen": "#a4a61d",
	"yellow": "#dfb317",
	"orange": "#fe7d37",
	"red": "#e05d44",
	"blue": "#007ec6",
	"gray": "#555",
	"lightgray": "#9f9f9f",
}


def get_coverage_color(percent: float) -> str:
	"""Get color based on coverage percentage."""
	if percent >= 80:
		return COLORS["brightgreen"]
	elif percent >= 60:
		return COLORS["yellowgreen"]
	elif percent >= 40:
		return COLORS["orange"]
	else:
		return COLORS["red"]


def get_tests_color(passed: int, failed: int) -> str:
	"""Get color based on test results."""
	if failed > 0:
		return COLORS["red"]
	elif passed > 0:
		return COLORS["brightgreen"]
	else:
		return COLORS["gray"]


def estimate_text_width(text: str) -> int:
	"""Estimate text width in pixels for the badge font.

	Uses approximate character widths for DejaVu Sans 11px.
	"""
	# Approximate widths for common characters
	narrow_chars = "iIl1|!.,;:'"
	wide_chars = "mwMWOQGD%@"

	width = 0
	for char in text:
		if char in narrow_chars:
			width += 4
		elif char in wide_chars:
			width += 10
		elif char.isupper():
			width += 8
		else:
			width += 7

	return width + 10  # Add padding


def generate_badge_svg(label: str, value: str, color: str) -> str:
	"""Generate a GitHub-style flat badge SVG.

	Args:
	    label: Left side text (e.g., "coverage", "tests")
	    value: Right side text (e.g., "85%", "42 passed")
	    color: Hex color for the value background (with or without #)

	Returns:
	    SVG string

	"""
	if not color.startswith("#"):
		color = f"#{color}"

	label_width = estimate_text_width(label)
	value_width = estimate_text_width(value)
	total_width = label_width + value_width

	label_x = label_width / 2
	value_x = label_width + value_width / 2

	svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h{label_width}v20H0z"/>
        <path fill="{color}" d="M{label_width} 0h{value_width}v20H{label_width}z"/>
        <path fill="url(#b)" d="M0 0h{total_width}v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="{label_x}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
        <text x="{label_x}" y="14">{label}</text>
        <text x="{value_x}" y="15" fill="#010101" fill-opacity=".3">{value}</text>
        <text x="{value_x}" y="14">{value}</text>
    </g>
</svg>
"""
	return svg


def read_coverage_from_db(coverage_path: Path) -> float:
	"""Read coverage percentage from .coverage sqlite database.

	Args:
	    coverage_path: Path to .coverage file

	Returns:
	    Coverage percentage (0-100)

	"""
	conn = sqlite3.connect(coverage_path)
	cursor = conn.cursor()

	# Get total lines and covered lines from the database
	try:
		# coverage.py stores arc data, we need to calculate from file table
		cursor.execute("SELECT nums_and_args FROM meta")
		# The coverage percentage is usually calculated from the line data
		# Let's try a simpler approach - read from the file table if it exists

		# Try to get summary from the coverage data
		cursor.execute("SELECT COUNT(*) FROM file")
		file_count = cursor.fetchone()[0]

		if file_count == 0:
			conn.close()
			return 0.0

		# Get line counts from line_bits table
		cursor.execute("""
            SELECT
                file.path,
                length(line_bits.numbits) as total_lines
            FROM file
            LEFT JOIN line_bits ON file.id = line_bits.file_id
        """)

		total_statements = 0
		covered_statements = 0

		# Actually, the coverage database structure varies by version
		# Let's use the coverage module directly if available
		conn.close()

		# Fall back to using coverage module
		try:
			from coverage import Coverage

			cov = Coverage(data_file=str(coverage_path))
			cov.load()
			report_data = cov.get_data()

			for filename in report_data.measured_files():
				analysis = cov._analyze(filename)
				total_statements += len(analysis.statements)
				covered_statements += len(analysis.statements) - len(analysis.missing)

			if total_statements == 0:
				return 0.0

			return (covered_statements / total_statements) * 100

		except ImportError:
			# If coverage module not available, try parsing coverage.txt
			raise RuntimeError(
				"coverage module not available, cannot read .coverage database directly"
			)

	except sqlite3.OperationalError:
		conn.close()
		raise RuntimeError(f"Could not read coverage data from {coverage_path}")


def read_coverage_from_txt(coverage_path: Path) -> float:
	"""Read coverage percentage from coverage.txt report.

	Args:
	    coverage_path: Path to coverage.txt file

	Returns:
	    Coverage percentage (0-100)

	"""
	content = coverage_path.read_text()

	# Look for TOTAL line, e.g., "TOTAL    1234    567    54%"
	match = re.search(r"^TOTAL\s+\d+\s+\d+\s+(\d+)%", content, re.MULTILINE)
	if match:
		return float(match.group(1))

	# Try alternate format with cover column
	match = re.search(r"^TOTAL\s+\d+\s+\d+\s+\d+\s+(\d+)%", content, re.MULTILINE)
	if match:
		return float(match.group(1))

	raise RuntimeError(f"Could not parse coverage percentage from {coverage_path}")


def parse_pytest_results(results_path: Path) -> tuple[int, int, int]:
	"""Parse pytest output to get test counts.

	Args:
	    results_path: Path to file containing pytest output

	Returns:
	    Tuple of (passed, failed, total)

	"""
	content = results_path.read_text()

	passed = 0
	failed = 0
	skipped = 0
	errors = 0

	# Look for summary line like "42 passed, 3 failed, 1 skipped in 1.23s"
	# or "===== 42 passed in 1.23s ====="
	summary_match = re.search(
		r"=+\s*([\d\w\s,]+(?:passed|failed|error|skipped)[^=]*)\s*=+",
		content,
		re.IGNORECASE,
	)

	if summary_match:
		summary = summary_match.group(1)

		passed_match = re.search(r"(\d+)\s*passed", summary, re.IGNORECASE)
		if passed_match:
			passed = int(passed_match.group(1))

		failed_match = re.search(r"(\d+)\s*failed", summary, re.IGNORECASE)
		if failed_match:
			failed = int(failed_match.group(1))

		skipped_match = re.search(r"(\d+)\s*skipped", summary, re.IGNORECASE)
		if skipped_match:
			skipped = int(skipped_match.group(1))

		error_match = re.search(r"(\d+)\s*error", summary, re.IGNORECASE)
		if error_match:
			errors = int(error_match.group(1))

	total = passed + failed + skipped + errors
	return passed, failed + errors, total


def resolve_color(color_input: str) -> str:
	"""Resolve color name or hex code to hex value.

	Args:
	    color_input: Color name (e.g., "green") or hex code (e.g., "#4c1" or "4c1")

	Returns:
	    Hex color code with #

	"""
	if color_input in COLORS:
		return COLORS[color_input]
	if color_input.startswith("#"):
		return color_input
	return f"#{color_input}"


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Generate GitHub-style SVG badges",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=__doc__,
	)

	# Output
	parser.add_argument(
		"-o",
		"--output",
		type=Path,
		help="Output SVG file path (default: stdout)",
	)

	# Generic mode
	parser.add_argument(
		"--label",
		type=str,
		help="Badge label (left side text)",
	)
	parser.add_argument(
		"--value",
		type=str,
		help="Badge value (right side text)",
	)
	parser.add_argument(
		"--color",
		type=str,
		default="gray",
		help="Badge color (name or hex, default: gray)",
	)

	# Coverage mode
	parser.add_argument(
		"--coverage",
		type=Path,
		metavar="PATH",
		help="Path to .coverage file or coverage.txt report",
	)

	# Tests mode
	parser.add_argument(
		"--pytest-results",
		type=Path,
		metavar="PATH",
		help="Path to file containing pytest output",
	)

	args = parser.parse_args()

	# Determine mode and generate badge
	try:
		if args.coverage:
			# Coverage mode
			coverage_path = args.coverage
			if not coverage_path.exists():
				print(
					f"Error: Coverage file not found: {coverage_path}", file=sys.stderr
				)
				return 1

			if coverage_path.suffix == ".txt" or coverage_path.name == "coverage.txt":
				percent = read_coverage_from_txt(coverage_path)
			else:
				percent = read_coverage_from_db(coverage_path)

			label = "coverage"
			value = f"{percent:.0f}%"
			color = get_coverage_color(percent)

		elif args.pytest_results:
			# Tests mode
			if not args.pytest_results.exists():
				print(
					f"Error: Pytest results file not found: {args.pytest_results}",
					file=sys.stderr,
				)
				return 1

			passed, failed, total = parse_pytest_results(args.pytest_results)
			label = "tests"

			if failed > 0:
				value = f"{passed}/{total} passed"
			else:
				value = f"{passed} passed"

			color = get_tests_color(passed, failed)

		elif args.label and args.value:
			# Generic mode
			label = args.label
			value = args.value
			color = resolve_color(args.color)

		else:
			parser.error(
				"Must specify either --coverage, --pytest-results, or both --label and --value"
			)
			return 1

		svg = generate_badge_svg(label, value, color)

		if args.output:
			args.output.parent.mkdir(parents=True, exist_ok=True)
			args.output.write_text(svg)
			print(f"Badge written to {args.output}")
		else:
			print(svg)

		return 0

	except Exception as e:
		print(f"Error: {e}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	sys.exit(main())
