"""
Worm Gear Calculator

A Python library for calculating worm gear dimensions.

Usage:
    from wormcalc import design_from_envelope, validate_design, to_json

    design = design_from_envelope(
        worm_od=20,
        wheel_od=65,
        ratio=30
    )
    
    validation = validate_design(design)
    print(to_json(design, validation))
"""

from .core import (
    # Dataclasses
    WormParameters,
    WheelParameters,
    WormGearDesign,
    DesignResult,
    ManufacturingParams,
    Hand,
    WormProfile,
    WormType,

    # Constants
    STANDARD_MODULES,

    # Functions
    design_from_envelope,
    design_from_wheel,
    design_from_module,
    design_from_centre_distance,
    calculate_worm,
    calculate_wheel,
    calculate_centre_distance,
    calculate_globoid_throat_radii,
    calculate_manufacturing_params,
    nearest_standard_module,
    is_standard_module,
    estimate_efficiency,
)

from .validation import (
    ValidationResult,
    ValidationMessage,
    Severity,
    validate_design,
    create_design_result,
    calculate_minimum_teeth,
    calculate_profile_shift,
)

from .output import (
    to_json,
    to_markdown,
    to_summary,
    design_to_dict,
)


__version__ = "0.1.0"
__author__ = "Paul Fremantle"

__all__ = [
    # Version
    "__version__",

    # Dataclasses
    "WormParameters",
    "WheelParameters",
    "WormGearDesign",
    "DesignResult",
    "ManufacturingParams",
    "Hand",
    "WormProfile",
    "WormType",
    "ValidationResult",
    "ValidationMessage",
    "Severity",

    # Constants
    "STANDARD_MODULES",

    # Design functions
    "design_from_envelope",
    "design_from_wheel",
    "design_from_module",
    "design_from_centre_distance",
    "calculate_worm",
    "calculate_wheel",
    "calculate_centre_distance",
    "calculate_globoid_throat_radii",
    "calculate_manufacturing_params",

    # Utility functions
    "nearest_standard_module",
    "is_standard_module",
    "estimate_efficiency",

    # Validation
    "validate_design",
    "create_design_result",
    "calculate_minimum_teeth",
    "calculate_profile_shift",

    # Output
    "to_json",
    "to_markdown",
    "to_summary",
    "design_to_dict",
]
