# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: ##[[VERSION]]##
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""CLI tool to get information about Makefile recipes/targets.

Parses a makefile and displays detailed info about targets including
dependencies, comments, and echo messages. Supports fuzzy matching
and wildcard patterns.

Usage: python recipe_info.py [-f makefile] [--all | target1 target2 ...]
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Literal, Set, Union, overload


@overload
def _scan_makefile(
	lines: List[str],
	target_name: str,
) -> int: ...
@overload
def _scan_makefile(
	lines: List[str],
	target_name: None = None,
) -> Dict[str, int]: ...
def _scan_makefile(
	lines: List[str],
	target_name: str | None = None,
) -> Union[Dict[str, int], int]:
	"""Scan makefile for target definitions, skipping define blocks.

	Args:
		lines: Makefile lines
		target_name: If provided, return line index for this specific target.
					If None, return dict of all targets.

	Returns:
		If target_name is None: dict mapping target names to line indices
		If target_name is provided: line index of that target, or -1 if not found

	"""
	in_define_block: bool = False
	target_rx: re.Pattern = re.compile(r"^([a-zA-Z0-9_-]+)[ \t]*:")
	targets: Dict[str, int] = {}

	for i, line in enumerate(lines):
		# Track if we're inside a define block (embedded scripts)
		if line.startswith("define "):
			in_define_block = True
			continue
		if line.startswith("endef"):
			in_define_block = False
			continue

		# Skip lines inside define blocks
		if in_define_block:
			continue

		# Match target definitions
		match = target_rx.match(line)
		if match:
			tgt_name: str = match.group(1)
			if target_name is not None:
				# Looking for specific target
				if tgt_name == target_name:
					return i
			else:
				# Collecting all targets
				targets[tgt_name] = i

	# Return results based on mode
	if target_name is not None:
		return -1  # Target not found
	return targets


def _scan_makefile_variables(lines: List[str]) -> Dict[str, int]:
	"""Scan makefile for variable definitions, skipping define blocks.

	Returns dict mapping variable names to line indices.
	Only matches variables that start with uppercase letter or underscore.
	"""
	in_define_block: bool = False
	# Match: VARNAME := value, VARNAME ?= value, VARNAME += value, VARNAME = value
	# Allow leading whitespace to match variables inside ifeq/endif blocks
	var_rx: re.Pattern = re.compile(r"^\s*([A-Z_][A-Z0-9_]*)\s*(\?=|:=|\+=|=)\s*(.*)$")
	variables: Dict[str, int] = {}

	for i, line in enumerate(lines):
		# Track if we're inside a define block
		if line.startswith("define "):
			in_define_block = True
			continue
		if line.startswith("endef"):
			in_define_block = False
			continue

		# Skip lines inside define blocks
		if in_define_block:
			continue

		# Match variable definitions
		match = var_rx.match(line)
		if match:
			var_name: str = match.group(1)
			# Only store the first definition (in case of multiple assignments)
			if var_name not in variables:
				variables[var_name] = i

	return variables


class Colors:
	"""ANSI color codes"""

	def __init__(self, enabled: bool = True) -> None:
		"init color codes, or empty strings if `not enabled`"
		if enabled:
			self.RESET = "\033[0m"
			self.BOLD = "\033[1m"
			self.RED = "\033[31m"
			self.GREEN = "\033[32m"
			self.YELLOW = "\033[33m"
			self.BLUE = "\033[34m"
			self.MAGENTA = "\033[35m"
			self.CYAN = "\033[36m"
			self.WHITE = "\033[37m"
		else:
			self.RESET = self.BOLD = ""
			self.RED = self.GREEN = self.YELLOW = ""
			self.BLUE = self.MAGENTA = self.CYAN = self.WHITE = ""


