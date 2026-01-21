"""
Bore and keyway feature generation for worm gear components.

Supports:
- Center bores (through holes)
- Keyways per DIN 6885 / ISO 6885 standard
- Set screw holes for shaft retention
"""

import math
from dataclasses import dataclass
from typing import Optional, Tuple
from build123d import *


# DIN 6885 Keyway dimensions lookup table
# Format: bore_range: (key_width, key_height, shaft_depth, hub_depth)
# bore_range is (min_bore, max_bore) in mm
DIN_6885_KEYWAYS = {
    (6, 8): (2, 2, 1.2, 1.0),
    (8, 10): (3, 3, 1.8, 1.4),
    (10, 12): (4, 4, 2.5, 1.8),
    (12, 17): (5, 5, 3.0, 2.3),
    (17, 22): (6, 6, 3.5, 2.8),
    (22, 30): (8, 7, 4.0, 3.3),
    (30, 38): (10, 8, 5.0, 3.3),
    (38, 44): (12, 8, 5.0, 3.3),
    (44, 50): (14, 9, 5.5, 3.8),
    (50, 58): (16, 10, 6.0, 4.3),
    (58, 65): (18, 11, 7.0, 4.4),
    (65, 75): (20, 12, 7.5, 4.9),
    (75, 85): (22, 14, 9.0, 5.4),
    (85, 95): (25, 14, 9.0, 5.4),
}


# Set screw sizing based on bore diameter
# Format: bore_range: (screw_size_name, thread_diameter_mm)
# Common sizes: M3 (3mm), M4 (4mm), M5 (5mm), M6 (6mm)
SET_SCREW_SIZES = {
    (2, 6): ("M2.5", 2.5),    # Very small bores (below DIN 6885 range)
    (6, 10): ("M3", 3.0),     # Small bores
    (10, 20): ("M4", 4.0),    # Medium bores
    (20, 35): ("M5", 5.0),    # Large bores
    (35, 60): ("M6", 6.0),    # Very large bores
    (60, 100): ("M8", 8.0),   # Extra large bores
}


def calculate_default_bore(pitch_diameter: float, root_diameter: float) -> tuple[float, bool]:
    """
    Calculate a sensible default bore diameter based on gear dimensions.

    Uses approximately 25% of pitch diameter, but constrained by:
    - Minimum: 2mm (practical minimum for small gears)
    - Maximum: Leaves at least 25% of root diameter as rim, or 1mm minimum

    The result is rounded to nice values:
    - Below 6mm: round to nearest 0.5mm
    - 6-12mm: round to nearest 0.5mm
    - 12mm and above: round to nearest 1mm

    Note: DIN 6885 keyways only cover bores >= 6mm. For smaller bores,
    keyways will be omitted automatically.

    Args:
        pitch_diameter: Gear pitch diameter in mm
        root_diameter: Gear root diameter in mm

    Returns:
        Tuple of (bore_diameter, has_warning) where:
        - bore_diameter: Recommended bore in mm (rounded), or None if impossible
        - has_warning: True if rim is thin (< 1.5mm) - part may need care
    """
    # Target ~25% of pitch diameter
    target = pitch_diameter * 0.25

    # Minimum practical bore is 2mm
    min_bore = 2.0

    # Maximum bore: leave at least 25% of root as rim, with 1mm absolute minimum
    # (root_diameter - max_bore) / 2 >= max(root_diameter * 0.25 / 2, 1.0)
    # Simplified: max_bore = root_diameter * 0.75 - but at least leave 1mm rim each side
    min_rim = max(root_diameter * 0.125, 1.0)  # 12.5% of root, min 1mm per side
    max_bore = root_diameter - 2 * min_rim

    # If gear is too small for any bore, return None
    if max_bore < min_bore:
        return (None, False)

    # Clamp to valid range
    bore = max(min_bore, min(target, max_bore))

    # Round to nice values
    if bore < 12:
        # Round to nearest 0.5mm for small bores
        bore = round(bore * 2) / 2
    else:
        # Round to nearest 1mm for larger bores
        bore = round(bore)

    # Final clamp after rounding
    bore = max(min_bore, min(bore, max_bore))

    # Check if rim is thin (warning threshold: < 1.5mm)
    actual_rim = (root_diameter - bore) / 2
    has_warning = actual_rim < 1.5

    return (bore, has_warning)


