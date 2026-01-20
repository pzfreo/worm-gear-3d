# Worm Gear Design Tool - Unified Web Interface Specification

**Version:** 2.0 (Integrated Calculator + 3D Generator)
**Status:** Design specification for implementation
**Goal:** Single integrated tool that replaces wormgearcalc and provides 3D CAD generation

---

## Vision

A complete worm gear design solution in the browser:
- **Engineers** design using standard parameters (module, angles)
- **Makers** design from envelope constraints (what fits)
- **Everyone** gets validated parameters + CNC-ready STEP files
- **No installation** required - runs entirely in browser via WebAssembly

---

## Core Principle

**Guide users from design intent → validated parameters → manufacturing-ready CAD files with clear feedback at every step.**

---

## Two Main Design Paths

### Path A: Standard Engineering Approach ⚙️

**For:** Engineers familiar with standard gear terminology
**Starting Point:** Module, ratio, pressure angle
**Use Case:** "I want an M2, 30:1 worm gear with 20° pressure angle"

**Flow:**
```
1. Select "Standard Design (Module-Based)"
   ↓
2. Enter standard parameters:
   • Module (ISO 54 standard)
   • Ratio
   • Pressure angle
   • Optional: Number of starts, backlash, hand
   ↓
3. Calculator computes:
   • All derived dimensions (ODs, pitch diameters, etc.)
   • Efficiency estimate
   • Self-locking analysis
   • Validation warnings
   ↓
4. Manufacturing options:
   • Worm length
   • Wheel face width
   • Wheel type (helical vs hobbed)
   • Bore diameter
   • Keyway (DIN 6885)
   ↓
5. Generate STEP files + design JSON
```

**Minimum Required Inputs:**
- Module (mm)
- Ratio (integer)

**Optional Inputs:**
- Pressure angle (default: 20°)
- Number of starts (default: 1)
- Backlash (default: 0mm)
- Hand (default: right)
- Profile shift coefficient (default: 0)

---

### Path B: Envelope Constraint Approach 📐

**For:** Makers/luthiers/designers with space constraints
**Starting Point:** Maximum ODs, ratio
**Use Case:** "I need 30:1 that fits in a 20mm worm × 65mm wheel envelope"

**Flow:**
```
1. Select "Design from Constraints (Envelope)"
   ↓
2. Enter constraints:
   • Worm max OD
   • Wheel max OD
   • Ratio
   • Optional: pressure angle, starts, backlash
   ↓
3. Calculator proposes:
   • Module that fits (may suggest rounding to ISO 54)
   • All computed dimensions
   • Efficiency estimate
   • Self-locking analysis
   • Warnings if constraints conflict
   ↓
4. User reviews/accepts or adjusts constraints
   ↓
5. Manufacturing options (same as Path A)
   ↓
6. Generate STEP files + design JSON
```

**Minimum Required Inputs:**
- Worm max OD (mm)
- Wheel max OD (mm)
- Ratio (integer)

**Optional Inputs:**
- Pressure angle (default: 20°)
- Number of starts (default: 1)
- Backlash (default: 0mm)
- Hand (default: right)
- Round to standard module (default: yes)

---

## Path C: Import Existing Design 📁

**For:** Reproducible builds, iteration, version control
**Use Case:** "I have a proven design JSON, just regenerate the CAD"

**Flow:**
```
1. Select "Import Design"
   ↓
2. Load JSON:
   • Drag-drop file
   • Paste JSON text
   • URL parameter (?design=...)
   ↓
3. Show design summary
   ↓
4. Optional: Override manufacturing params
   • Worm length, wheel width, bore, keyway
   ↓
5. Generate STEP files
```

---

## User Interface - Landing Page

