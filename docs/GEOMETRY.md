# Worm Gear Geometry Generator - Specification

## Overview

Tool 2 in the worm gear system. Takes validated parameters from the calculator (Tool 1) and generates CNC-ready STEP geometry.

**Status: Not yet implemented**

## Target: CNC Manufacture

The geometry must be exact and watertight - no relying on hobbing to "fix" approximations. Target manufacturing methods:

- **Worm**: 4-axis lathe with live tooling, or 5-axis mill
- **Wheel**: 5-axis mill (true form), or indexed 4-axis with ball-nose finishing

## Relationship to Tool 1

```
Tool 1 (Calculator)          Tool 2 (Geometry)
─────────────────           ─────────────────
Constraints ──► Parameters ──► STEP files
              (JSON export)    
```

Tool 2 accepts JSON output from Tool 1:

```json
{
  "worm": {
    "module_mm": 2.0,
    "num_starts": 1,
    "pitch_diameter_mm": 16.29,
    "tip_diameter_mm": 20.29,
    "root_diameter_mm": 11.29,
    "lead_mm": 6.283,
    "lead_angle_deg": 7.0,
    "addendum_mm": 2.0,
    "dedendum_mm": 2.5,
    "thread_thickness_mm": 3.14
  },
  "wheel": {
    "module_mm": 2.0,
    "num_teeth": 30,
    "pitch_diameter_mm": 60.0,
    "tip_diameter_mm": 64.0,
    "root_diameter_mm": 55.0,
    "throat_diameter_mm": 62.0,
    "helix_angle_deg": 83.0,
    "addendum_mm": 2.0,
    "dedendum_mm": 2.5
  },
  "assembly": {
    "centre_distance_mm": 38.14,
    "pressure_angle_deg": 20.0,
    "backlash_mm": 0.05,
    "hand": "right"
  }
}
```

## Geometry Construction

### Worm

Relatively straightforward - helical sweep of trapezoidal profile.

```python
# Pseudocode
def build_worm(params):
    # 1. Create tooth profile in axial plane (trapezoidal)
    profile = trapezoidal_profile(
        pitch_half_thickness=params.axial_pitch / 4,
        addendum=params.addendum,
        dedendum=params.dedendum,
        pressure_angle=params.pressure_angle
    )
    
    # 2. Create helix path at pitch radius
    helix = Helix(
        pitch=params.lead,
        height=params.length + params.lead,  # Extra for trimming
        radius=params.pitch_radius
    )
    
    # 3. Position profile perpendicular to helix, Y-axis radial
    positioned_profile = orient_to_helix(profile, helix)
    
    # 4. Sweep
    thread = sweep(positioned_profile, helix)
    
    # 5. Add core cylinder
    core = Cylinder(radius=params.root_radius, height=params.length)
    
    # 6. Union and trim to length
    worm = (core + thread).intersect(trim_box)
    
    # 7. Add features (bore, keyway)
    worm = add_features(worm, params.features)
    
    return worm
```

### Worm Wheel - The Challenge

The wheel tooth is NOT a standard involute. It's the envelope of the worm thread surface as the worm rotates.

#### Option A: Simulated Hobbing (Most Accurate)

Simulate the manufacturing process:

```python
def build_wheel_hobbing(params, worm_params):
    # 1. Create blank cylinder
    blank = Cylinder(
        radius=params.tip_radius,
        height=params.face_width
    )
    
    # 2. Create worm cutter (slightly oversized worm)
    cutter = build_worm(worm_params, oversized=True)
    
    # 3. Position at centre distance
    cutter = cutter.translate(Y=centre_distance)
    
    # 4. Simulate hobbing - rotate both at gear ratio
    num_steps = 360 * params.num_teeth  # One step per degree of wheel
    for step in range(num_steps):
        wheel_angle = step / params.num_teeth
        worm_angle = step  # Worm rotates num_teeth times faster
        
        rotated_cutter = cutter.rotate(Z, worm_angle)
        rotated_blank = blank.rotate(wheel_axis, wheel_angle)
        
        blank = blank - rotated_cutter
    
    return blank
```

**Pros**: Geometrically exact
**Cons**: Very slow (thousands of boolean operations)

#### Option B: Envelope Calculation (Mathematical)

Calculate the tooth surface analytically:

```python
def build_wheel_envelope(params, worm_params):
    # 1. Parameterize worm thread surface as S(u, v)
    # u = along helix, v = across tooth flank
    
    # 2. For each wheel rotation angle θ:
    #    - Transform worm surface by rotation about wheel axis
    #    - Find contact curve where surface normal ⊥ relative velocity
    #    - Collect contact points
    
    # 3. Build B-spline surface through contact points
    
    # 4. Create solid from surfaces
```

**Pros**: Cleaner geometry, faster
**Cons**: Complex mathematics, potential for surface discontinuities

#### Option C: Practical Hybrid (Recommended Starting Point)

1. Generate helical gear with correct base parameters
2. Apply throating cut (cylinder at worm tip radius)
3. Document as approximation suitable for CNC