def get_din_6885_keyway(bore_diameter: float) -> Optional[Tuple[float, float, float, float]]:
    """
    Look up DIN 6885 keyway dimensions for a given bore diameter.

    Args:
        bore_diameter: Bore diameter in mm

    Returns:
        Tuple of (key_width, key_height, shaft_depth, hub_depth) in mm,
        or None if bore is outside standard range
    """
    for (min_d, max_d), dims in DIN_6885_KEYWAYS.items():
        if min_d <= bore_diameter < max_d:
            return dims
    return None


def get_set_screw_size(bore_diameter: float) -> Tuple[str, float]:
    """
    Determine appropriate set screw size based on bore diameter.

    Args:
        bore_diameter: Bore diameter in mm

    Returns:
        Tuple of (size_name, thread_diameter) in mm (e.g., ("M4", 4.0))

    Raises:
        ValueError: If bore is too small for set screws
    """
    if bore_diameter < 2.0:
        raise ValueError(
            f"Bore diameter {bore_diameter}mm is too small for set screws (min 2mm)"
        )

    for (min_d, max_d), (name, diameter) in SET_SCREW_SIZES.items():
        if min_d <= bore_diameter < max_d:
            return (name, diameter)

    # For bores larger than table, use M8
    return ("M8", 8.0)


@dataclass
class BoreFeature:
    """
    Bore (center hole) feature specification.

    Attributes:
        diameter: Bore diameter in mm
        through: If True, bore goes all the way through (default)
        depth: If not through, depth of bore in mm
    """
    diameter: float
    through: bool = True
    depth: Optional[float] = None

    def __post_init__(self):
        if self.diameter <= 0:
            raise ValueError(f"Bore diameter must be positive, got {self.diameter}")
        if not self.through and self.depth is None:
            raise ValueError("Non-through bore requires depth specification")
        if self.depth is not None and self.depth <= 0:
            raise ValueError(f"Bore depth must be positive, got {self.depth}")


@dataclass
class KeywayFeature:
    """
    Keyway feature specification per DIN 6885 / ISO 6885.

    If width and depth are not specified, they are auto-calculated from
    the bore diameter using DIN 6885 standard dimensions.

    Attributes:
        width: Key width in mm (auto from bore if None)
        depth: Keyway depth in mm (auto from bore if None)
        length: Keyway length in mm (full length if None)
        is_shaft: True for shaft keyway (worm), False for hub keyway (wheel)
    """
    width: Optional[float] = None
    depth: Optional[float] = None
    length: Optional[float] = None
    is_shaft: bool = False  # False = hub (wheel), True = shaft (worm)

    def get_dimensions(self, bore_diameter: float) -> Tuple[float, float]:
        """
        Get keyway width and depth, using DIN 6885 if not specified.

        Args:
            bore_diameter: Bore diameter in mm

        Returns:
            Tuple of (width, depth) in mm

        Raises:
            ValueError: If bore is outside DIN 6885 range and dimensions not specified
        """
        if self.width is not None and self.depth is not None:
            return (self.width, self.depth)

        # Look up standard dimensions
        dims = get_din_6885_keyway(bore_diameter)
        if dims is None:
            raise ValueError(
                f"Bore diameter {bore_diameter}mm is outside DIN 6885 range (6-95mm). "
                "Please specify keyway width and depth manually."
            )

        key_width, key_height, shaft_depth, hub_depth = dims

        width = self.width if self.width is not None else key_width
        if self.depth is not None:
            depth = self.depth
        else:
            depth = shaft_depth if self.is_shaft else hub_depth

        return (width, depth)


@dataclass
class SetScrewFeature:
    """
    Set screw hole feature specification for shaft retention.

    Set screws are threaded holes drilled radially through the bore wall,
    allowing grub screws to secure the gear to a shaft.

    If size is not specified, it is auto-calculated from the bore diameter.

    Attributes:
        size: Screw size name (e.g., "M3", "M4") - auto-sized if None
        diameter: Thread diameter in mm - auto-sized if None
        count: Number of set screws (1-3, default: 1)
        angular_offset: Starting angle in degrees (0 = aligned with +X axis)
                       For parts with keyways, screws are automatically positioned
                       90° from keyway to avoid interference
    """
    size: Optional[str] = None
    diameter: Optional[float] = None
    count: int = 1
    angular_offset: float = 90.0  # Default: 90° from keyway (top position)

    def __post_init__(self):
        if self.count < 1 or self.count > 3:
            raise ValueError(f"Set screw count must be 1-3, got {self.count}")
        if self.diameter is not None and self.diameter <= 0:
            raise ValueError(f"Set screw diameter must be positive, got {self.diameter}")

    def get_screw_specs(self, bore_diameter: float) -> Tuple[str, float]:
        """
        Get set screw size and diameter, auto-sizing if not specified.

        Args:
            bore_diameter: Bore diameter in mm

        Returns:
            Tuple of (size_name, thread_diameter) in mm
        """
        if self.size is not None and self.diameter is not None:
            return (self.size, self.diameter)

        # Auto-size from bore
        auto_size, auto_diameter = get_set_screw_size(bore_diameter)

        size = self.size if self.size is not None else auto_size
        diameter = self.diameter if self.diameter is not None else auto_diameter

        return (size, diameter)


