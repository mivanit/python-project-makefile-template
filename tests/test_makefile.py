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

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def make_env(tmp_path: Path) -> Path:
    """Create an isolated make environment in *tmp_path*.

    Copies makefile, pyproject.toml, and .meta/scripts/ (for targets that call
    Python helper scripts). Creates the minimal directory skeleton the makefile
    expects (myproject/, tests/, docs/, docs/resources/).
    """
    shutil.copy(PROJECT_ROOT / "makefile", tmp_path / "makefile")
    shutil.copy(PROJECT_ROOT / "pyproject.toml", tmp_path / "pyproject.toml")

    meta_scripts = PROJECT_ROOT / ".meta" / "scripts"
    if meta_scripts.is_dir():
        shutil.copytree(meta_scripts, tmp_path / ".meta" / "scripts")

    for d in ("myproject", "tests", "docs", "docs/resources"):
        (tmp_path / d).mkdir(parents=True, exist_ok=True)

    return tmp_path


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
    return subprocess.run(
        cmd,
        cwd=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


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
            assert not d.exists(), f"__pycache__ at {d.relative_to(make_env)} still exists"

    def test_removes_pyc_files(self, make_env: Path) -> None:
        pyc = make_env / "myproject" / "mod.pyc"
        pyo = make_env / "tests" / "test_x.pyo"
        pyc.touch()
        pyo.touch()
        result = run_make(make_env, "clean")
        assert result.returncode == 0, result.stderr
        assert not pyc.exists(), ".pyc file should be removed"
        assert not pyo.exists(), ".pyo file should be removed"

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


# ---------------------------------------------------------------------------
# version / publish
# ---------------------------------------------------------------------------


class TestVersion:
    """Verify gen-version-info populates PROJ_VERSION without trailing whitespace."""

    @pytest.fixture()
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
        eval_print = (
            "_test-ver: gen-version-info\n"
            '\t@printf "%s" "$(PROJ_VERSION)"'
        )
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
                "bash", "-c",
                f'[ "{clean_version}" = "{proj_version}" ]',
            ],
            capture_output=True,
            text=True,
        )
        assert comparison.returncode == 0, (
            f"Publish version confirmation would fail: "
            f"user types [{clean_version!r}] but PROJ_VERSION is [{proj_version!r}]"
        )


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
            (i, line)
            for i, line in enumerate(content.splitlines(), 1)
            if "\t" in line
        ]
        assert not lines_with_tabs, (
            "YAML contains TAB characters on line(s): "
            + "; ".join(f"L{n}: {line!r}" for n, line in lines_with_tabs)
        )

    def test_valid_yaml_syntax(self) -> None:
        """YAML should parse without errors."""
        yaml = pytest.importorskip("yaml")
        with open(self.YAML_PATH) as f:
            data = yaml.safe_load(f)
        assert data is not None
        assert "jobs" in data
