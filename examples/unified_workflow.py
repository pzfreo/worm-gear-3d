"""
Unified Workflow Example - wormgear package

Demonstrates the complete workflow:
1. Calculate design parameters
2. Validate design
3. Save to JSON
4. Load from JSON
5. Generate 3D geometry

This replaces the old two-step process (wormgearcalc → wormgear-geometry)
with a unified Python API.
"""

from wormgear import (
    # Calculator functions
    calculate_design_from_module,
    validate_design,

    # IO functions
    save_design_json,
    load_design_json,

    # Geometry generation
    WormGeometry,
    WheelGeometry,
    GloboidWormGeometry,

    # Features
    BoreFeature,
    KeywayFeature,
)


def main():
    print("=" * 60)
    print("Unified Wormgear Workflow Example")
    print("=" * 60)

    # Step 1: Calculate design
    print("\n1. Calculate design from module and ratio...")
    design = calculate_design_from_module(
        module=2.0,
        ratio=30,
        target_lead_angle=7.0,
        pressure_angle=20.0,
        backlash=0.05,
        profile="ZA"  # Straight flanks for CNC
    )

    print(f"   ✓ Worm: {design.worm.pitch_diameter_mm:.2f}mm pitch dia, {design.worm.lead_angle_deg:.2f}° lead angle")
    print(f"   ✓ Wheel: {design.wheel.num_teeth} teeth, {design.wheel.pitch_diameter_mm:.2f}mm pitch dia")
    print(f"   ✓ Centre distance: {design.assembly.centre_distance_mm:.2f}mm")
    print(f"   ✓ Ratio: {design.assembly.ratio}:1")
    print(f"   ✓ Efficiency: {design.assembly.efficiency_percent:.1f}%")
    print(f"   ✓ Self-locking: {design.assembly.self_locking}")

    # Step 2: Validate design
    print("\n2. Validate design...")
    validation = validate_design(design)

    print(f"   Valid: {validation.valid}")
    print(f"   Errors: {len(validation.errors)}")
    print(f"   Warnings: {len(validation.warnings)}")
    print(f"   Infos: {len(validation.infos)}")

    if validation.messages:
        print("   Messages:")
        for msg in validation.messages[:3]:  # Show first 3
            print(f"     [{msg.severity.value.upper()}] {msg.message}")

    # Step 3: Save to JSON
    print("\n3. Save design to JSON...")
    json_path = "/tmp/example_design.json"
    save_design_json(design, json_path)
    print(f"   ✓ Saved to {json_path}")

    # Step 4: Load from JSON (simulating web calc → CLI workflow)
    print("\n4. Load design from JSON...")
    loaded_design = load_design_json(json_path)
    print(f"   ✓ Loaded: {loaded_design.worm.pitch_diameter_mm:.2f}mm worm")

    # Step 5: Generate 3D geometry
    print("\n5. Generate 3D geometry...")

    # Worm with bore and keyway
    print("   Generating worm...")
    worm_geo = WormGeometry(
        params=loaded_design.worm,
        assembly_params=loaded_design.assembly,
        length=40.0,
        sections_per_turn=36,
        bore=BoreFeature(diameter=8.0),
        keyway=KeywayFeature()  # DIN 6885 standard keyway
    )
    worm = worm_geo.build()
    print(f"   ✓ Worm built: {worm.volume:.2f} mm³")

    # Wheel with bore and keyway
    print("   Generating wheel...")
    wheel_geo = WheelGeometry(
        params=loaded_design.wheel,
        worm_params=loaded_design.worm,
        assembly_params=loaded_design.assembly,
        bore=BoreFeature(diameter=12.0),
        keyway=KeywayFeature()
    )
    wheel = wheel_geo.build()
    print(f"   ✓ Wheel built: {wheel.volume:.2f} mm³")

    # Step 6: Export STEP files
    print("\n6. Export STEP files...")
    worm_geo.export_step("/tmp/worm_m2_z1.step")
    wheel_geo.export_step("/tmp/wheel_m2_z30.step")
    print("   ✓ worm_m2_z1.step")
    print("   ✓ wheel_m2_z30.step")

    print("\n" + "=" * 60)
    print("✅ Complete workflow executed successfully!")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  - {json_path}")
    print("  - /tmp/worm_m2_z1.step")
    print("  - /tmp/wheel_m2_z30.step")


def globoid_example():
    """Example with globoid worm for better contact."""
    print("\n" + "=" * 60)
    print("Globoid Worm Example")
    print("=" * 60)

    # Calculate globoid design
    print("\n1. Calculate globoid design...")
    design = calculate_design_from_module(
        module=2.0,
        ratio=30,
        globoid=True,
        throat_reduction=0.1  # Creates hourglass shape
    )

    print(f"   ✓ Globoid worm design")
    print(f"   ✓ Centre distance: {design.assembly.centre_distance_mm:.2f}mm (reduced for throat)")

    # Save and load
    save_design_json(design, "/tmp/globoid_design.json")
    loaded = load_design_json("/tmp/globoid_design.json")

    # Generate globoid geometry
    print("\n2. Generate globoid worm...")
    globoid_worm = GloboidWormGeometry(
        params=loaded.worm,
        assembly_params=loaded.assembly,
        wheel_pitch_diameter=loaded.wheel.pitch_diameter_mm,
        length=40.0
    )
    worm = globoid_worm.build()
    print(f"   ✓ Globoid worm built: {worm.volume:.2f} mm³")

    globoid_worm.export_step("/tmp/globoid_worm_m2_z1.step")
    print("   ✓ Exported to globoid_worm_m2_z1.step")


if __name__ == "__main__":
    main()
    globoid_example()
