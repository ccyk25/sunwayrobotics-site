# Sunway Robotics Club website

Live site for Sunway Robotics Club.

```
public/        the built website: this is what gets deployed (index.html, the-circuit.html, partners.html, assets/)
src/pages/     page sources (Claude Design .dc.html)
src/build/     export + photo grading scripts
src/render/    Blender scripts for the hero animation
```

## Deploying (Cloudflare Pages)

1. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.
2. Pick this repo.
3. Build settings: Framework preset **None**, build command **(leave empty)**, build output directory **`public`**.
4. Save and Deploy. Every push to `main` redeploys automatically.
