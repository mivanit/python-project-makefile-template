"usage: mypy ... | mypy_report.py [--mode jsonl|exclude]"

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_mypy_output(lines: List[str]) -> Dict[str, int]:
	"given mypy output, turn it into a dict of `filename: error_count`"
	pattern: re.Pattern[str] = re.compile(r"^(?P<file>[^:]+):\d+:\s+error:")
	counts: Dict[str, int] = {}
	for line in lines:
		m = pattern.match(line)
		if m:
			f_raw: str = m.group("file")
			f_norm: str = Path(f_raw).as_posix()
			counts[f_norm] = counts.get(f_norm, 0) + 1
	return counts


def main() -> None:
	"cli interface for mypy_report"
	parser: argparse.ArgumentParser = argparse.ArgumentParser()
	parser.add_argument("--mode", choices=["jsonl", "toml"], default="jsonl")
	args: argparse.Namespace = parser.parse_args()
	lines: List[str] = sys.stdin.read().splitlines()
	error_dict: Dict[str, int] = parse_mypy_output(lines)
	sorted_errors: List[Tuple[str, int]] = sorted(
		error_dict.items(),
		key=lambda x: x[1],
	)
	if len(sorted_errors) == 0:
		print("# no errors found!")
		return
	if args.mode == "jsonl":
		for fname, count in sorted_errors:
			print(json.dumps({"filename": fname, "errors": count}))
	elif args.mode == "toml":
		for fname, count in sorted_errors:
			print(f'"{fname}", # {count}')
	else:
		msg: str = f"unknown mode {args.mode}"
		raise ValueError(msg)
	print(f"# total errors: {sum(error_dict.values())}")


if __name__ == "__main__":
	main()
