# Worm Gear Calculator - Web Application

Browser-based worm gear calculator using Pyodide to run Python in WebAssembly.

## Quick Start

### Local Testing

**Important**: You MUST use an HTTP server. Opening `index.html` directly (file://) will not work due to CORS restrictions.

Serve the web directory with any HTTP server:

```bash
# Using Python (recommended)
cd web
python3 -m http.server 8000

# Using Node.js
npx serve web

# Using PHP
cd web
php -S localhost:8000
```

Then open http://localhost:8000 in your browser.

**Troubleshooting**: If you get errors about Python files not loading, first visit http://localhost:8000/test.html to diagnose the issue.

### GitHub Pages Deployment

This app is designed to be deployed to GitHub Pages:

1. Push the `web/` directory to your repository
2. Go to repository Settings → Pages
3. Set source to deploy from the `main` branch, `/web` folder
4. Access at `https://pzfreo.github.io/wormgearcalc/`

## Features

- **Four design modes**:
  - Envelope: Design from both ODs
  - From Wheel: Design from wheel OD and target lead angle
  - From Module: Design from standard module
  - From Centre Distance: Design from fixed shaft positions

- **Real-time validation**: Instant feedback on design parameters

- **Export options**:
  - Copy JSON to clipboard
  - Download Markdown file
  - Share link with parameters in URL

- **Progressive enhancement**: Works entirely in the browser, no server required

## Architecture

```
web/
├── index.html       # UI layout and structure
├── app.js           # Pyodide loader and application logic
├── style.css        # Styling and responsive design
├── wormcalc/        # Python calculator package
│   ├── __init__.py  # Package exports
│   ├── core.py      # Design calculations
│   ├── validation.py # Engineering validation rules
│   └── output.py    # JSON/Markdown formatters
└── README.md        # This file
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14.1+
- Edge 90+

Requires WebAssembly support and modern JavaScript features.

## Performance

- **First load**: 5-10 seconds (downloading Pyodide WASM)
- **Subsequent loads**: 1-2 seconds (cached)
- **Calculations**: <1ms (pure Python, no dependencies)

## URL Parameters

Share designs by encoding parameters in the URL:

```
https://pzfreo.github.io/wormgearcalc/?mode=envelope&worm_od=20&wheel_od=65&ratio=30
```

All input parameters can be included for complete design sharing.

## Development

The Python files in `wormcalc/` are copied from `src/wormcalc/` during build. To update:

```bash
# Copy updated Python files
cp src/wormcalc/{__init__.py,core.py,validation.py,output.py} web/wormcalc/

# Commit and push
git add web/
git commit -m "Update web app"
git push
```

## Troubleshooting

### "Loading calculator..." never completes

- Check browser console for errors
- Ensure CDN access to Pyodide (cdn.jsdelivr.net)
- Try clearing browser cache

### Calculations not updating

- Check browser console for Python errors
- Verify all input fields have valid values
- Try refreshing the page

### Export buttons not working

- Copy to clipboard requires HTTPS (works on GitHub Pages)
- Check clipboard permissions in browser settings

## Credits

Created by Paul Fremantle (pzfreo) for designing custom worm gears for CNC manufacture.

Built with:
- [Pyodide](https://pyodide.org/) - Python in WebAssembly
- Pure HTML/CSS/JavaScript - No build tools required
