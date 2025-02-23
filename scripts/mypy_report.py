"usage: mypy ... | mypy_report.py [--mode jsonl|exclude]"

from __future__ import annotations
import sys
import argparse
import re
import json
from typing import List, Dict, Tuple


def parse_mypy_output(lines: List[str]) -> Dict[str, int]:
	"given mypy output, turn it into a dict of `filename: error_count`"
	pattern: re.Pattern[str] = re.compile(r"^(?P<file>[^:]+):\d+:\s+error:")
	counts: Dict[str, int] = {}
	for line in lines:
		m = pattern.match(line)
		if m:
			f: str = m.group("file")
			counts[f] = counts.get(f, 0) + 1
	return counts


def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument("--mode", choices=["jsonl", "toml"], default="jsonl")
	args = parser.parse_args()
	lines: List[str] = sys.stdin.read().splitlines()
	error_dict: Dict[str, int] = parse_mypy_output(lines)
	sorted_errors: List[Tuple[str, int]] = sorted(
		error_dict.items(), key=lambda x: x[1]
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
		raise ValueError(f"unknown mode {args.mode}")


if __name__ == "__main__":
	main()
