from __future__ import annotations

import functools
import urllib.parse
import argparse
import fnmatch
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Union
import warnings
from jinja2 import Template

try:
	import tomllib  # Python 3.11+
except ImportError:
	import tomli as tomllib


TEMPLATE_MD: str = """\
# Inline TODOs

{% for tag, file_map in grouped|dictsort %}
# {{ tag }}
{% for filepath, item_list in file_map|dictsort %}
## [`{{ filepath }}`](/{{ filepath }})
{% for itm in item_list %}
- [ ] {{ itm.content }}  
[`/{{ filepath }}#{{ itm.line_num }}`](/{{ filepath }}#{{ itm.line_num }}) | [Make Issue]({{ itm.issue_url }})
{% if itm.context %}
```text
{{ itm.context.strip() }}
```
{% endif %}
{% endfor %}

{% endfor %}
{% endfor %}
"""

TEMPLATE_ISSUE: str = """\
# source

[`{file}#L{line_num}`]({repo_url}/blob/{branch}/{file}#L{line_num})

# context
```python
{context}
```
"""

@dataclass
class Config:
	"""Configuration for the inline-todo scraper"""

	search_dir: Path = Path(".")
	out_file: Path = Path("docs/todo-inline.md")
	tags: List[str] = field(
		default_factory=lambda: ["CRIT", "TODO", "FIXME", "HACK", "BUG"]
	)
	extensions: List[str] = field(default_factory=lambda: ["py", "md"])
	exclude: List[str] = field(default_factory=lambda: ["docs/**", ".venv/**"])
	context_lines: int = 2
	tag_label_map: dict[str, str] = field(
		default_factory=lambda: {
			"CRIT": "bug",
			"TODO": "enhancement",
			"FIXME": "bug",
			"BUG": "bug",
			"HACK": "enhancement",
		}
	)

	template_md: str = TEMPLATE_MD
	# template for the output markdown file

	template_issue: str = TEMPLATE_ISSUE
	# template for the issue creation
	
	repo_url: str = "UNKNOWN"
	# for the issue creation url

	branch: str = "main"
	# branch for links to files on github


	@classmethod
	def read(cls, config_file: Path) -> Config:
		output: Config
		if config_file.is_file():
			# read file and load if present
			with config_file.open("rb") as f:
				data: Dict[str, Any] = tomllib.load(f)

			# try to get the repo url
			repo_url: str = "UNKNOWN"
			try:
				urls: Dict[str, str] = {
					k.lower(): v for k, v in data["project"]["urls"].items()
				}
				if "repository" in urls:
					repo_url = urls["repository"]
				if "github" in urls:
					repo_url = urls["github"]
			except Exception as e:
				warnings.warn(
					f"No repository URL found in pyproject.toml, 'make issue' links will not work.\n{e}"
				)

			# load the inline-todo config if present
			data_inline_todo: Dict[str, Any] = data.get("tool", {}).get(
				"inline-todo", {}
			)

			if "repo_url" not in data_inline_todo:
				data_inline_todo["repo_url"] = repo_url

			output = cls.load(data_inline_todo)
		else:
			# return default otherwise
			output = cls()

		return output

	@classmethod
	def load(cls, data: dict) -> Config:
		data = {
			k: Path(v) if k in {"search_dir", "out_file"} else v
			for k, v in data.items()
		}
		
		return cls(**data)


CFG: Config = Config()
# this is messy, but we use a global config so we can get `TodoItem().issue_url` to work

@dataclass
class TodoItem:
	"""Holds one todo occurrence"""

	tag: str
	file: str
	line_num: int
	content: str
	context: str = ""

	def serialize(self) -> Dict[str, Union[str, int]]:
		return asdict(self)


	@property
	def issue_url(self) -> str:
		"""Constructs a GitHub issue creation URL for a given TodoItem."""
		title: str = self.content.split(self.tag, 1)[-1].lstrip(":").strip()
		if not title:
			title = "Issue from inline todo"
		body: str = CFG.template_issue.format(
			file=self.file,
			line_num=self.line_num,
			context=self.context,
			repo_url=CFG.repo_url,
			branch=CFG.branch,
		).strip()
		label: str = CFG.tag_label_map.get(self.tag, self.tag)
		query: Dict[str, str] = dict(title=title, body=body, labels=label)
		query_string: str = urllib.parse.urlencode(query)
		return f"{CFG.repo_url}/issues/new?{query_string}"


def scrape_file(
	file_path: Path,
	tags: List[str],
	context_lines: int,
) -> List[TodoItem]:
	"""Scrapes a file for lines containing any of the specified tags"""
	items: List[TodoItem] = []
	if not file_path.is_file():
		return items
	lines: List[str] = file_path.read_text(encoding="utf-8").splitlines(True)

	for i, line in enumerate(lines):
		for tag in tags:
			if tag in line[:200]:
				start: int = max(0, i - context_lines)
				end: int = min(len(lines), i + context_lines + 1)
				snippet: str = "".join(lines[start:end])
				items.append(
					TodoItem(
						tag=tag,
						file=file_path.as_posix(),
						line_num=i + 1,
						content=line.strip("\n"),
						context=snippet,
					)
				)
				break
	return items


def collect_files(
	search_dir: Path,
	extensions: List[str],
	exclude: List[str],
) -> List[Path]:
	"""Recursively collects all files with specified extensions, excluding matches via globs"""
	results: List[Path] = []
	for ext in extensions:
		results.extend(search_dir.rglob(f"*.{ext}"))

	filtered: List[Path] = []
	for f in results:
		# Skip if it matches any exclude glob
		if not any(fnmatch.fnmatch(f.as_posix(), pattern) for pattern in exclude):
			filtered.append(f)
	return filtered


def group_items_by_tag_and_file(
	items: List[TodoItem],
) -> Dict[str, Dict[str, List[TodoItem]]]:
	"""Groups items by tag, then by file"""
	grouped: Dict[str, Dict[str, List[TodoItem]]] = {}
	for itm in items:
		grouped.setdefault(itm.tag, {}).setdefault(itm.file, []).append(itm)
	for tag_dict in grouped.values():
		for file_list in tag_dict.values():
			file_list.sort(key=lambda x: x.line_num)
	return grouped


def main(config_file: Path) -> None:
	global CFG
	# read configuration
	cfg: Config = Config.read(config_file)
	CFG = cfg

	# get data
	files: List[Path] = collect_files(cfg.search_dir, cfg.extensions, cfg.exclude)
	all_items: List[TodoItem] = []
	n_files: int = len(files)
	for i, fpath in enumerate(files):
		print(f"Scraping {i + 1:>2}/{n_files:>2}: {fpath.as_posix():<60}", end="\r")
		all_items.extend(scrape_file(fpath, cfg.tags, cfg.context_lines))
	# write raw to jsonl
	with open(cfg.out_file.with_suffix(".jsonl"), "w", encoding="utf-8") as f:
		for itm in all_items:
			f.write(json.dumps(itm.serialize()) + "\n")

	# group, render, and write md output
	grouped: Dict[str, Dict[str, List[TodoItem]]] = group_items_by_tag_and_file(
		all_items
	)

	rendered: str = Template(cfg.template_md).render(grouped=grouped)
	cfg.out_file.with_suffix(".md").write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
	# parse args
	parser: argparse.ArgumentParser = argparse.ArgumentParser("inline_todo")
	parser.add_argument(
		"--config-file",
		default="pyproject.toml",
		help="Path to the TOML config, will look under [tool.inline-todo].",
	)
	args: argparse.Namespace = parser.parse_args()
	# call main
	main(Path(args.config_file))
