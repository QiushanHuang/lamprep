from __future__ import annotations

from lamprep.manual_registry.base import ManualRegistry


REGISTRY = ManualRegistry(
    version="29Aug2024",
    allowed_commands=(
        "units",
        "dimension",
        "boundary",
        "atom_style",
        "read_data",
        "pair_style",
        "pair_coeff",
        "velocity",
        "timestep",
        "fix nve",
        "fix nvt",
        "fix npt",
        "minimize",
        "thermo",
        "thermo_style",
        "dump",
        "run",
    ),
    allowed_pair_styles=("lj/cut", "eam", "eam/alloy"),
    supported_workflows={
        "minimize": ("force_field",),
        "equilibrate_nve": ("force_field", "timestep", "run_length"),
        "equilibrate_nvt": ("force_field", "temperature", "timestep", "run_length"),
        "equilibrate_npt": ("force_field", "temperature", "pressure", "timestep", "run_length"),
        "heat": ("force_field", "temperature_start", "temperature_stop", "timestep", "run_length"),
        "cool": ("force_field", "temperature_start", "temperature_stop", "timestep", "run_length"),
    },
    citations={
        "Commands_structure": "https://docs.lammps.org/Commands_structure.html",
    },
)