```
┌─────────────────────────────────────────────────────────────────┐
│  🔩 Worm Gear Design Tool                                       │
│  Design → Validate → Generate CNC-Ready STEP Files             │
└─────────────────────────────────────────────────────────────────┘

Choose how to start:

┌─────────────────────────────────────────────┐
│ ⚙️  Standard Engineering Design             │
│                                              │
│ Start with module and standard parameters   │
│ Traditional gear engineering approach       │
│                                              │
│ Best for: Engineers, standard applications  │
│                                              │
│          [Start with Module] ────────────►  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 📐 Design from Envelope Constraints         │
│                                              │
│ I know what size it needs to be             │
│ Calculator proposes valid designs           │
│                                              │
│ Best for: Space-constrained applications    │
│                                              │
│          [Design from ODs] ──────────────►  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 📁 Import Existing Design                   │
│                                              │
│ Load JSON from previous design              │
│ Reproducible builds                         │
│                                              │
│ Best for: Regenerating proven designs       │
│                                              │
│          [Import JSON] ──────────────────►  │
└─────────────────────────────────────────────┘

───────────────────── or ─────────────────────

┌─────────────────────────────────────────────┐
│ 📚 Example Gallery                          │
│                                              │
│ Browse preset designs with descriptions     │
│                                              │
│ • Guitar tuning machine (7mm, 12:1)        │
│ • Light duty drive (M2, 30:1)              │
│ • High ratio reducer (M3, 60:1)            │
│                                              │
│          [Browse Examples] ──────────────►  │
└─────────────────────────────────────────────┘
```

---

## Detailed UI Flow - Path A (Standard)

### Step 1: Standard Parameters Input

```
┌────────────────────────────────────────────────────┐
│ Standard Engineering Design                        │
├────────────────────────────────────────────────────┤
│                                                     │
│ Required Parameters                                │
│                                                     │
│ Module (mm):      [_2.0__] ⓘ ISO 54 standard      │
│                   Common: 0.5, 1.0, 1.5, 2.0, 3.0  │
│                                                     │
│ Gear Ratio:       [__30__] : 1                     │
│                                                     │
│ ────────────────────────────────                   │
│                                                     │
│ Optional Parameters (click to expand)              │
│ ▼ Advanced Options                                 │
│                                                     │
│   Pressure Angle:  [_20°_] ⓘ Standard: 20° or 25°│
│   Number of Starts: [__1__]                        │
│   Backlash:        [_0.0_] mm                      │
│   Hand:            [Right ▼]                       │
│   Profile Shift:   [_0.0_]                         │
│                                                     │
│   [☐] Prefer standard diameter quotient (DIN 3975)│
│       ⓘ Adjusts design to use q = 8, 10, 12.5, etc.│
│                                                     │
│             [Calculate Design] ─────────►          │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Input Validation (Real-time):**
- Module: Must be > 0.3mm (warn if non-standard ISO 54)
- Ratio: Must be integer ≥ 2
- Pressure angle: Typical 14.5°, 20°, 25°
- Starts: Integer 1-4 (more is unusual)

---

### Step 2: Calculation Results & Validation

```
┌────────────────────────────────────────────────────┐
│ Design Results                                      │
├────────────────────────────────────────────────────┤
│                                                     │
│ ✓ Design Valid                                     │
│                                                     │
│ ═══ Worm ═══                                       │
│ Tip diameter (OD):   20.00 mm                      │
│ Pitch diameter:      16.00 mm                      │
│ Root diameter:       11.00 mm                      │
│ Lead:                6.28 mm (1 start)             │
│ Lead angle:          7.1°                          │
│ Diameter quotient:   8.0 (q = d₁/m) ✓ DIN 3975    │
│                                                     │
│ ═══ Wheel ═══                                      │
│ Tip diameter (OD):   64.00 mm                      │
│ Pitch diameter:      60.00 mm                      │
│ Root diameter:       55.00 mm                      │
│ Throat diameter:     62.00 mm                      │
│ Teeth:               30                            │
│ Helix angle:         82.9°                         │
│                                                     │
│ ═══ Assembly ═══                                   │
│ Centre distance:     38.00 mm                      │
│ Efficiency (est):    72%                           │
│ Self-locking:        No                            │
│                                                     │
│ ⚠️  1 Warning:                                     │
│ • Low lead angle (7.1°) - efficiency only 72%.    │
│   Consider increasing to 10-15° for better         │
│   efficiency, or accept for self-locking benefit.  │
│                                                     │
│         [Adjust Parameters]  [Continue to 3D] ──►  │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Validation Display:**

