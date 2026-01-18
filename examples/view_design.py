#!/usr/bin/env python3
"""
Interactive viewer for worm gear designs.

Requires ocp-vscode extension for VS Code or CQ-Editor.
"""

import sys
import argparse
from pathlib import Path

# Add parent src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from wormgear_geometry import load_design_json, WormGeometry, WheelGeometry
from build123d import *


def main():
    parser = argparse.ArgumentParser(
        description="View worm gear design in OCP viewer"
    )
    parser.add_argument(
        'design_file',
        type=str,
        help='JSON file from wormgearcalc'
    )
    parser.add_argument(
        '--part',
        choices=['worm', 'wheel', 'both'],
        default='both',
        help='Which part(s) to display (default: both)'
    )
    parser.add_argument(
        '--worm-length',
        type=float,
        default=40.0,
        help='Worm length in mm (default: 40)'
    )
    parser.add_argument(
        '--wheel-width',
        type=float,
        default=None,
        help='Wheel face width in mm (default: auto)'
    )

    args = parser.parse_args()

    # Load design
    print(f"Loading design from {args.design_file}...")
    design = load_design_json(args.design_file)

    print(f"\nDesign parameters:")
    print(f"  Module: {design.worm.module_mm} mm")
    print(f"  Ratio: {design.assembly.ratio}:1")
    print(f"  Worm: {design.worm.num_starts}-start")
    print(f"  Wheel: {design.wheel.num_teeth} teeth")
    print(f"  Centre distance: {design.assembly.centre_distance_mm:.2f} mm")

    parts_to_show = []

    # Build worm
    if args.part in ['worm', 'both']:
        print(f"\nBuilding worm (length: {args.worm_length} mm)...")
        worm_geo = WormGeometry(
            params=design.worm,
            assembly_params=design.assembly,
            length=args.worm_length
        )
        worm = worm_geo.build()
        print(f"  Volume: {worm.volume:.2f} mm³")

        # Position worm at centre distance
        worm_positioned = worm.translate((0, 0, design.assembly.centre_distance_mm))
        parts_to_show.append(('worm', worm_positioned))

    # Build wheel
    if args.part in ['wheel', 'both']:
        print(f"\nBuilding wheel...")
        wheel_geo = WheelGeometry(
            params=design.wheel,
            worm_params=design.worm,
            assembly_params=design.assembly,
            face_width=args.wheel_width
        )
        wheel = wheel_geo.build()
        print(f"  Face width: {wheel_geo.face_width:.2f} mm")
        print(f"  Volume: {wheel.volume:.2f} mm³")
        parts_to_show.append(('wheel', wheel))

    # Display in viewer
    print("\nOpening OCP viewer...")
    print("(Requires ocp-vscode extension in VS Code or CQ-Editor)\n")

    try:
        from ocp_vscode import show, set_port, set_defaults, reset_show

        # Configure viewer
        set_defaults(
            helper_scale=1,
            transparent=False,
            angular_tolerance=0.1,
            edge_accuracy=0.01
        )

        # Show parts with labels
        reset_show()
        for name, part in parts_to_show:
            show(part, names=[name])

        print(f"✓ Displaying {len(parts_to_show)} part(s) in viewer")

    except ImportError:
        print("ERROR: ocp-vscode not installed")
        print("\nTo install:")
        print("  1. Install VS Code extension: OCP CAD Viewer")
        print("  2. pip install ocp-vscode")
        print("\nAlternatively, export to STEP and view in CAD software:")
        print(f"  python -m wormgear_geometry.cli {args.design_file}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
