# Human Verification Test Plan for `lamprep` v1

## Goal

Verify that the first implementation slice of `lamprep` behaves correctly for the approved atomic/materials scope and that the UX is safe when prompts are ambiguous or unsupported.

## Manual verification matrix

### 1. Supported prompt to script flow

- Prompt for a simple Lennard-Jones minimization workflow.
- Confirm the tool asks only for missing required inputs.
- Confirm the final script contains the expected setup, force-field, minimize, thermo, and run sections.
- Confirm the output script ordering matches the LAMMPS manual structure.

### 2. Supported materials equilibration flow

- Prompt for an EAM-based NVT equilibration.
- Confirm the tool requests missing metallic pair-coefficient details if they are absent.
- Confirm the rendered script uses only the supported `v1` command subset.

### 3. Heating and cooling flow

- Prompt for a temperature ramp workflow.
- Confirm the tool distinguishes between heating and cooling intents.
- Confirm stage ordering and target temperatures are preserved in the rendered script.

### 4. Deformation flow

- Prompt for a tensile deformation workflow.
- Confirm the tool asks for axis and rate when omitted.
- Confirm the generated script includes the expected deformation controls for the selected version.

### 5. Unsupported bonded molecular request

- Prompt for a bonded molecular setup using bond, angle, or dihedral styles.
- Confirm the tool refuses the request explicitly and does not emit an input script.

### 6. Version-specific validation

- Run the same structured spec against two supported LAMMPS versions.
- Confirm a version-specific incompatibility is surfaced with the selected version named in the error.

### 7. Optional runtime smoke check

- When a local `lmp` binary is available, run the generated script through the smoke-check command.
- Confirm failures preserve the original LAMMPS diagnostics.

## Exit criteria

- All supported prompts complete with a deterministic script.
- All unsupported prompts fail with actionable validation or scope errors.
- Human reviewers confirm the generated scripts are recognizable, ordered, and idiomatic for LAMMPS users.
