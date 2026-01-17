"""
JSON input/output for worm gear parameters.

Loads design parameters from wormgearcalc (Tool 1) JSON output.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


@dataclass
class WormParams:
    """Worm parameters from calculator."""
    module_mm: float
    num_starts: int
    pitch_diameter_mm: float
    tip_diameter_mm: float
    root_diameter_mm: float
    lead_mm: float
    lead_angle_deg: float
    addendum_mm: float
    dedendum_mm: float
    thread_thickness_mm: float
    hand: str  # "RIGHT" or "LEFT"
    profile_shift: float = 0.0


@dataclass
class WheelParams:
    """Wheel parameters from calculator."""
    module_mm: float
    num_teeth: int
    pitch_diameter_mm: float
    tip_diameter_mm: float
    root_diameter_mm: float
    throat_diameter_mm: float
    helix_angle_deg: float
    addendum_mm: float
    dedendum_mm: float
    profile_shift: float = 0.0


@dataclass
class AssemblyParams:
    """Assembly parameters from calculator."""
    centre_distance_mm: float
    pressure_angle_deg: float
    backlash_mm: float
    hand: str
    ratio: int
    efficiency_percent: Optional[float] = None
    self_locking: Optional[bool] = None


@dataclass
class WormGearDesign:
    """Complete worm gear design from calculator."""
    worm: WormParams
    wheel: WheelParams
    assembly: AssemblyParams


def load_design_json(filepath: Union[str, Path]) -> WormGearDesign:
    """
    Load worm gear design from calculator JSON export.

    Args:
        filepath: Path to JSON file from wormgearcalc

    Returns:
        WormGearDesign with all parameters

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or missing required fields
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Design file not found: {filepath}")

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Check for 'design' wrapper (some exports have this)
    if 'design' in data:
        data = data['design']

    # Validate required sections
    if 'worm' not in data or 'wheel' not in data or 'assembly' not in data:
        raise ValueError(
            "Invalid design JSON - must contain 'worm', 'wheel', and 'assembly' sections"
        )

    # Parse worm parameters
    worm_data = data['worm']
    worm = WormParams(
        module_mm=worm_data['module_mm'],
        num_starts=worm_data['num_starts'],
        pitch_diameter_mm=worm_data['pitch_diameter_mm'],
        tip_diameter_mm=worm_data['tip_diameter_mm'],
        root_diameter_mm=worm_data['root_diameter_mm'],
        lead_mm=worm_data['lead_mm'],
        lead_angle_deg=worm_data['lead_angle_deg'],
        addendum_mm=worm_data['addendum_mm'],
        dedendum_mm=worm_data['dedendum_mm'],
        thread_thickness_mm=worm_data['thread_thickness_mm'],
        hand=worm_data['hand'],
        profile_shift=worm_data.get('profile_shift', 0.0)
    )

    # Parse wheel parameters
    wheel_data = data['wheel']
    wheel = WheelParams(
        module_mm=wheel_data['module_mm'],
        num_teeth=wheel_data['num_teeth'],
        pitch_diameter_mm=wheel_data['pitch_diameter_mm'],
        tip_diameter_mm=wheel_data['tip_diameter_mm'],
        root_diameter_mm=wheel_data['root_diameter_mm'],
        throat_diameter_mm=wheel_data['throat_diameter_mm'],
        helix_angle_deg=wheel_data['helix_angle_deg'],
        addendum_mm=wheel_data['addendum_mm'],
        dedendum_mm=wheel_data['dedendum_mm'],
        profile_shift=wheel_data.get('profile_shift', 0.0)
    )

    # Parse assembly parameters
    asm_data = data['assembly']
    assembly = AssemblyParams(
        centre_distance_mm=asm_data['centre_distance_mm'],
        pressure_angle_deg=asm_data['pressure_angle_deg'],
        backlash_mm=asm_data['backlash_mm'],
        hand=asm_data['hand'],
        ratio=asm_data['ratio'],
        efficiency_percent=asm_data.get('efficiency_percent'),
        self_locking=asm_data.get('self_locking')
    )

    return WormGearDesign(worm=worm, wheel=wheel, assembly=assembly)
