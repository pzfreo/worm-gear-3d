"""
Command-line interface for worm gear geometry generation.
"""

import argparse
import sys
from pathlib import Path

from .io import load_design_json
from .worm import WormGeometry
from .wheel import WheelGeometry


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate CNC-ready STEP files for worm gear pairs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate both worm and wheel
  wormgear-geometry design.json

  # Specify output directory
  wormgear-geometry design.json -o output/

  # Custom worm length
  wormgear-geometry design.json --worm-length 50

  # Custom wheel face width
  wormgear-geometry design.json --wheel-width 12
        """
    )

    parser.add_argument(
        'design_file',
        type=str,
        help='JSON file from wormgearcalc (Tool 1)'
    )

    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default='.',
        help='Output directory for STEP files (default: current directory)'
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
        help='Wheel face width in mm (default: auto-calculated)'
    )

    parser.add_argument(
        '--worm-only',
        action='store_true',
        help='Generate only the worm'
    )

    parser.add_argument(
        '--wheel-only',
        action='store_true',
        help='Generate only the wheel'
    )

    args = parser.parse_args()

    # Load design
    try:
        print(f"Loading design from {args.design_file}...")
        design = load_design_json(args.design_file)
    except Exception as e:
        print(f"Error loading design: {e}", file=sys.stderr)
        return 1

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine what to generate
    generate_worm = not args.wheel_only
    generate_wheel = not args.worm_only

    # Generate worm
    if generate_worm:
        print(f"\nGenerating worm ({design.worm.num_starts}-start, module {design.worm.module_mm}mm)...")
        worm_geo = WormGeometry(
            params=design.worm,
            assembly_params=design.assembly,
            length=args.worm_length
        )

        output_file = output_dir / f"worm_m{design.worm.module_mm}_z{design.worm.num_starts}.step"
        worm_geo.export_step(str(output_file))

    # Generate wheel
    if generate_wheel:
        print(f"\nGenerating wheel ({design.wheel.num_teeth} teeth, module {design.wheel.module_mm}mm)...")
        wheel_geo = WheelGeometry(
            params=design.wheel,
            worm_params=design.worm,
            assembly_params=design.assembly,
            face_width=args.wheel_width
        )

        output_file = output_dir / f"wheel_m{design.wheel.module_mm}_z{design.wheel.num_teeth}.step"
        wheel_geo.export_step(str(output_file))

    print(f"\n✓ Generation complete! Files saved to {output_dir}")
    print(f"  Ratio: {design.assembly.ratio}:1")
    print(f"  Centre distance: {design.assembly.centre_distance_mm:.2f} mm")

    return 0


if __name__ == '__main__':
    sys.exit(main())