- ✓ **Valid** (green) - No errors, safe to proceed
- ⚠️ **Warnings** (yellow) - Valid but suboptimal, show advice
- ❌ **Errors** (red) - Invalid, must fix before proceeding

**Common Warnings:**
- Lead angle < 3°: "Very inefficient, only ~50% efficiency"
- Lead angle > 25°: "Not self-locking - needs brake/lock"
- Module non-standard: "Module 2.3mm not ISO 54 - prefer 2.0mm or 2.5mm"
- Wheel teeth < 24: "Risk of undercut - verify with CAD"

**Common Errors:**
- Lead angle < 1°: "Impractical - too steep, increase module or starts"
- Worm pitch dia < 3×module: "Worm shaft too weak"
- Wheel teeth < 17: "Severe undercut - impossible to manufacture"

---

### Step 3: Manufacturing Parameters

```
┌────────────────────────────────────────────────────┐
│ Manufacturing Options                               │
├────────────────────────────────────────────────────┤
│                                                     │
│ Worm Dimensions                                    │
│                                                     │
│ Length:           [__40__] mm                      │
│                   ⓘ Minimum for full engagement:   │
│                     ~15mm (suggested: 30-50mm)     │
│                                                     │
│ Bore:             [Auto: 4.0mm ▼]                  │
│                   • Auto (~25% of pitch dia)       │
│                   • Custom diameter                │
│                   • No bore (solid)                │
│                                                     │
│ Keyway:           [☑] DIN 6885 (auto-sized)       │
│                   ⓘ 4mm bore: no keyway available  │
│                     (DIN 6885 requires ≥6mm)       │
│                                                     │
│ ─────────────────────────────────────              │
│                                                     │
│ Wheel Dimensions                                   │
│                                                     │
│ Face Width:       [Auto: 12mm ▼]                   │
│                   ⓘ Suggested: 0.7 × worm OD       │
│                     (calculated: 14mm)             │
│                                                     │
│ Tooth Type:       ( ) Helical (simple)             │
│                   (•) Hobbed (throated) [Recommended]│
│                   ⓘ Hobbed provides better contact │
│                                                     │
│ Bore:             [Auto: 15mm ▼]                   │
│ Keyway:           [☑] DIN 6885 (5×2.3mm)          │
│                                                     │
│         [Generate STEP Files] ─────────►           │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Auto-Calculations (shown as defaults):**
- Worm length: 40mm (user should specify based on shaft needs)
- Worm bore: ~25% of pitch diameter, rounded to nice value
- Wheel bore: ~25% of pitch diameter
- Wheel face width: ~0.7 × worm OD (based on standard practice)
- Keyway: DIN 6885 auto-sized from bore (if bore ≥ 6mm)

**Thin Rim Warning:**
If auto-bore results in rim < 1.5mm:
```
⚠️ Thin rim on small bore - handle with care
Worm: 2.0mm bore, rim thickness 1.38mm
```

---

### Step 4: Generation & Download

```
┌────────────────────────────────────────────────────┐
│ Generating Geometry...                              │
├────────────────────────────────────────────────────┤
│                                                     │
│ [████████████████░░░░] 80%                        │
│                                                     │
│ Building wheel (hobbed, 30 teeth)...               │
│                                                     │
└────────────────────────────────────────────────────┘

↓ After completion ↓

