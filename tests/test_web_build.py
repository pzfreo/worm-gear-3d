"""
Tests for web build script and package deployment.

These tests ensure the web interface has all necessary files for
WASM geometry generation in the browser.
"""

import subprocess
import json
from pathlib import Path
import pytest


# Define the repository root
REPO_ROOT = Path(__file__).parent.parent
WEB_DIR = REPO_ROOT / "web"
BUILD_SCRIPT = WEB_DIR / "build.sh"
SRC_DIR = REPO_ROOT / "src" / "wormgear"


# List of all files that MUST be present after build for WASM to work
REQUIRED_WASM_FILES = [
    "wormgear/__init__.py",
    "wormgear/core/__init__.py",
    "wormgear/core/worm.py",
    "wormgear/core/wheel.py",
    "wormgear/core/features.py",
    "wormgear/core/globoid_worm.py",
    "wormgear/core/virtual_hobbing.py",
    "wormgear/io/__init__.py",
    "wormgear/io/loaders.py",
    "wormgear/io/schema.py",
    "wormgear/calculator/__init__.py",
    "wormgear/calculator/core.py",
    "wormgear/calculator/validation.py",
]


def test_build_script_exists():
    """Build script should exist and be executable."""
    assert BUILD_SCRIPT.exists(), f"Build script not found at {BUILD_SCRIPT}"
    assert BUILD_SCRIPT.stat().st_mode & 0o111, "Build script is not executable"