def create_bore(
    part: Part,
    bore: BoreFeature,
    part_length: float,
    axis: Axis = Axis.Z
) -> Part:
    """
    Create a bore (center hole) in a part.

    Args:
        part: The part to add bore to
        bore: Bore specification
        part_length: Length of the part along bore axis (for through holes)
        axis: Axis along which to create bore (default: Z)

    Returns:
        Part with bore cut
    """
    bore_radius = bore.diameter / 2

    if bore.through:
        # Through bore - extend slightly beyond part
        bore_depth = part_length + 1.0
    else:
        bore_depth = bore.depth

    # Create bore cylinder
    bore_cyl = Cylinder(
        radius=bore_radius,
        height=bore_depth,
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )

    # Rotate to correct axis if needed
    if axis == Axis.X:
        bore_cyl = bore_cyl.rotate(Axis.Y, 90)
    elif axis == Axis.Y:
        bore_cyl = bore_cyl.rotate(Axis.X, 90)
    # Z axis is default, no rotation needed

    # Subtract from part
    result = part - bore_cyl

    return result


def create_keyway(
    part: Part,
    bore: BoreFeature,
    keyway: KeywayFeature,
    part_length: float,
    axis: Axis = Axis.Z
) -> Part:
    """
    Create a keyway in a part (requires bore to already exist or be specified).

    For hub keyways (wheel): The slot is cut into the hub material around the bore.
    The depth (t2) is measured radially outward from the bore surface.

    For shaft keyways (worm): The slot is cut into the shaft.
    The depth (t1) is measured radially inward from the shaft outer surface.
    Note: For a shaft with a bore, the keyway is cut from the outer surface inward.

    Args:
        part: The part to add keyway to
        bore: Bore specification (keyway is relative to bore)
        keyway: Keyway specification
        part_length: Length of the part along axis
        axis: Axis along which keyway runs (default: Z)

    Returns:
        Part with keyway cut
    """
    bore_radius = bore.diameter / 2
    width, depth = keyway.get_dimensions(bore.diameter)

    # Keyway length - use full length if not specified
    if keyway.length is not None:
        kw_length = keyway.length
    else:
        kw_length = part_length

    if keyway.is_shaft:
        # Shaft keyway (worm): cut from center axis outward
        # The keyway slot sits at the bore surface and extends outward by 'depth'
        # But since we have a bore hole, we need to create a slot that goes
        # from the center through the bore and into the shaft material by 'depth'
        #
        # DIN 6885 t1 is measured from the shaft surface, so the bottom of the
        # keyway is at radius = bore_radius + depth
        keyway_box = Box(
            bore_radius + depth,  # from center to (bore_radius + depth)
            width,  # tangential width
            kw_length + 1.0,  # axial length (slightly longer for clean cut)
            align=(Align.MIN, Align.CENTER, Align.CENTER)
        )
        # Position starting from center (X=0), extending in +X direction
        # No translation needed - MIN alignment puts it at origin
    else:
        # Hub keyway (wheel): cut into the hub material around the bore
        # The slot extends from inside the bore outward through the hub material
        # DIN 6885 t2 is measured from the bore surface outward
        #
        # To avoid a facet covering the bore, extend the box inward past the
        # bore surface so it fully intersects with the cylindrical bore
        keyway_box = Box(
            bore_radius + depth,  # from center to (bore_radius + depth)
            width,  # tangential width
            kw_length + 1.0,  # axial length (slightly longer for clean cut)
            align=(Align.MIN, Align.CENTER, Align.CENTER)
        )
        # Position starting from center (X=0), extending in +X direction
        # No translation needed - MIN alignment puts it at origin

    # Rotate to correct axis if needed
    if axis == Axis.X:
        keyway_box = keyway_box.rotate(Axis.Y, 90)
    elif axis == Axis.Y:
        keyway_box = keyway_box.rotate(Axis.X, 90)

    # Subtract from part
    result = part - keyway_box

    return result


