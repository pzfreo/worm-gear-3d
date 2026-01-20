# Worm Gear 3D Generator - Web Tool Specification

## Vision

A browser-based tool that guides engineers and designers from **design intent** → **validated parameters** → **CNC-ready CAD files**, with clear paths for different use cases and skill levels.

---

## Core Principle

**The tool should make it impossible to generate invalid geometry while remaining flexible for experienced users.**

---

## Three Input Methods - Positioning & Purpose

### Method 1: Calculator-First (Recommended Path) ⭐

**Target User:** Engineers designing a new worm gear drive
**Use Case:** "I need a worm gear with X ratio, Y constraints, and proper engineering validation"

**Workflow:**
1. Land on tool → See prominent "Design a New Worm Gear" button
2. Opens integrated calculator interface (or links to wormgearcalc)
3. User specifies:
   - **Design constraints** (ratio, center distance, module, etc.)
   - **Performance requirements** (efficiency, self-locking, etc.)
4. Calculator validates and computes all derived parameters
5. "Send to 3D Generator" button → auto-populates geometry tool with validated JSON
6. User tweaks manufacturing parameters (worm length, wheel width, bore, keyway)
7. Generate STEP files

**Why This is Primary:**
- Guarantees engineering-valid geometry
- Educates users about worm gear design
- Prevents invalid parameter combinations
- Provides efficiency/performance feedback

---

### Method 2: Direct Parameter Entry (Expert Mode)

**Target User:** Experienced users iterating on existing designs
**Use Case:** "I know exactly what I want, just let me type it in quickly"

**Workflow:**
1. Click "Expert Mode: Direct Parameters"
2. Comprehensive form with all parameters visible
3. Real-time validation with clear error messages
4. Tooltips explaining each parameter
5. "Validate Design" button runs engineering checks before generation
6. Shows warnings (not blocking) for unusual but valid combinations
7. Generate STEP files

**When to Use:**
- Tweaking an existing design
- Regenerating from documented parameters
- Educational/experimental use

**Safeguards Needed:**
- Validation against impossible geometry (undercut, interference, etc.)
- Warnings for poor choices (low efficiency, extreme ratios, etc.)
- "This design may not mesh properly" alerts

---

### Method 3: JSON Import (Reproducible Builds)

**Target User:** Engineers with version-controlled designs
**Use Case:** "I have a proven design file, just regenerate the CAD"

**Workflow:**
1. Click "Import Existing Design (JSON)"
2. Drag-drop or paste JSON
3. Tool validates JSON structure and parameters
4. Shows design summary and validation status
5. Allow override of manufacturing parameters (lengths, bore, keyway)
6. Generate STEP files

**When to Use:**
- Regenerating previously validated designs
- Batch processing multiple designs
- Integration with other tools/scripts

---

## Unified Interface Design

### Landing Page - Clear Path Selection

```
┌─────────────────────────────────────────────────────────────┐
│  🔩 Worm Gear 3D Generator                                  │
│  Generate CNC-ready STEP files from validated parameters   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Choose Your Starting Point:                                │
│                                                             │
│  ┌───────────────────────────────────────────────┐         │
│  │ 🎯 Design a New Worm Gear (Recommended)       │         │
│  │                                                │         │
│  │ Start with design requirements (ratio, size)  │         │
│  │ Calculator ensures valid geometry              │         │
│  │                                                │         │
│  │          [Start Design Calculator] ──────────►│         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  ┌───────────────────────────────────────────────┐         │
│  │ ⚡ Quick Generation (Expert Mode)              │         │
│  │                                                │         │
│  │ Enter all parameters directly                  │         │
│  │ For experienced users with known values        │         │
│  │                                                │         │
│  │          [Enter Parameters Directly]           │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  ┌───────────────────────────────────────────────┐         │
│  │ 📁 Import Existing Design                      │         │
│  │                                                │         │
│  │ Load JSON from calculator or previous design  │         │
│  │ Reproducible builds from validated files       │         │
│  │                                                │         │
│  │          [Import JSON File]                    │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features to Add

### 1. Integrated Design Validation

**Before Generation:**
- Geometric validation (no interference, proper clearances)
- Manufacturing feasibility checks
- Performance warnings (efficiency, self-locking, etc.)

**Display as:**
```
✓ Geometry Valid
✓ No Tooth Interference
⚠️ Low Efficiency (62%) - Consider higher lead angle
⚠️ Self-locking (Lead angle 4.8°) - Verify with materials
```

### 2. Design Summary Panel

**Always visible after parameter entry:**
```
┌─────────────────────────────────────┐
│ Design Summary                      │
├─────────────────────────────────────┤
│ Type: Right-hand worm gear          │
│ Ratio: 30:1                         │
│ Module: 2.0 mm (ISO 54)            │
│ Center Distance: 38.1 mm            │
│ Estimated Efficiency: 72%           │
│ Self-Locking: No                    │
│                                     │
│ Worm: Ø20mm × 40mm (1-start)      │
│ Wheel: Ø64mm × 12mm (30 teeth)     │
└─────────────────────────────────────┘
```

### 3. Manufacturing Parameters (Separate Section)

**After design is validated, user sets:**
- Worm length (with suggested minimum)
- Wheel face width (with suggested optimal range)
- Wheel type (Helical vs Hobbed - with explanation)
- Bore diameter and tolerance class
- Keyway (ISO 6885 standard sizes - auto-suggest based on bore)
- Set screw holes (optional)

### 4. Output Package

**When generation completes:**
```
✅ Generation Complete

