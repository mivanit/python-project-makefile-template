"""Tests for Makefile target behavior.

Tests run in an isolated tmp directory (copied makefile + minimal structure)
so they never mutate the real project tree.

Tests marked "EXPECTED TO FAIL before fix" verify bugs from the cleanup plan:
- clean removes TYPE_ERRORS_DIR (shouldn't)
- docs-clean doesn't remove TYPE_ERRORS_DIR (should)
- .mypy_cache only removed at root, not recursively
- $(eval) trailing whitespace in gen-version-info
- TAB character in CI YAML
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

try:
	import tomllib
except ModuleNotFoundError:
	import tomli as tomllib  # type: ignore[no-redef]

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_pyproject_version(env: Path) -> str:
	"""Return the bare version string (e.g. ``0.5.2``) from *env*/pyproject.toml."""
	with open(env / "pyproject.toml", "rb") as f:
		data = tomllib.load(f)
	return data["project"]["version"]


def _set_pyproject_version(env: Path, version: str) -> None:
	"""Rewrite the ``version = "..."`` line in *env*/pyproject.toml."""
	pp = env / "pyproject.toml"
	text = pp.read_text()
	pp.write_text(
		re.sub(r'(?m)^(\s*version\s*=\s*")([^"]+)(")', rf"\g<1>{version}\3", text)
	)


# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def make_env(request: pytest.FixtureRequest) -> Path:
	"""Create an isolated make environment in ``tests/.temp/<test_name>``.

	Copies makefile, pyproject.toml, and .meta/scripts/ (for targets that call
	Python helper scripts). Creates the minimal directory skeleton the makefile
	expects (myproject/, tests/, docs/, docs/resources/).
	"""
	env = PROJECT_ROOT / "tests" / ".temp" / request.node.name
	if env.exists():
		shutil.rmtree(env)
	env.mkdir(parents=True)

	shutil.copy(PROJECT_ROOT / "makefile", env / "makefile")
	shutil.copy(PROJECT_ROOT / "pyproject.toml", env / "pyproject.toml")

	meta_scripts = PROJECT_ROOT / ".meta" / "scripts"
	if meta_scripts.is_dir():
		shutil.copytree(meta_scripts, env / ".meta" / "scripts")

	for d in ("myproject", "tests", "docs", "docs/resources"):
		(env / d).mkdir(parents=True, exist_ok=True)

	return env


def run_make(
	env: Path,
	*args: str,
	**make_vars: str,
) -> subprocess.CompletedProcess[str]:
	"""Run ``make`` in *env* with optional variable overrides.

	>>> run_make(env, "clean")
	>>> run_make(env, "--eval=...", "_target", RUN_GLOBAL="1")
	"""
	cmd: list[str] = ["make", "-f", "makefile"]
	cmd.extend(f"{k}={v}" for k, v in make_vars.items())
	cmd.extend(args)
	# Strip Make variables so the inner make runs as a top-level invocation
	# (not a sub-make inheriting MAKELEVEL from `make test`).
	clean_env = {
		k: v
		for k, v in os.environ.items()
		if k not in ("MAKELEVEL", "MAKEFLAGS", "MFLAGS")
	}
	return subprocess.run(
		cmd,
		cwd=env,
		capture_output=True,
		text=True,
		timeout=30,
		env=clean_env,
		check=False,
	)


_has_ruff = shutil.which("ruff") is not None

_GIT_ENV_VARS = {
	"GIT_AUTHOR_NAME": "Test",
	"GIT_AUTHOR_EMAIL": "test@test.com",
	"GIT_COMMITTER_NAME": "Test",
	"GIT_COMMITTER_EMAIL": "test@test.com",
}


@pytest.fixture
def git_env(make_env: Path) -> Path:
	"""Create an isolated make environment with an initialized git repo.

	Extends *make_env* with ``git init``, an initial commit, a ``v0.0.1`` tag,
	and a ``.lastversion`` file pointing at that tag.

	Uses environment variables instead of ``git config`` to avoid mutating state.
	"""
	git_env_vars = {**os.environ, **_GIT_ENV_VARS}
	# Create .lastversion before git init so everything is in the initial commit.
	versions_dir = make_env / ".meta" / "versions"
	versions_dir.mkdir(parents=True, exist_ok=True)
	(versions_dir / ".lastversion").write_text("v0.0.1")
	subprocess.run(
		["git", "init"], cwd=make_env, capture_output=True, check=True, env=git_env_vars
	)
	subprocess.run(
		["git", "add", "."],
		cwd=make_env,
		capture_output=True,
		check=True,
		env=git_env_vars,
	)
	subprocess.run(
		["git", "commit", "-m", "initial"],
		cwd=make_env,
		capture_output=True,
		check=True,
		env=git_env_vars,
	)
	subprocess.run(
		["git", "tag", "v0.0.1"],
		cwd=make_env,
		capture_output=True,
		check=True,
		env=git_env_vars,
	)
	return make_env


# ---------------------------------------------------------------------------
# make clean
# ---------------------------------------------------------------------------


class TestClean:
	"""Verify ``make clean`` removes (or preserves) the right things."""

	# -- targets that should be removed (all PASS today) --------------------

	def test_removes_ruff_cache(self, make_env: Path) -> None:
		d = make_env / ".ruff_cache"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_pytest_cache(self, make_env: Path) -> None:
		d = make_env / ".pytest_cache"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_root_mypy_cache(self, make_env: Path) -> None:
		d = make_env / ".mypy_cache"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_dist(self, make_env: Path) -> None:
		d = make_env / "dist"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_build(self, make_env: Path) -> None:
		d = make_env / "build"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_egg_info(self, make_env: Path) -> None:
		d = make_env / "myproject.egg-info"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_coverage(self, make_env: Path) -> None:
		f = make_env / ".coverage"
		f.touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not f.exists()

	def test_removes_tests_temp(self, make_env: Path) -> None:
		d = make_env / "tests" / "_temp"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_pycache_recursively(self, make_env: Path) -> None:
		"""__pycache__ in package, tests, docs, and nested subdirs."""
		dirs = [
			make_env / "myproject" / "__pycache__",
			make_env / "myproject" / "sub" / "__pycache__",
			make_env / "tests" / "__pycache__",
			make_env / "docs" / "__pycache__",
		]
		for d in dirs:
			d.mkdir(parents=True, exist_ok=True)
			(d / "mod.cpython-313.pyc").touch()

		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		for d in dirs:
			assert not d.exists(), (
				f"__pycache__ at {d.relative_to(make_env)} still exists"
			)

	def test_removes_pyc_files(self, make_env: Path) -> None:
		pyc = make_env / "myproject" / "mod.pyc"
		pyo = make_env / "tests" / "test_x.pyo"
		pyc.touch()
		pyo.touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not pyc.exists(), ".pyc file should be removed"
		assert not pyo.exists(), ".pyo file should be removed"

	def test_removes_root_pycache(self, make_env: Path) -> None:
		"""__pycache__ at project root should be removed (exercises find from .)."""
		d = make_env / "__pycache__"
		d.mkdir()
		(d / "mod.cpython-313.pyc").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists(), "__pycache__ at project root should be removed"

	# -- clean should NOT remove these -------------------------------------

	def test_preserves_venv(self, make_env: Path) -> None:
		"""make clean should NOT remove .venv (only dep-clean does)."""
		d = make_env / ".venv"
		d.mkdir()
		(d / "pyvenv.cfg").touch()
		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert d.exists(), ".venv should NOT be removed by make clean"

	# -- BUG: clean should NOT remove TYPE_ERRORS_DIR -----------------------

	def test_does_not_remove_type_errors_dir(self, make_env: Path) -> None:
		"""EXPECTED TO FAIL before fix — clean currently rm-rf's $(TYPE_ERRORS_DIR)."""
		d = make_env / ".meta" / ".type-errors"
		d.mkdir(parents=True, exist_ok=True)
		sentinel = d / "ty.txt"
		sentinel.touch()

		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert d.exists(), ".meta/.type-errors should NOT be removed by make clean"
		assert sentinel.exists(), "files inside .meta/.type-errors should be preserved"

	# -- BUG: clean should remove nested .mypy_cache dirs -------------------

	def test_removes_mypy_cache_recursively(self, make_env: Path) -> None:
		"""EXPECTED TO FAIL before fix — clean only removes root .mypy_cache."""
		nested = make_env / "myproject" / ".mypy_cache"
		nested.mkdir(parents=True, exist_ok=True)
		(nested / "sentinel").touch()

		result = run_make(make_env, "clean")
		assert result.returncode == 0, result.stderr
		assert not nested.exists(), ".mypy_cache inside myproject/ should be removed"


