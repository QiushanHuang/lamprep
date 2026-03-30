# LAMMPS Setup Generator Design

Date: 2026-03-30

## Summary

This document specifies a Python library plus CLI for fast, validated generation of LAMMPS input scripts. The first implementation cycle covers a vertical slice composed of:

- a canonical internal simulation spec
- a natural-language front end with interactive clarification
- a versioned, manual-backed validator
- an idiomatic LAMMPS script renderer
- an atomic/materials workflow pack
- an optional runtime smoke check against an installed `lmp` binary

The design is pinned to official LAMMPS documentation releases and must not emit script lines that fall outside the modeled command registry for the selected LAMMPS version.

## Goals

- Generate `in.*` LAMMPS input scripts quickly from structured requests or natural-language prompts.
- Keep correctness anchored in the official LAMMPS manual rather than in free-form prompt generation.
- Support multiple pinned LAMMPS versions through separate validated registries.
- Ask targeted clarification questions when the prompt omits required information.
- Provide both a library API and a CLI surface.
- Cover a constrained `v1` workflow set for atomic and materials-focused simulations.

## Non-Goals

- Generating `data.*` files in `v1`
- Creating full run directories or scheduler job files in `v1`
- Supporting bonded molecular force fields in `v1`
- Emitting arbitrary raw LAMMPS commands outside the supported registry
- Treating an LLM output as authoritative without validator approval

## Scope

### In Scope for `v1`

- Input script generation only
- Hybrid natural-language handling:
  - rule-based extraction for common patterns
  - optional LLM assistance for richer prompts
- Interactive clarification for missing required fields
- Manual-backed validation for a curated command subset
- Atomic and materials-focused workflows, including:
  - energy minimization
  - NVE, NVT, and NPT runs
  - heating and cooling schedules
  - tensile or box-deformation workflows
- System definition by either:
  - referencing an existing structure or data file
  - creating simple atomic systems directly in the input script for supported cases
- Optional script smoke testing with an installed LAMMPS executable

### Out of Scope for `v1`

- Bond, angle, dihedral, improper, and other bonded molecular features
- Broad coverage of all LAMMPS commands
- Automatic extraction of every supported command directly from docs at runtime
- Full workflow automation beyond validated input-script generation

## Source of Truth

Correctness is derived from a version-pinned command registry built from official LAMMPS manual pages and then reviewed into maintained Python schemas. The runtime LAMMPS binary is an optional secondary check, not the primary source of truth.

The initial design aligns with the current official documentation release metadata visible on the LAMMPS docs site, which reports release docs with git info `11Feb2026`.

## User Experience

### Library-First Model

The core package exposes typed APIs for:

- prompt-to-draft-spec conversion
- clarification planning
- spec validation against a selected LAMMPS version
- input-script rendering
- optional runtime smoke validation

The CLI is a thin layer over the same library behavior. It must not contain separate validation logic.

### Primary CLI Flows

- `lamprep generate`
  - accepts natural language or structured input
  - drives the clarification loop
  - validates the resulting spec
  - writes `in.*` output
- `lamprep validate`
  - validates a structured spec against a selected LAMMPS version
- `lamprep render`
  - renders an already validated spec to script text
- `lamprep check`
  - runs optional `lmp -in ...` smoke validation when LAMMPS is installed

The package name and console entry point for `v1` are `lamprep`.

## Supported `v1` Workflow Pack

The first workflow pack is intentionally narrow and fully testable.

### Common Atomic and Materials Workflows

- `minimize`
- `equilibrate_nve`
- `equilibrate_nvt`
- `equilibrate_npt`
- `heat`
- `cool`
- `deform_tensile`

### Expected Command Surface

The registry for `v1` should model a curated subset of commands typically required by those workflows, including categories such as:

- initialization and setup
  - `units`
  - `dimension`
  - `boundary`
  - `atom_style`
- system definition
  - `read_data`
  - supported `lattice` and `create_*` paths for simple atomic setups
