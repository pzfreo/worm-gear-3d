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
        Create helical gear by extruding and twisting tooth space profiles.

        Uses extrusion with rotation rather than helix sweep to avoid
        self-intersection issues with tight helix pitches.
        """
        z = self.params.num_teeth
        m = self.params.module_mm
        tip_radius = self.params.tip_diameter_mm / 2
        root_radius = self.params.root_diameter_mm / 2
        pitch_radius = self.params.pitch_diameter_mm / 2
        pressure_angle = math.radians(self.assembly_params.pressure_angle_deg)

        # The wheel's helix angle equals 90° - worm lead angle
        # This determines how much the teeth twist over the face width
        lead_angle = math.radians(self.worm_params.lead_angle_deg)

        # Total twist angle over face width
        # At pitch radius, the teeth advance by (face_width * tan(lead_angle)) axially
        # This corresponds to a rotation of: twist = face_width * tan(lead_angle) / pitch_radius (radians)
        twist_radians = self.face_width * math.tan(lead_angle) / pitch_radius
        twist_degrees = math.degrees(twist_radians)

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
        space_width_root = max(0.1 * m, space_width_root)

        half_root = space_width_root / 2
        half_tip = space_width_tip / 2

        # Extend cut beyond face to get clean edges
        extension = 0.5
        cut_height = self.face_width + 2 * extension

        # Number of sections for lofting the twisted extrusion
        num_sections = max(8, int(abs(twist_degrees) / 5) + 1)

        # Cut tooth spaces
        gear = blank

        for i in range(z):
            base_angle = (360 / z) * i

            # Create sections along Z for lofting
            sections = []

            for s in range(num_sections):
                t = s / (num_sections - 1)  # 0 to 1
                z_pos = -cut_height / 2 + t * cut_height

                # Rotation at this Z position (linear interpolation of twist)
                rotation_at_z = -twist_degrees / 2 + t * twist_degrees
                section_angle = base_angle + rotation_at_z
                section_angle_rad = math.radians(section_angle)

                # Create profile plane at this Z, rotated appropriately
                radial = Vector(math.cos(section_angle_rad), math.sin(section_angle_rad), 0)
                tangent = Vector(-math.sin(section_angle_rad), math.cos(section_angle_rad), 0)

                # Profile plane: origin at pitch radius, X = radial outward, Y = tangential
                origin = Vector(
                    pitch_radius * math.cos(section_angle_rad),
                    pitch_radius * math.sin(section_angle_rad),
                    z_pos
                )
                profile_plane = Plane(origin=origin, x_dir=radial, z_dir=Vector(0, 0, 1))

                # Profile offsets from pitch radius (in radial direction)
                inner = root_radius - pitch_radius - 0.3
                outer = tip_radius + 0.3 - pitch_radius

                with BuildSketch(profile_plane) as sk:
                    with BuildLine():
                        # Create involute-like curved flanks
                        num_flank_points = 5
                        left_flank = []
                        right_flank = []

                        for j in range(num_flank_points):
                            t_flank = j / (num_flank_points - 1)
                            r_pos = inner + t_flank * (outer - inner)

                            linear_width = half_root + t_flank * (half_tip - half_root)
                            curve_factor = 4 * t_flank * (1 - t_flank)
                            bulge = curve_factor * 0.05 * (half_root - half_tip)
                            width = linear_width + bulge

                            left_flank.append((r_pos, -width))
                            right_flank.append((r_pos, width))

                        Spline(left_flank)
                        Line(left_flank[-1], right_flank[-1])
                        Spline(list(reversed(right_flank)))
                        Line(right_flank[0], left_flank[0])
                    make_face()

                sections.append(sk.sketch.faces()[0])

            # Loft the sections to create twisted tooth space
            try:
                space = loft(sections, ruled=True)
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
