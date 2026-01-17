# Worm Gear Geometry Generator

**Status: Phase 1 complete - basic geometry generation working**

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

## Features

### Phase 1: Basic Geometry ✓ Complete
- [x] JSON input from wormgearcalc
- [x] Worm thread generation (helical sweep with trapezoidal profile)
- [x] Wheel generation (hybrid: helical gear + throat cut)
- [x] STEP export
- [x] Python API
- [x] Command-line interface
- [x] OCP viewer support (VS Code / Jupyter)
- [x] Multi-start worm support
- [x] Profile shift support
- [x] Backlash handling

### Phase 2: Features (Next)
- [ ] Bore with tolerances
- [ ] Keyways (ISO 6885 standard)
- [ ] Set screw holes
- [ ] Hub options (flush/extended/flanged)

### Phase 3: Advanced (Future)
- [ ] Envelope calculation for wheel (mathematical accuracy)
- [ ] Assembly positioning
- [ ] Manufacturing specs output (markdown)

## Installation

```bash
pip install build123d
pip install -e .

# Optional: For visualization in VS Code
pip install ocp-vscode
```

## Usage

### Command Line

```bash
# Generate both worm and wheel from calculator JSON
wormgear-geometry design.json

# Specify output directory
wormgear-geometry design.json -o output/

# Custom dimensions
wormgear-geometry design.json --worm-length 50 --wheel-width 12

# Generate only worm or wheel
wormgear-geometry design.json --worm-only
wormgear-geometry design.json --wheel-only
```

### Python API

```python
from wormgear_geometry import load_design_json, WormGeometry, WheelGeometry

# Load parameters from calculator
design = load_design_json("design.json")

# Build and export worm
worm_geo = WormGeometry(
    params=design.worm,
    assembly_params=design.assembly,
    length=40  # mm
)
worm_geo.export_step("worm.step")

# Build and export wheel
wheel_geo = WheelGeometry(
    params=design.wheel,
    worm_params=design.worm,
    assembly_params=design.assembly
)
wheel_geo.export_step("wheel.step")
```

### Visualization (OCP Viewer)

```python
# Display in VS Code with OCP CAD Viewer extension
worm_geo.show()  # Opens worm in viewer
wheel_geo.show()  # Opens wheel in viewer

# Or use the viewer script
python examples/view_design.py design.json
```

See `examples/` directory for more usage patterns.

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