┌────────────────────────────────────────────────────┐
│ ✅ Generation Complete!                            │
├────────────────────────────────────────────────────┤
│                                                     │
│ Download Files:                                    │
│                                                     │
│ 📥 [worm_m2_z1_r30.step]         (16 KB)          │
│ 📥 [wheel_m2_z30_r30_hobbed.step] (1.1 MB)        │
│ 📥 [design.json]                  (2 KB)           │
│                                                     │
│ ─────────────────────────────────────              │
│                                                     │
│ Design Summary                                     │
│                                                     │
│ Module: 2.0mm (ISO 54)                             │
│ Ratio: 30:1                                        │
│ Centre distance: 38.00mm (±0.05mm)                 │
│ Efficiency: 72%                                    │
│ Self-locking: No                                   │
│                                                     │
│ Worm:  Ø20mm × 40mm, bore 4mm, no keyway          │
│ Wheel: Ø64mm × 12mm, bore 15mm, keyway 5×2.3mm   │
│                                                     │
│ ⓘ Assembly Notes:                                  │
│ • Axes must be perpendicular (90°)                │
│ • Lubrication required                             │
│ • Verify alignment within ±0.1mm                  │
│                                                     │
│      [Design Another]  [Adjust & Regenerate]       │
│                                                     │
└────────────────────────────────────────────────────┘
```

---

## Detailed UI Flow - Path B (Envelope Constraints)

### Step 1: Constraint Input

```
┌────────────────────────────────────────────────────┐
│ Design from Envelope Constraints                   │
├────────────────────────────────────────────────────┤
│                                                     │
│ What space do you have?                            │
│                                                     │
│ Worm Max OD:      [__20__] mm                      │
│                   ⓘ Outside diameter constraint    │
│                                                     │
│ Wheel Max OD:     [__65__] mm                      │
│                   ⓘ Outside diameter constraint    │
│                                                     │
│ Gear Ratio:       [__30__] : 1                     │
│                                                     │
│ ────────────────────────────────                   │
│                                                     │
│ ▼ Options                                          │
│                                                     │
│   Pressure Angle:  [_20°_]                         │
│   Number of Starts: [__1__]                        │
│   Backlash:        [_0.0_] mm                      │
│   Hand:            [Right ▼]                       │
│                                                     │
│   [☑] Round to standard module (ISO 54)           │
│       ⓘ Recommended for manufacturability          │
│                                                     │
│        [Calculate Proposed Design] ─────────►      │
│                                                     │
└────────────────────────────────────────────────────┘
```

---

### Step 2: Proposed Design with Constraint Feedback

**Scenario A: Design fits cleanly**

```
┌────────────────────────────────────────────────────┐
│ Proposed Design (fits constraints)                 │
├────────────────────────────────────────────────────┤
│                                                     │
│ ✓ Valid design found                               │
│                                                     │
│ Calculated Module: 2.05mm                          │
│ → Rounded to: 2.0mm (ISO 54 standard)             │
│                                                     │
│ ═══ Worm ═══                                       │
│ Tip diameter:   20.00 mm  (max: 20.00) ✓          │
│ Pitch diameter: 16.00 mm                           │
│ Root diameter:  11.00 mm                           │
│ Lead angle:     7.1°                               │
│                                                     │
│ ═══ Wheel ═══                                      │
│ Tip diameter:   64.00 mm  (max: 65.00) ✓          │
│ Pitch diameter: 60.00 mm                           │
│ Root diameter:  55.00 mm                           │
│ Teeth:          30                                 │
│                                                     │
│ ═══ Performance ═══                                │
│ Centre distance: 38.00 mm                          │
│ Efficiency:      72%                               │
│ Self-locking:    No                                │
│                                                     │
│ ⓘ Fits with margin:                                │
│   Worm: 0.0mm margin                               │
│   Wheel: 1.0mm margin                              │
│                                                     │
│    [Adjust Constraints]  [Accept & Continue] ──►   │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Scenario B: Design requires tradeoffs**

