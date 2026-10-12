
# =====================================================================
# Background: workshop back wall (pegboards, shelves, cable tray),
# floor work-cell markings + cables, overhead light beams.
# =====================================================================
import random
rnd = random.Random(7)
BGY = float(os.environ.get('BGY', '5.0'))           # back wall plane (y)
PEG = '/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/img/peg_mask.png'
bd.hide_render = True                                 # old glowing backdrop is replaced by the wall
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.003, 0.0025, 0.006, 1)

M_WALL = mat('wall', srgb('#191722'), 0.0, 0.85)
M_STEEL = mat('steel', srgb('#34323D'), 0.75, 0.35)
M_RUB = mat('rubber', srgb('#121116'), 0.0, 0.6)
M_BIN = mat('bin', srgb('#2A2733'), 0.05, 0.55)
M_LED = mat('led', srgb('#FFFFFF'), 0, 0.3, srgb('#EDE7FF'), 1.1)
M_LEDV = mat('ledv', srgb('#A98BF5'), 0, 0.3, srgb('#A98BF5'), 3.0)
M_SCREEN = mat('screen', srgb('#120E22'), 0, 0.15, srgb('#7B5BD6'), 1.4)
M_CABLE = mat('cable', srgb('#0D0D11'), 0.0, 0.45)

