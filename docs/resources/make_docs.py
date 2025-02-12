"""
python project makefile template -- docs generation script
originally by Michael Ivanitskiy (mivanits@umich.edu)
https://github.com/mivanit/python-project-makefile-template
license: https://creativecommons.org/licenses/by-sa/4.0/
modifications from the original should be denoted with `~~~~~`
as this makes it easier to find edits when updating
"""

import argparse
from functools import reduce
import inspect
import re
import tomllib
from typing import Any, Dict, List, Optional, Union
import warnings
from pathlib import Path

import pdoc  # type: ignore[import-not-found]
import pdoc.doc  # type: ignore[import-not-found]
import pdoc.extract  # type: ignore[import-not-found]
import pdoc.render  # type: ignore[import-not-found]
import pdoc.render_helpers  # type: ignore[import-not-found]
from markupsafe import Markup

# ====================================================================================================
# CONFIGURATION
PACKAGE_NAME: str
PACKAGE_REPO_URL: str
PACKAGE_CODE_URL: str
PACKAGE_VERSION: str
# ====================================================================================================

TOOL_PATH: str = "tool.makefile.make-docs"

def deep_get(
		d: dict,
		path: str,
		default: Any = None,
		sep: str = ".",
		warn_msg_on_default: Optional[str] = None,
	) -> Any:

	output: Any = reduce(
		function=lambda x, y: x.get(y, default) if isinstance(x, dict) else default, 
		sequence=path.split(sep) if isinstance(path, str) else path,
		initial=d,
	)

	if warn_msg_on_default and output == default:
		warnings.warn(warn_msg_on_default.format(path=path))

	return output


pdoc.render_helpers.markdown_extensions["alerts"] = True
pdoc.render_helpers.markdown_extensions["admonitions"] = True


def get_package_meta_global(config_path: Union[str, Path] = Path("pyproject.toml")):
	"""set global vars from pyproject.toml

	sets the global vars:

	- `PACKAGE_NAME`
	- `PACKAGE_REPO_URL`
	- `PACKAGE_CODE_URL`
	- `PACKAGE_VERSION`
	"""
	global PACKAGE_NAME, PACKAGE_REPO_URL, PACKAGE_CODE_URL, PACKAGE_VERSION
	config_path = Path(config_path)
	with config_path.open("rb") as f:
		pyproject_data = tomllib.load(f)
	PACKAGE_VERSION = deep_get(pyproject_data, "project.version", "unknown", warn_msg_on_default="could not find {path}")
	PACKAGE_NAME = deep_get(pyproject_data, "project.name", "unknown", warn_msg_on_default="could not find {path}")
	PACKAGE_REPO_URL = deep_get(pyproject_data, "project.urls.Repository", "unknown", warn_msg_on_default="could not find {path}")
	PACKAGE_CODE_URL = f"{PACKAGE_REPO_URL}/blob/{PACKAGE_VERSION}/"


def add_package_meta_pdoc_globals(
	config_path: Union[str, Path] = Path("pyproject.toml"),
):
	"adds the package meta to the pdoc globals"
	get_package_meta_global(config_path)
	pdoc.render.env.globals["package_version"] = PACKAGE_VERSION
	pdoc.render.env.globals["package_name"] = PACKAGE_NAME
	pdoc.render.env.globals["package_repo_url"] = PACKAGE_REPO_URL
	pdoc.render.env.globals["package_code_url"] = PACKAGE_CODE_URL


def increment_markdown_headings(markdown_text: str, increment: int = 2) -> str:
	"""
	Increment all Markdown headings in the given text by the specified amount.

	Args:
	    markdown_text (str): The input Markdown text.
	    increment (int): The number of levels to increment the headings by. Default is 2.

	Returns:
	    str: The Markdown text with incremented heading levels.
	"""

	def replace_heading(match):
		current_level = len(match.group(1))
		new_level = min(current_level + increment, 6)  # Cap at h6
		return "#" * new_level + match.group(2)

	# Regular expression to match Markdown headings
	heading_pattern = re.compile(r"^(#{1,6})(.+)$", re.MULTILINE)

	# Replace all headings with incremented versions
	return heading_pattern.sub(replace_heading, markdown_text)


OUTPUT_DIR: Path = Path("docs")


def format_signature(sig: inspect.Signature, colon: bool) -> str:
	"""Format a function signature for Markdown. Returns a single-line Markdown string."""
	# First get a list with all params as strings.
	result = pdoc.doc._PrettySignature._params(sig)  # type: ignore
	return_annot = pdoc.doc._PrettySignature._return_annotation_str(sig)  # type: ignore

	def _format_param(param: str) -> str:
		"""Format a parameter for Markdown, including potential links."""
		# This is a simplified version. You might need to adjust this
		# to properly handle links in your specific use case.
		return f"`{param}`"

	# Format each parameter
	pretty_result = [_format_param(param) for param in result]

	# Join parameters
	params_str = ", ".join(pretty_result)

	# Add return annotation
	anno = ")"
	if return_annot:
		anno += f" -> `{return_annot}`"
	if colon:
		anno += ":"

	# Construct the full signature
	rendered = f"`(`{params_str}`{anno}`"

	return rendered


