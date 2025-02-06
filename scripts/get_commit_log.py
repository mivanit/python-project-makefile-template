import subprocess
import sys

last_version: str = sys.argv[1].strip()
commit_log_file: str = sys.argv[2].strip()

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
