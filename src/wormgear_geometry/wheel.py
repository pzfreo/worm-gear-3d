"""
Wheel geometry generation using build123d.

Creates worm wheel using hybrid approach:
1. Helical gear with correct tooth profile
2. Toroidal throat cut to match worm curvature
"""

import math
from build123d import *
from .io import WheelParams, WormParams, AssemblyParams


class WheelGeometry:
    """
    Generates 3D geometry for a worm wheel.

    Uses hybrid approach (Option C from spec):
    - Creates helical gear with involute-approximation teeth
    - Applies toroidal throat cut to match worm curvature
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
        if face_width is None:
            d1 = worm_params.pitch_diameter_mm
            ratio = assembly_params.ratio
            self.face_width = 0.73 * (d1 ** (1/3)) * math.sqrt(ratio)
            self.face_width = max(0.3 * d1, min(0.67 * d1, self.face_width))
        else:
            self.face_width = face_width

    def build(self) -> Part:
        """
        Build the complete wheel geometry.

        Returns:
            build123d Part object ready for export
        """
        # Create helical gear
        gear = self._create_helical_gear()

        # Apply toroidal throat cut
        throated_gear = self._apply_throat_cut(gear)

        return throated_gear

    def _create_helical_gear(self) -> Part:
        """
        Create helical gear by sweeping tooth spaces along helical paths.
        """
        z = self.params.num_teeth
        m = self.params.module_mm
        tip_radius = self.params.tip_diameter_mm / 2
        root_radius = self.params.root_diameter_mm / 2
        pitch_radius = self.params.pitch_diameter_mm / 2
        pressure_angle = math.radians(self.assembly_params.pressure_angle_deg)

        # The wheel's helix angle should match the worm's lead angle
        lead_angle = math.radians(self.worm_params.lead_angle_deg)

        # Create gear blank
        blank = Cylinder(
            radius=tip_radius,
            height=self.face_width,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

        # Calculate tooth space dimensions
        circular_pitch = math.pi * m
        space_width_pitch = circular_pitch / 2 + self.assembly_params.backlash_mm

        # Space is wider at tip, narrower at root (inverse of tooth shape)
        space_width_tip = space_width_pitch + 2 * (tip_radius - pitch_radius) * math.tan(pressure_angle)
        space_width_root = space_width_pitch - 2 * (pitch_radius - root_radius) * math.tan(pressure_angle)
        space_width_root = max(0.5, space_width_root)

        half_root = space_width_root / 2
        half_tip = space_width_tip / 2

        # Helical twist across face width (using lead angle)
        twist_rad = self.face_width * math.tan(lead_angle) / pitch_radius
        twist_deg = math.degrees(twist_rad)

        # Extend cut beyond face to get clean edges
        extension = 2
        cut_height = self.face_width + 2 * extension
        twist_extended_rad = cut_height * math.tan(lead_angle) / pitch_radius
        twist_extended_deg = math.degrees(twist_extended_rad)

        # Calculate helix pitch for the sweep
        if abs(twist_extended_deg) > 0.1:
            helix_pitch = cut_height / (twist_extended_deg / 360)
        else:
            helix_pitch = 10000  # Nearly straight

        # Cut tooth spaces
        gear = blank

        for i in range(z):
            base_angle = (360 / z) * i

            # Create helix path for this tooth space
            helix_path = Helix(
                pitch=helix_pitch,
                height=cut_height,
                radius=pitch_radius,
                center=(0, 0, -cut_height / 2),
            )

            # Rotate helix to correct starting angle
            helix_path = helix_path.rotate(Axis.Z, base_angle - twist_extended_deg / 2)

            # Get start point and tangent for sweep plane
            start_pt = helix_path @ 0
            tangent = helix_path % 0

            # Radial direction at start
            start_angle_rad = math.radians(base_angle - twist_extended_deg / 2)
            radial = Vector(math.cos(start_angle_rad), math.sin(start_angle_rad), 0)

            # Create sweep plane with X = radial outward, Z = along helix
            sweep_plane = Plane(origin=start_pt, x_dir=radial, z_dir=tangent)

            # Profile offsets from pitch radius
            inner = root_radius - pitch_radius - 0.5
            outer = tip_radius + 0.5 - pitch_radius

            # Create and sweep tooth space with involute-like curved flanks
            try:
                with BuildPart() as space_builder:
                    with BuildSketch(sweep_plane):
                        with BuildLine():
                            # Create involute-like curved flanks to match worm
                            num_flank_points = 5
                            left_flank = []
                            right_flank = []

                            for j in range(num_flank_points):
                                # Parameter along the flank (0 = inner/root, 1 = outer/tip)
                                t_flank = j / (num_flank_points - 1)
                                r_pos = inner + t_flank * (outer - inner)

                                # Interpolate width with slight curve (involute approximation)
                                linear_width = half_root + t_flank * (half_tip - half_root)
                                # Add subtle curve - max bulge at middle of flank
                                curve_factor = 4 * t_flank * (1 - t_flank)
                                bulge = curve_factor * 0.05 * (half_root - half_tip)
                                width = linear_width + bulge

                                left_flank.append((r_pos, -width))
                                right_flank.append((r_pos, width))

                            # Build profile: left flank up, across outer, right flank down, across inner
                            Spline(left_flank)
                            Line(left_flank[-1], right_flank[-1])  # Outer edge
                            Spline(list(reversed(right_flank)))
                            Line(right_flank[0], left_flank[0])  # Inner edge (closes profile)
                        make_face()
                    sweep(path=helix_path)

                space = space_builder.part
                gear = gear - space
            except Exception as e:
                print(f"Warning: Tooth space {i} failed: {e}")

        return gear

    def _apply_throat_cut(self, gear: Part) -> Part:
        """
        Apply toroidal throat cut to match worm curvature.

        The throat is created by revolving a circle (worm tip profile)
        around the wheel axis at the centre distance. This creates a
        torus that represents the envelope of the worm as it meshes
        with the wheel.
        """
        centre_distance = self.assembly_params.centre_distance_mm
        worm_tip_radius = self.worm_params.tip_diameter_mm / 2
        clearance = 0.1  # Small clearance for fit

        # Create torus by revolving a circle around the wheel axis (Z)
        # Circle is positioned at X = centre_distance, in the XZ plane
        with BuildPart() as torus_builder:
            with BuildSketch(Plane.XZ) as sk:
                with Locations([(centre_distance, 0)]):
                    Circle(worm_tip_radius + clearance)
            revolve(axis=Axis.Z)

        throat_torus = torus_builder.part

        # Subtract torus from gear
        throated_gear = gear - throat_torus

        return throated_gear

    def show(self):
        """Display the wheel in OCP viewer."""
        wheel = self.build()
        try:
            from ocp_vscode import show as ocp_show
            ocp_show(wheel)
        except ImportError:
            try:
                show(wheel)
            except:
                print("No viewer available.")
        return wheel

    def export_step(self, filepath: str):
        """Build and export wheel to STEP file."""
        wheel = self.build()

        if hasattr(wheel, 'export_step'):
            wheel.export_step(filepath)
        else:
            from build123d import export_step as exp_step
            exp_step(wheel, filepath)

        print(f"Exported wheel to {filepath}")