@dataclass
class MakeRecipe:
	"""Information about a Makefile recipe/target."""

	target: str
	comments: List[str]
	dependencies: List[str]
	echo_message: str

	@classmethod
	def from_makefile(cls, lines: List[str], target: str) -> MakeRecipe:
		"""Parse and create a MakeRecipe from makefile lines for *target*."""
		i: int = _scan_makefile(lines, target_name=target)
		if i == -1:
			err_msg: str = f"target '{target}' not found in makefile"
			raise ValueError(err_msg)

		line: str = lines[i]

		# contiguous comment block immediately above
		# (skip backward past .PHONY declarations and blank lines)
		comments: List[str] = []
		j: int = i - 1
		blank_count: int = 0
		stripped: str
		while j >= 0:
			stripped = lines[j].lstrip()
			if stripped.startswith("#"):
				comments.append(stripped[1:].lstrip())
				blank_count = 0  # Reset blank counter when we hit a comment
				j -= 1
			elif stripped == "":
				# Track consecutive blank lines
				blank_count += 1
				if blank_count >= 2:  # noqa: PLR2004
					# Hit 2 blank lines in a row - stop
					break
				j -= 1
			elif stripped.startswith(".PHONY:"):
				# Skip .PHONY declarations
				blank_count = 0  # Reset blank counter
				j -= 1
			else:
				# Hit a non-comment, non-blank, non-.PHONY line - stop
				break
		comments.reverse()

		# prerequisites
		deps_str: str = line.split(":", 1)[1].strip()
		deps: List[str] = deps_str.split() if deps_str else []

		# first echo in the recipe
		echo_msg: str = ""
		k: int = i + 1
		while k < len(lines) and (
			lines[k].startswith("\t") or lines[k].startswith("    ")
		):
			m = re.match(r"@?echo[ \t]+(.*)", lines[k].lstrip())
			if m:
				content: str = m.group(1).strip()
				if (content.startswith('"') and content.endswith('"')) or (
					content.startswith("'") and content.endswith("'")
				):
					content = content[1:-1]
				echo_msg = content
				break
			k += 1

		return cls(
			target=target,
			comments=comments,
			dependencies=deps,
			echo_message=echo_msg,
		)

	def describe(self, color: bool = False) -> List[str]:
		"""Return a list of description lines for this recipe."""
		output: List[str] = []
		c: Colors = Colors(enabled=color)

		# Target name (bold blue) with colon in white
		output.append(f"{c.BOLD}{c.BLUE}{self.target}{c.RESET}{c.WHITE}:{c.RESET}")

		# Echo message (description) in yellow
		if self.echo_message:
			output.append(f"  {c.YELLOW}{self.echo_message}{c.RESET}")

		# Dependencies in magenta
		if self.dependencies:
			deps_str = " ".join(
				f"{c.MAGENTA}{dep}{c.RESET}" for dep in self.dependencies
			)
			output.append(f"  {c.RED}depends-on:{c.RESET} {deps_str}")

		# Comments in green
		if self.comments:
			output.append(f"  {c.RED}comments:{c.RESET}")
			output.extend(f"    {c.GREEN}{line}{c.RESET}" for line in self.comments)

		return output