def test_build_script_runs_successfully():
    """Build script should run without errors."""
    result = subprocess.run(
        [str(BUILD_SCRIPT)],
        cwd=WEB_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Build script failed:\n{result.stderr}"
    assert "✅ Build complete!" in result.stdout, "Build didn't complete successfully"


def test_all_required_files_copied():
    """All required Python files should be copied to web/src/wormgear/."""
    # Run build first
    subprocess.run([str(BUILD_SCRIPT)], cwd=WEB_DIR, check=True, capture_output=True)

    web_src_dir = WEB_DIR / "src" / "wormgear"

    for required_file in REQUIRED_WASM_FILES:
        file_path = WEB_DIR / "src" / required_file
        assert file_path.exists(), f"Required file missing after build: {required_file}"
        assert file_path.stat().st_size > 0, f"File is empty: {required_file}"


def test_app_lazy_js_has_all_files():
    """app-lazy.js should list all required files in packageFiles array."""
    app_lazy_path = WEB_DIR / "app-lazy.js"
    assert app_lazy_path.exists(), "app-lazy.js not found"

    content = app_lazy_path.read_text()

    # Check that packageFiles array exists
    assert "packageFiles = [" in content, "packageFiles array not found in app-lazy.js"

    # Check each required file is listed
    for required_file in REQUIRED_WASM_FILES:
        # Convert path to the format used in app-lazy.js
        assert required_file in content, (
            f"Required file '{required_file}' not listed in app-lazy.js packageFiles array"
        )


def test_no_pycache_in_output():
    """Build should not include __pycache__ directories."""
    # Run build first
    subprocess.run([str(BUILD_SCRIPT)], cwd=WEB_DIR, check=True, capture_output=True)

    web_src_dir = WEB_DIR / "src" / "wormgear"
    pycache_dirs = list(web_src_dir.rglob("__pycache__"))

    assert len(pycache_dirs) == 0, f"Found {len(pycache_dirs)} __pycache__ directories in output"


def test_no_pyc_files_in_output():
    """Build should not include .pyc files."""
    # Run build first
    subprocess.run([str(BUILD_SCRIPT)], cwd=WEB_DIR, check=True, capture_output=True)

    web_src_dir = WEB_DIR / "src" / "wormgear"
    pyc_files = list(web_src_dir.rglob("*.pyc"))

    assert len(pyc_files) == 0, f"Found {len(pyc_files)} .pyc files in output"


def test_source_files_exist():
    """Source files in src/wormgear should exist (needed by build script)."""
    for required_file in REQUIRED_WASM_FILES:
        src_file = SRC_DIR / required_file.replace("wormgear/", "")
        assert src_file.exists(), f"Source file missing: {src_file}"


def test_build_script_validation_list_matches():
    """Build script REQUIRED_FILES should match our test requirements."""
    build_script_content = BUILD_SCRIPT.read_text()

    # Extract REQUIRED_FILES array from bash script
    assert "REQUIRED_FILES=(" in build_script_content, "REQUIRED_FILES not found in build.sh"

    # Check each file is in the validation list
    for required_file in REQUIRED_WASM_FILES:
        # Build script checks for src/wormgear/... format
        build_script_path = f"src/{required_file}"
        assert build_script_path in build_script_content, (
            f"File '{build_script_path}' not in build.sh REQUIRED_FILES validation list"
        )


def test_vercel_json_has_build_command():
    """vercel.json should have buildCommand configured."""
    vercel_json = REPO_ROOT / "vercel.json"
    assert vercel_json.exists(), "vercel.json not found"

    config = json.loads(vercel_json.read_text())
    assert "buildCommand" in config, "vercel.json missing buildCommand"
    assert "./build.sh" in config["buildCommand"], "buildCommand doesn't reference build.sh"


def test_vercel_json_has_output_directory():
    """vercel.json should have outputDirectory configured."""
    vercel_json = REPO_ROOT / "vercel.json"
    config = json.loads(vercel_json.read_text())

    assert "outputDirectory" in config, "vercel.json missing outputDirectory"
    assert config["outputDirectory"] == ".", "outputDirectory should be '.'"


def test_gitignore_excludes_generated_files():
    """Generated web/src/wormgear/ should be in .gitignore."""
    gitignore = REPO_ROOT / ".gitignore"
    assert gitignore.exists(), ".gitignore not found"

    content = gitignore.read_text()
    assert "web/src/wormgear/" in content, (
        "Generated files not in .gitignore - they should not be committed"
    )


def test_vercelignore_does_not_exclude_src():
    """src/ directory should NOT be in .vercelignore (needed by build script)."""
    vercelignore = REPO_ROOT / ".vercelignore"
    assert vercelignore.exists(), ".vercelignore not found"

    content = vercelignore.read_text()

    # Check that src/ is not excluded (or is commented out)
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    active_ignores = [line for line in lines if not line.startswith("#")]

    assert "src/" not in active_ignores, (
        "src/ is in .vercelignore - build script needs access to src/ directory"
    )


@pytest.mark.skipif(
    not (WEB_DIR / "src" / "wormgear" / "__init__.py").exists(),
    reason="Build not run yet"
)
def test_package_version_accessible():
    """Package should have __version__ accessible after build."""
    init_file = WEB_DIR / "src" / "wormgear" / "__init__.py"
    content = init_file.read_text()

    assert "__version__" in content, "Package __init__.py should define __version__"


def test_index_html_loads_pyodide():
    """index.html should load Pyodide from CDN."""
    index_html = WEB_DIR / "index.html"
    assert index_html.exists(), "index.html not found"

    content = index_html.read_text()
    assert "pyodide.js" in content, "index.html doesn't load Pyodide"
    assert "cdn.jsdelivr.net/pyodide" in content, "Pyodide should be loaded from CDN"


def test_pyodide_version_consistency():
    """Pyodide version should be consistent between HTML and JavaScript."""
    index_html = WEB_DIR / "index.html"
    app_lazy = WEB_DIR / "app-lazy.js"

    html_content = index_html.read_text()
    js_content = app_lazy.read_text()

    # Extract version from HTML (e.g., v0.29.0)
    import re
    html_match = re.search(r'pyodide/v([0-9.]+)/', html_content)
    js_matches = re.findall(r'pyodide/v([0-9.]+)/', js_content)

    assert html_match, "Pyodide version not found in index.html"
    assert js_matches, "Pyodide version not found in app-lazy.js"

    html_version = html_match.group(1)

    # All JS versions should match HTML version
    for js_version in js_matches:
        assert js_version == html_version, (
            f"Pyodide version mismatch: HTML has {html_version}, "
            f"but app-lazy.js has {js_version}"
        )


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
