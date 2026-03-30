"""Sanity checks for integration scenario fixtures."""

from __future__ import annotations

import json
from pathlib import Path


SCENARIOS_PATH = Path(__file__).with_name("scenarios_v1.json")


def load_scenarios() -> list[dict]:
    """Load the versioned integration scenarios."""
    return json.loads(SCENARIOS_PATH.read_text())


def test_scenarios_have_unique_ids() -> None:
    scenarios = load_scenarios()
    ids = [scenario["id"] for scenario in scenarios]
    assert len(ids) == len(set(ids))


def test_supported_scenarios_define_expected_commands() -> None:
    scenarios = load_scenarios()
    supported = [scenario for scenario in scenarios if scenario["type"] == "supported"]
    assert supported
    for scenario in supported:
        assert scenario["expected_workflow"]
        assert scenario["expected_commands"]


def test_unsupported_scenarios_define_expected_error() -> None:
    scenarios = load_scenarios()
    unsupported = [scenario for scenario in scenarios if scenario["type"] == "unsupported"]
    assert unsupported
    for scenario in unsupported:
        assert scenario["expected_error"]
