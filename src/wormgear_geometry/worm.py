"""
Worm geometry generation using build123d.

Creates CNC-ready worm geometry with helical threads.
"""

import math
from build123d import *
from .io import WormParams, AssemblyParams


class WormGeometry:
    """
    Generates 3D geometry for a worm.

    Uses helical sweep of trapezoidal tooth profile.
    """

    def __init__(
        self,
        params: WormParams,
        assembly_params: AssemblyParams,
        length: float = 40.0
    ):
        """
        Initialize worm geometry generator.

        Args:
            params: Worm parameters from calculator
            assembly_params: Assembly parameters (for pressure angle)
            length: Total worm length in mm (default: 40)
        """
        self.params = params
        self.assembly_params = assembly_params
        self.length = length

    def build(self) -> Part:
        """
        Build the complete worm geometry.

        Returns:
            build123d Part object ready for export
        """
        # Create core cylinder at root diameter
        core = Cylinder(
            radius=self.params.root_diameter_mm / 2,
            height=self.length,
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

        # Create thread(s)
        threads = self._create_threads()

        # Union core and threads
        worm = core + threads

        return worm

    def _create_threads(self) -> Part:
        """Create helical thread(s) on the worm."""
        # For multi-start worms, create multiple threads offset by lead/num_starts
        threads = []

        for start_index in range(self.params.num_starts):
            # Angular offset for this start
            angle_offset = (360 / self.params.num_starts) * start_index

            thread = self._create_single_thread(angle_offset)
            threads.append(thread)

        # Union all threads
        if len(threads) == 1:
            return threads[0]
        else:
            result = threads[0]
            for thread in threads[1:]:
                result = result + thread
            return result

    def _create_single_thread(self, start_angle: float = 0) -> Part:
        """
        Create a single helical thread.

        Args:
            start_angle: Starting angle offset in degrees (for multi-start)

        Returns:
            Part representing one thread
        """
        # Calculate helix parameters
        pitch_radius = self.params.pitch_diameter_mm / 2
        lead_angle_rad = math.radians(self.params.lead_angle_deg)

        # Number of complete turns needed
        num_turns = math.ceil(self.length / self.params.lead_mm) + 1

        # Create helix path
        helix_height = num_turns * self.params.lead_mm
        helix_path = Helix(
            pitch=self.params.lead_mm,
            height=helix_height,
            radius=pitch_radius,
            direction=(0, 0, 1) if self.params.hand == "RIGHT" else (0, 0, -1)
        )

        # Rotate helix to start at correct angle
        if start_angle != 0:
            helix_path = helix_path.rotate(Axis.Z, start_angle)

        # Create tooth profile and sweep along helix
        with BuildPart() as thread_builder:
            # Create profile at start of helix
            with BuildSketch(Plane.XZ.offset(pitch_radius)):
                add(self._create_tooth_profile())

            # Sweep profile along helix path
            sweep(path=helix_path, multisection=False)

        thread = thread_builder.part

        # Trim to actual length
        thread = thread & Box(
            self.params.tip_diameter_mm,
            self.params.tip_diameter_mm,
            self.length,
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

        return thread

    def _create_tooth_profile(self) -> Sketch:
        """
        Create trapezoidal tooth profile in axial plane.

        Profile is symmetric about centerline, with flanks at pressure angle.

        Returns:
            Sketch of tooth profile
        """
        pressure_angle_rad = math.radians(self.assembly_params.pressure_angle_deg)

        # Dimensions
        addendum = self.params.addendum_mm
        dedendum = self.params.dedendum_mm
        total_depth = addendum + dedendum

        # Thread thickness at pitch line (adjusted for backlash)
        pitch_thickness = self.params.thread_thickness_mm - self.assembly_params.backlash_mm

        # Calculate top and bottom widths
        # At tip (addendum above pitch line)
        tip_half_width = pitch_thickness / 2 - addendum * math.tan(pressure_angle_rad)

        # At root (dedendum below pitch line)
        root_half_width = pitch_thickness / 2 + dedendum * math.tan(pressure_angle_rad)

        # Create profile as polygon
        # Coordinates in (radial, axial) space
        points = [
            (addendum, -tip_half_width),           # Tip left
            (addendum, tip_half_width),            # Tip right
            (-dedendum, root_half_width),          # Root right
            (-dedendum, -root_half_width),         # Root left
        ]

        with BuildSketch() as profile_sketch:
            with BuildLine():
                for i in range(len(points)):
                    p1 = points[i]
                    p2 = points[(i + 1) % len(points)]
                    Line(p1, p2)
            make_face()

        return profile_sketch.sketch

    def show(self):
        """
        Display the worm in OCP viewer (Jupyter or VS Code).

        Returns:
            The built worm part for viewer display
        """
        worm = self.build()
        try:
            from ocp_vscode import show as ocp_show
            ocp_show(worm)
        except ImportError:
            # Fall back to build123d show if available
            try:
                show(worm)
            except:
                print("No viewer available. Install ocp-vscode or run in Jupyter with build123d viewer.")
        return worm

    def export_step(self, filepath: str):
        """
        Build and export worm to STEP file.

        Args:
            filepath: Output STEP file path
        """
        worm = self.build()

        # Convert to Part if needed
        if hasattr(worm, 'export_step'):
            worm.export_step(filepath)
        else:
            # Use exporter for Compound objects
            from build123d import export_step as exp_step
            exp_step(worm, filepath)

        print(f"Exported worm to {filepath}")
