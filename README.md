# Sunway Robotics Club website

Live site for Sunway Robotics Club.

```
public/        the built website: this is what gets deployed (index.html, the-circuit.html, partners.html, assets/)
src/pages/     page sources (Claude Design .dc.html)
src/build/     export + photo grading scripts
src/render/    Blender scripts for the hero animation
```

## Deploying (Cloudflare Workers)

The repo is connected to a Cloudflare Worker named `sunwayrobotics-site`. `wrangler.jsonc` tells it to serve `public/` as static files.
Every push to `main` redeploys automatically. Live at https://sunwayrobotics-site.ccyk25.workers.dev
