# Integration Tests

This directory holds end-to-end scenarios for the `lamprep` vertical slice defined in the design spec.

## Test layers

- `test_scenarios_schema.py` validates the integration scenario manifest itself.
- `test_prompt_flows.py` is a placeholder for end-to-end prompt-to-script tests that will be enabled as implementation lands.
- `scenarios_v1.json` is the machine-readable contract for the first supported workflows.

## Human verification linkage

The human-review checklist in [human-verification-issue.md](/Users/joshua/Desktop/Qiushan_Studio/1_AI/AGENT/skill/docs/test-plans/human-verification-issue.md) mirrors these scenarios so manual and automated validation stay aligned.
