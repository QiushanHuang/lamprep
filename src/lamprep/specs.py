from __future__ import annotations

import copy
from dataclasses import dataclass, field
import json
from typing import Any


@dataclass(eq=True)
class ForceFieldSpec:
    style: str
    coefficients: list[str]


@dataclass(eq=True)
class RunStage:
    stage_type: str
    steps: int
    timestep: float
    temperature_start: float | None = None
    temperature_stop: float | None = None
    pressure_start: float | None = None
    pressure_stop: float | None = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(eq=True)
class OutputSpec:
    thermo_every: int
    dump_every: int | None = None
    dump_fields: list[str] = field(default_factory=list)


@dataclass(eq=True)
class SimulationSpec:
    lammps_version: str
    workflow_type: str
    system_definition_mode: str
    units: str
    dimension: int
    boundary: str
    atom_style: str
    force_field: ForceFieldSpec
    run_stages: list[RunStage]
    outputs: OutputSpec
    structure_reference: str | None = None
    create_box: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lammps_version": self.lammps_version,
            "workflow_type": self.workflow_type,
            "system_definition_mode": self.system_definition_mode,
            "units": self.units,
            "dimension": self.dimension,
            "boundary": self.boundary,
            "atom_style": self.atom_style,
            "structure_reference": self.structure_reference,
            "create_box": dict(self.create_box),
            "force_field": {
                "style": self.force_field.style,
                "coefficients": list(self.force_field.coefficients),
            },
            "run_stages": [
                {
                    "stage_type": stage.stage_type,
                    "steps": stage.steps,
                    "timestep": stage.timestep,
                    "temperature_start": stage.temperature_start,
                    "temperature_stop": stage.temperature_stop,
                    "pressure_start": stage.pressure_start,
                    "pressure_stop": stage.pressure_stop,
                    "extras": dict(stage.extras),
                }
                for stage in self.run_stages
            ],
            "outputs": {
                "thermo_every": self.outputs.thermo_every,
                "dump_every": self.outputs.dump_every,
                "dump_fields": list(self.outputs.dump_fields),
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SimulationSpec":
        force_field = payload["force_field"]
        return cls(
            lammps_version=payload["lammps_version"],
            workflow_type=payload["workflow_type"],
            system_definition_mode=payload["system_definition_mode"],
            units=payload["units"],
            dimension=payload["dimension"],
            boundary=payload["boundary"],
            atom_style=payload["atom_style"],
            structure_reference=payload.get("structure_reference"),
            create_box=dict(payload.get("create_box", {})),
            force_field=ForceFieldSpec(
                style=force_field["style"],
                coefficients=list(force_field["coefficients"]),
            ),
            run_stages=[
                RunStage(
                    stage_type=stage["stage_type"],
                    steps=stage["steps"],
                    timestep=stage["timestep"],
                    temperature_start=stage.get("temperature_start"),
                    temperature_stop=stage.get("temperature_stop"),
                    pressure_start=stage.get("pressure_start"),
                    pressure_stop=stage.get("pressure_stop"),
                    extras=copy.deepcopy(stage.get("extras", {})),
                )
                for stage in payload["run_stages"]
            ],
            outputs=OutputSpec(
                thermo_every=payload["outputs"]["thermo_every"],
                dump_every=payload["outputs"].get("dump_every"),
                dump_fields=list(payload["outputs"].get("dump_fields", [])),
            ),
        )

    @classmethod
    def from_json(cls, payload: str) -> "SimulationSpec":
        return cls.from_dict(json.loads(payload))
