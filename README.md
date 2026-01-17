# Worm Gear Geometry Generator

**Status: Not yet implemented - starter repository**

Python library for generating CNC-ready STEP files from worm gear parameters using build123d.

## Overview

This is **Tool 2** in the worm gear design system. It takes validated parameters from the calculator (Tool 1) and produces exact 3D CAD models for CNC manufacturing.

**Calculator (Tool 1)**: https://github.com/pzfreo/wormgearcalc
**Web Calculator**: https://pzfreo.github.io/wormgearcalc/

## Workflow

```
1. Design in calculator
   https://pzfreo.github.io/wormgearcalc/
   ↓
2. Export JSON parameters
   ↓
3. Generate geometry (this tool)
   python generate_pair.py design.json
   ↓
4. Get STEP files for CNC
   worm_m2_z1.step
   wheel_m2_z30.step
   assembly.step
```

## Target Manufacturing

- **Worm**: 4-axis lathe with live tooling, or 5-axis mill
- **Wheel**: 5-axis mill (true form), or indexed 4-axis with ball-nose finishing

Geometry is exact and watertight - no approximations, no relying on manufacturing process to "fix" the model.

## Planned Features

### Phase 1: Basic Geometry
- [x] Project structure (you are here)
- [ ] Worm thread generation (helical sweep)
- [ ] Wheel generation (hybrid: helical + throat cut)
- [ ] STEP export with validation
- [ ] Basic CLI

### Phase 2: Features
- [ ] Bore with tolerances
- [ ] Keyways (ISO 6885 standard)
- [ ] Set screw holes
- [ ] Hub options (flush/extended/flanged)

### Phase 3: Advanced
- [ ] Envelope calculation for wheel (mathematical accuracy)
- [ ] Assembly positioning
- [ ] Manufacturing specs output (markdown)

## Installation (when ready)

```bash
pip install build123d
pip install -e .
```

## Usage (planned API)

```python
from wormgear_geometry import WormGeometry, WheelGeometry, BoreFeatures

# Load parameters from calculator
params = load_design_json("design.json")

# Build worm
worm = WormGeometry(
    params=params.worm,
    length=40,
    bore=BoreFeatures(diameter=6, keyway=True)
).build()

worm.export_step("worm.step")

# Build wheel
wheel = WheelGeometry(
    params=params.wheel,
    worm_params=params.worm,
    centre_distance=params.assembly.centre_distance,
    bore=BoreFeatures(diameter=10, keyway=True)
).build()

wheel.export_step("wheel.step")
```

## Documentation

- **CLAUDE.md** - Context for Claude Code (AI assistant)
- **docs/GEOMETRY.md** - Full technical specification
- **docs/ENGINEERING_CONTEXT.md** - Standards and formulas

## Dependencies

- **build123d** - Modern Python CAD library
- **OCP** - OpenCascade bindings (via build123d)

## Background

Created for custom worm gear design in luthier (violin making) applications, where standard gears often don't fit unusual envelope constraints. The calculator determines if a design is feasible; this tool makes it manufacturable.

## Author

Paul Fremantle (pzfreo)
Luthier and hobby programmer

## License

MIT (to be added)