@dataclass
class MakeVariable:
	"""Information about a Makefile variable."""

	name: str
	raw_value: str  # as written in makefile, e.g., "$(shell git describe)"
	operator: Literal["=", ":=", "?=", "+="]
	comments: List[str]  # comments above the definition

	@classmethod
	def from_makefile(
		cls,
		lines: List[str],
		var_name: str,
		var_line_idx: int,
	) -> MakeVariable:
		"""Parse and create a MakeVariable from makefile lines."""
		line: str = lines[var_line_idx]

		# Parse the variable definition line (allow leading whitespace for ifeq blocks)
		var_rx: re.Pattern = re.compile(
			r"^\s*([A-Z_][A-Z0-9_]*)\s*(\?=|:=|\+=|=)\s*(.*)$"
		)
		match = var_rx.match(line)
		if not match:
			err_msg: str = f"variable '{var_name}' not found at line {var_line_idx}"
			raise ValueError(err_msg)

		operator: Literal["=", ":=", "?=", "+="] = match.group(2)  # type: ignore[assignment]
		raw_value: str = match.group(3)

		# Collect contiguous comment block above (same logic as MakeRecipe)
		comments: List[str] = []
		j: int = var_line_idx - 1
		blank_count: int = 0
		while j >= 0:
			stripped: str = lines[j].lstrip()
			if stripped.startswith("#"):
				comments.append(stripped[1:].lstrip())
				blank_count = 0
				j -= 1
			elif stripped == "":
				blank_count += 1
				if blank_count >= 2:  # noqa: PLR2004
					break
				j -= 1
			else:
				break
		comments.reverse()

		return cls(
			name=var_name,
			raw_value=raw_value,
			operator=operator,
			comments=comments,
		)

	def describe(self, color: bool = True) -> List[str]:
		"""Return a list of description lines for this variable."""
		output: List[str] = []
		c: Colors = Colors(enabled=color)

		# Variable name in bold cyan, operator in white
		output.append(
			f"{c.BOLD}{c.CYAN}{self.name}{c.RESET} {c.WHITE}{self.operator}{c.RESET}"
		)

		# Raw value in yellow
		output.append(f"  {c.YELLOW}{self.raw_value}{c.RESET}")

		# Comments in green (same style as targets)
		if self.comments:
			output.append(f"  {c.RED}comments:{c.RESET}")
			output.extend(f"    {c.GREEN}{line}{c.RESET}" for line in self.comments)

		# Hint for computed values
		output.append(f"  {c.WHITE}(run 'make info-long' for computed values){c.RESET}")

		return output


def find_all_variables(lines: List[str]) -> Dict[str, int]:
	"""Find all variable definitions in the makefile.

	Returns dict mapping variable names to line indices.
	"""
	return _scan_makefile_variables(lines)


def find_all_targets(lines: List[str]) -> List[str]:
	"""Find all .PHONY target names in the makefile."""
	# First, get all .PHONY declarations
	phony_targets: Set[str] = set()
	# Use chr(36) to get dollar sign - works both standalone and embedded in makefile
	# issue being that the makefile processes dollar sign as an escape character
	phony_pattern: re.Pattern = re.compile(r"^\.PHONY:\s+(.+)" + chr(36))

	for line in lines:
		match = phony_pattern.match(line)
		if match:
			# Get all targets from this .PHONY line (space-separated)
			target_names: List[str] = match.group(1).split()
			phony_targets.update(target_names)

	# Now scan for actual target definitions and filter to .PHONY ones
	all_target_defs: Dict[str, int] = _scan_makefile(lines)
	return [tgt for tgt in all_target_defs if tgt in phony_targets]


def get_all_recipes(lines: List[str]) -> List[MakeRecipe]:
	"""Get MakeRecipe objects for all .PHONY targets in the makefile."""
	targets: List[str] = find_all_targets(lines)
	return [MakeRecipe.from_makefile(lines, target) for target in targets]


def describe_target(makefile_path: Path, target: str) -> None:
	"""Emit the description for *target*."""
	lines: List[str] = makefile_path.read_text(encoding="utf-8").splitlines()
	recipe: MakeRecipe = MakeRecipe.from_makefile(lines, target)

	for line in recipe.describe():
		print(line)