def ramp_mat(name, img_path, scale, c0, c1, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (*scale, 1)
    it = nt.nodes.new('ShaderNodeTexImage'); it.image = bpy.data.images.load(img_path); it.interpolation = 'Linear'
    rp = nt.nodes.new('ShaderNodeValToRGB')
    rp.color_ramp.elements[0].color = (*c0, 1); rp.color_ramp.elements[1].color = (*c1, 1)
    nt.links.new(tc.outputs['UV'], mp.inputs[0]); nt.links.new(mp.outputs[0], it.inputs[0])
    nt.links.new(it.outputs['Color'], rp.inputs['Fac']); nt.links.new(rp.outputs['Color'], b.inputs['Base Color'])
    return m

def wall_plane(name, cx, cz, w, h, m, dy=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, BGY - 0.02 - dy, cz), rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object; o.name = name; o.scale = (w, h, 1); o.data.materials.append(m)
    return o

# ---------- wall ----------
box('wall', (60, 0.2, 14), (0, BGY + 0.1, 7), M_WALL, 0)
for i in range(-12, 13):
    box('seam', (0.025, 0.02, 14), (i * 2.4, BGY - 0.005, 7), M_STEEL, 0)
box('skirt', (60, 0.08, 0.22), (0, BGY - 0.04, 0.11), M_STEEL, 0)

# ---------- pegboards with tools ----------
def tools_on(cx, cz, w, h, n, keep_clear=None):
    for _ in range(n):
        for _try in range(20):
            x = cx + rnd.uniform(-w / 2 + 0.25, w / 2 - 0.25); z = cz + rnd.uniform(-h / 2 + 0.35, h / 2 - 0.35)
            if keep_clear and abs(x - keep_clear[0]) < keep_clear[1] and abs(z - keep_clear[2]) < keep_clear[3]: continue
            break
        y = BGY - 0.09; kind = rnd.choice(['wrench', 'wrench', 'driver', 'driver', 'pliers', 'coil', 'square'])
        tilt = rnd.uniform(-0.15, 0.15)
        if kind == 'wrench':
            L = rnd.uniform(0.35, 0.6)
            o = box('wr', (0.045, 0.03, L), (x, y, z), M_STEEL, 0.01); o.rotation_euler = (0, tilt, 0)
            torus('wrh', 0.055, 0.018, (x, y, z + L / 2 + 0.04), M_STEEL)
        elif kind == 'driver':
            cyl('drh', 0.04, 0.16, (x, y, z + 0.12), (0, 0, 0), rnd.choice([M_RUB, M_BIN, M_LEDV if rnd.random() < 0.25 else M_RUB]), verts=16)
            cyl('drs', 0.012, 0.3, (x, y, z - 0.12), (0, 0, 0), M_STEEL, verts=8)
        elif kind == 'pliers':
            for s in (-1, 1):
                o = box('pl', (0.03, 0.03, 0.34), (x + s * 0.04, y, z), M_RUB, 0.008); o.rotation_euler = (0, s * 0.18, 0)
        elif kind == 'coil':
            torus('coil', 0.15, 0.04, (x, y - 0.02, z), M_CABLE)
        else:
            o = box('sq', (0.04, 0.03, 0.42), (x, y, z), M_STEEL, 0.005)
            box('sq2', (0.3, 0.03, 0.04), (x + 0.13, y, z - 0.19), M_STEEL, 0.005)

def pegboard(cx, cz, w, h, n, keep_clear=None):
    m = ramp_mat('peg', PEG, (w / 0.26, h / 0.26), srgb('#060609'), srgb('#2C2936'))
    wall_plane('pegboard', cx, cz, w, h, m)
    box('pegframe_t', (w + 0.06, 0.06, 0.05), (cx, BGY - 0.05, cz + h / 2), M_STEEL, 0.01)
    box('pegframe_b', (w + 0.06, 0.06, 0.05), (cx, BGY - 0.05, cz - h / 2), M_STEEL, 0.01)
    tools_on(cx, cz, w, h, n, keep_clear)

# ---------- shelving with parts ----------
def shelf_unit(cx, w, h=3.6, levels=4, depth=0.55):
    for s in (-1, 1):
        box('up', (0.06, depth, h), (cx + s * w / 2, BGY - depth / 2, h / 2), M_STEEL, 0.01)
    for i in range(levels):
        z = 0.35 + i * (h - 0.5) / (levels - 1)
        box('shelf', (w, depth, 0.04), (cx, BGY - depth / 2, z), M_STEEL, 0.008)
        if i > 0:
            box('shelfled', (w - 0.1, 0.02, 0.012), (cx, BGY - depth + 0.03, z - 0.03), M_LED, 0)
        x = cx - w / 2 + 0.12
        while x < cx + w / 2 - 0.3:
            kind = rnd.choice(['bin', 'bin', 'bin', 'motor', 'wheel', 'box', 'gap'])
            if kind == 'bin':
                bw = rnd.uniform(0.3, 0.45); bh = rnd.uniform(0.18, 0.28)
                box('bin', (bw, 0.38, bh), (x + bw / 2, BGY - 0.28, z + 0.02 + bh / 2), M_BIN, 0.02)
                box('label', (0.1, 0.01, 0.04), (x + bw / 2, BGY - 0.475, z + 0.02 + bh * 0.6), M_LEDV if rnd.random() < 0.5 else M_LED, 0)
                x += bw + 0.05
            elif kind == 'motor':
                cyl('motor', 0.08, 0.22, (x + 0.1, BGY - 0.3, z + 0.1), (0, math.pi / 2, 0), M_STEEL, verts=20); x += 0.3
            elif kind == 'wheel':
                cyl('wheel', 0.13, 0.07, (x + 0.14, BGY - 0.3, z + 0.15), (math.pi / 2, 0, 0), M_RUB, verts=24); x += 0.34
            elif kind == 'box':
                bw = rnd.uniform(0.25, 0.5); bh = rnd.uniform(0.25, 0.45)
                box('carton', (bw, 0.4, bh), (x + bw / 2, BGY - 0.28, z + 0.02 + bh / 2), M_RUB, 0.01); x += bw + 0.05
            else:
                x += 0.25

# ---------- workbench with monitor ----------
def bench(cx, w=2.6):
    box('benchtop', (w, 0.8, 0.07), (cx, BGY - 0.45, 0.95), M_STEEL, 0.01)
    for s in (-1, 1):
        box('benchleg', (0.06, 0.7, 0.92), (cx + s * (w / 2 - 0.1), BGY - 0.45, 0.46), M_STEEL, 0.005)
    box('monitor', (0.9, 0.05, 0.55), (cx - 0.4, BGY - 0.25, 1.55), M_RUB, 0.02)
    box('screen', (0.82, 0.01, 0.47), (cx - 0.4, BGY - 0.28, 1.55), M_SCREEN, 0)
    box('stand', (0.06, 0.06, 0.32), (cx - 0.4, BGY - 0.22, 1.13), M_STEEL, 0)
    box('scope', (0.45, 0.35, 0.25), (cx + 0.6, BGY - 0.4, 1.11), M_BIN, 0.02)
    box('scopescr', (0.2, 0.01, 0.12), (cx + 0.5, BGY - 0.58, 1.14), M_SCREEN, 0)
    cyl('spool', 0.12, 0.1, (cx + 1.0, BGY - 0.5, 1.1), (math.pi / 2, 0, 0), M_LEDV, verts=24)

# ---------- cable tray along the top ----------
TRAYZ = 6.4
box('tray', (60, 0.35, 0.06), (0, BGY - 0.3, TRAYZ), M_STEEL, 0.01)
box('traylip', (60, 0.03, 0.12), (0, BGY - 0.47, TRAYZ + 0.06), M_STEEL, 0.005)
def droop(x0, x1, z0, sag, r=0.02, y=None, m=None):
    y = BGY - 0.35 if y is None else y
    cd = bpy.data.curves.new('cable', 'CURVE'); cd.dimensions = '3D'; cd.bevel_depth = r; cd.bevel_resolution = 3
    sp = cd.splines.new('BEZIER'); sp.bezier_points.add(2)
    pts = [(x0, y, z0), ((x0 + x1) / 2, y - 0.05, z0 - sag), (x1, y, z0)]
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new('cable', cd); bpy.context.collection.objects.link(o); o.data.materials.append(m or M_CABLE)
    return o

# layout (x): centre pegboard behind the logo board, shelves either side, bench + pegboards further out
pegboard(0, 3.6, 4.6, 2.9, 10, keep_clear=(0, 1.15, 3.45, 1.45))
shelf_unit(-4.6, 3.0); shelf_unit(4.6, 3.0)
pegboard(-8.4, 3.1, 3.2, 2.2, 9); bench(-8.4)
pegboard(8.4, 3.4, 3.2, 2.6, 10)
shelf_unit(12.2, 2.6, 3.4, 3); shelf_unit(-12.2, 2.6, 3.4, 3)
for x0 in (-11.0, -6.5, -2.6, 2.2, 6.1, 10.4):
    droop(x0, x0 + rnd.uniform(1.2, 2.2), TRAYZ - 0.02, rnd.uniform(0.35, 0.8), rnd.choice([0.015, 0.022]), m=None)

# ---------- floor: work-cell hazard tape around each arm + cables ----------
from PIL import Image as _I
_hz = '/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/img/hazard.png'
if not os.path.exists(_hz):
    _im = _I.new('L', (256, 64), 0)
    _px = _im.load()
    for _x in range(256):
        for _y in range(64):
            _px[_x, _y] = 255 if ((_x + _y) // 32) % 2 == 0 else 0
    _im.save(_hz)
M_TAPE = ramp_mat('tape', _hz, (1, 1), srgb('#0C0B10'), srgb('#8C72D9'), 0.5)
def tape(cx, cy, length, along_x, w=0.1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, cy, 0.003))
    o = bpy.context.object; o.name = 'tape'
    if along_x: o.scale = (length, w, 1)
    else: o.scale = (w, length, 1); o.rotation_euler = (0, 0, 0)
    o.data.materials.append(M_TAPE)
    # stripe count along the tape
    if not along_x:
        for loop in o.data.uv_layers.active.data: loop.uv = (loop.uv[1], loop.uv[0])
    for loop in o.data.uv_layers.active.data: loop.uv = (loop.uv[0] * length / 0.4, loop.uv[1])
    return o
for sx in (-1, 1):
    cx = sx * 4.1; cw, ch = 2.6, 2.0
    tape(cx, YA - ch / 2, cw, True); tape(cx, YA + ch / 2, cw, True)
    tape(cx - cw / 2, YA, ch, False); tape(cx + cw / 2, YA, ch, False)
# thin guide line under the hanging board
box('floorline', (2.4, 0.03, 0.004), (0, YP - 0.2, 0.002), M_LED, 0)
# floor cables from each arm base back to the wall
for sx in (-1, 1):
    cd = bpy.data.curves.new('fcable', 'CURVE'); cd.dimensions = '3D'; cd.bevel_depth = 0.028; cd.bevel_resolution = 3
    sp = cd.splines.new('BEZIER'); sp.bezier_points.add(2)
    pts = [(sx * 4.1, YA + 0.45, 0.03), (sx * 5.2, (YA + BGY) / 2, 0.03), (sx * 5.6, BGY - 0.15, 0.03)]
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new('fcable', cd); bpy.context.collection.objects.link(o); o.data.materials.append(M_CABLE)

# ---------- overhead light beams (faked additive cones, no volume cost) ----------
def beam(x, y, top, bottom, r_bottom, strength):
    h = top - bottom
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r_bottom, radius2=0.08, depth=h, location=(x, y, bottom + h / 2))
    o = bpy.context.object; o.name = 'beam'
    m = bpy.data.materials.new('beam'); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); em = nt.nodes.new('ShaderNodeEmission'); add = nt.nodes.new('ShaderNodeAddShader')
    em.inputs['Color'].default_value = (*srgb('#C9B9FF'), 1)
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 3.0
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    fade = nt.nodes.new('ShaderNodeMath'); fade.operation = 'POWER'; fade.inputs[1].default_value = 0.7
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    k = nt.nodes.new('ShaderNodeMath'); k.operation = 'MULTIPLY'; k.inputs[1].default_value = strength
    nt.links.new(lw.outputs['Facing'], inv.inputs[1]); nt.links.new(inv.outputs[0], pw.inputs[0])
    nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], fade.inputs[0])
    nt.links.new(pw.outputs[0], mul.inputs[0]); nt.links.new(fade.outputs[0], mul.inputs[1])
    nt.links.new(mul.outputs[0], k.inputs[0]); nt.links.new(k.outputs[0], em.inputs['Strength'])
    nt.links.new(tr.outputs[0], add.inputs[0]); nt.links.new(em.outputs[0], add.inputs[1]); nt.links.new(add.outputs[0], out.inputs['Surface'])
    o.data.materials.append(m)
    try: o.visible_shadow = False
    except Exception: pass
    return o
BEAMS = os.environ.get('BEAMS', '1') == '1'
if BEAMS:
    beam(0, YP - 0.15, 9.5, TOPZ + 0.15, 1.15, float(os.environ.get('BEAMK', '0.14')) * 1.3)   # stops at the top of the board, keeps the logo crisp
    for sx in (-1, 1):
        beam(sx * 4.1, YA, 9.5, 0.0, 1.6, float(os.environ.get('BEAMK', '0.14')) * 0.7)
def spot(name, loc, power, size_deg, color=(1, 0.97, 1)):
    bpy.ops.object.light_add(type='SPOT', location=loc)
    l = bpy.context.object; l.name = name; l.data.energy = power; l.data.spot_size = math.radians(size_deg); l.data.spot_blend = 0.6
    l.data.color = color; l.data.shadow_soft_size = 0.4
    return l
spot('beamC', (0, YP - 0.6, 9.3), 1300, 30)
for sx in (-1, 1):
    spot('beamA', (sx * 4.1, YA, 9.3), 900, 24, srgb('#D9CCFF'))
