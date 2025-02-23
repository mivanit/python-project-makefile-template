"usage: mypy ... | mypy_report.py [--mode jsonl|exclude]"

import sys
import argparse
import re
import json


def parse_mypy_output(lines: list[str]) -> dict[str, int]:
	"given mypy output, turn it into a dict of `filename: error_count`"
	pattern: re.Pattern[str] = re.compile(r"^(?P<file>[^:]+):\d+:\s+error:")
	counts: dict[str, int] = {}
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
	lines: list[str] = sys.stdin.read().splitlines()
	error_dict: dict[str, int] = parse_mypy_output(lines)
	sorted_errors: list[tuple[str, int]] = sorted(
		error_dict.items(), key=lambda x: x[1]
	)
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
