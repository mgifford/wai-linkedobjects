"""Tests for scripts/validate.py.

Covers:
- count_success_criteria
- extract_sc_identifiers
- validate_wcag_completeness
- validate_json_ld
- validate_all_jsonld_files
"""

import json
import types
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_valid_doc() -> dict:
    """Return the smallest document that passes validate_json_ld."""
    return {
        "@context": "https://example.org/context.jsonld",
        "@id": "https://example.org/doc",
        "@type": "Standard",
        "identifier": "TEST-1",
        "title": "Test Standard",
        "description": "A test standard.",
    }


def _wcag_doc_with_sc(sc_list: list[dict]) -> dict:
    """Return a minimal WCAG document wrapping *sc_list* in one guideline."""
    doc = _minimal_valid_doc()
    doc["principles"] = [
        {
            "guidelines": [
                {"successCriteria": sc_list}
            ]
        }
    ]
    doc["metadata"] = {"totalSuccessCriteria": len(sc_list)}
    return doc


# ---------------------------------------------------------------------------
# count_success_criteria
# ---------------------------------------------------------------------------

class TestCountSuccessCriteria:
    """Tests for count_success_criteria."""

    def test_empty_document_returns_zero(
        self, validate_module: types.ModuleType
    ) -> None:
        """An empty document has no success criteria."""
        assert validate_module.count_success_criteria({}) == 0

    def test_document_without_principles_returns_zero(
        self, validate_module: types.ModuleType
    ) -> None:
        """A document with no 'principles' key returns zero."""
        assert validate_module.count_success_criteria({"title": "No Principles"}) == 0

    def test_principle_without_guidelines_returns_zero(
        self, validate_module: types.ModuleType
    ) -> None:
        """A principle with no 'guidelines' key contributes zero."""
        doc = {"principles": [{"name": "P1"}]}
        assert validate_module.count_success_criteria(doc) == 0

    def test_guideline_without_success_criteria_returns_zero(
        self, validate_module: types.ModuleType
    ) -> None:
        """A guideline with no 'successCriteria' key contributes zero."""
        doc = {"principles": [{"guidelines": [{"name": "G1"}]}]}
        assert validate_module.count_success_criteria(doc) == 0

    def test_single_success_criterion(self, validate_module: types.ModuleType) -> None:
        """One success criterion in one guideline gives count of 1."""
        doc = _wcag_doc_with_sc([{"identifier": "1.1.1"}])
        assert validate_module.count_success_criteria(doc) == 1

    def test_multiple_success_criteria_across_guidelines(
        self, validate_module: types.ModuleType
    ) -> None:
        """Criteria spread across multiple guidelines are all counted."""
        doc = {
            "principles": [
                {
                    "guidelines": [
                        {
                            "successCriteria": [
                                {"identifier": "1.1.1"},
                                {"identifier": "1.1.2"},
                            ]
                        },
                        {"successCriteria": [{"identifier": "1.2.1"}]},
                    ]
                },
                {
                    "guidelines": [
                        {"successCriteria": [{"identifier": "2.1.1"}]},
                    ]
                },
            ]
        }
        assert validate_module.count_success_criteria(doc) == 4


# ---------------------------------------------------------------------------
# extract_sc_identifiers
# ---------------------------------------------------------------------------

class TestExtractScIdentifiers:
    """Tests for extract_sc_identifiers."""

    def test_empty_document_returns_empty_set(
        self, validate_module: types.ModuleType
    ) -> None:
        """An empty document yields an empty identifier set."""
        assert validate_module.extract_sc_identifiers({}) == set()

    def test_extracts_single_identifier(
        self, validate_module: types.ModuleType
    ) -> None:
        """A single SC identifier is extracted correctly."""
        doc = _wcag_doc_with_sc([{"identifier": "1.1.1", "name": "Non-text Content"}])
        assert validate_module.extract_sc_identifiers(doc) == {"1.1.1"}

    def test_extracts_multiple_identifiers(
        self, validate_module: types.ModuleType
    ) -> None:
        """Multiple SC identifiers are all extracted."""
        sc_list = [{"identifier": f"1.1.{i}"} for i in range(1, 4)]
        doc = _wcag_doc_with_sc(sc_list)
        assert validate_module.extract_sc_identifiers(doc) == {
            "1.1.1", "1.1.2", "1.1.3"
        }

    def test_sc_without_identifier_key_is_ignored(
        self, validate_module: types.ModuleType
    ) -> None:
        """A success criterion missing the 'identifier' key is silently skipped."""
        doc = _wcag_doc_with_sc([{"name": "No ID here"}])
        assert validate_module.extract_sc_identifiers(doc) == set()

    def test_deduplicate_identifiers(self, validate_module: types.ModuleType) -> None:
        """Duplicate identifiers across guidelines appear only once in the set."""
        doc = {
            "principles": [
                {
                    "guidelines": [
                        {"successCriteria": [{"identifier": "1.1.1"}]},
                        {"successCriteria": [{"identifier": "1.1.1"}]},
                    ]
                }
            ]
        }
        assert validate_module.extract_sc_identifiers(doc) == {"1.1.1"}


