# Engineering Context for Worm Gear Geometry

This document provides the engineering background, standards, and formulas needed for implementing the geometry generator.

## Standards

### Primary Standards
- **DIN 3975** - Worm gear geometry definitions
- **DIN 3996** - Worm gear load capacity
- **ISO 54 / DIN 780** - Standard modules

### Feature Standards
- **ISO 6885 / DIN 6885** - Parallel keys and keyways
- **ISO 4017** - Hexagon head screws (for set screws)

## Standard Modules (ISO 54)

Used for tooth sizing. The calculator validates against these:

```
0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
1.125, 1.25, 1.375, 1.5, 1.75, 2.0, 2.25, 2.5,
2.75, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0,
7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 14.0, 16.0,
18.0, 20.0, 22.0, 25.0, 28.0, 32.0, 36.0, 40.0,
45.0, 50.0
```

Units: millimeters

## Keyway Dimensions (DIN 6885)

Standard parallel key sizes based on bore diameter:

| Bore Ø (mm) | Key Width (mm) | Key Height (mm) | Shaft Depth (mm) | Hub Depth (mm) |
|-------------|----------------|-----------------|------------------|----------------|
| 6 - 8       | 2              | 2               | 1.2              | 1.0            |
| 8 - 10      | 3              | 3               | 1.8              | 1.4            |
| 10 - 12     | 4              | 4               | 2.5              | 1.8            |
| 12 - 17     | 5              | 5               | 3.0              | 2.3            |
| 17 - 22     | 6              | 6               | 3.5              | 2.8            |
| 22 - 30     | 8              | 7               | 4.0              | 3.3            |
| 30 - 38     | 10             | 8               | 5.0              | 3.3            |
| 38 - 44     | 12             | 8               | 5.0              | 3.3            |
| 44 - 50     | 14             | 9               | 5.5              | 3.8            |
| 50 - 58     | 16             | 10              | 6.0              | 4.3            |

**Keyway profile**: Parallel sides, radiused bottom (R = key width / 10)

## Worm Geometry Formulas

### Basic Relationships

```
Axial pitch (Pa) = π × module
Lead (L) = axial pitch × num_starts
Pitch diameter (d1) = module × reference_diameter_factor

Reference diameter factor typically:
  - For single start (z1=1): ~12-20 (depends on ratio)
  - For multi-start: scales with starts
```

### Thread Profile (Trapezoidal)

```
Addendum (ha) = module × (1.0 + profile_shift)
Dedendum (hf) = module × (1.0 + clearance_factor - profile_shift)
Clearance factor = 0.25 (typical)

Tip diameter (da) = pitch_diameter + 2 × addendum
Root diameter (df) = pitch_diameter - 2 × dedendum

Thread thickness at pitch line = axial_pitch / 2
Flank angle = pressure_angle (typically 20°)
```

### Profile Shift

```
Profile shift coefficient: x (dimensionless)
  x > 0: positive shift (increases addendum, decreases dedendum)
  x < 0: negative shift (decreases addendum, increases dedendum)
  x = 0: standard tooth

Typical range: -0.5 to +0.8

Purpose: Prevent undercut on low tooth count gears
Calculation: See calculator validation module
```

### Lead Angle

```
tan(γ) = lead / (π × pitch_diameter)

Where:
  γ = lead angle

Practical ranges:
  γ < 1°   - Too shallow (manufacturing issues)
  γ = 1-3° - Very low efficiency (~40-50%), strong self-locking
  γ = 3-5° - Low efficiency (~50-65%), self-locking
  γ = 5-15° - Medium efficiency (~65-85%), may self-lock
  γ > 15°  - High efficiency (~85-95%), not self-locking
  γ > 45°  - Impractical geometry
```

## Wheel Geometry Formulas

### Basic Relationships

```
Transverse module = axial module (for worm gears)
Pitch diameter (d2) = module × num_teeth
Centre distance (a) = (d1 + d2) / 2

Helix angle (β) = 90° - lead_angle
```

### Tooth Dimensions

```
Addendum (ha) = module × (1.0 + profile_shift)
Dedendum (hf) = module × (1.0 + clearance_factor - profile_shift)

Tip diameter (da) = pitch_diameter + 2 × addendum
Root diameter (df) = pitch_diameter - 2 × dedendum

Throat diameter (dg) = tip_diameter (approximately)
  More exactly: dg = da + module × 0.5 (for good wrap)
```