HTML_TO_MD_MAP: Dict[str, str] = {
	"&gt;": ">",
	"&lt;": "<",
	"&amp;": "&",
	"&quot;": '"',
	"&#39": "'",
	"&apos;": "'",
}


def markup_safe(sig: inspect.Signature) -> str:
	"mark some text as safe, no escaping needed"
	output: str = str(sig)
	return Markup(output)


def use_markdown_format():
	"set some functions to output markdown format"
	pdoc.render_helpers.format_signature = format_signature
	pdoc.render.env.filters["markup_safe"] = markup_safe
	pdoc.render.env.filters["increment_markdown_headings"] = increment_markdown_headings


def pdoc_combined(*modules, output_file: Path) -> None:
	"""Render the documentation for a list of modules into a single HTML file.

	Args:
	    *modules: Paths or names of the modules to document.
	    output_file: Path to the output HTML file.

	This function will:
	1. Extract all modules and submodules.
	2. Generate documentation for each module.
	3. Combine all module documentation into a single HTML file.
	4. Write the combined documentation to the specified output file.

	Rendering options can be configured by calling `pdoc.render.configure` in advance.
	"""
	# Extract all modules and submodules
	all_modules: Dict[str, pdoc.doc.Module] = {}
	for module_name in pdoc.extract.walk_specs(modules):
		all_modules[module_name] = pdoc.doc.Module.from_name(module_name)

	# Generate HTML content for each module
	module_contents: List[str] = []
	for module in all_modules.values():
		module_html = pdoc.render.html_module(module, all_modules)
		module_contents.append(module_html)

	# Combine all module contents
	combined_content = "\n".join(module_contents)

	# Write the combined content to the output file
	with output_file.open("w", encoding="utf-8") as f:
		f.write(combined_content)


def ignore_warnings(config_path: Union[str, Path] = Path("pyproject.toml")):
	# Read the pyproject.toml file
	config_path = Path(config_path)
	with config_path.open("rb") as f:
		pyproject_data = tomllib.load(f)

	# Extract the warning messages from the tool.pdoc.ignore section
	warning_messages: List[str] = deep_get(pyproject_data, f"{TOOL_PATH}.warnings_ignore", [])

	# Process and apply the warning filters
	for message in warning_messages:
		warnings.filterwarnings("ignore", message=message)


if __name__ == "__main__":
	# parse args
	# --------------------------------------------------
	argparser: argparse.ArgumentParser = argparse.ArgumentParser()
	argparser.add_argument(
		"--serve",
		"-s",
		action="store_true",
		help="Whether to start an HTTP server to serve the documentation",
	)
	argparser.add_argument(
		"--warn-all",
		"-w",
		action="store_true",
		help="Whether to show all warnings, instead of ignoring the ones specified in pyproject.toml:tool.pdoc.ignore",
	)
	argparser.add_argument(
		"--combined",
		"-c",
		action="store_true",
		help="Whether to combine the documentation for multiple modules into a single markdown file",
	)
	parsed_args = argparser.parse_args()

	# configure pdoc
	# --------------------------------------------------
	add_package_meta_pdoc_globals()

	if not parsed_args.warn_all:
		ignore_warnings()

	pdoc.render.configure(
		edit_url_map={
			PACKAGE_NAME: PACKAGE_CODE_URL,
		},
		template_directory=(
			Path("docs/resources/templates/html/")
			if not parsed_args.combined
			else Path("docs/resources/templates/markdown/")
		),
		show_source=True,
		math=True,
		mermaid=True,
		search=True,
	)

	# do the rendering
	# --------------------------------------------------
	if not parsed_args.combined:
		pdoc.pdoc(
			PACKAGE_NAME,
			output_directory=OUTPUT_DIR,
		)
	else:
		use_markdown_format()
		pdoc_combined(
			PACKAGE_NAME, output_file=OUTPUT_DIR / "combined" / f"{PACKAGE_NAME}.md"
		)

	# http server if needed
	# --------------------------------------------------
	if parsed_args.serve:
		import http.server
		import os
		import socketserver

		port: int = 8000
		os.chdir(OUTPUT_DIR)
		with socketserver.TCPServer(
			("", port), http.server.SimpleHTTPRequestHandler
		) as httpd:
			print(f"Serving at http://localhost:{port}")
			httpd.serve_forever()
