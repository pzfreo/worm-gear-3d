#!/usr/bin/env python3
"""
Example: Generate a complete worm gear pair from calculator JSON.

This demonstrates the Python API for wormgear-geometry.
"""

from wormgear_geometry import (
    load_design_json,
    WormGeometry,
    WheelGeometry
)


def main():
    # Load design from calculator
    design = load_design_json('sample_m2_ratio30.json')

    print("Design loaded:")
    print(f"  Worm: {design.worm.num_starts}-start, module {design.worm.module_mm}mm")
    print(f"  Wheel: {design.wheel.num_teeth} teeth")
    print(f"  Ratio: {design.assembly.ratio}:1")
    print(f"  Centre distance: {design.assembly.centre_distance_mm:.2f}mm")
    print()

    # Generate worm
    print("Building worm...")
    worm_geo = WormGeometry(
        params=design.worm,
        assembly_params=design.assembly,
        length=40  # mm
    )
    worm = worm_geo.build()
    print(f"  Volume: {worm.volume:.2f} mm³")
    worm_geo.export_step('worm.step')

    # Generate wheel
    print("\nBuilding wheel...")
    wheel_geo = WheelGeometry(
        params=design.wheel,
        worm_params=design.worm,
        assembly_params=design.assembly
    )
    wheel = wheel_geo.build()
    print(f"  Face width: {wheel_geo.face_width:.2f} mm")
    print(f"  Volume: {wheel.volume:.2f} mm³")
    wheel_geo.export_step('wheel.step')

    print("\n✓ Complete! Import worm.step and wheel.step into your CAD software.")


if __name__ == '__main__':
    main()