# ---------------------------------------------------------------------------
# validate_wcag_completeness
# ---------------------------------------------------------------------------

class TestValidateWcagCompleteness:
    """Tests for validate_wcag_completeness."""

    def test_no_errors_when_count_matches(
        self, validate_module: types.ModuleType
    ) -> None:
        """No errors when actual SC count equals metadata value."""
        sc_list = [{"identifier": "1.1.1"}, {"identifier": "4.1.3"}]
        doc = _wcag_doc_with_sc(sc_list)
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.2.jsonld")
        assert errors == []

    def test_error_on_count_mismatch(self, validate_module: types.ModuleType) -> None:
        """Reports an error when actual count differs from metadata."""
        sc_list = [{"identifier": "1.1.1"}, {"identifier": "4.1.3"}]
        doc = _wcag_doc_with_sc(sc_list)
        doc["metadata"]["totalSuccessCriteria"] = 99
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.2.jsonld")
        assert any("count mismatch" in e for e in errors)

    def test_missing_413_in_wcag_22(self, validate_module: types.ModuleType) -> None:
        """Reports an error when 4.1.3 is absent from a WCAG 2.2 document."""
        doc = _wcag_doc_with_sc([{"identifier": "1.1.1"}])
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.2.jsonld")
        assert any("4.1.3" in e for e in errors)

    def test_missing_413_in_wcag_21(self, validate_module: types.ModuleType) -> None:
        """Reports an error when 4.1.3 is absent from a WCAG 2.1 document."""
        doc = _wcag_doc_with_sc([{"identifier": "1.1.1"}])
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.1.jsonld")
        assert any("4.1.3" in e for e in errors)

    def test_no_413_check_for_wcag_20(self, validate_module: types.ModuleType) -> None:
        """4.1.3 check is skipped for files not named wcag-2.1 or wcag-2.2."""
        doc = _wcag_doc_with_sc([{"identifier": "1.1.1"}])
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.0.jsonld")
        # Count mismatch would fire, but not the 4.1.3 check
        assert not any("4.1.3" in e for e in errors)

    def test_duplicate_identifiers_reported(
        self, validate_module: types.ModuleType
    ) -> None:
        """Reports error when the same identifier appears twice."""
        doc = {
            "principles": [
                {
                    "guidelines": [
                        {
                            "successCriteria": [
                                {"identifier": "1.1.1"},
                                {"identifier": "1.1.1"},
                                {"identifier": "4.1.3"},
                            ]
                        }
                    ]
                }
            ],
            "metadata": {"totalSuccessCriteria": 3},
        }
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.2.jsonld")
        assert any("Duplicate" in e or "duplicate" in e for e in errors)

    def test_no_metadata_key_skips_count_check(
        self, validate_module: types.ModuleType
    ) -> None:
        """When 'metadata' is absent, the count check is simply skipped."""
        doc = {
            "principles": [
                {
                    "guidelines": [
                        {"successCriteria": [{"identifier": "4.1.3"}]}
                    ]
                }
            ]
        }
        errors = validate_module.validate_wcag_completeness(doc, "wcag-2.2.jsonld")
        # Only count-mismatch check is skipped; 4.1.3 is present so no other error
        assert errors == []


# ---------------------------------------------------------------------------
# validate_json_ld
# ---------------------------------------------------------------------------