Downloads:
📥 worm_m2_z1_r30.step (16 KB)
📥 wheel_m2_z30_r30.step (1.1 MB)
📥 design_summary.pdf (includes dimensions, tolerances, BOM)
📥 design_parameters.json (for reproducible builds)

Assembly Instructions:
- Center distance: 38.145 mm (±0.05)
- Alignment: Axes must be 90°
- Lubrication: Required
```

### 5. Educational Content

**Contextual help:**
- "What's the difference between helical and hobbed wheels?"
- "How do I choose the right module?"
- "What does self-locking mean?"
- Link to engineering resources (DIN 3975, etc.)

### 6. Preset Library

**Include proven designs:**
- "Tuning Machine (7mm, 12:1, self-locking)"
- "Light Duty Drive (M2, 30:1, 72% efficiency)"
- "High Ratio Reducer (M3, 60:1)"

Each preset shows:
- Typical application
- Key characteristics
- "Use This Design" or "Customize"

---

## Calculator Integration Options

### Option A: Embedded (Ideal)

Embed the calculator directly in the web tool:
- Single-page application
- No context switching
- Direct parameter flow

### Option B: Deep Linking (Easier Implementation)

Calculator on separate page with:
- "Send to 3D Generator" button
- Exports JSON with special parameter
- 3D tool accepts `?design=<encoded_json>` URL parameter
- Seamless handoff

### Option C: Side-by-Side (Intermediate)

Split-screen view:
- Calculator on left
- Live preview/generation on right
- Update 3D preview as calculator changes

**Recommendation:** Start with Option B (deep linking), migrate to Option A over time.

---

## Technical Requirements

### Validation Engine

Must check:
1. **Geometric validity:**
   - No undercut on wheel teeth
   - Proper clearance between worm and wheel
   - Thread profile feasibility

2. **Manufacturing feasibility:**
   - Can this be made on stated equipment (4-axis vs 5-axis)?
   - Are tolerances achievable?
   - Bore size vs part size ratio

3. **Engineering soundness:**
   - Reasonable efficiency for stated application
   - Safe stress levels (optional, advanced)
   - Proper module selection per ISO 54

### Error Messages - Actionable & Educational

**Bad:** "Invalid parameter"
**Good:** "Wheel has too few teeth (8) for 25° pressure angle - minimum 12 teeth required to avoid undercut. Increase teeth or reduce pressure angle."

**Bad:** "Generation failed"
**Good:** "Lead angle too steep (45°) - worm thread interferes with wheel. Maximum lead angle for this module: 30°. Reduce lead or increase module."

### Performance Monitoring

Track and display:
- Package load time
- Geometry generation time
- Warn if generation will take >2 minutes (suggest using CLI for complex designs)

---

## User Journeys

### Journey 1: First-Time User (Engineering Student)

1. Lands on page → Reads "Design a New Worm Gear"
2. Clicks button → Opens calculator
3. Enters: "I need 30:1 ratio, about 40mm center distance"
4. Calculator suggests: M2 module, shows efficiency (72%)
5. Student reviews, accepts design
6. "Send to 3D Generator" → Parameters auto-fill
7. Sets worm length to 40mm, chooses helical wheel
8. Clicks Generate → Waits 45 seconds
9. Downloads STEP files + design summary PDF
10. Opens in FreeCAD → Sees complete meshed pair

**Success Metric:** Can complete first design without external help

---

### Journey 2: Experienced Machinist (Reproducing a Design)

1. Has JSON file from previous project
2. Clicks "Import Existing Design"
3. Drags JSON file → Tool validates and shows summary
4. Sees familiar design: "M2 30:1 worm gear"
5. Changes worm length from 40mm to 50mm (needs longer shaft)
6. Adds 8mm bore with 3mm keyway
7. Clicks Generate → 45 seconds
8. Downloads STEP files, opens in CAM software
9. Verifies toolpaths, starts machining

**Success Metric:** Can modify and regenerate in <2 minutes

---

### Journey 3: Product Designer (Exploring Options)

1. Needs worm gear for guitar tuning machine
2. Clicks "Design New Worm Gear"
3. Enters rough requirements: "compact, self-locking, ~15:1"
4. Calculator shows several options with tradeoffs:
   - Option A: Self-locking but 58% efficiency
   - Option B: 75% efficiency but not self-locking
5. Chooses Option A (self-locking critical for tuners)
6. Generates 3D files
7. Downloads, imports to Fusion 360
8. Tests fit in assembly
9. Realizes needs different center distance
10. Returns to tool, adjusts in calculator
11. Regenerates quickly

**Success Metric:** Can iterate through 3+ design options in <15 minutes

---

## Success Criteria

The tool is successful when:

1. **95% of users** complete their first generation without errors
2. **Engineers trust the output** - files import cleanly to CAD/CAM software
3. **Clear traceability** - Every STEP file can be regenerated from JSON
4. **Fast iteration** - Parameter tweaks → new STEP files in <60 seconds
5. **Educational value** - Users learn about worm gear engineering through using it
6. **No invalid geometry** - Impossible to generate unmachineable parts

---

## Phased Implementation

### Phase 1: Core UX Improvements (Next)
- [ ] New landing page with clear path selection
- [ ] Design summary panel
- [ ] Manufacturing parameters section (separate from design params)
- [ ] Better validation error messages
- [ ] Preset library (3-5 proven designs)

### Phase 2: Calculator Integration
- [ ] Deep linking from wormgearcalc
- [ ] URL parameter support for JSON import
- [ ] Bidirectional flow (can send back to calculator)

### Phase 3: Enhanced Output
- [ ] Design summary PDF generation
- [ ] Manufacturing specification sheet
- [ ] Export JSON with all settings for reproducibility

### Phase 4: Advanced Features
- [ ] Assembly visualization (show worm + wheel together)
- [ ] Interference checking visualization
- [ ] Manufacturing notes per feature (e.g., "Use ball-nose endmill for throating")
- [ ] Cost estimation (material + machine time)

### Phase 5: Power User Features
- [ ] Batch generation from multiple JSON files
- [ ] API for programmatic access
- [ ] CLI tool for local generation (already exists, needs polish)

---

## Open Questions for Paul

1. **Calculator Integration:** Do you want to:
   - Embed wormgearcalc into this tool?
   - Keep separate and deep-link between them?
   - Rebuild calculator interface in this tool?

2. **Target Audience Priority:**
   - Hobbyist machinists (garage CNC)?
   - Professional mechanical engineers?
   - Students learning gear design?
   - (This affects language, validation strictness, presets)

3. **Manufacturing Focus:**
   - Primarily for CNC machining?
   - Also for 3D printing (would need different tolerances)?
   - Hobbing/gear cutting (traditional manufacturing)?

4. **Validation Philosophy:**
   - Block invalid combinations entirely?
   - Allow with strong warnings?
   - "Unsafe mode" for experts to override?

5. **Documentation Level:**
   - Just dimensions?
   - Include tolerancing (GD&T)?
   - Material recommendations?
   - Assembly instructions?

---

## Technical Architecture Notes

### Keep:
- Pyodide/build123d approach (browser-based, no backend)
- STEP export (industry standard)
- JSON as interchange format

### Consider Adding:
- STL export (for 3D printing / quick preview)
- DXF export (for 2D profiles / CAM setup)
- Assembly STEP (both parts positioned correctly)

### Future Possibilities:
- WebGL 3D preview (before generating STEP)
- Interactive assembly view (rotate worm, see wheel mesh)
- Tooth contact analysis visualization

---

## Next Steps (After Agreement on Spec)

1. **Review & refine this spec** with Paul
2. **Create wireframes** for new landing page and interface
3. **Prioritize Phase 1 features** based on impact vs effort
4. **Implement incrementally** - each PR improves one aspect
5. **Test with real users** - get feedback from machinist community

---

**Goal:** Make this THE tool for custom worm gear generation - trusted, fast, educational, and delightful to use.
