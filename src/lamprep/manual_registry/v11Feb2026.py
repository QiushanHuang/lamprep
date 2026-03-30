from __future__ import annotations

from lamprep.manual_registry.base import ManualRegistry


REGISTRY = ManualRegistry(
    version="11Feb2026",
    allowed_commands=(
        "units",
        "dimension",
        "boundary",
        "atom_style",
        "read_data",
        "lattice",
        "create_box",
        "create_atoms",
        "pair_style",
        "pair_coeff",
        "velocity",
        "timestep",
        "fix nve",
        "fix nvt",
        "fix npt",
        "fix deform",
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
        "deform_tensile": ("force_field", "deformation_axis", "strain_rate", "timestep", "run_length"),
    },
    citations={
        "Commands_structure": "https://docs.lammps.org/Commands_structure.html",
        "minimize": "https://docs.lammps.org/minimize.html",
        "fix_nh": "https://docs.lammps.org/fix_nh.html",
        "fix_deform": "https://docs.lammps.org/fix_deform.html",
        "pair_eam": "https://docs.lammps.org/pair_eam.html",
    },
)
