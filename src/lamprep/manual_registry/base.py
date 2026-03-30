from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ManualRegistry:
    version: str
    allowed_commands: tuple[str, ...]
    allowed_pair_styles: tuple[str, ...]
    supported_workflows: dict[str, tuple[str, ...]]
    citations: dict[str, str]
