# ---------- hanging display panel (frame inlaid), held by two wires ----------
VARIANT = os.environ.get('VARIANT', 'wire')        # wire | ceiling | glass
fx0, fz1 = P(409, 110); fx1, fz0 = P(591, 379); t = 0.065
MG = 0.0; PT = 0.1
PW, PH = (fx1 - fx0) + 2 * MG, (fz1 - fz0) + 2 * MG
PZ = (fz0 + fz1) / 2
if VARIANT == 'glass':
    sc.cycles.transmission_bounces = 3; sc.cycles.max_bounces = 6
    M_PANEL = bpy.data.materials.new('glass'); M_PANEL.use_nodes = True
    gb = M_PANEL.node_tree.nodes['Principled BSDF']
    gb.inputs['Base Color'].default_value = (*srgb('#CFC2F5'), 1); gb.inputs['Roughness'].default_value = 0.18
    gb.inputs['Transmission Weight'].default_value = 1.0; gb.inputs['IOR'].default_value = 1.45
else:
    M_PANEL = M_SLAB
panel = box('panel', (PW, PT, PH), (0, FACE + PT / 2, PZ), M_PANEL, 0.03)
frame = empty('frame', (0, FACE + PT / 2 - 0.03, 0))
for nm, sz, lc in (('ft', (fx1 - fx0 + t, PT + 0.08, t), ((fx0 + fx1) / 2, 0, fz1)), ('fb', (fx1 - fx0 + t, PT + 0.08, t), ((fx0 + fx1) / 2, 0, fz0)),
                   ('fl', (t, PT + 0.08, fz1 - fz0), (fx0, 0, (fz0 + fz1) / 2)), ('fr', (t, PT + 0.08, fz1 - fz0), (fx1, 0, (fz0 + fz1) / 2))):
    box(nm, sz, lc, M_FRAME, 0.01, frame)
# edge light strip along the panel's top and sides
TOPZ = PZ + PH / 2 + t / 2
CEILZ = float(os.environ.get('CEILZ', '5.95'))
WTOP = CEILZ if VARIANT == 'ceiling' else 16
for sx in (-1, 1):
    x = sx * (PW / 2 - 0.16)
    cyl('clamp', 0.06, 0.1, (x, FACE + PT / 2, TOPZ + 0.04), (0, 0, 0), M_METAL)
    cyl('wire', 0.011, WTOP - TOPZ, (x, FACE + PT / 2, (WTOP + TOPZ) / 2), (0, 0, 0), M_METAL, verts=12)
    if VARIANT == 'ceiling':
        cyl('pulley', 0.11, 0.08, (x, FACE + PT / 2, CEILZ - 0.12), m=M_DARK)
if VARIANT == 'ceiling':
    for yy in (-0.35, 0.55):
        box('rail', (12, 0.14, 0.14), (0, FACE + yy, CEILZ), M_METAL, 0.02)
    for i in range(-14, 15):
        box('rung', (0.06, 0.9, 0.06), (i * 0.42, FACE + 0.1, CEILZ), M_DARK, 0.0)
    box('cglow', (12, 0.04, 0.03), (0, FACE - 0.35, CEILZ - 0.09), M_GLOW, 0.0)
