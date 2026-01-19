# OCP.wasm Installation Status

## Current Issue

The web interface is getting an error when trying to install build123d from the OCP.wasm package repository:

```
ValueError: Unsupported content type: text/html; charset=utf-8
```

**Root Cause:** The package index at `https://yeicor.github.io/OCP.wasm` is returning HTML instead of Python package metadata when queried by micropip.

## What We've Tried

### ✅ Completed
1. Updated to Pyodide v0.29.0 (latest, matches YACV)
2. Followed exact bootstrap pattern from OCP.wasm repository
3. Used `pre=True` parameter for micropip.install()
4. Set proper index URLs with OCP.wasm as priority
5. Fixed file loading paths for both local and deployed versions

### ❌ Still Failing
- Package index queries return HTML (404 or directory listing)
- Cannot install lib3mf, build123d, or OCP from the index
- micropip expects PyPI-format metadata but gets webpage

## Investigation Findings

### From YACV Project
- Uses Pyodide v0.29.0 ✅ (we now match this)
- Installs their own `yacv_server` package which bundles build123d
- Package index at `https://yeicor.github.io/OCP.wasm` worked for them

### From OCP.wasm Repository
- Contains bootstrap code that sets index URLs
- References `https://yeicor.github.io/OCP.wasm` as package index
- Uses Cloudflare worker proxy for some downloads
- Test suite downloads build123d from GitHub and patches it

## Possible Solutions

### Option 1: Direct Wheel Installation (Recommended)
Download pre-built WebAssembly wheels and install them directly:

```javascript
// Instead of using package index, install from direct URLs
await micropip.install('https://github.com/yeicor/OCP.wasm/releases/download/vX.X.X/lib3mf-X.X.X-py3-none-any.whl');
await micropip.install('https://github.com/yeicor/OCP.wasm/releases/download/vX.X.X/cadquery_ocp-X.X.X-cp311-cp311-emscripten_wasm32.whl');
await micropip.install('https://github.com/yeicor/OCP.wasm/releases/download/vX.X.X/build123d-X.X.X-py3-none-any.whl');
```

**Status:** Need to find the actual release URLs or wheel file locations.

### Option 2: Package Index Format Fix
The package index might need a specific URL structure:

```javascript
// Try with /simple/ suffix (standard for PyPI-compatible indexes)
micropip.set_index_urls([
    "https://yeicor.github.io/OCP.wasm/simple",  // Try /simple
    "https://pypi.org/simple"
]);
```

**Status:** Unknown if this path exists.

### Option 3: Build Custom Package Bundle
Create our own package bundle with OCP.wasm:

1. Download OCP.wasm wheels from releases
2. Host them in our own `web/packages/` directory
3. Install from local URLs

**Status:** Would work but requires finding wheel files first.

### Option 4: Contact OCP.wasm Maintainer
The repository maintainer (Yeicor) might know:
- Current status of the package index
- Correct installation method for standalone projects
- Alternative download URLs

**Status:** Could open a GitHub issue.

### Option 5: Alternative: Use YACV's yacv_server
Install their server package which bundles everything:

```javascript
await micropip.install("yacv_server", pre=True);
```

**Status:** Might work but includes extra dependencies we don't need.

## Next Steps

### Immediate (You Can Try)
1. **Test latest commit locally:**
   ```bash
   cd web && python3 serve.py 8000
   ```
   See if Pyodide v0.29.0 helps with the package index

2. **Check browser console** for more detailed error messages

3. **Try manual wheel installation** if you can find the wheel URLs

### Investigation Needed
1. **Check OCP.wasm GitHub Releases:**
   - Look for wheel files in releases
   - Check if there's a different download method

2. **Check GitHub Pages URL:**
   - Visit `https://yeicor.github.io/OCP.wasm/` directly
   - Look for directory structure
   - Check if /simple/ path exists

3. **Review YACV deployment:**
   - Check their live site's network tab
   - See what URLs they actually fetch
   - Check if yacv_server has its own wheel repo

### Alternative Approach
If OCP.wasm proves too difficult, consider:
- Generate STL/GLTF instead of STEP (using pure Python mesh libraries)
- Use server-side generation (defeats the purpose but would work)
- Wait for OCP.wasm maintainer to fix/document the install process

## Files Updated
- `web/index.html` - Pyodide v0.29.0, better error handling
- All file paths work locally and deployed
- Better Python traceback display

## Testing Checklist
When we get it working, verify:
- [ ] Pyodide loads (v0.29.0)
- [ ] micropip available
- [ ] lib3mf installs
- [ ] OCP installs
- [ ] build123d installs
- [ ] Can create Box, Cylinder
- [ ] wormgear_geometry loads
- [ ] Can generate worm
- [ ] Can generate wheel
- [ ] STEP files download

## Resources
- OCP.wasm Repo: https://github.com/yeicor/OCP.wasm
- YACV Repo: https://github.com/yeicor-3d/yet-another-cad-viewer
- Pyodide Docs: https://pyodide.org/
- Package Index Spec: https://peps.python.org/pep-0503/

## Current Commits
- `c80b935` - Fix OCP.wasm installation and file loading paths
- `3b9b86c` - Upgrade to Pyodide v0.29.0 to match YACV

---

**Summary:** We're very close! The infrastructure is all there, we just need to find the correct way to install the WebAssembly packages. This is likely a simple URL format issue or requires direct wheel URLs instead of using the package index.