```
┌────────────────────────────────────────────────────┐
│ ⚠️  Proposed Design (tight constraints)            │
├────────────────────────────────────────────────────┤
│                                                     │
│ Design found, but constraints conflict             │
│                                                     │
│ Problem:                                           │
│ • Worm OD 20mm is too small for 30:1 ratio        │
│ • Calculated module would be 1.8mm                │
│ • Rounded to 2.0mm ISO 54 → worm OD becomes 20mm  │
│ • This leaves NO margin for error                  │
│                                                     │
│ Suggestions:                                       │
│ → Increase worm OD to 22mm (gives 2mm margin)     │
│ → Reduce ratio to 25:1 (fits in 20mm)            │
│ → Use 1.5mm module (non-standard but fits)        │
│                                                     │
│ Current Calculated Design:                         │
│ Module: 2.0mm (ISO 54)                             │
│ Worm OD: 20.00mm (max: 20.00) ⚠️ at limit         │
│ Wheel OD: 64.00mm (max: 65.00) ✓                  │
│ Efficiency: 72%                                    │
│                                                     │
│    [Adjust Constraints]  [Accept Anyway] ──►       │
│                                                     │
└────────────────────────────────────────────────────┘
```

**Scenario C: Impossible constraints**

```
┌────────────────────────────────────────────────────┐
│ ❌ Cannot fit design in constraints                │
├────────────────────────────────────────────────────┤
│                                                     │
│ The specified constraints are impossible:          │
│                                                     │
│ Problem:                                           │
│ • 30:1 ratio requires module ≥ 1.5mm              │
│ • Module 1.5mm needs worm OD ≥ 18mm               │
│ • Module 1.5mm needs wheel OD ≥ 49.5mm            │
│ • Your wheel OD limit: 45mm ← TOO SMALL           │
│                                                     │
│ To fix, you must either:                           │
│ → Increase wheel OD to ≥ 50mm                     │
│ → Reduce ratio to ≤ 25:1                          │
│ → Accept very small module (weak, not recommended)│
│                                                     │
│           [Adjust Constraints]                      │
│                                                     │
└────────────────────────────────────────────────────┘
```

---

Then continues to Step 3 (Manufacturing) and Step 4 (Generation) same as Path A.

---

## Validation Rules & Messaging

### Validation Severity Levels

**❌ Error (Blocking):**
- Lead angle < 1°
- Module < 0.3mm
- Wheel teeth < 17 (severe undercut)
- Worm diameter quotient q < 3 (shaft too weak)

**⚠️ Warning (Proceed with caution):**
- Lead angle 1-3° (very inefficient)
- Lead angle > 25° (not self-locking, mention need for brake)
- Module non-standard (suggest nearest ISO 54)
- Wheel teeth 17-24 (some undercut risk)
- Worm diameter quotient q < 5 (verify shaft strength)
- Worm diameter quotient q > 20 (very thick, check efficiency)
- Worm diameter quotient q non-standard (suggest nearest DIN 3975: 8, 10, 12.5, 16, 20, 25)
- Rim thickness < 1.5mm (thin rim)

**ℹ️ Info (Helpful context):**
- Efficiency estimate explanation
- Self-locking behavior
- Standard module benefits (ISO 54)
- Standard diameter quotient benefits (DIN 3975)
- Manufacturing notes

### Message Style

**Bad:** "Invalid parameter"

**Good:** "Lead angle 0.8° is too steep - impossible to manufacture. Increase module to 2.0mm or add more starts."

**Bad:** "Warning: low efficiency"

**Good:** "Low efficiency (52%) due to lead angle 3.2°. Increase to 10-15° for typical 70-85% efficiency. Alternatively, accept lower efficiency if self-locking is required."

**Example q validation messages:**

**Error (q < 3):**
"Worm shaft too weak - diameter quotient q=2.8 is below minimum. Increase worm diameter or reduce module to achieve q ≥ 3."