def create_set_screw(
    part: Part,
    bore: BoreFeature,
    set_screw: SetScrewFeature,
    part_length: float,
    axis: Axis = Axis.Z
) -> Part:
    """
    Create set screw holes in a part (requires bore to already exist or be specified).

    Set screws are drilled radially through the bore wall. Multiple set screws
    are evenly spaced around the circumference.

    Args:
        part: The part to add set screw holes to
        bore: Bore specification (set screws go through bore wall)
        set_screw: Set screw specification
        part_length: Length of the part along axis
        axis: Axis along which part is oriented (default: Z)

    Returns:
        Part with set screw holes cut
    """
    bore_radius = bore.diameter / 2
    screw_size, screw_diameter = set_screw.get_screw_specs(bore.diameter)

    # Set screw holes are drilled radially (perpendicular to axis)
    # They should extend from outside the part through the bore wall
    # Use a generous length to ensure they fully penetrate
    screw_hole_length = bore_radius + 10.0  # Extend 10mm beyond center

    # Calculate angular positions for multiple set screws
    # Evenly distributed around circumference
    if set_screw.count == 1:
        angles = [set_screw.angular_offset]
    else:
        # Multiple screws: distribute evenly (e.g., 2 screws = 180° apart)
        angle_step = 360.0 / set_screw.count
        angles = [set_screw.angular_offset + i * angle_step for i in range(set_screw.count)]

    result = part

    for angle in angles:
        # Create cylindrical hole for set screw
        # The hole is positioned at the bore surface and drilled radially inward
        screw_hole = Cylinder(
            radius=screw_diameter / 2,
            height=screw_hole_length,
            align=(Align.MIN, Align.CENTER, Align.CENTER)
        )

        # Position and orient the hole based on axis
        if axis == Axis.Z:
            # Part is along Z axis, set screw holes are in XY plane
            # Rotate hole to be radial at the specified angle
            screw_hole = screw_hole.rotate(Axis.Z, angle)
        elif axis == Axis.X:
            # Part is along X axis, set screw holes are in YZ plane
            screw_hole = screw_hole.rotate(Axis.Y, 90)  # Orient along X
            screw_hole = screw_hole.rotate(Axis.X, angle)
        elif axis == Axis.Y:
            # Part is along Y axis, set screw holes are in XZ plane
            screw_hole = screw_hole.rotate(Axis.X, -90)  # Orient along Y
            screw_hole = screw_hole.rotate(Axis.Y, angle)

        # Subtract from part
        result = result - screw_hole

    return result


def add_bore_and_keyway(
    part: Part,
    part_length: float,
    bore: Optional[BoreFeature] = None,
    keyway: Optional[KeywayFeature] = None,
    set_screw: Optional[SetScrewFeature] = None,
    axis: Axis = Axis.Z
) -> Part:
    """
    Add bore, keyway, and set screw holes to a part.

    Convenience function that applies features in order: bore → keyway → set screws.

    Args:
        part: The part to modify
        part_length: Length of the part along axis
        bore: Bore specification (required if keyway or set_screw specified)
        keyway: Keyway specification (optional)
        set_screw: Set screw specification (optional)
        axis: Axis for bore and features (default: Z)

    Returns:
        Modified part with requested features

    Raises:
        ValueError: If keyway or set_screw specified without bore
    """
    if keyway is not None and bore is None:
        raise ValueError("Keyway requires a bore to be specified")

    if set_screw is not None and bore is None:
        raise ValueError("Set screw requires a bore to be specified")

    result = part

    if bore is not None:
        result = create_bore(result, bore, part_length, axis)

    if keyway is not None:
        result = create_keyway(result, bore, keyway, part_length, axis)

    if set_screw is not None:
        result = create_set_screw(result, bore, set_screw, part_length, axis)

    # Ensure we return a single Part/Solid, not a ShapeList
    # Boolean operations can sometimes split geometry into multiple pieces
    if hasattr(result, 'solids'):
        solids = list(result.solids())
        if len(solids) == 1:
            result = solids[0]
        elif len(solids) > 1:
            # Return the largest solid (the main part)
            result = max(solids, key=lambda s: s.volume)

    return result