# ---------------------------------------------------------------------------
# make docs-clean
# ---------------------------------------------------------------------------


class TestDocsClean:
	"""Verify ``make docs-clean`` behaviour."""

	def test_removes_type_errors_dir(self, make_env: Path) -> None:
		"""EXPECTED TO FAIL before fix — docs-clean doesn't touch TYPE_ERRORS_DIR."""
		d = make_env / ".meta" / ".type-errors"
		d.mkdir(parents=True, exist_ok=True)
		(d / "basedpyright.txt").touch()

		result = run_make(make_env, "docs-clean", RUN_GLOBAL="1")
		assert result.returncode == 0, f"make docs-clean failed: {result.stderr}"
		assert not d.exists(), ".meta/.type-errors should be removed by make docs-clean"

	def test_preserves_resources_dir(self, make_env: Path) -> None:
		sentinel = make_env / "docs" / "resources" / "keep.txt"
		sentinel.write_text("preserve me")
		result = run_make(make_env, "docs-clean", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert sentinel.exists(), "docs/resources/ should be preserved by docs-clean"

	def test_removes_generated_html(self, make_env: Path) -> None:
		generated = make_env / "docs" / "myproject.html"
		generated.write_text("<html></html>")
		result = run_make(make_env, "docs-clean", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not generated.exists(), "generated html should be removed"

	def test_preserves_nojekyll(self, make_env: Path) -> None:
		nojekyll = make_env / "docs" / ".nojekyll"
		nojekyll.touch()
		result = run_make(make_env, "docs-clean", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert nojekyll.exists(), ".nojekyll should be preserved (in no_clean config)"

	def test_removes_generated_subdirectory(self, make_env: Path) -> None:
		gen_dir = make_env / "docs" / "coverage"
		gen_dir.mkdir(parents=True, exist_ok=True)
		(gen_dir / "index.html").write_text("<html></html>")
		result = run_make(make_env, "docs-clean", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not gen_dir.exists(), "generated subdirectory should be removed"


# ---------------------------------------------------------------------------
# make dep-clean
# ---------------------------------------------------------------------------


class TestDepClean:
	"""Verify ``make dep-clean`` removes dependency artifacts."""

	def test_removes_venv(self, make_env: Path) -> None:
		d = make_env / ".venv"
		d.mkdir()
		(d / "pyvenv.cfg").touch()
		result = run_make(make_env, "dep-clean")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_uv_lock(self, make_env: Path) -> None:
		f = make_env / "uv.lock"
		f.write_text("lock content")
		result = run_make(make_env, "dep-clean")
		assert result.returncode == 0, result.stderr
		assert not f.exists()

	def test_removes_requirements_txt_files(self, make_env: Path) -> None:
		req_dir = make_env / ".meta" / "requirements"
		req_dir.mkdir(parents=True, exist_ok=True)
		(req_dir / "requirements-base.txt").write_text("numpy")
		(req_dir / "requirements-dev.txt").write_text("pytest")
		result = run_make(make_env, "dep-clean")
		assert result.returncode == 0, result.stderr
		assert not list(req_dir.glob("*.txt")), ".txt files should be removed"

	def test_succeeds_when_nothing_to_clean(self, make_env: Path) -> None:
		result = run_make(make_env, "dep-clean")
		assert result.returncode == 0, result.stderr

	def test_preserves_non_txt_in_requirements_dir(self, make_env: Path) -> None:
		req_dir = make_env / ".meta" / "requirements"
		req_dir.mkdir(parents=True, exist_ok=True)
		keep = req_dir / "README.md"
		keep.write_text("keep me")
		(req_dir / "requirements.txt").write_text("to remove")
		result = run_make(make_env, "dep-clean")
		assert result.returncode == 0, result.stderr
		assert keep.exists(), "non-.txt files should be preserved"


# ---------------------------------------------------------------------------
# make clean-all
# ---------------------------------------------------------------------------


class TestCleanAll:
	"""Verify ``make clean-all`` runs clean + docs-clean + dep-clean."""

	def test_removes_clean_targets(self, make_env: Path) -> None:
		d = make_env / ".ruff_cache"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean-all", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not d.exists()

	def test_removes_dep_clean_targets(self, make_env: Path) -> None:
		venv = make_env / ".venv"
		venv.mkdir()
		(venv / "pyvenv.cfg").touch()
		lock = make_env / "uv.lock"
		lock.write_text("lock")
		result = run_make(make_env, "clean-all", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not venv.exists()
		assert not lock.exists()

	def test_removes_docs_clean_targets(self, make_env: Path) -> None:
		gen = make_env / "docs" / "myproject.html"
		gen.write_text("<html></html>")
		result = run_make(make_env, "clean-all", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not gen.exists()

	def test_removes_type_errors_dir(self, make_env: Path) -> None:
		"""clean-all should remove TYPE_ERRORS_DIR transitively via docs-clean."""
		d = make_env / ".meta" / ".type-errors"
		d.mkdir(parents=True, exist_ok=True)
		(d / "ty.txt").touch()
		result = run_make(make_env, "clean-all", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert not d.exists(), ".meta/.type-errors should be removed by clean-all"

	def test_succeeds_on_empty_env(self, make_env: Path) -> None:
		result = run_make(make_env, "clean-all", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr


# ---------------------------------------------------------------------------
# write-proj-version / gen-version-info / version / publish
# ---------------------------------------------------------------------------


class TestWriteProjVersion:
	"""Verify ``make write-proj-version`` extracts version from pyproject.toml."""

	def test_creates_version_file(self, make_env: Path) -> None:
		result = run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		version_file = make_env / ".meta" / "versions" / ".version"
		assert version_file.exists()

	def test_version_matches_pyproject(self, make_env: Path) -> None:
		run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		version_file = make_env / ".meta" / "versions" / ".version"
		content = version_file.read_text()
		expected = "v" + _read_pyproject_version(make_env)
		assert content == expected

	def test_version_file_has_no_trailing_newline(self, make_env: Path) -> None:
		run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		version_file = make_env / ".meta" / "versions" / ".version"
		content = version_file.read_text()
		assert not content.endswith("\n")

	def test_creates_versions_directory(self, make_env: Path) -> None:
		versions_dir = make_env / ".meta" / "versions"
		if versions_dir.exists():
			shutil.rmtree(versions_dir)
		result = run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert versions_dir.exists()

	def test_null_on_missing_version_key(self, make_env: Path) -> None:
		"""write-proj-version produces NULL when pyproject.toml has no version key."""
		pp = make_env / "pyproject.toml"
		text = pp.read_text()
		pp.write_text(re.sub(r'(?m)^\s*version\s*=\s*"[^"]*"\s*\n?', "", text))
		result = run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		assert result.returncode != 0
		version_file = make_env / ".meta" / "versions" / ".version"
		assert version_file.exists()
		assert version_file.read_text() == "NULL"

	def test_null_on_malformed_toml(self, make_env: Path) -> None:
		"""write-proj-version produces NULL when pyproject.toml is garbage."""
		(make_env / "pyproject.toml").write_text("this is not valid toml {{{}}}")
		result = run_make(make_env, "write-proj-version", RUN_GLOBAL="1")
		assert result.returncode != 0
		version_file = make_env / ".meta" / "versions" / ".version"
		assert version_file.exists()
		assert version_file.read_text() == "NULL"


class TestGenVersionInfo:
	"""Verify ``make gen-version-info`` correctly evaluates version variables."""

	@pytest.fixture
	def version_env(self, make_env: Path) -> Path:
		versions_dir = make_env / ".meta" / "versions"
		versions_dir.mkdir(parents=True, exist_ok=True)
		(versions_dir / ".version").write_text("v1.2.3")
		local_dir = make_env / ".meta" / "local"
		local_dir.mkdir(parents=True, exist_ok=True)
		return make_env

	def _eval_var(self, env: Path, var_name: str) -> str:
		"""Run gen-version-info and return the value of *var_name*."""
		eval_noop = "write-proj-version: ;"
		eval_print = f'_test-var: gen-version-info\n\t@printf "%s" "$({var_name})"'
		result = run_make(
			env,
			f"--eval={eval_noop}",
			f"--eval={eval_print}",
			"_test-var",
			RUN_GLOBAL="1",
		)
		assert result.returncode == 0, f"make failed: {result.stderr}"
		return result.stdout

	def test_proj_version_reads_from_version_file(self, version_env: Path) -> None:
		version = self._eval_var(version_env, "PROJ_VERSION")
		# NOTE: --eval="write-proj-version: ;" is processed before the makefile,
		# so the makefile's recipe wins and overwrites our pre-created file.
		# We verify against the real pyproject.toml version instead.
		expected = "v" + _read_pyproject_version(version_env)
		assert version.strip() == expected

	def test_last_version_reads_from_lastversion_file(self, version_env: Path) -> None:
		(version_env / ".meta" / "versions" / ".lastversion").write_text("v1.0.0")
		version = self._eval_var(version_env, "LAST_VERSION")
		assert version.strip() == "v1.0.0"

	def test_last_version_null_when_no_file(self, version_env: Path) -> None:
		lastver = version_env / ".meta" / "versions" / ".lastversion"
		if lastver.exists():
			lastver.unlink()
		version = self._eval_var(version_env, "LAST_VERSION")
		assert version.strip() == "NULL"

	def test_python_version_is_valid(self, version_env: Path) -> None:
		version = self._eval_var(version_env, "PYTHON_VERSION")
		assert re.match(r"\d+\.\d+\.\d+", version.strip()), (
			f"PYTHON_VERSION doesn't look like X.Y.Z: {version!r}"
		)

	def test_last_version_no_trailing_whitespace(self, version_env: Path) -> None:
		(version_env / ".meta" / "versions" / ".lastversion").write_text("v1.0.0")
		version = self._eval_var(version_env, "LAST_VERSION")
		assert version == version.strip(), (
			f"LAST_VERSION has trailing whitespace: [{version!r}]"
		)

	def test_python_version_no_trailing_whitespace(self, version_env: Path) -> None:
		version = self._eval_var(version_env, "PYTHON_VERSION")
		assert version == version.strip(), (
			f"PYTHON_VERSION has trailing whitespace: [{version!r}]"
		)

	@pytest.mark.parametrize("var", ["PROJ_VERSION", "LAST_VERSION", "PYTHON_VERSION"])
	def test_eval_var_no_trailing_whitespace(self, version_env: Path, var: str) -> None:
		"""Regression: all three $(eval) variables must have no trailing whitespace."""
		# Ensure LAST_VERSION is not NULL so we test the real value.
		(version_env / ".meta" / "versions" / ".lastversion").write_text("v1.0.0")
		value = self._eval_var(version_env, var)
		assert value == value.strip(), f"{var} has whitespace: [{value!r}]"


class TestVersion:
	"""Verify gen-version-info populates PROJ_VERSION without trailing whitespace."""

	@pytest.fixture
	def version_env(self, make_env: Path) -> Path:
		"""Pre-create version files so gen-version-info can run without full setup."""
		versions_dir = make_env / ".meta" / "versions"
		versions_dir.mkdir(parents=True, exist_ok=True)
		(versions_dir / ".version").write_text("v1.2.3")

		local_dir = make_env / ".meta" / "local"
		local_dir.mkdir(parents=True, exist_ok=True)

		return make_env

	def _get_proj_version(self, env: Path) -> str:
		"""Run gen-version-info and return the raw PROJ_VERSION string."""
		# Override write-proj-version to no-op (we pre-created the file).
		# Inject _test-ver target that prints PROJ_VERSION after eval.
		eval_noop = "write-proj-version: ;"
		eval_print = '_test-ver: gen-version-info\n\t@printf "%s" "$(PROJ_VERSION)"'
		result = run_make(
			env,
			f"--eval={eval_noop}",
			f"--eval={eval_print}",
			"_test-ver",
			RUN_GLOBAL="1",
		)
		assert result.returncode == 0, f"make failed: {result.stderr}"
		return result.stdout

	def test_proj_version_no_trailing_whitespace(self, version_env: Path) -> None:
		"""EXPECTED TO FAIL before fix — $(eval ... ) has trailing space."""
		version = self._get_proj_version(version_env)
		assert len(version) > 0, "PROJ_VERSION should not be empty"
		assert version == version.strip(), (
			f"PROJ_VERSION has trailing whitespace: [{version!r}]"
		)

	def test_publish_version_comparison(self, version_env: Path) -> None:
		"""EXPECTED TO FAIL before fix — trailing space makes publish confirmation always reject.

		Simulates the shell comparison from the publish target:
			if [ "$$NEW_VERSION" != "$(PROJ_VERSION)" ]; then exit 1; fi
		where the user types the *clean* version string.
		"""
		proj_version = self._get_proj_version(version_env)

		# The user would type the trimmed version (e.g. "v1.2.3").
		clean_version = proj_version.strip()

		# Reproduce the exact publish comparison in bash.
		comparison = subprocess.run(
			[
				"bash",
				"-c",
				f'[ "{clean_version}" = "{proj_version}" ]',
			],
			capture_output=True,
			text=True,
			check=False,
		)
		assert comparison.returncode == 0, (
			f"Publish version confirmation would fail: "
			f"user types [{clean_version!r}] but PROJ_VERSION is [{proj_version!r}]"
		)


# ---------------------------------------------------------------------------
# make gen-commit-log
# ---------------------------------------------------------------------------


class TestGenCommitLog:
	"""Verify ``make gen-commit-log`` generates commit history."""

	@pytest.fixture
	def commit_log_env(self, git_env: Path) -> Path:
		"""Extend *git_env* with a second commit so there is log output."""
		git_env_vars = {**os.environ, **_GIT_ENV_VARS}
		subprocess.run(
			["git", "branch", "-M", "main"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		(git_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		(git_env / "newfile.py").write_text("# new file")
		subprocess.run(
			["git", "add", "."],
			cwd=git_env,
			capture_output=True,
			check=True,
			env=git_env_vars,
		)
		subprocess.run(
			["git", "commit", "-m", "add newfile"],
			cwd=git_env,
			capture_output=True,
			check=True,
			env=git_env_vars,
		)
		return git_env

	def test_generates_commit_log_file(self, commit_log_env: Path) -> None:
		result = run_make(
			commit_log_env,
			"--eval=write-proj-version: ;",
			"gen-commit-log",
			RUN_GLOBAL="1",
		)
		assert result.returncode == 0, result.stderr
		log_file = commit_log_env / ".meta" / "local" / ".commit_log"
		assert log_file.exists(), "commit log file should be created"

	def test_commit_log_contains_commit_message(self, commit_log_env: Path) -> None:
		run_make(
			commit_log_env,
			"--eval=write-proj-version: ;",
			"gen-commit-log",
			RUN_GLOBAL="1",
		)
		log_file = commit_log_env / ".meta" / "local" / ".commit_log"
		content = log_file.read_text()
		assert "newfile" in content.lower() or "add" in content.lower()

	def test_fails_when_last_version_is_null(self, git_env: Path) -> None:
		lastver = git_env / ".meta" / "versions" / ".lastversion"
		if lastver.exists():
			lastver.unlink()
		(git_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		result = run_make(
			git_env,
			"--eval=write-proj-version: ;",
			"gen-commit-log",
			RUN_GLOBAL="1",
		)
		assert result.returncode != 0
		combined = result.stdout + result.stderr
		assert "NULL" in combined or "ERROR" in combined

	def test_empty_commit_log_when_no_new_commits(self, git_env: Path) -> None:
		"""When tag is at HEAD, commit log should be empty."""
		(git_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		result = run_make(
			git_env,
			"gen-commit-log",
			RUN_GLOBAL="1",
		)
		assert result.returncode == 0, result.stderr
		log_file = git_env / ".meta" / "local" / ".commit_log"
		assert log_file.exists()
		content = log_file.read_text().strip()
		assert content == "", f"Expected empty commit log, got: {content!r}"


# ---------------------------------------------------------------------------
# make version
# ---------------------------------------------------------------------------


class TestVersionTarget:
	"""Verify ``make version`` output and same-version guard."""

	@pytest.fixture
	def version_target_env(self, git_env: Path) -> Path:
		"""Extend *git_env* with a post-tag commit and local dir."""
		git_env_vars = {**os.environ, **_GIT_ENV_VARS}
		subprocess.run(
			["git", "branch", "-M", "main"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		(git_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		(git_env / "extra.py").write_text("# extra")
		subprocess.run(
			["git", "add", "."],
			cwd=git_env,
			capture_output=True,
			check=True,
			env=git_env_vars,
		)
		subprocess.run(
			["git", "commit", "-m", "post-tag work"],
			cwd=git_env,
			capture_output=True,
			check=True,
			env=git_env_vars,
		)
		return git_env

	def test_version_fails_when_versions_match(self, version_target_env: Path) -> None:
		"""``make version`` should exit 1 when PROJ_VERSION == LAST_VERSION."""
		env = version_target_env
		# Patch pyproject.toml so write-proj-version produces v0.0.1
		# (matching the v0.0.1 tag and .lastversion from git_env).
		_set_pyproject_version(env, "0.0.1")
		result = run_make(env, "version", RUN_GLOBAL="1")
		assert result.returncode != 0
		assert "same as last published" in result.stdout.lower()

	def test_version_succeeds_when_versions_differ(
		self, version_target_env: Path
	) -> None:
		"""``make version`` should succeed and print both version strings."""
		env = version_target_env
		# pyproject.toml has 0.5.2 → PROJ_VERSION=v0.5.2, LAST_VERSION=v0.0.1
		result = run_make(env, "version", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert "v0.0.1" in result.stdout
		expected_proj = "v" + _read_pyproject_version(env)
		assert expected_proj in result.stdout


# ---------------------------------------------------------------------------
# make info / make info-long
# ---------------------------------------------------------------------------


class TestInfo:
	"""Verify ``make info`` prints key variables."""

	@pytest.fixture
	def info_env(self, make_env: Path) -> Path:
		versions_dir = make_env / ".meta" / "versions"
		versions_dir.mkdir(parents=True, exist_ok=True)
		(versions_dir / ".version").write_text("v0.0.0")
		(make_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		return make_env

	def test_info_succeeds(self, info_env: Path) -> None:
		result = run_make(info_env, "info", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr

	def test_info_prints_python(self, info_env: Path) -> None:
		result = run_make(info_env, "info", RUN_GLOBAL="1")
		assert "PYTHON" in result.stdout

	def test_info_prints_package_name(self, info_env: Path) -> None:
		result = run_make(info_env, "info", RUN_GLOBAL="1")
		assert "PACKAGE_NAME" in result.stdout
		assert "myproject" in result.stdout

	def test_info_prints_proj_version(self, info_env: Path) -> None:
		result = run_make(info_env, "info", RUN_GLOBAL="1")
		assert "PROJ_VERSION" in result.stdout

	def test_info_prints_pytest_options(self, info_env: Path) -> None:
		result = run_make(info_env, "info", RUN_GLOBAL="1")
		assert "PYTEST_OPTIONS" in result.stdout


class TestInfoLong:
	"""Verify ``make info-long`` prints extended variables."""

	@pytest.fixture
	def info_env(self, make_env: Path) -> Path:
		versions_dir = make_env / ".meta" / "versions"
		versions_dir.mkdir(parents=True, exist_ok=True)
		(versions_dir / ".version").write_text("v0.0.0")
		(make_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		return make_env

	def test_info_long_succeeds(self, info_env: Path) -> None:
		result = run_make(info_env, "info-long", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr

	def test_info_long_prints_publish_branch(self, info_env: Path) -> None:
		result = run_make(info_env, "info-long", RUN_GLOBAL="1")
		assert "PUBLISH_BRANCH" in result.stdout
		assert "main" in result.stdout

	def test_info_long_prints_docs_dir(self, info_env: Path) -> None:
		result = run_make(info_env, "info-long", RUN_GLOBAL="1")
		assert "DOCS_DIR" in result.stdout

	def test_info_long_prints_run_global(self, info_env: Path) -> None:
		result = run_make(info_env, "info-long", RUN_GLOBAL="1")
		assert "RUN_GLOBAL" in result.stdout

	def test_info_long_prints_type_checkers(self, info_env: Path) -> None:
		result = run_make(info_env, "info-long", RUN_GLOBAL="1")
		assert "TYPE_CHECKERS" in result.stdout


# ---------------------------------------------------------------------------
# make help (default target, help-targets, smart help)
# ---------------------------------------------------------------------------


class TestDefault:
	"""Verify ``make`` (default target) shows help."""

	def test_default_runs_successfully(self, make_env: Path) -> None:
		result = run_make(make_env, "default", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr

	def test_default_shows_targets(self, make_env: Path) -> None:
		result = run_make(make_env, "default", RUN_GLOBAL="1")
		assert "make targets" in result.stdout.lower() or "make " in result.stdout


class TestHelp:
	"""Verify ``make help`` and smart help variants."""

	def test_help_no_args_prints_targets(self, make_env: Path) -> None:
		result = run_make(make_env, "help", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		assert "make targets" in result.stdout.lower()

	def test_help_no_args_mentions_usage(self, make_env: Path) -> None:
		result = run_make(make_env, "help", RUN_GLOBAL="1")
		assert "make help=" in result.stdout or "HELP" in result.stdout

	def test_help_with_target(self, make_env: Path) -> None:
		"""``make help=clean`` shows info about the clean target."""
		result = run_make(make_env, help="clean")
		assert result.returncode == 0, result.stderr
		assert "clean" in result.stdout.lower()

	def test_help_with_wildcard(self, make_env: Path) -> None:
		"""``make help=*`` shows all targets."""
		result = run_make(make_env, help="*")
		assert result.returncode == 0, result.stderr
		assert "clean" in result.stdout.lower()
		assert "test" in result.stdout.lower()

	def test_help_case_variations(self, make_env: Path) -> None:
		"""``make H=clean`` works the same as ``make help=clean``."""
		result = run_make(make_env, H="clean")
		assert result.returncode == 0, result.stderr
		assert "clean" in result.stdout.lower()

	def test_help_targets_lists_phony_targets(self, make_env: Path) -> None:
		result = run_make(make_env, "help-targets")
		assert result.returncode == 0, result.stderr
		assert "make clean" in result.stdout
		assert "make test" in result.stdout

	def test_help_variable_lookup(self, make_env: Path) -> None:
		"""``make help=PACKAGE_NAME`` shows variable info."""
		result = run_make(make_env, help="PACKAGE_NAME")
		assert result.returncode == 0, result.stderr
		assert "PACKAGE_NAME" in result.stdout

	def test_help_nonexistent_target(self, make_env: Path) -> None:
		"""``make help=nonexistent`` exits non-zero with 'not found' message."""
		result = run_make(make_env, help="nonexistent")
		assert result.returncode != 0
		assert "not found" in result.stderr.lower()


# ---------------------------------------------------------------------------
# make verify-git
# ---------------------------------------------------------------------------


class TestVerifyGit:
	"""Verify ``make verify-git`` checks branch and clean status."""

	def test_passes_on_main_branch_clean(self, git_env: Path) -> None:
		subprocess.run(
			["git", "branch", "-M", "main"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		result = run_make(git_env, "verify-git")
		assert result.returncode == 0, result.stderr

	def test_fails_on_wrong_branch(self, git_env: Path) -> None:
		subprocess.run(
			["git", "checkout", "-b", "feature-branch"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		result = run_make(git_env, "verify-git")
		assert result.returncode != 0

	def test_fails_on_dirty_working_tree(self, git_env: Path) -> None:
		subprocess.run(
			["git", "branch", "-M", "main"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		(git_env / "untracked_file.txt").write_text("dirty")
		subprocess.run(
			["git", "add", "untracked_file.txt"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		result = run_make(git_env, "verify-git")
		assert result.returncode != 0

	def test_custom_publish_branch(self, git_env: Path) -> None:
		subprocess.run(
			["git", "checkout", "-b", "release"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		result = run_make(git_env, "verify-git", PUBLISH_BRANCH="release")
		assert result.returncode == 0, result.stderr

	def test_fails_with_untracked_files(self, git_env: Path) -> None:
		"""verify-git should fail with purely untracked files (not just staged)."""
		subprocess.run(
			["git", "branch", "-M", "main"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		(git_env / "untracked.txt").write_text("untracked")
		# Do NOT git add — file is purely untracked.
		result = run_make(git_env, "verify-git")
		assert result.returncode != 0


# ---------------------------------------------------------------------------
# make format / make format-check (conditional on ruff)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _has_ruff, reason="ruff not installed")
class TestFormatCheck:
	"""Verify ``make format-check`` runs ruff linting."""

	def test_format_check_echoes_description(self, make_env: Path) -> None:
		result = run_make(make_env, "format-check", RUN_GLOBAL="1")
		assert "check" in result.stdout.lower()

	def test_format_check_runs_without_crash(self, make_env: Path) -> None:
		result = run_make(make_env, "format-check", RUN_GLOBAL="1")
		assert result.returncode in (0, 1)

	def test_catches_bad_formatting(self, make_env: Path) -> None:
		"""format-check should fail on code with lint errors (unused import)."""
		bad = make_env / "myproject" / "bad.py"
		bad.write_text("import os\n\nx = 1\n")
		result = run_make(make_env, "format-check", RUN_GLOBAL="1")
		assert result.returncode != 0


@pytest.mark.skipif(not _has_ruff, reason="ruff not installed")
class TestFormat:
	"""Verify ``make format`` runs ruff formatting and fixing."""

	def test_format_echoes_description(self, make_env: Path) -> None:
		result = run_make(make_env, "format", RUN_GLOBAL="1")
		assert "format" in result.stdout.lower()

	def test_format_runs_without_crash(self, make_env: Path) -> None:
		result = run_make(make_env, "format", RUN_GLOBAL="1")
		assert result.returncode in (0, 1)

	def test_fixes_bad_formatting(self, make_env: Path) -> None:
		"""format should reformat a poorly-formatted file."""
		bad = make_env / "myproject" / "badly_formatted.py"
		bad.write_text("x=1\ny    =    2\n")
		run_make(make_env, "format", RUN_GLOBAL="1")
		# ruff format runs first and fixes spacing; ruff check --fix may still
		# report unfixable lint errors (e.g. D100), but the file should be reformatted.
		fixed = bad.read_text()
		assert "x = 1" in fixed, f"Expected ruff to fix spacing: {fixed!r}"


# ---------------------------------------------------------------------------
# makefile variable overrides
# ---------------------------------------------------------------------------


class TestMakefileVariableOverrides:
	"""Verify that makefile variables can be overridden from the command line."""

	@pytest.fixture
	def override_env(self, make_env: Path) -> Path:
		versions_dir = make_env / ".meta" / "versions"
		versions_dir.mkdir(parents=True, exist_ok=True)
		(versions_dir / ".version").write_text("v0.0.0")
		(make_env / ".meta" / "local").mkdir(parents=True, exist_ok=True)
		return make_env

	def test_run_global_sets_python(self, override_env: Path) -> None:
		"""RUN_GLOBAL=1 should make PYTHON=python (not uv run python)."""
		result = run_make(override_env, "info", RUN_GLOBAL="1")
		assert result.returncode == 0, result.stderr
		for line in result.stdout.splitlines():
			if (
				"PYTHON =" in line
				and "PYTHON_VERSION" not in line
				and "PYTHON_BASE" not in line
			):
				assert "uv run" not in line
				break

	def test_package_name_override(self, make_env: Path) -> None:
		d = make_env / "custom_pkg.egg-info"
		d.mkdir()
		(d / "sentinel").touch()
		result = run_make(make_env, "clean", PACKAGE_NAME="custom_pkg")
		assert result.returncode == 0, result.stderr
		assert not d.exists(), "clean should remove custom_pkg.egg-info"

	def test_makefile_name_override(self, make_env: Path) -> None:
		shutil.copy(make_env / "makefile", make_env / "Makefile.custom")
		result = run_make(
			make_env,
			"-f",
			"Makefile.custom",
			"help-targets",
			MAKEFILE_NAME="Makefile.custom",
		)
		assert result.returncode == 0, result.stderr
		assert "make targets" in result.stdout.lower()

	def test_tests_dir_override(self, make_env: Path) -> None:
		"""TESTS_DIR=custom_tests should make clean remove custom_tests/_temp/."""
		custom_temp = make_env / "custom_tests" / "_temp"
		custom_temp.mkdir(parents=True)
		(custom_temp / "sentinel").touch()
		result = run_make(make_env, "clean", TESTS_DIR="custom_tests")
		assert result.returncode == 0, result.stderr
		assert not custom_temp.exists(), "custom_tests/_temp/ should be removed"

	def test_pytest_options_override(self, override_env: Path) -> None:
		"""PYTEST_OPTIONS should be passed through to info output."""
		result = run_make(
			override_env, "info", RUN_GLOBAL="1", PYTEST_OPTIONS="--maxfail=1"
		)
		assert result.returncode == 0, result.stderr
		assert "--maxfail=1" in result.stdout

	def test_uv_nosync_adds_no_sync_flag(self, make_env: Path) -> None:
		"""UV_NOSYNC=1 with RUN_GLOBAL=0 should set PYTHON to 'uv run --no-sync ...'."""
		eval_print = '_test-python:\n\t@printf "%s" "$(PYTHON)"'
		result = run_make(
			make_env,
			f"--eval={eval_print}",
			"_test-python",
			UV_NOSYNC="1",
			RUN_GLOBAL="0",
		)
		assert result.returncode == 0, result.stderr
		assert "uv run --no-sync" in result.stdout


# ---------------------------------------------------------------------------
# CI YAML
# ---------------------------------------------------------------------------


class TestCIYaml:
	"""Validate the GitHub Actions workflow file."""

	YAML_PATH = PROJECT_ROOT / ".github" / "workflows" / "makefile-checks.yml"

	def test_no_tab_characters(self) -> None:
		"""EXPECTED TO FAIL before fix — line 24 has a TAB after "3.13"."""
		content = self.YAML_PATH.read_text()
		lines_with_tabs = [
			(i, line) for i, line in enumerate(content.splitlines(), 1) if "\t" in line
		]
		assert not lines_with_tabs, (
			"YAML contains TAB characters on line(s): "
			+ "; ".join(f"L{n}: {line!r}" for n, line in lines_with_tabs)
		)

	def test_valid_yaml_syntax(self) -> None:
		"""YAML should parse without errors."""
		with open(self.YAML_PATH) as f:
			data = yaml.safe_load(f)
		assert data is not None
		assert "jobs" in data


# ---------------------------------------------------------------------------
# makefile template assembly
# ---------------------------------------------------------------------------


class TestAssembly:
	"""Verify the built makefile matches what assemble.py would produce."""

	TEMPLATE = PROJECT_ROOT / "makefile.template"
	BUILT = PROJECT_ROOT / "makefile"
	PLACEHOLDER = "##[[VERSION]]##"

	def test_makefile_matches_template(self) -> None:
		"""Built makefile should equal makefile.template with version replaced."""
		version = _read_pyproject_version(PROJECT_ROOT)
		version_line = f"#| version: v{version}"
		expected = self.TEMPLATE.read_text().replace(
			self.PLACEHOLDER,
			f"{version_line:<68}|",
		)
		actual = self.BUILT.read_text()
		assert actual == expected, (
			"makefile is out of sync with makefile.template — "
			"run `python scripts/assemble.py`"
		)


# ---------------------------------------------------------------------------
# verify-git quoting
# ---------------------------------------------------------------------------


class TestVerifyGitQuoting:
	"""Document the unquoted $(PUBLISH_BRANCH) bug in verify-git."""

	@pytest.mark.xfail(reason="PUBLISH_BRANCH is unquoted in shell comparison (line 542)")
	def test_publish_branch_with_space(self, git_env: Path) -> None:
		"""verify-git should handle a PUBLISH_BRANCH containing a space."""
		subprocess.run(
			["git", "checkout", "-b", "my branch"],
			cwd=git_env,
			capture_output=True,
			check=True,
		)
		result = run_make(git_env, "verify-git", PUBLISH_BRANCH="my branch")
		assert result.returncode == 0, result.stderr
