from __future__ import annotations

from lamprep.manual_registry.base import ManualRegistry
from lamprep.manual_registry.v11Feb2026 import REGISTRY as REGISTRY_11FEB2026
from lamprep.manual_registry.v29Aug2024 import REGISTRY as REGISTRY_29AUG2024

__all__ = [
    "ManualRegistry",
    "REGISTRIES",
    "get_supported_versions",
    "get_registry",
]

REGISTRIES: dict[str, ManualRegistry] = {
    "29Aug2024": REGISTRY_29AUG2024,
    "11Feb2026": REGISTRY_11FEB2026,
}


def get_supported_versions() -> list[str]:
    return list(REGISTRIES)


def get_registry(version: str) -> ManualRegistry:
    try:
        return REGISTRIES[version]
    except KeyError as exc:
        raise ValueError(f"Unsupported LAMMPS version: {version}") from exc
