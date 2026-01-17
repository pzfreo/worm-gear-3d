# Examples

## Sample Design Files

### sample_m2_ratio30.json

Example output from the wormgearcalc (Tool 1):
- Module: 2.0 mm (ISO 54 standard)
- Ratio: 30:1
- Worm: 1-start
- Wheel: 30 teeth
- Centre distance: 38.145 mm

## Python API Examples

### generate_pair.py

Demonstrates using the Python API to generate a worm gear pair:

```bash
cd examples
python3 generate_pair.py
```

This will create:
- `worm.step` - Worm geometry
- `wheel.step` - Wheel geometry

### view_design.py

Interactive viewer script using OCP viewer (requires VS Code extension):

```bash
cd examples
python3 view_design.py sample_m2_ratio30.json
```

Options:
```bash
# View only the worm
python3 view_design.py sample_m2_ratio30.json --part worm

# View only the wheel
python3 view_design.py sample_m2_ratio30.json --part wheel

# Custom dimensions
python3 view_design.py sample_m2_ratio30.json --worm-length 50 --wheel-width 12
```

### visualize.ipynb

Jupyter notebook for interactive visualization and experimentation:

```bash
jupyter notebook visualize.ipynb
```

The notebook demonstrates:
- Loading designs from JSON
- Building and visualizing parts
- Viewing worm and wheel together
- Exporting to STEP files

## CLI Usage

### Basic generation

Generate both worm and wheel from a design file:

```bash
wormgear-geometry sample_m2_ratio30.json
```

### Custom parameters

Specify worm length and wheel width:

```bash
wormgear-geometry sample_m2_ratio30.json --worm-length 50 --wheel-width 12
```

### Output directory

Save to specific directory:

```bash
wormgear-geometry sample_m2_ratio30.json -o ~/my_gears/
```

### Generate only worm or wheel

```bash
# Worm only
wormgear-geometry sample_m2_ratio30.json --worm-only

# Wheel only
wormgear-geometry sample_m2_ratio30.json --wheel-only
```

## Visualization Options

### OCP Viewer (Recommended for Development)

For interactive visualization in VS Code or Jupyter:

1. **Install VS Code extension**: OCP CAD Viewer
2. **Install Python package**: `pip install ocp-vscode`
3. **Use the viewer**:
   ```python
   from wormgear_geometry import WormGeometry
   worm_geo = WormGeometry(params, assembly_params, length=40)
   worm_geo.show()  # Opens in OCP viewer
   ```

### Using Generated STEP Files

The generated STEP files can be imported into:
- **FreeCAD** - Free, open-source CAD
- **Fusion 360** - Autodesk CAD/CAM
- **SolidWorks** - Professional CAD
- **OnShape** - Cloud-based CAD
- **Any CAM software** for CNC toolpath generation

## Next Steps

1. Import STEP files into your CAD software
2. Verify dimensions match the design
3. Check that worm and wheel mesh correctly
4. Generate toolpaths for CNC manufacturing
5. Consider adding features (bores, keyways) if needed

## Getting Design Files

Create custom designs using the calculator:
- **Web Calculator**: https://pzfreo.github.io/wormgearcalc/
- **Python Library**: https://github.com/pzfreo/wormgearcalc

Export the design as JSON and use it with this geometry generator.