def main() -> None:  # noqa: PLR0912, PLR0915, C901
	"""CLI entry point."""
	parser: argparse.ArgumentParser = argparse.ArgumentParser(
		"recipe_info",
		description="Get detailed information about Makefile recipes/targets and variables",
	)
	parser.add_argument(
		"-f",
		"--file",
		default="makefile",
		help="Path to the Makefile (default: ./makefile)",
	)
	parser.add_argument(
		"-a",
		"--all",
		action="store_true",
		help="Print help for all targets in the Makefile",
	)
	parser.add_argument(
		"--no-color",
		action="store_true",
		help="Disable colored output (color is enabled by default)",
	)
	parser.add_argument(
		"targets", nargs="*", help="Target or variable names (case-insensitive)"
	)
	args: argparse.Namespace = parser.parse_args()

	lines: List[str] = Path(args.file).read_text(encoding="utf-8").splitlines()
	c: Colors = Colors(enabled=not args.no_color)

	# Get all targets and variables upfront
	all_targets: List[str] = find_all_targets(lines)
	all_variables: Dict[str, int] = find_all_variables(lines)

	recipes: List[MakeRecipe] = []
	variables: List[MakeVariable] = []

	if args.all:
		recipes = get_all_recipes(lines)
	elif args.targets:
		for query in args.targets:
			has_wildcard: bool = any(char in query for char in ["*", "?", "["])

			if has_wildcard:
				# Pattern matching mode for targets
				matched_targets: List[str] = [
					t for t in all_targets if fnmatch.fnmatch(t, query)
				]
				for matched in matched_targets:
					recipes.append(MakeRecipe.from_makefile(lines, matched))

				# Pattern matching for variables (case-insensitive)
				matched_vars: List[str] = [
					v
					for v in all_variables
					if fnmatch.fnmatch(v.lower(), query.lower())
				]

				variables.extend(
					[
						MakeVariable.from_makefile(
							lines=lines,
							var_name=var_name,
							var_line_idx=all_variables[var_name],
						)
						for var_name in matched_vars
					]
				)

				if not matched_targets and not matched_vars:
					print(
						f"Error: no targets or variables match pattern "
						f"'{c.RED}{query}{c.RESET}'",
						file=sys.stderr,
					)
					sys.exit(1)
			else:
				# Exact/case-insensitive lookup
				found_target: bool = False
				found_variable: bool = False

				# Check for exact target match
				if query in all_targets:
					recipes.append(MakeRecipe.from_makefile(lines, query))
					found_target = True

				# Check for case-insensitive variable match
				query_upper: str = query.upper()
				for var_name, var_line_idx in all_variables.items():
					if var_name.upper() == query_upper:
						variables.append(
							MakeVariable.from_makefile(
								lines=lines,
								var_name=var_name,
								var_line_idx=var_line_idx,
							)
						)
						found_variable = True
						break

				if not found_target and not found_variable:
					# Find similar targets and variables (fuzzy matching)
					all_names: List[str] = all_targets + list(all_variables.keys())
					fuzzy_matches: List[str] = difflib.get_close_matches(
						query,
						all_names,
						n=5,
						cutoff=0.5,
					)
					# Also find names that contain the query
					substring_matches: List[str] = [
						n
						for n in all_names
						if query.lower() in n.lower() and n not in fuzzy_matches
					]
					matches: List[str] = (fuzzy_matches + substring_matches)[:5]

					print(
						f"Error: '{c.RED}{query}{c.RESET}' not found as target or variable",
						file=sys.stderr,
					)
					if matches:
						suggestions: str = ", ".join(
							f"{c.BLUE}{m}{c.RESET}" for m in matches
						)
						print(f"Did you mean: {suggestions}?", file=sys.stderr)
					sys.exit(1)

	if not recipes and not variables:
		parser.error("Provide target/variable names or use --all flag")

	# Print descriptions
	use_color: bool = not args.no_color
	output_lines: List[str] = []

	# Targets first
	for recipe in recipes:
		output_lines.extend(recipe.describe(color=use_color))

	# Separator if we have both
	if recipes and variables:
		output_lines.append("-" * 40)

	# Variables
	for var in variables:
		output_lines.extend(var.describe(color=use_color))

	print("\n".join(output_lines).replace("\n\n", f"\n{'-' * 40}\n"))


if __name__ == "__main__":
	main()
