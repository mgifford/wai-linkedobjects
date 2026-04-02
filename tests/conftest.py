"""Pytest configuration and shared fixtures.

Provides importlib-based helpers for loading scripts whose filenames
contain hyphens (which are not valid Python identifiers).
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def load_hyphenated_module(file_stem: str) -> types.ModuleType:
    """Load a Python script whose filename contains hyphens.

    Args:
        file_stem: Filename stem, e.g. ``"fetch-axe-rules"``.

    Returns:
        The imported module object.
    """
    module_name = file_stem.replace("-", "_")
    file_path = SCRIPTS_DIR / f"{file_stem}.py"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def validate_module() -> types.ModuleType:
    """Return the ``validate`` module."""
    return load_hyphenated_module("validate")


@pytest.fixture(scope="session")
def generate_wcag_module() -> types.ModuleType:
    """Return the ``generate-wcag`` module."""
    return load_hyphenated_module("generate-wcag")


@pytest.fixture(scope="session")
def fetch_axe_module() -> types.ModuleType:
    """Return the ``fetch-axe-rules`` module."""
    return load_hyphenated_module("fetch-axe-rules")


@pytest.fixture(scope="session")
def fetch_standards_module() -> types.ModuleType:
    """Return the ``fetch-standards`` module."""
    return load_hyphenated_module("fetch-standards")
