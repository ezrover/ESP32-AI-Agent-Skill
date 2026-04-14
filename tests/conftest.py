"""
Shared fixtures and helpers for gpio-config test suite.

Provides platform fixtures, fixture file loading, and assertion helpers
used across all test modules.
"""

import json
import sys
from pathlib import Path

import pytest

# Add the scripts and tests directories to sys.path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
TESTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(TESTS_DIR))

from platforms import ConflictType, get_platform  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fixtures_dir():
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def load_fixture(fixtures_dir):
    """Return a helper that loads a JSON fixture by filename."""
    def _load(name):
        with open(fixtures_dir / name) as f:
            return json.load(f)
    return _load


@pytest.fixture
def esp32_platform():
    """Return a fresh Esp32Platform instance (ESP32 WROOM)."""
    return get_platform("esp32", module="WROOM")


@pytest.fixture
def esp32s3_platform():
    """Return a fresh Esp32Platform instance (ESP32-S3 WROOM)."""
    return get_platform("esp32", variant="esp32s3", module="WROOM")


# ---------------------------------------------------------------------------
# Assertion helpers (plain functions — importable via helpers fixture)
# ---------------------------------------------------------------------------

def _get_warning_codes(result):
    """Extract the list of warning code strings from a ValidationResult."""
    return [w["code"] for w in result.warnings]


def _get_error_codes(result):
    """Extract the list of error code strings from a ValidationResult."""
    return [e["code"] for e in result.errors]


def _assert_valid(result):
    """Assert that a ValidationResult has no errors."""
    assert result.valid is True, f"Expected valid, got errors: {result.errors}"
    assert len(result.errors) == 0


def _assert_invalid(result):
    """Assert that a ValidationResult has at least one error."""
    assert result.valid is False
    assert len(result.errors) > 0


class _Helpers:
    """Namespace for assertion/extraction helpers, exposed via fixture."""
    get_warning_codes = staticmethod(_get_warning_codes)
    get_error_codes = staticmethod(_get_error_codes)
    assert_valid = staticmethod(_assert_valid)
    assert_invalid = staticmethod(_assert_invalid)


@pytest.fixture
def helpers():
    """Provide assertion helpers: helpers.assert_valid, helpers.get_error_codes, etc."""
    return _Helpers
