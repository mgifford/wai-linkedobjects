"""Tests for scripts/generate-wcag.py.

Covers:
- slug_from_name
- build_sc_object
- generate_wcag_22
- save_json_ld
"""

import json
import types
from pathlib import Path


# ---------------------------------------------------------------------------
# slug_from_name
# ---------------------------------------------------------------------------

class TestSlugFromName:
    """Tests for slug_from_name."""

    def test_simple_name(self, generate_wcag_module: types.ModuleType) -> None:
        """Lowercase words joined by hyphens."""
        result = generate_wcag_module.slug_from_name("Non-text Content")
        assert result == "non-text-content"

    def test_removes_parentheses(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Parentheses are stripped from the slug."""
        result = generate_wcag_module.slug_from_name("Captions (Prerecorded)")
        assert "(" not in result
        assert ")" not in result

    def test_removes_commas(self, generate_wcag_module: types.ModuleType) -> None:
        """Commas are stripped from the slug."""
        result = generate_wcag_module.slug_from_name(
            "Error Prevention (Legal, Financial, Data)"
        )
        assert "," not in result

    def test_spaces_become_hyphens(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Spaces are replaced with hyphens."""
        result = generate_wcag_module.slug_from_name("Focus Visible")
        assert result == "focus-visible"

    def test_all_lowercase(self, generate_wcag_module: types.ModuleType) -> None:
        """Output is fully lowercase."""
        result = generate_wcag_module.slug_from_name("Audio Control")
        assert result == result.lower()

    def test_known_slug_non_text_content(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Verify a known WCAG slug produced correctly."""
        result = generate_wcag_module.slug_from_name("Non-text Content")
        assert result == "non-text-content"

    def test_dash_in_name_preserved(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """A hyphen already in the name is kept."""
        result = generate_wcag_module.slug_from_name("Audio-only (Live)")
        assert "audio-only" in result


# ---------------------------------------------------------------------------
# build_sc_object
# ---------------------------------------------------------------------------

class TestBuildScObject:
    """Tests for build_sc_object."""

    _SC_111 = {"id": "1.1.1", "name": "Non-text Content", "level": "A",
               "guideline": "1.1"}

    def test_returns_dict(self, generate_wcag_module: types.ModuleType) -> None:
        """build_sc_object always returns a dict."""
        obj = generate_wcag_module.build_sc_object(self._SC_111)
        assert isinstance(obj, dict)

    def test_identifier_field(self, generate_wcag_module: types.ModuleType) -> None:
        """The 'identifier' field matches the sc id."""
        sc = {"id": "1.4.3", "name": "Contrast (Minimum)", "level": "AA",
              "guideline": "1.4"}
        obj = generate_wcag_module.build_sc_object(sc)
        assert obj["identifier"] == "1.4.3"

    def test_name_field(self, generate_wcag_module: types.ModuleType) -> None:
        """The 'name' field matches the sc name."""
        sc = {"id": "2.1.1", "name": "Keyboard", "level": "A", "guideline": "2.1"}
        obj = generate_wcag_module.build_sc_object(sc)
        assert obj["name"] == "Keyboard"

    def test_level_field(self, generate_wcag_module: types.ModuleType) -> None:
        """The 'level' field is preserved."""
        sc = {"id": "4.1.3", "name": "Status Messages", "level": "AA",
              "guideline": "4.1"}
        obj = generate_wcag_module.build_sc_object(sc)
        assert obj["level"] == "AA"

    def test_at_type_is_success_criterion(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """@type is 'SuccessCriterion'."""
        obj = generate_wcag_module.build_sc_object(self._SC_111)
        assert obj["@type"] == "SuccessCriterion"

    def test_at_id_contains_slug(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """@id URL contains the name slug."""
        obj = generate_wcag_module.build_sc_object(self._SC_111)
        assert "non-text-content" in obj["@id"]

    def test_understanding_url_present(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """An 'understanding' URL is included."""
        obj = generate_wcag_module.build_sc_object(self._SC_111)
        assert "understanding" in obj
        assert obj["understanding"].startswith("https://")

    def test_version_22_urls(self, generate_wcag_module: types.ModuleType) -> None:
        """Default version produces WCAG22 URLs."""
        obj = generate_wcag_module.build_sc_object(self._SC_111, version="2.2")
        assert "WCAG22" in obj["@id"]
        assert "WCAG22" in obj["understanding"]

    def test_version_21_urls(self, generate_wcag_module: types.ModuleType) -> None:
        """Passing version='2.1' produces WCAG21 URLs."""
        obj = generate_wcag_module.build_sc_object(self._SC_111, version="2.1")
        assert "WCAG21" in obj["@id"]
        assert "WCAG21" in obj["understanding"]

# ---------------------------------------------------------------------------
# generate_wcag_22
# ---------------------------------------------------------------------------


class TestGenerateWcag22:
    """Tests for generate_wcag_22."""

    def test_returns_dict(self, generate_wcag_module: types.ModuleType) -> None:
        """generate_wcag_22 returns a dict."""
        doc = generate_wcag_module.generate_wcag_22()
        assert isinstance(doc, dict)

    def test_required_jsonld_fields_present(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """@context, @id, and @type are all present."""
        doc = generate_wcag_module.generate_wcag_22()
        assert "@context" in doc
        assert "@id" in doc
        assert "@type" in doc

    def test_at_type_is_standard(self, generate_wcag_module: types.ModuleType) -> None:
        """@type is 'Standard'."""
        doc = generate_wcag_module.generate_wcag_22()
        assert doc["@type"] == "Standard"

    def test_identifier_is_wcag_22(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Identifier field is 'WCAG 2.2'."""
        doc = generate_wcag_module.generate_wcag_22()
        assert doc["identifier"] == "WCAG 2.2"

    def test_four_principles(self, generate_wcag_module: types.ModuleType) -> None:
        """WCAG 2.2 has exactly 4 principles."""
        doc = generate_wcag_module.generate_wcag_22()
        assert len(doc["principles"]) == 4

    def test_total_success_criteria_count(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Total success criteria count equals the reference list length."""
        doc = generate_wcag_module.generate_wcag_22()
        expected = len(generate_wcag_module.WCAG_22_SUCCESS_CRITERIA)
        assert doc["metadata"]["totalSuccessCriteria"] == expected

    def test_413_status_messages_present(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """4.1.3 Status Messages is present in the generated document."""
        doc = generate_wcag_module.generate_wcag_22()
        all_ids: set[str] = set()
        for principle in doc["principles"]:
            for guideline in principle["guidelines"]:
                for sc in guideline["successCriteria"]:
                    all_ids.add(sc["identifier"])
        assert "4.1.3" in all_ids

    def test_no_duplicate_identifiers(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """All success criteria have unique identifiers."""
        doc = generate_wcag_module.generate_wcag_22()
        all_ids: list[str] = []
        for principle in doc["principles"]:
            for guideline in principle["guidelines"]:
                for sc in guideline["successCriteria"]:
                    all_ids.append(sc["identifier"])
        assert len(all_ids) == len(set(all_ids))

    def test_metadata_new_in_version(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """metadata.newInVersion lists WCAG 2.2-specific criteria."""
        doc = generate_wcag_module.generate_wcag_22()
        new_in_22 = doc["metadata"]["newInVersion"]
        assert "2.5.7" in new_in_22
        assert "3.3.7" in new_in_22
        assert "3.3.8" in new_in_22

    def test_principles_are_sorted(
        self, generate_wcag_module: types.ModuleType
    ) -> None:
        """Principles are in order: 1, 2, 3, 4."""
        doc = generate_wcag_module.generate_wcag_22()
        ids = [p["identifier"] for p in doc["principles"]]
        assert ids == sorted(ids)


# ---------------------------------------------------------------------------
# save_json_ld
# ---------------------------------------------------------------------------

class TestSaveJsonLd:
    """Tests for save_json_ld."""

    def test_creates_file(
        self, tmp_path: Path, generate_wcag_module: types.ModuleType
    ) -> None:
        """save_json_ld creates the output file."""
        output = tmp_path / "out.jsonld"
        generate_wcag_module.save_json_ld({"key": "value"}, output)
        assert output.exists()

    def test_file_contains_valid_json(
        self, tmp_path: Path, generate_wcag_module: types.ModuleType
    ) -> None:
        """The written file contains valid JSON."""
        output = tmp_path / "out.jsonld"
        data = {"hello": "world", "number": 42}
        generate_wcag_module.save_json_ld(data, output)
        loaded = json.loads(output.read_text())
        assert loaded == data

    def test_creates_parent_directories(
        self, tmp_path: Path, generate_wcag_module: types.ModuleType
    ) -> None:
        """Parent directories are created if they do not exist."""
        output = tmp_path / "nested" / "deep" / "out.jsonld"
        generate_wcag_module.save_json_ld({"a": 1}, output)
        assert output.exists()

    def test_custom_indent(
        self, tmp_path: Path, generate_wcag_module: types.ModuleType
    ) -> None:
        """Indent parameter controls JSON indentation."""
        output = tmp_path / "out.jsonld"
        generate_wcag_module.save_json_ld({"a": 1}, output, indent=4)
        raw = output.read_text()
        assert "    " in raw  # 4-space indent

    def test_non_ascii_preserved(
        self, tmp_path: Path, generate_wcag_module: types.ModuleType
    ) -> None:
        """Non-ASCII characters are preserved (ensure_ascii=False)."""
        output = tmp_path / "out.jsonld"
        generate_wcag_module.save_json_ld({"name": "Ünïcödé"}, output)
        raw = output.read_text(encoding="utf-8")
        assert "Ünïcödé" in raw