**Warning (q < 5):**
"Worm shaft may be weak - diameter quotient q=4.2 is below recommended minimum of 5. Verify strength calculations or increase worm diameter."

**Info (q non-standard):**
"Diameter quotient q=11.3 is not a DIN 3975 standard value. Nearest standards: q=10 or q=12.5. Check 'Prefer standard q' for automatic adjustment."

---

## Technical Architecture

### Stack

```
┌─────────────────────────────────────────┐
│  Single Page Application (HTML/JS)     │
├─────────────────────────────────────────┤
│  Pyodide 0.25+ (Python in WASM)        │
│  ├─ wormcalc package (calculator)      │
│  ├─ wormgear_geometry (3D generation)  │
│  ├─ build123d + OCP (CAD kernel)       │
│  └─ micropip (package manager)         │
├─────────────────────────────────────────┤
│  UI Framework: Vanilla JS (keep simple)│
│  Styling: CSS (responsive)              │
│  Optional: Three.js for preview         │
└─────────────────────────────────────────┘
```

### Data Flow

```
User Input
    ↓
Calculator (wormcalc)
    ↓
Validation Results + Computed Parameters
    ↓
User confirms/adjusts
    ↓
Add Manufacturing Params
    ↓
3D Geometry Generator (wormgear_geometry)
    ↓
STEP Files + Design JSON
```

### Loading Strategy

1. **Initial page load:** Fast, shows UI immediately
2. **Pyodide init:** Load in background with progress indicator
3. **Package install:** Load wormcalc + wormgear_geometry on first use
4. **Caching:** Cache Pyodide/packages in browser (IndexedDB)
5. **Performance:** Show "Initializing..." only on first visit

---

## File Outputs

### When user clicks "Generate":

**Always:**
1. `worm_mX_zY_rZ.step` - Worm STEP file
2. `wheel_mX_zY_rZ.step` - Wheel STEP file (or `_hobbed`)
3. `design.json` - Complete design parameters (for reproducibility)

**Optional (Phase 2):**
4. `README.txt` - Plain text summary
5. `assembly-notes.md` - Assembly instructions

### design.json structure

Same as current wormgearcalc output:
```json
{
  "worm": { ... },
  "wheel": { ... },
  "assembly": { ... },
  "validation": {
    "valid": true,
    "warnings": [...],
    "errors": []
  },
  "metadata": {
    "design_mode": "from-module",
    "generated_at": "2026-01-20T...",
    "tool_version": "2.0.0"
  }
}
```

---

## Implementation Phases

### Phase 1: Core Integration (MVP) 🎯
- [ ] Integrate wormcalc code into web interface
- [ ] Implement Path A (standard/module-based)
- [ ] Implement Path B (envelope constraints)
- [ ] Implement Path C (JSON import)
- [ ] Connect calculator → 3D generator flow
- [ ] Basic validation UI (errors, warnings, info)
- [ ] Manufacturing parameter controls
- [ ] STEP file download
- [ ] design.json export

### Phase 2: Polish & Usability
- [ ] Example gallery with presets
- [ ] Improved validation messages (actionable)
- [ ] Design summary panel
- [ ] Assembly notes generation
- [ ] Mobile responsive design
- [ ] Loading states & progress indicators
- [ ] Error recovery (retry logic)
- [ ] Share links (URL params with encoded JSON)

### Phase 3: Advanced Features
- [ ] 3D preview (Three.js or model-viewer)
- [ ] Interactive assembly view (rotate worm, see wheel mesh)
- [ ] Manufacturing notes with tolerances
- [ ] PDF export of design summary
- [ ] Offline support (service worker)
- [ ] Batch generation (multiple designs)

### Phase 4: Educational & Pro Features
- [ ] Inline help & tooltips
- [ ] "What's this?" explanations for each parameter
- [ ] Efficiency calculator with graphs
- [ ] Comparison mode (compare 2-3 designs side-by-side)
- [ ] Design optimization suggestions
- [ ] Material recommendations
- [ ] Cost estimation (material + machining time)