class TestValidateJsonLd:
    """Tests for validate_json_ld."""

    def test_valid_document_returns_true(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A fully valid document passes validation."""
        fp = tmp_path / "valid.jsonld"
        fp.write_text(json.dumps(_minimal_valid_doc()))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is True
        assert errors == []

    def test_invalid_json_returns_false(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A file with invalid JSON is reported as invalid."""
        fp = tmp_path / "bad.jsonld"
        fp.write_text("{not valid json")
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("Invalid JSON" in e for e in errors)

    def test_missing_context_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without @context is invalid."""
        doc = _minimal_valid_doc()
        del doc["@context"]
        fp = tmp_path / "no_context.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("@context" in e for e in errors)

    def test_missing_id_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without @id is invalid."""
        doc = _minimal_valid_doc()
        del doc["@id"]
        fp = tmp_path / "no_id.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("@id" in e for e in errors)

    def test_missing_type_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without @type is invalid."""
        doc = _minimal_valid_doc()
        del doc["@type"]
        fp = tmp_path / "no_type.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("@type" in e for e in errors)

    def test_missing_identifier_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without 'identifier' is invalid."""
        doc = _minimal_valid_doc()
        del doc["identifier"]
        fp = tmp_path / "no_identifier.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("identifier" in e for e in errors)

    def test_missing_title_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without 'title' is invalid."""
        doc = _minimal_valid_doc()
        del doc["title"]
        fp = tmp_path / "no_title.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("title" in e for e in errors)

    def test_missing_description_reported(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A document without 'description' is invalid."""
        doc = _minimal_valid_doc()
        del doc["description"]
        fp = tmp_path / "no_description.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("description" in e for e in errors)

    def test_context_definition_file_skipped(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """context.jsonld files that only define @context are accepted."""
        fp = tmp_path / "context.jsonld"
        fp.write_text(json.dumps({
            "@context": {"xsd": "http://www.w3.org/2001/XMLSchema#"}
        }))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is True
        assert errors == []

    def test_wcag_file_triggers_completeness_check(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """Files named 'wcag*' also run WCAG completeness checks."""
        sc_list = [{"identifier": "1.1.1"}]  # missing 4.1.3
        doc = _minimal_valid_doc()
        doc["principles"] = [{"guidelines": [{"successCriteria": sc_list}]}]
        doc["metadata"] = {"totalSuccessCriteria": 1}
        fp = tmp_path / "wcag-2.2.jsonld"
        fp.write_text(json.dumps(doc))
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert any("4.1.3" in e for e in errors)

    def test_unreadable_file_returns_false(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """A non-existent file path returns an error gracefully."""
        fp = tmp_path / "nonexistent.jsonld"
        valid, errors = validate_module.validate_json_ld(fp)
        assert valid is False
        assert errors


# ---------------------------------------------------------------------------
# validate_all_jsonld_files
# ---------------------------------------------------------------------------

class TestValidateAllJsonldFiles:
    """Tests for validate_all_jsonld_files."""

    def test_no_files_returns_false(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """Returns False when no JSON-LD files are found."""
        result = validate_module.validate_all_jsonld_files(tmp_path)
        assert result is False

    def test_all_valid_files_returns_true(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """Returns True when every JSON-LD file is valid."""
        for i in range(3):
            doc = _minimal_valid_doc()
            doc["@id"] = f"https://example.org/doc{i}"
            doc["identifier"] = f"TEST-{i}"
            (tmp_path / f"doc{i}.jsonld").write_text(json.dumps(doc))
        result = validate_module.validate_all_jsonld_files(tmp_path)
        assert result is True

    def test_one_invalid_file_returns_false(
        self, tmp_path: Path, validate_module: types.ModuleType
    ) -> None:
        """Returns False when at least one file is invalid."""
        # Valid file
        (tmp_path / "valid.jsonld").write_text(json.dumps(_minimal_valid_doc()))
        # Invalid file (missing @context)
        bad = _minimal_valid_doc()
        del bad["@context"]
        (tmp_path / "invalid.jsonld").write_text(json.dumps(bad))
        result = validate_module.validate_all_jsonld_files(tmp_path)
        assert result is False

    def test_wcag_file_sc_count_printed(
        self,
        tmp_path: Path,
        validate_module: types.ModuleType,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Success criteria count is printed for valid WCAG files."""
        sc_list = [{"identifier": "1.1.1"}, {"identifier": "4.1.3"}]
        doc = _minimal_valid_doc()
        doc["principles"] = [{"guidelines": [{"successCriteria": sc_list}]}]
        doc["metadata"] = {"totalSuccessCriteria": 2}
        (tmp_path / "wcag-2.2.jsonld").write_text(json.dumps(doc))
        validate_module.validate_all_jsonld_files(tmp_path)
        captured = capsys.readouterr()
        assert "2 success criteria" in captured.out