### Face Width

```
Recommended face width (b):
  For single-start worm: b ≈ 0.73 × d1^(1/3) × (ratio)^(1/2)

Practical minimum: b ≥ 0.3 × d1
Practical maximum: b ≤ 0.67 × d1

This ensures adequate contact area while avoiding excessive overhang.
```

## Assembly Geometry

### Centre Distance

```
Centre distance (a) = (worm_pitch_diameter + wheel_pitch_diameter) / 2

Tolerance: Typically ±0.02 to ±0.05 mm
Too tight: Binding, excessive wear
Too loose: Backlash, noise
```

### Backlash

```
Normal backlash allowance: 0.02 - 0.10 mm

Applied as:
  - Reduce worm thread thickness by backlash
  - Increase wheel tooth space by backlash

Effect on geometry:
  - Worm: Reduce addendum slightly (backlash / 2)
  - Wheel: Increase dedendum slightly (backlash / 2)
```

### Hand (Thread Direction)

```
Right-hand worm:
  - Looking along worm axis, thread rises to the right
  - Helix rotation: clockwise when advancing away from viewer

Left-hand worm:
  - Looking along worm axis, thread rises to the left
  - Helix rotation: counter-clockwise when advancing away from viewer

Critical: Wheel helix must match worm hand for correct mesh
```

## Efficiency and Self-Locking

### Efficiency Formula

```
η = tan(γ) / tan(γ + ρ)

Where:
  η = efficiency (0-1)
  γ = lead angle (radians)
  ρ = friction angle = atan(μ / cos(α))
  μ = friction coefficient (0.03-0.08 typical for lubricated bronze/steel)
  α = pressure angle (radians)
```

### Self-Locking Threshold

```
Conservative: γ < 6° is self-locking
Depends on: Materials, lubrication, load direction, surface finish

Self-locking means: Worm can drive wheel, but wheel cannot drive worm
(Torque reversal is resisted by friction)
```

## Validation Thresholds (from Calculator)

| Rule | Threshold | Severity | Rationale |
|------|-----------|----------|-----------|
| Lead angle < 1° | Too low | Error | Manufacturing difficulty |
| Lead angle 1-3° | Very low | Warning | Low efficiency |
| Lead angle > 25° | High | Warning | Not self-locking |
| Lead angle > 45° | Too high | Error | Impractical |
| Module < 0.3mm | Too small | Error | Precision limits |
| Wheel teeth < 17 | Too few | Error | Severe undercut |
| Wheel teeth 17-24 | Low | Warning | Potential undercut |
| Worm pitch_dia < 3×module | Too thin | Error | Strength issues |

These are engineering rules, not hard geometry constraints. The geometry generator should accept any parameters from the calculator.

## Manufacturing Tolerances

### Recommended Tolerances (for CNC)

```
Diameters:
  - Outside diameter: ±0.02 mm (IT6/IT7)
  - Pitch diameter: Reference only (verify by tooth contact)
  - Root diameter: +0.05/-0 mm (clearance side loose)

Lengths:
  - Worm length: ±0.1 mm
  - Wheel face width: ±0.1 mm

Angles:
  - Lead angle: ±0.5° (verify by helix measurement)
  - Pressure angle: ±0.5° (controlled by cutter/model)

Positions:
  - Centre distance: ±0.02 mm (adjustable by shims in assembly)
  - Keyway position: ±0.1° (angular)

Surface Finish:
  - Thread flanks: Ra 1.6 μm (improves efficiency)
  - Tooth flanks: Ra 1.6 μm
  - Bores: Ra 3.2 μm (general machined)
```

## Material Considerations (Not Modeled, but Context)

**Typical combinations:**
- **Worm**: Hardened steel (58-62 HRC)
- **Wheel**: Phosphor bronze, aluminum bronze

**Why**: Hard worm reduces wear, soft wheel conforms and prevents damage

**Geometry implication**: The STEP files don't specify material, but manufacturing specs should note the intended pairing.

## References

1. **DIN 3975** - Definitions and parameters of cylindrical worm gears
2. **DIN 3996** - Calculation of load capacity of cylindrical worm gears
3. **ISO 54** - Modules for cylindrical gears
4. **ISO 6885** - Parallel keys and their keyways
5. **Machinery's Handbook** - Section on worm gearing (general reference)

---

**Note**: This document provides context. The actual dimensions come from the calculator's JSON output, which has already applied these formulas and validations.