---

## Open Design Questions

### 1. Module Input - Dropdown vs Freeform?

**Option A: Dropdown with standards**
```
Module: [2.0mm (ISO 54) ▼]
        Options: 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0
        Or: [Custom value...]
```

**Option B: Freeform with suggestion**
```
Module: [__2.0__] mm
        ⓘ Standard values (ISO 54): 0.5, 1.0, 1.5, 2.0, 2.5, 3.0...
        [Suggest nearest standard]
```

**Recommendation:** Option A for Path A (standard), Option B for Path B (constraints may yield non-standard)

---

### 2. How to handle "Accept Anyway" for warnings?

When design has warnings but user wants to proceed:

**Option A: Require explicit acknowledgment**
```
⚠️ This design has 2 warnings. Proceed anyway?

[☐] I understand the efficiency will be low (52%)
[☐] I understand it's not self-locking

         [Yes, Continue Anyway]
```

**Option B: Just show warnings, allow continue**
```
⚠️ 2 Warnings (click to view)

         [Continue to Manufacturing]
```

**Recommendation:** Option B (trust users, don't add friction). Phase 2 could add Option A for critical errors only.

---

### 3. Manufacturing defaults - Show or hide initially?

**Option A: Always visible**
- Pros: Transparent, user sees everything
- Cons: Overwhelming for beginners

**Option B: Start with "Auto" defaults, click to customize**
```
Manufacturing Options: [Auto ▼]
  When clicked:
  [Custom ▼]
    • Worm length: ...
    • Bore: ...
    • Keyway: ...
```

**Recommendation:** Option B with good defaults. Advanced users expand, beginners click "Generate" with auto settings.

---

### 4. 3D Preview - Essential or Phase 2?

**Arguments for Phase 1:**
- Huge value add - see before generating
- Catch mistakes visually
- Educational (see how gears mesh)

**Arguments for Phase 2:**
- Adds complexity (Three.js, rendering)
- STEP generation already works
- Can iterate on core UX first

**Recommendation:** Phase 2. Get calculator + generator working first, add preview as enhancement.

---

### 5. Mobile Support - How much?

Constraints:
- WebAssembly requires modern browsers
- STEP generation is memory-intensive
- Small screens make complex forms hard

**Proposal:**
- Phase 1: Desktop-first (works on mobile but not optimized)
- Phase 2: Responsive design (smaller forms, touch-friendly)
- Phase 3: Mobile-specific simplifications (wizard-style for small screens)

---

## Success Metrics

The tool succeeds when:

1. **95% of users** complete their first design without errors
2. **Engineers validate output** - STEP files import cleanly to CAD/CAM
3. **Fast iteration** - Tweak params → new STEP in <60 seconds
4. **Clear traceability** - Every STEP regenerable from design.json
5. **Useful feedback** - Validation messages help fix issues
6. **Replaces both tools** - wormgearcalc can be retired

---

## Migration from wormgearcalc

### Compatibility

- Accept existing wormgearcalc JSON without changes
- Support URL params from wormgearcalc links
- Provide redirect from old tool to new

### Deprecation Plan

1. **Month 1-2:** Build new integrated tool
2. **Month 3:** Soft launch, link from wormgearcalc
3. **Month 4:** Add banner to wormgearcalc: "Try the new version!"
4. **Month 5:** Default to new tool, old tool at /legacy
5. **Month 6+:** Redirect old tool to new, archive old code

---

## Next Steps

1. **Review this spec** - Validate approach with Paul
2. **Wireframe key screens** - Especially validation results, error states
3. **Start with Path A** - Standard design is simpler, build confidence
4. **Iterate on UX** - Get validation messaging right
5. **Add Path B** - Envelope constraints (reuse wormcalc logic)
6. **Polish & ship** - Example gallery, share links, etc.

---

**Ready to build when design is validated!**
