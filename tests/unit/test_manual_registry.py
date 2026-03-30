from __future__ import annotations

from lamprep.manual_registry import get_registry, get_supported_versions


def test_supported_versions_are_explicit_and_ordered() -> None:
    assert get_supported_versions() == ["29Aug2024", "11Feb2026"]


def test_main_registry_exposes_deformation_workflow() -> None:
    registry = get_registry("11Feb2026")
    assert "deform_tensile" in registry.supported_workflows
    assert "fix deform" in registry.allowed_commands


def test_older_registry_is_narrower() -> None:
    registry = get_registry("29Aug2024")
    assert "deform_tensile" not in registry.supported_workflows


def test_unsupported_version_raises_value_error() -> None:
    try:
        get_registry("unknown")
    except ValueError as exc:
        assert str(exc) == "Unsupported LAMMPS version: unknown"
    else:
        raise AssertionError("expected ValueError")


def test_registry_lookup_returns_isolated_mappings() -> None:
    registry = get_registry("11Feb2026")
    registry.supported_workflows["mutated"] = ("value",)
    registry.citations["new"] = "https://example.com"

    fresh_registry = get_registry("11Feb2026")

    assert "mutated" not in fresh_registry.supported_workflows
    assert "new" not in fresh_registry.citations