- force-field and neighbor settings
  - `pair_style lj/cut` for simple atomic Lennard-Jones workflows
  - EAM-family metallic models for the materials workflows in `v1`
  - matching `pair_coeff` handling for the supported pair-style families
  - neighbor and communication settings only when needed by supported recipes
- run configuration
  - `velocity`
  - `timestep`
  - `fix nve`
  - `fix nvt`
  - `fix npt`
  - `fix deform`
  - `minimize`
  - `run`
- observability
  - `thermo`
  - `thermo_style`
  - `dump`

The exact modeled subset is part of the registry contract and must be explicit per supported LAMMPS version.

## Architecture

The design uses a spec-first compiler architecture:

1. natural-language interpretation
2. clarification loop
3. canonical `SimulationSpec`
4. versioned validation
5. rendering
6. optional runtime smoke check

The renderer never consumes raw prompts. It only renders a validated `SimulationSpec`.

### Core Modules

- `manual_registry`
  - stores versioned command schemas and citations
  - separates LAMMPS releases cleanly
- `spec_models`
  - defines typed internal models for the canonical simulation spec
- `nl_frontend`
  - converts prompts into draft specs and unresolved questions
- `clarification`
  - determines which missing fields must be requested next
- `validator`
  - checks the canonical spec against a chosen version registry
- `renderer`
  - emits stable, idiomatic LAMMPS input scripts
- `recipes.atomic_materials`
  - encodes supported workflow families and their required fields
- `runtime_check`
  - optionally runs `lmp -in` smoke tests
- `cli`
  - exposes the library behavior without duplicating domain logic

## Canonical Internal Model

The central invariant is that every renderable request becomes one canonical `SimulationSpec`. That model should be stable across front ends and mostly stable across LAMMPS versions.

### Required High-Level Fields

- `lammps_version`
- `workflow_type`
- `system_definition_mode`
- `units`
- `dimension`
- `boundary`
- `atom_style`
- `force_field`
- `run_stages`
- `outputs`

### Likely Nested Structures

- `SystemDefinition`
  - `read_data`
  - `create_atoms_simple`
- `ForceFieldSpec`
  - supported atomic or materials pair styles
  - corresponding coefficient information
- `EnsembleStage`
  - stage type such as minimize, nve, nvt, npt, heat, cool, deform
  - target temperatures and pressures as applicable
  - timestep
  - number of steps
- `OutputSpec`
  - thermo cadence and content
  - dump cadence and format

The spec should represent intent, not raw LAMMPS source lines.

## Natural-Language Front End

The NL layer is a convenience interface, not a correctness boundary.

### Behavior

- classify the prompt into a supported workflow family
- extract directly stated entities
- identify missing required fields
- produce one targeted clarification question at a time
- refuse unsupported requests cleanly

### Hybrid Strategy

- Rule-based extraction handles known phrasing for common workflows.
- Optional LLM assistance expands prompt understanding when the request uses richer language.
- All extracted values, whether rule-based or LLM-assisted, are normalized into the same draft spec format.
- The validator treats LLM-derived fields exactly the same as rule-derived fields.

### Clarification Policy

When a request is missing required fields, the system asks the smallest next question needed to reach a valid spec. It should not guess on materially significant settings such as:

- LAMMPS version
- structure source
- pair style family
- temperature and pressure targets
- timestep
- run length
- deformation axis or strain rate

Project-defined safe defaults may be used only for values intentionally designated as optional in the recipe catalog, and those defaults must be surfaced to the user before rendering.

## Versioned Manual Registry

The registry is the backbone of compliance.

### Registry Inputs

- official LAMMPS manual pages for the supported command subset
- semi-automated extraction of command signatures and structured options
- manual review and cleanup into maintained Python schemas

### Registry Responsibilities

- record which commands are supported for each LAMMPS version
- record allowed option combinations for the supported subset
- capture workflow-specific compatibility rules
- keep command citations and doc references available for diagnostics

### Multi-Version Strategy

- each LAMMPS release supported by the tool gets its own registry package or data bundle
- validation selects the registry strictly from `SimulationSpec.lammps_version`
- the same high-level spec may validate under one version and fail under another

