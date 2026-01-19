# Web Interface Deployment Guide

This guide explains how to deploy the worm gear web interface to various hosting platforms.

## GitHub Pages (Recommended)

The project includes automated GitHub Actions workflow for deployment.

### Automatic Deployment

1. **Enable GitHub Pages** in your repository:
   - Go to Settings → Pages
   - Source: "GitHub Actions"

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Wait for deployment**:
   - Check Actions tab for deployment status
   - Usually takes 2-3 minutes

4. **Access your site**:
   ```
   https://your-username.github.io/worm-gear-3d/
   ```

### Manual Deployment to GitHub Pages

If you prefer manual deployment:

```bash
# Create gh-pages branch
git checkout --orphan gh-pages

# Copy web files
cp -r web/* .
cp -r src .
cp -r examples .
touch .nojekyll

# Commit and push
git add .
git commit -m "Deploy web interface"
git push origin gh-pages
```

Then enable GitHub Pages in Settings → Pages → Source: "gh-pages" branch.

## Local Testing

Always test locally before deploying:

```bash
cd web
python3 serve.py 8000
```

Open http://localhost:8000 and test:
- [ ] Page loads without errors
- [ ] Pyodide initializes successfully
- [ ] OCP.wasm packages install
- [ ] Test build123d button works
- [ ] Can load sample designs
- [ ] Geometry generation works
- [ ] STEP files download correctly

## Other Hosting Options

### Netlify

1. **Connect repository**:
   - Sign in to Netlify
   - "New site from Git"
   - Select your repository

2. **Configure build settings**:
   - Build command: (leave empty)
   - Publish directory: `web`
   - Add environment variable: `NODE_VERSION = 18`

3. **Deploy**:
   - Click "Deploy site"
   - Custom domain (optional): yourname.netlify.app

**Netlify configuration file** (`netlify.toml` in repo root):

```toml
[build]
  publish = "web"
  command = "echo 'No build needed - static files'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vercel

1. **Import project**:
   - Sign in to Vercel
   - "New Project"
   - Import from GitHub

2. **Configure**:
   - Framework Preset: "Other"
   - Root Directory: `web`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

3. **Deploy**:
   - Click "Deploy"
   - Production URL: yourproject.vercel.app

**Vercel configuration file** (`vercel.json` in repo root):

```json
{
  "buildCommand": "echo 'No build needed'",
  "outputDirectory": "web",
  "cleanUrls": true
}
```

### Cloudflare Pages

1. **Create Pages project**:
   - Go to Cloudflare Pages
   - "Create a project"
   - Connect to GitHub

2. **Build settings**:
   - Build command: (leave empty)
   - Build output directory: `web`

3. **Deploy**:
   - Automatic deployments on push

### AWS S3 + CloudFront

For production deployments with custom domain:

```bash
# Install AWS CLI
aws configure

# Create S3 bucket
aws s3 mb s3://worm-gear-web

# Enable static website hosting
aws s3 website s3://worm-gear-web \
  --index-document index.html \
  --error-document index.html

# Upload files
cd web
aws s3 sync . s3://worm-gear-web --acl public-read

