# Implementation TODO

## Phase 1: Basic Geometry (Start Here)

### Setup
- [x] Project structure created
- [x] Documentation extracted
- [ ] Install build123d and test basic operations
- [ ] Create test fixture for sample JSON

### Worm Implementation (worm.py)
- [ ] Create dataclass for worm parameters
- [ ] Implement basic cylinder (core)
- [ ] Create trapezoidal tooth profile
  - Use pressure angle for flank angle
  - Apply profile shift if present
- [ ] Generate helix path at pitch radius
  - Account for lead and hand (right/left)
- [ ] Sweep profile along helix
- [ ] Union with core, trim to length
- [ ] Export to STEP and validate in CAD software

### Wheel Implementation (wheel.py) - Hybrid Approach
- [ ] Create dataclass for wheel parameters
- [ ] Implement basic helical involute gear
  - Match helix angle to worm lead angle
  - Use transverse module = axial module
- [ ] Create throating cylinder
  - Position at worm tip radius + clearance
  - Oriented perpendicular to wheel axis
  - Positioned at centre distance
- [ ] Boolean subtract throat from gear
- [ ] Export to STEP and validate

### Testing
- [ ] Test worm STEP export (reimport, check volume)
- [ ] Test wheel STEP export (reimport, check volume)
- [ ] Test pair together (check centre distance, no interference)
- [ ] Import to CAM software, verify toolpaths

## Phase 2: Features

### I/O Module (io.py)
- [ ] Implement `load_design_json()` function
- [ ] Parse JSON from calculator
- [ ] Validate required fields present
- [ ] Return structured dataclasses

### Features Module (features.py)
- [ ] Implement `BoreFeatures` dataclass
  - Through bore
  - Counterbore option
- [ ] Implement bore cutting function
  - Cylinder subtraction
  - Validate clearances

- [ ] Implement `KeywayFeatures` dataclass
  - Auto-select from DIN 6885 table based on bore
  - Manual override option
- [ ] Implement keyway cutting function
  - Rectangular profile with radiused bottom
  - Position: top dead center by default

- [ ] Implement `SetScrewFeatures` dataclass
  - Thread size (M3, M4, M5, etc.)
  - Angle from keyway
- [ ] Implement set screw hole function
  - Pilot hole for tap size
  - Depth based on thread size

### Integration
- [ ] Add features to `WormGeometry.build()`
- [ ] Add features to `WheelGeometry.build()`
- [ ] Test combined geometry (gear + bore + keyway + set screw)

## Phase 3: Polish

### Assembly (assembly.py)
- [ ] Position worm and wheel at correct centre distance
- [ ] Orient based on hand (right/left)
- [ ] Export as assembly STEP (named components)
- [ ] Test in CAD assembly viewer

### Manufacturing Specs (specs.py)
- [ ] Generate markdown spec from parameters
- [ ] Include dimensions with tolerances
- [ ] Include material recommendations
- [ ] Include surface finish requirements

### CLI (cli.py)
- [ ] Basic command: `wormgear-geometry design.json`
- [ ] Options for features (--bore, --keyway, etc.)
- [ ] Options for worm length
- [ ] Output directory specification
- [ ] Assembly vs individual parts option

## Phase 4: Advanced (Future)

### Accurate Wheel Envelope
- [ ] Research envelope calculation mathematics
- [ ] Parameterize worm surface S(u, v)
- [ ] Calculate contact curves
- [ ] Generate B-spline surfaces
- [ ] Compare with hybrid approach
- [ ] Document accuracy differences

### Documentation
- [ ] Add docstrings to all functions
- [ ] Create usage examples
- [ ] Add troubleshooting guide
- [ ] Document manufacturing workflows

### Testing
- [ ] Unit tests for all modules
- [ ] Integration tests for full workflow
- [ ] Geometry validation tests
- [ ] Reference designs test suite

## First Steps

1. **Install build123d**:
   ```bash
   pip install build123d
   ```

2. **Test basic operation**:
   ```python
   from build123d import *

   cylinder = Cylinder(radius=10, height=20)
   cylinder.export_step("test.step")
   # Open test.step in FreeCAD/Fusion360 to verify
   ```

3. **Implement simple worm** (just core + one thread):
   - Load sample JSON
   - Extract worm parameters
   - Create core cylinder
   - Create single helical sweep
   - Export and verify

4. **Build from there** following the checklist above

## Questions to Resolve

- [ ] How to handle very fine threads in build123d? (small lead angle)
- [ ] Best approach for helix orientation (ensure profile perpendicular)?
- [ ] Tolerance representation in STEP files?
- [ ] Validation strategy (OCC checker? Volume comparison?)

## References While Implementing

- build123d docs: https://build123d.readthedocs.io/
- py_gearworks source: https://github.com/gumyr/py_gearworks
- DIN 3975 standard (worm geometry definitions)
- GEOMETRY.md in this repo (detailed specification)