This design favors explicit compatibility over silent cross-version guessing.

## Validation

Validation happens after clarification and before rendering.

### Validation Rules

- reject any workflow outside the supported `v1` catalog
- reject unsupported command or option combinations for the chosen version
- reject incomplete specs
- reject cross-field contradictions
- reject unsupported force-field and workflow pairings

### Examples of Validation Failures

- a deformation workflow without a defined axis or deformation rate
- an NPT request missing the required pressure target
- a materials workflow requesting a pair style not modeled for the selected version
- a bonded molecular request in `v1`

Validation errors should be specific, actionable, and tied to the failing spec field or compatibility rule.

## Rendering

Rendering converts a validated spec into idiomatic LAMMPS input text.

### Rendering Rules

- emit commands in a stable order that follows LAMMPS input-script structure
- preserve deterministic output for the same validated spec
- avoid rendering commands that were not explicitly approved by validation
- support concise explanatory comments when they clarify recipe behavior

### Rendering Layout

The renderer should map output into the LAMMPS structure described in the official manual:

- initialization
- atom or system definition
- simulation settings
- run commands

This keeps generated scripts recognizable to LAMMPS users and aligned with official documentation conventions.

## Optional Runtime Check

Runtime validation is optional and secondary.

### Behavior

- if an `lmp` executable is configured, `lamprep check` can run `lmp -in generated.in`
- the command is used as a smoke test, not as a substitute for registry validation
- failures should surface the original LAMMPS message plus the corresponding spec context when that mapping is available

The tool must still be fully useful without a locally installed LAMMPS binary.

## Error Handling

The system should fail at the spec boundary instead of emitting questionable scripts.

- ambiguous prompt
  - ask one clarification question for the most blocking missing field
- unsupported intent
  - reject immediately with a clear scope message
- version mismatch
  - report the selected version and the incompatible rule
- validation failure
  - identify the exact field and workflow rule that failed
- runtime smoke-check failure
  - preserve original `lmp` diagnostics

No best-effort fallback should emit raw script text outside the validated command registry.

## Testing Strategy

The tool needs strong tests because the value proposition is correctness.

### Automated Tests

- unit tests for spec model construction and normalization
- clarification tests for missing-field sequencing
- registry tests for each supported LAMMPS version
- validator tests for accepted and rejected combinations
- renderer golden tests for representative workflows
- NL frontend tests based on prompt-to-draft-spec behavior
- integration tests for optional `lmp -in` smoke checks when a binary is available

### Regression Corpus

Maintain a prompt and spec corpus that covers:

- minimize
- NVE
- NVT
- NPT
- heating
- cooling
- tensile deformation
- simple Lennard-Jones atomic systems
- materials-style atomic systems using supported metallic pair styles

## Implementation Constraints

- Python is the implementation language.
- The package should be library-first, with the CLI as a thin wrapper.
- The first implementation cycle is limited to the atomic and materials vertical slice.
- Bonded molecular support is deferred to a later spec and implementation cycle.

## Acceptance Criteria for the First Spec

The design is successful if the first implementation cycle can:

- accept a natural-language request for a supported atomic or materials workflow
- ask for missing required fields interactively
- build a canonical `SimulationSpec`
- validate that spec against a selected LAMMPS version
- render a deterministic `in.*` script
- optionally run an `lmp -in` smoke test
- refuse unsupported bonded molecular requests cleanly

## References

- LAMMPS documentation index, release docs with git info `11Feb2026`: <https://docs.lammps.org/genindex.html>
- LAMMPS command overview: <https://docs.lammps.org/Commands.html>
- LAMMPS input script structure: <https://docs.lammps.org/Commands_structure.html>
- `read_data` command: <https://docs.lammps.org/read_data.html>
- `minimize` command: <https://docs.lammps.org/minimize.html>
- `fix nvt` and `fix npt` via `fix nh`: <https://docs.lammps.org/fix_nh.html>
- `fix deform` command: <https://docs.lammps.org/fix_deform.html>
- `pair_style eam` command: <https://docs.lammps.org/pair_eam.html>