# Set CORS for Pyodide
aws s3api put-bucket-cors --bucket worm-gear-web --cors-configuration file://cors.json
```

**cors.json**:
```json
{
  "CORSRules": [{
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3000
  }]
}
```

## Custom Domain

### GitHub Pages

1. Add `CNAME` file to `web/`:
   ```
   worm-gears.yourdomain.com
   ```

2. Configure DNS:
   ```
   Type: CNAME
   Name: worm-gears
   Value: your-username.github.io
   ```

3. Enable HTTPS in repository settings

### Netlify/Vercel

- Both provide automatic SSL
- Add custom domain in project settings
- Follow DNS configuration instructions

## Performance Optimization

### Enable Caching

Add these headers to improve load times:

**Netlify** (`web/_headers`):
```
/*
  Cache-Control: public, max-age=3600
  Cross-Origin-Embedder-Policy: require-corp
  Cross-Origin-Opener-Policy: same-origin

/*.wasm
  Cache-Control: public, max-age=31536000, immutable

/*.whl
  Cache-Control: public, max-age=31536000, immutable
```

**Vercel** (`vercel.json`):
```json
{
  "headers": [{
    "source": "/(.*)",
    "headers": [
      {
        "key": "Cache-Control",
        "value": "public, max-age=3600"
      },
      {
        "key": "Cross-Origin-Embedder-Policy",
        "value": "require-corp"
      },
      {
        "key": "Cross-Origin-Opener-Policy",
        "value": "same-origin"
      }
    ]
  }, {
    "source": "/*.wasm",
    "headers": [{
      "key": "Cache-Control",
      "value": "public, max-age=31536000, immutable"
    }]
  }]
}
```

### CDN Configuration

For faster global access:
- Enable CDN on your hosting provider
- Use CloudFlare in front of your origin
- Consider regional replication for S3

## Monitoring

### Error Tracking

Add error tracking to `index.html`:

```javascript
window.addEventListener('error', (event) => {
  // Log to your error tracking service
  console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});
```

### Analytics

Add privacy-friendly analytics:

```html
<!-- Plausible (recommended) -->
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.js"></script>

<!-- Or Umami -->
<script async defer
  data-website-id="your-id"
  src="https://analytics.umami.is/umami.js"></script>
```

## Troubleshooting Deployment

### CORS Errors

**Symptoms**: "Access to XMLHttpRequest blocked by CORS policy"

**Fix**:
- Ensure proper headers are set (see above)
- Check Pyodide CDN is accessible
- Verify OCP.wasm repository is reachable

### 404 Errors for Resources

**Symptoms**: Cannot load `src/` or `examples/` files

**Fix**:
- Ensure deployment includes all directories
- Check GitHub Actions workflow copies files
- Verify paths are relative (use `../src/` not `/src/`)

### Large File Warnings

**Symptoms**: GitHub warns about large files

**Fix**:
- OCP.wasm wheels are downloaded at runtime, not included in repo
- Ensure `.gitignore` excludes `*.whl` files
- If wheel files accidentally committed, use git-lfs or BFG

### Slow Initial Load

**Expected**: First load takes 30-90 seconds
- Pyodide: ~10MB download
- OCP.wasm packages: 50-100MB total
- Subsequent loads are cached and faster

**Improvements**:
- Enable CDN caching
- Use service worker for offline support
- Add loading progress indicator

## Security Considerations

### Content Security Policy

Add CSP headers for security:

```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline'
    https://cdn.jsdelivr.net https://yeicor.github.io;
  worker-src 'self' blob:;
  style-src 'self' 'unsafe-inline';
  connect-src 'self' https://pypi.org https://yeicor.github.io;
```

**Note**: `unsafe-eval` is required for Pyodide to work.

### HTTPS Only

Always deploy with HTTPS:
- GitHub Pages: Automatic
- Netlify/Vercel: Automatic
- Custom server: Use Let's Encrypt

## Deployment Checklist

Before deploying to production:

- [ ] Test all features locally
- [ ] Verify CORS headers are correct
- [ ] Check console for errors
- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test on mobile devices
- [ ] Verify STEP file downloads work
- [ ] Check page load performance
- [ ] Enable caching headers
- [ ] Set up error tracking
- [ ] Add analytics (optional)
- [ ] Configure custom domain (optional)
- [ ] Enable HTTPS
- [ ] Test with slow 3G connection
- [ ] Add monitoring/uptime checks

## Support

If deployment fails:

1. Check GitHub Actions logs (Actions tab)
2. Review browser console for errors
3. Test locally with `python3 serve.py`
4. Open issue on GitHub with:
   - Browser version
   - Error messages
   - Deployment platform

## Related Documentation

- [README.md](README.md) - Usage guide
- [PYODIDE_INTEGRATION.md](PYODIDE_INTEGRATION.md) - Technical architecture
- [SETUP_OCP.md](SETUP_OCP.md) - OCP.wasm setup (not needed for cloud hosting)
