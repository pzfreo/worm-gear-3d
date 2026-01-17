"""
Wheel geometry generation using build123d.

Creates worm wheel using hybrid approach: helical involute gear + throating cut.
"""

import math
from build123d import *
from .io import WheelParams, WormParams, AssemblyParams


class WheelGeometry:
    """
    Generates 3D geometry for a worm wheel.

    Uses hybrid approach: creates helical involute gear, then applies
    throating cylinder cut to match worm curvature.
    """

    def __init__(
        self,
        params: WheelParams,
        worm_params: WormParams,
        assembly_params: AssemblyParams,
        face_width: float = None
    ):
        """
        Initialize wheel geometry generator.

        Args:
            params: Wheel parameters from calculator
            worm_params: Worm parameters (needed for throating)
            assembly_params: Assembly parameters
            face_width: Wheel face width in mm (default: auto-calculated)
        """
        self.params = params
        self.worm_params = worm_params
        self.assembly_params = assembly_params

        # Calculate face width if not provided
        # Rule of thumb: b ≈ 0.73 × d1^(1/3) × sqrt(ratio)
        if face_width is None:
            d1 = worm_params.pitch_diameter_mm
            ratio = assembly_params.ratio
            self.face_width = 0.73 * (d1 ** (1/3)) * math.sqrt(ratio)
            # Clamp to practical range
            self.face_width = max(0.3 * d1, min(0.67 * d1, self.face_width))
        else:
            self.face_width = face_width

    def build(self) -> Part:
        """
        Build the complete wheel geometry.

        Returns:
            build123d Part object ready for export
        """
        # Create basic helical gear
        gear = self._create_helical_gear()

        # Apply throating cut
        throated_gear = self._apply_throat_cut(gear)

        return throated_gear

    def _create_helical_gear(self) -> Part:
        """
        Create basic helical involute gear.

        This is a simplified approach - creates straight involute teeth
        then helixes them to match the worm.
        """
        # Create gear blank (cylinder)
        blank = Cylinder(
            radius=self.params.tip_diameter_mm / 2,
            height=self.face_width,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

        # Create tooth spaces (simplified approach - use rectangles)
        # In a production version, we'd use true involute curves
        tooth_space = self._create_tooth_space()

        # Pattern around circumference
        with BuildPart() as gear_builder:
            add(blank)

            # Cut each tooth space
            for i in range(self.params.num_teeth):
                angle = (360 / self.params.num_teeth) * i
                rotated_space = tooth_space.rotate(Axis.Z, angle)
                gear_builder.part = gear_builder.part - rotated_space

        gear = gear_builder.part

        # Apply helix twist to teeth
        # Twist amount: helix_angle over the face width
        twist_angle = math.degrees(
            math.atan(self.face_width / self.params.pitch_diameter_mm) *
            math.tan(math.radians(self.params.helix_angle_deg))
        )

        # Note: build123d doesn't have built-in twist, so we approximate with sections
        # For now, return the gear without twist (will still mesh, just not perfectly)
        # TODO: Implement true helical twist using multiple cross-sections

        return gear

    def _create_tooth_space(self) -> Part:
        """
        Create a single tooth space (gap between teeth).

        Simplified approach using rectangular cut.
        A production version would use true involute curves.
        """
        # Tooth space at pitch diameter
        circular_pitch = math.pi * self.params.module_mm
        space_width = circular_pitch / 2  # Half of circular pitch
        space_depth = self.params.addendum_mm + self.params.dedendum_mm

        # Create radial cut
        # Position at pitch radius, extend outward and inward
        pitch_radius = self.params.pitch_diameter_mm / 2

        with BuildPart() as space_builder:
            Box(
                space_width,
                self.params.tip_diameter_mm,  # Long enough to cut through
                self.face_width * 1.1,  # Slightly taller than gear
                align=(Align.CENTER, Align.MIN, Align.CENTER)
            )

        return space_builder.part

    def _apply_throat_cut(self, gear: Part) -> Part:
        """
        Apply throating cylinder cut to match worm curvature.

        The throat is cut by a cylinder at the worm's tip radius,
        positioned at the correct centre distance.
        """
        # Throat cutting cylinder parameters
        throat_radius = self.worm_params.tip_diameter_mm / 2 + 0.1  # Small clearance
        throat_length = self.params.tip_diameter_mm * 2  # Long enough

        # Create cutting cylinder
        # Positioned perpendicular to wheel axis, at centre distance
        throat_cutter = Cylinder(
            radius=throat_radius,
            height=throat_length,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

        # Rotate to be perpendicular to wheel (along X axis)
        throat_cutter = throat_cutter.rotate(Axis.Y, 90)

        # Move to correct position (centre distance from wheel centre)
        # In assembly, worm is above wheel at centre distance
        throat_cutter = throat_cutter.translate((0, 0, self.assembly_params.centre_distance_mm))

        # Subtract from gear
        throated_gear = gear - throat_cutter

        return throated_gear

    def export_step(self, filepath: str):
        """
        Build and export wheel to STEP file.

        Args:
            filepath: Output STEP file path
        """
        wheel = self.build()

        # Convert to Part if needed
        if hasattr(wheel, 'export_step'):
            wheel.export_step(filepath)
        else:
            # Use exporter for Compound objects
            from build123d import export_step as exp_step
            exp_step(wheel, filepath)

        print(f"Exported wheel to {filepath}")