```python
def build_wheel_hybrid(params, worm_params):
    # 1. Build helical gear
    wheel = build_helical_gear(
        module=params.module,
        num_teeth=params.num_teeth,
        helix_angle=params.helix_angle,
        face_width=params.face_width,
        pressure_angle=params.pressure_angle
    )
    
    # 2. Throating cut - cylinder matching worm envelope
    throat_cutter = Cylinder(
        radius=worm_params.tip_radius + clearance,
        height=params.face_width * 2
    )
    throat_cutter = throat_cutter.rotate(X, 90)  # Perpendicular to wheel
    throat_cutter = throat_cutter.translate(Y=centre_distance)
    
    wheel = wheel - throat_cutter
    
    # 3. Add features
    wheel = add_features(wheel, params.features)
    
    return wheel
```

**Pros**: Much simpler, fast, produces functional geometry
**Cons**: Not mathematically exact (but CNC will cut what you give it)

**Recommendation**: Start with Option C, iterate to Option B if accuracy issues arise.

## Feature Options

### Bore

```python
@dataclass
class BoreFeatures:
    diameter: float
    through: bool = True
    counterbore_diameter: Optional[float] = None
    counterbore_depth: Optional[float] = None
```

### Keyway (ISO 6885 / DIN 6885)

```python
@dataclass  
class KeywayFeatures:
    width: Optional[float] = None   # Auto from bore if None
    depth: Optional[float] = None   # Auto from standard
    length: Optional[float] = None  # Through if None
```

Standard keyway sizes (DIN 6885):

| Bore (mm) | Key Width | Key Height | Shaft Depth | Hub Depth |
|-----------|-----------|------------|-------------|-----------|
| 6-8       | 2         | 2          | 1.2         | 1.0       |
| 8-10      | 3         | 3          | 1.8         | 1.4       |
| 10-12     | 4         | 4          | 2.5         | 1.8       |
| 12-17     | 5         | 5          | 3.0         | 2.3       |
| 17-22     | 6         | 6          | 3.5         | 2.8       |

### Set Screw

```python
@dataclass
class SetScrewFeatures:
    thread_size: str = "M4"  # e.g., "M3", "M4", "M5"
    angle_from_keyway: float = 90  # degrees
    depth: Optional[float] = None  # Auto based on thread
```

### Hub

```python
@dataclass
class HubFeatures:
    style: str = "flush"  # flush | extended | flanged
    extended_length: Optional[float] = None
    extended_diameter: Optional[float] = None
    flange_diameter: Optional[float] = None
    flange_thickness: Optional[float] = None
```

## Proposed API

```python
from wormgears import WormGeometry, WheelGeometry, BoreFeatures

# From JSON (Tool 1 output)
params = load_design_json("design.json")

# Build worm
worm_geo = WormGeometry(
    params=params.worm,
    length=40,
    bore=BoreFeatures(diameter=6, keyway=True)
)
worm_part = worm_geo.build()
worm_part.export_step("worm_m2_z1.step")

# Build wheel
wheel_geo = WheelGeometry(
    params=params.wheel,
    worm_params=params.worm,
    centre_distance=params.assembly.centre_distance,
    bore=BoreFeatures(diameter=10, keyway=True, set_screw="M4")
)
wheel_part = wheel_geo.build()
wheel_part.export_step("wheel_m2_z30.step")

# Build assembly (positioned)
assembly = build_assembly(worm_part, wheel_part, params)
assembly.export_step("worm_gear_assembly.step")
```

## Build123d Integration

The geometry generator should integrate with py_gearworks patterns where sensible:

```python
# Similar to py_gearworks
worm.mesh_to(wheel)  # Position at correct centre distance
worm.center_location_top  # For adding features
```

## Output Requirements

### STEP Export

- Watertight solids (no gaps, overlaps)
- Clean topology (no degenerate faces)
- Appropriate precision (suggest 1e-6 tolerance)
- Named bodies/components for assembly

### Manufacturing Specs Sheet

Generate alongside STEP:

```markdown
# Worm - Manufacturing Specification

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Outside Diameter | 20.00 mm | ±0.02 |
| Pitch Diameter | 16.00 mm | Reference |
| Root Diameter | 11.00 mm | +0.05/-0 |
| Length | 40.00 mm | ±0.1 |
| Lead | 6.283 mm | ±0.01 |
| Lead Angle | 7.0° | Reference |
| Thread Hand | Right | - |

Material: [TBD by user]
Surface Finish: Ra 1.6 (thread flanks)
```

## Testing Strategy

1. **Geometry validation**
   - Export STEP, reimport, check volume matches
   - Check for bad faces/edges (OCC validation)
   
2. **Mesh compatibility**
   - Generate pair, check centre distance
   - Verify no interference at assembly

3. **Manufacturing validation**
   - Import to CAM software
   - Check toolpath generation succeeds

## Dependencies

- **build123d** - Core CAD operations
- **OCP** - OpenCascade Python bindings (via build123d)
- **py_gearworks** (optional) - Reference for API patterns

## Implementation Phases

### Phase 1: Basic Geometry
- Worm thread generation (sweep-based)
- Basic wheel (helical + throat cut)
- STEP export validation

### Phase 2: Features
- Bore with tolerances
- Keyways (ISO 6885)
- Set screw holes

### Phase 3: Accurate Wheel
- Envelope calculation
- B-spline surface generation
- Comparison with Phase 1 hybrid

### Phase 4: Polish
- Assembly positioning
- Manufacturing specs output
- Integration with Tool 1
