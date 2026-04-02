"""Tests for scripts/fetch-axe-rules.py.

Covers:
- fetch_axe_rules (success and failure paths)
- save_status_report
"""

import json
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests


# ---------------------------------------------------------------------------
# fetch_axe_rules
# ---------------------------------------------------------------------------

class TestFetchAxeRules:
    """Tests for fetch_axe_rules."""

    def test_success_returns_version_and_url(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """Returns a dict with status='success', version, and published_at on 200."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "tag_name": "v4.8.2",
            "published_at": "2024-01-15T10:00:00Z",
        }
        with patch("requests.get", return_value=mock_response):
            result = fetch_axe_module.fetch_axe_rules()

        assert result["status"] == "success"
        assert result["version"] == "4.8.2"
        assert result["published_at"] == "2024-01-15T10:00:00Z"
        assert "url" in result

    def test_version_prefix_stripped(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """The leading 'v' is stripped from the tag_name."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "tag_name": "v1.2.3",
            "published_at": "2023-06-01T00:00:00Z",
        }
        with patch("requests.get", return_value=mock_response):
            result = fetch_axe_module.fetch_axe_rules()

        assert result["version"] == "1.2.3"

    def test_network_error_returns_error_status(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """A RequestException returns status='error' with an error message."""
        with patch(
            "requests.get",
            side_effect=requests.exceptions.ConnectionError("Network unreachable"),
        ):
            result = fetch_axe_module.fetch_axe_rules()

        assert result["status"] == "error"
        assert "error" in result

    def test_http_error_returns_error_status(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """An HTTP error status (e.g. 404) is caught and returned as error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        with patch("requests.get", return_value=mock_response):
            result = fetch_axe_module.fetch_axe_rules()

        assert result["status"] == "error"

    def test_missing_tag_name_defaults_to_unknown(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """When tag_name is absent the version defaults to 'unknown'."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}
        with patch("requests.get", return_value=mock_response):
            result = fetch_axe_module.fetch_axe_rules()

        assert result["version"] == "unknown"


# ---------------------------------------------------------------------------
# save_status_report
# ---------------------------------------------------------------------------

class TestSaveStatusReport:
    """Tests for fetch-axe-rules save_status_report."""

    def test_creates_file(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """The output file is created."""
        output_file = str(tmp_path / "axe-status.json")
        fetch_axe_module.save_status_report({"status": "success"}, output_file)
        assert Path(output_file).exists()

    def test_report_contains_checked_at(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """The saved report includes a 'checked_at' timestamp."""
        output_file = str(tmp_path / "axe-status.json")
        fetch_axe_module.save_status_report({"status": "success"}, output_file)
        data = json.loads(Path(output_file).read_text())
        assert "checked_at" in data

    def test_report_contains_axe_info(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """The saved report wraps axe info under the 'axe-core' key."""
        axe_info = {"status": "success", "version": "4.8.2"}
        output_file = str(tmp_path / "axe-status.json")
        fetch_axe_module.save_status_report(axe_info, output_file)
        data = json.loads(Path(output_file).read_text())
        assert data["axe-core"] == axe_info

    def test_creates_parent_directory(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """Parent directories are created automatically."""
        output_file = str(tmp_path / "monitoring" / "axe-status.json")
        fetch_axe_module.save_status_report({"status": "success"}, output_file)
        assert Path(output_file).exists()

    def test_valid_json_output(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """The written file is valid JSON."""
        output_file = str(tmp_path / "axe-status.json")
        fetch_axe_module.save_status_report({"status": "success"}, output_file)
        # This should not raise
        json.loads(Path(output_file).read_text())


# ---------------------------------------------------------------------------
# main (integration-level smoke test)
# ---------------------------------------------------------------------------

class TestFetchAxeRulesMain:
    """Smoke tests for the main() entry point of fetch-axe-rules."""

    def test_main_success_exits_zero(
        self, fetch_axe_module: types.ModuleType
    ) -> None:
        """main() exits with code 0 when fetch succeeds."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "tag_name": "v4.8.2",
            "published_at": "2024-01-15T10:00:00Z",
        }
        with (
            patch("requests.get", return_value=mock_response),
            patch.object(fetch_axe_module, "save_status_report"),
            pytest.raises(SystemExit) as exc_info,
        ):
            fetch_axe_module.main()
        assert exc_info.value.code == 0

    def test_main_error_exits_one(
        self, tmp_path: Path, fetch_axe_module: types.ModuleType
    ) -> None:
        """main() exits with code 1 when fetch fails."""
        with (
            patch(
                "requests.get",
                side_effect=requests.exceptions.ConnectionError("fail"),
            ),
            patch.object(fetch_axe_module, "save_status_report"),
            pytest.raises(SystemExit) as exc_info,
        ):
            fetch_axe_module.main()
        assert exc_info.value.code == 1
