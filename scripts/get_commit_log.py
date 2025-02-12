import subprocess
import sys
from typing import List


def main(
	last_version: str,
	commit_log_file: str,
):
	if last_version == "NULL":
		print("!!! ERROR !!!", file=sys.stderr)
		print("LAST_VERSION is NULL, can't get commit log!", file=sys.stderr)
		sys.exit(1)

	try:
		log_cmd: List[str] = [
			"git",
			"log",
			f"{last_version}..HEAD",
			"--pretty=format:- %s (%h)",
		]
		commits: List[str] = (
			subprocess.check_output(log_cmd).decode("utf-8").strip().split("\n")
		)
		with open(commit_log_file, "w") as f:
			f.write("\n".join(reversed(commits)))
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}", file=sys.stderr)
		sys.exit(1)


if __name__ == "__main__":
	main(
		last_version=sys.argv[1].strip(),
		commit_log_file=sys.argv[2].strip(),
	)
