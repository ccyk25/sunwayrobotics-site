
# =====================================================================
# v4 scene: logo frame inlaid on a standing display monolith, arms in
# front of it with two-finger grippers, three-quarter camera.
# =====================================================================
CAMMODE = os.environ.get('CAM', 'wide')          # 'wide' (desktop) or 'portrait' (phone)
M_SLAB = mat('slab', srgb('#14131A'), 0.15, 0.55)
M_SLABEDGE = mat('slabedge', srgb('#2A2733'), 0.6, 0.3)

# ---------- set ----------
bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 8, 0)); fl = bpy.context.object; fl.data.materials.append(M_FLOOR)
bk = mat('back', (0, 0, 0), 0, 1, srgb('#2A1A4F'), 0.24)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 10, 10), rotation=(math.pi / 2, 0, 0))
bd = bpy.context.object; bd.scale = (70, 40, 1); bd.data.materials.append(bk)

