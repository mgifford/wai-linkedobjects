"""Tests for scripts/fetch-standards.py.

Covers:
- _fetch_standard (success and failure)
- fetch_wcag_latest / fetch_aria_latest / fetch_atag_latest / fetch_uaag_latest
- check_all_standards
- save_status_report
- main
"""

import json
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests


# ---------------------------------------------------------------------------
# _fetch_standard
# ---------------------------------------------------------------------------

class TestFetchStandard:
    """Tests for the private _fetch_standard helper."""

    def test_success_returns_available_status(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """A successful HTTP response returns status='available'."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {
            "Last-Modified": "Mon, 05 Oct 2023 00:00:00 GMT",
            "ETag": '"abc123"',
        }
        with patch("requests.get", return_value=mock_response):
            result = fetch_standards_module._fetch_standard(
                "WCAG 2.2", "https://www.w3.org/TR/WCAG22/"
            )

        assert result["status"] == "available"
        assert result["url"] == "https://www.w3.org/TR/WCAG22/"

    def test_success_includes_headers(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """last_modified and etag from HTTP headers are included in the result."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {
            "Last-Modified": "Tue, 01 Jan 2019 12:00:00 GMT",
            "ETag": '"etag-value"',
        }
        with patch("requests.get", return_value=mock_response):
            result = fetch_standards_module._fetch_standard(
                "ARIA 1.2", "https://www.w3.org/TR/wai-aria-1.2/"
            )

        assert result["last_modified"] == "Tue, 01 Jan 2019 12:00:00 GMT"
        assert result["etag"] == '"etag-value"'

    def test_missing_headers_default_to_unknown(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """When headers are absent the fields default to 'Unknown'."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {}
        with patch("requests.get", return_value=mock_response):
            result = fetch_standards_module._fetch_standard(
                "ATAG 2.0", "https://www.w3.org/TR/ATAG20/"
            )

        assert result["last_modified"] == "Unknown"
        assert result["etag"] == "Unknown"

    def test_request_exception_returns_error(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """A RequestException returns status='error' with an error message."""
        with patch(
            "requests.get",
            side_effect=requests.exceptions.ConnectionError("timeout"),
        ):
            result = fetch_standards_module._fetch_standard(
                "WCAG 2.2", "https://www.w3.org/TR/WCAG22/"
            )

        assert result["status"] == "error"
        assert "error" in result
        assert result["url"] == "https://www.w3.org/TR/WCAG22/"

    def test_http_error_returns_error_status(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """An HTTP 4xx/5xx response is caught and returned as error."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "503 Service Unavailable"
        )
        with patch("requests.get", return_value=mock_response):
            result = fetch_standards_module._fetch_standard(
                "UAAG 2.0", "https://www.w3.org/TR/UAAG20/"
            )

        assert result["status"] == "error"


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------

