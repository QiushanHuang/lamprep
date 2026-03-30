import json

from lamprep import ForceFieldSpec, OutputSpec, RunStage, SimulationSpec


def test_simulation_spec_round_trip() -> None:
    spec = SimulationSpec(
        lammps_version="11Feb2026",
        workflow_type="equilibrate_nvt",
        system_definition_mode="read_data",
        units="metal",
        dimension=3,
        boundary="p p p",
        atom_style="atomic",
        structure_reference="system.data",
        force_field=ForceFieldSpec(
            style="eam/alloy",
            coefficients=["* * Ni.eam.alloy Ni"],
        ),
        run_stages=[
            RunStage(
                stage_type="equilibrate_nvt",
                steps=1000,
                timestep=0.001,
                temperature_start=300.0,
                temperature_stop=300.0,
                extras={"temperature_damp": 0.1},
            )
        ],
        outputs=OutputSpec(
            thermo_every=100,
            dump_every=500,
            dump_fields=["id", "type", "x", "y", "z"],
        ),
    )

    payload = spec.to_dict()
    restored = SimulationSpec.from_dict(payload)

    assert restored == spec


def test_simulation_spec_json_round_trip_and_defensive_copy() -> None:
    spec = SimulationSpec(
        lammps_version="11Feb2026",
        workflow_type="equilibrate_nvt",
        system_definition_mode="read_data",
        units="metal",
        dimension=3,
        boundary="p p p",
        atom_style="atomic",
        structure_reference="system.data",
        force_field=ForceFieldSpec(
            style="eam/alloy",
            coefficients=["* * Ni.eam.alloy Ni"],
        ),
        run_stages=[
            RunStage(
                stage_type="equilibrate_nvt",
                steps=1000,
                timestep=0.001,
                temperature_start=300.0,
                temperature_stop=300.0,
                extras={"temperature_damp": 0.1},
            )
        ],
        outputs=OutputSpec(
            thermo_every=100,
            dump_every=500,
            dump_fields=["id", "type", "x", "y", "z"],
        ),
    )

    json_payload = spec.to_json()
    restored = SimulationSpec.from_json(json_payload)

    assert restored == spec
    assert json.loads(json_payload) == spec.to_dict()

    payload = spec.to_dict()
    copied = SimulationSpec.from_dict(payload)

    payload["force_field"]["coefficients"].append("new-coefficient")
    payload["run_stages"][0]["extras"]["temperature_damp"] = 0.2
    payload["outputs"]["dump_fields"].append("vx")

    assert copied.force_field.coefficients == ["* * Ni.eam.alloy Ni"]
    assert copied.run_stages[0].extras == {"temperature_damp": 0.1}
    assert copied.outputs.dump_fields == ["id", "type", "x", "y", "z"]