class TestConvenienceWrappers:
    """Tests for fetch_wcag_latest, fetch_aria_latest, etc."""

    def _mock_success(self) -> MagicMock:
        """Return a mock HTTP response that succeeds."""
        mock = MagicMock()
        mock.raise_for_status.return_value = None
        mock.headers = {"Last-Modified": "Mon, 01 Jan 2024 00:00:00 GMT", "ETag": '"x"'}
        return mock

    def test_fetch_wcag_latest_calls_correct_url(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """fetch_wcag_latest targets the WCAG 2.2 W3C URL."""
        with patch("requests.get", return_value=self._mock_success()) as mock_get:
            fetch_standards_module.fetch_wcag_latest()
        url = mock_get.call_args[0][0]
        assert "WCAG22" in url or "wcag22" in url.lower()

    def test_fetch_aria_latest_calls_correct_url(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """fetch_aria_latest targets the WAI-ARIA 1.2 W3C URL."""
        with patch("requests.get", return_value=self._mock_success()) as mock_get:
            fetch_standards_module.fetch_aria_latest()
        url = mock_get.call_args[0][0]
        assert "aria" in url.lower()

    def test_fetch_atag_latest_calls_correct_url(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """fetch_atag_latest targets the ATAG 2.0 W3C URL."""
        with patch("requests.get", return_value=self._mock_success()) as mock_get:
            fetch_standards_module.fetch_atag_latest()
        url = mock_get.call_args[0][0]
        assert "ATAG" in url or "atag" in url.lower()

    def test_fetch_uaag_latest_calls_correct_url(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """fetch_uaag_latest targets the UAAG 2.0 W3C URL."""
        with patch("requests.get", return_value=self._mock_success()) as mock_get:
            fetch_standards_module.fetch_uaag_latest()
        url = mock_get.call_args[0][0]
        assert "UAAG" in url or "uaag" in url.lower()

    def test_fetch_wcag_returns_available_on_success(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """fetch_wcag_latest returns status='available' on a successful request."""
        with patch("requests.get", return_value=self._mock_success()):
            result = fetch_standards_module.fetch_wcag_latest()
        assert result["status"] == "available"


# ---------------------------------------------------------------------------
# check_all_standards
# ---------------------------------------------------------------------------

class TestCheckAllStandards:
    """Tests for check_all_standards."""

    def _success_result(self) -> dict:
        """Helper that returns a representative 'available' result."""
        return {"url": "https://example.org", "status": "available",
                "last_modified": "Unknown", "etag": "Unknown"}

    def test_returns_dict_with_four_keys(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """check_all_standards returns a dict with wcag, aria, atag, uaag keys."""
        ok = self._success_result()
        with (
            patch.object(fetch_standards_module, "fetch_wcag_latest", return_value=ok),
            patch.object(fetch_standards_module, "fetch_aria_latest", return_value=ok),
            patch.object(fetch_standards_module, "fetch_atag_latest", return_value=ok),
            patch.object(fetch_standards_module, "fetch_uaag_latest", return_value=ok),
        ):
            result = fetch_standards_module.check_all_standards()

        assert set(result.keys()) == {"wcag", "aria", "atag", "uaag"}

    def test_delegates_to_individual_fetchers(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """Each standard is fetched via its dedicated function."""
        wcag_mock = MagicMock(return_value=self._success_result())
        aria_mock = MagicMock(return_value=self._success_result())
        atag_mock = MagicMock(return_value=self._success_result())
        uaag_mock = MagicMock(return_value=self._success_result())

        with (
            patch.object(fetch_standards_module, "fetch_wcag_latest", wcag_mock),
            patch.object(fetch_standards_module, "fetch_aria_latest", aria_mock),
            patch.object(fetch_standards_module, "fetch_atag_latest", atag_mock),
            patch.object(fetch_standards_module, "fetch_uaag_latest", uaag_mock),
        ):
            fetch_standards_module.check_all_standards()

        wcag_mock.assert_called_once()
        aria_mock.assert_called_once()
        atag_mock.assert_called_once()
        uaag_mock.assert_called_once()


# ---------------------------------------------------------------------------
# save_status_report
# ---------------------------------------------------------------------------

class TestSaveStatusReportStandards:
    """Tests for fetch-standards save_status_report."""

    def test_creates_file(
        self, tmp_path: Path, fetch_standards_module: types.ModuleType
    ) -> None:
        """The output file is created."""
        output_file = str(tmp_path / "standards-status.json")
        fetch_standards_module.save_status_report({}, output_file)
        assert Path(output_file).exists()

    def test_report_contains_checked_at(
        self, tmp_path: Path, fetch_standards_module: types.ModuleType
    ) -> None:
        """The report includes a 'checked_at' timestamp."""
        output_file = str(tmp_path / "standards-status.json")
        fetch_standards_module.save_status_report({}, output_file)
        data = json.loads(Path(output_file).read_text())
        assert "checked_at" in data

    def test_report_contains_standards(
        self, tmp_path: Path, fetch_standards_module: types.ModuleType
    ) -> None:
        """Standards data is nested under the 'standards' key."""
        standards = {"wcag": {"status": "available"}}
        output_file = str(tmp_path / "standards-status.json")
        fetch_standards_module.save_status_report(standards, output_file)
        data = json.loads(Path(output_file).read_text())
        assert data["standards"] == standards

    def test_creates_parent_directory(
        self, tmp_path: Path, fetch_standards_module: types.ModuleType
    ) -> None:
        """Nested directories are created automatically."""
        output_file = str(tmp_path / "monitoring" / "standards-status.json")
        fetch_standards_module.save_status_report({}, output_file)
        assert Path(output_file).exists()

    def test_valid_json_output(
        self, tmp_path: Path, fetch_standards_module: types.ModuleType
    ) -> None:
        """Written file is parseable as JSON."""
        output_file = str(tmp_path / "standards-status.json")
        fetch_standards_module.save_status_report({}, output_file)
        json.loads(Path(output_file).read_text())  # should not raise


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestFetchStandardsMain:
    """Smoke tests for the main() entry point of fetch-standards."""

    def _success_result(self) -> dict:
        """Return a representative 'available' result."""
        return {"url": "https://example.org", "status": "available",
                "last_modified": "Unknown", "etag": "Unknown"}

    def test_main_success_returns_zero(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """main() returns 0 when all standards are available."""
        all_ok = {
            "wcag": self._success_result(),
            "aria": self._success_result(),
            "atag": self._success_result(),
            "uaag": self._success_result(),
        }
        with (
            patch.object(
                fetch_standards_module, "check_all_standards", return_value=all_ok
            ),
            patch.object(fetch_standards_module, "save_status_report"),
        ):
            result = fetch_standards_module.main()
        assert result == 0

    def test_main_partial_error_returns_one(
        self, fetch_standards_module: types.ModuleType
    ) -> None:
        """main() returns 1 when at least one standard has an error."""
        mixed = {
            "wcag": self._success_result(),
            "aria": {
                "url": "https://example.org",
                "status": "error",
                "error": "timeout",
            },
            "atag": self._success_result(),
            "uaag": self._success_result(),
        }
        with (
            patch.object(
                fetch_standards_module, "check_all_standards", return_value=mixed
            ),
            patch.object(fetch_standards_module, "save_status_report"),
        ):
            result = fetch_standards_module.main()
        assert result == 1
