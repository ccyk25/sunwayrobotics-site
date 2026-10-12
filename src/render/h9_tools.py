
# =====================================================================
# Real workshop tools for the pegboards (built from proper silhouettes:
# extruded 2D outlines with holes + lathed handles), curated layouts.
# =====================================================================
M_CHROME = mat('chrome', srgb('#C9CCD4'), 1.0, 0.22)
M_SATIN = mat('satin', srgb('#9A9DA6'), 1.0, 0.38)
M_BLACKR = mat('blackrub', srgb('#141418'), 0.0, 0.55)
M_RED = mat('redgrip', srgb('#A32A22'), 0.0, 0.42)
M_YEL = mat('yellow', srgb('#E8B10C'), 0.0, 0.45)
M_VIO = mat('violetgrip', srgb('#7350C8'), 0.0, 0.4)
M_BLUE = mat('bluegrip', srgb('#2E559E'), 0.0, 0.42)
M_ORANGE = mat('orange', srgb('#E0661B'), 0.0, 0.45)
M_GREY = mat('greyplastic', srgb('#3B3D45'), 0.0, 0.5)
M_LCD = mat('lcd', srgb('#8E9A86'), 0.0, 0.3, srgb('#B9C7AE'), 0.35)
M_WIRE = {c: mat('wire' + c, srgb(c), 0.0, 0.35) for c in ('#C62828', '#1C1C1F', '#1E5BC6', '#E3B21B', '#2E8B3D', '#EDEDED')}

def _curve_obj(name, loops, depth, m, parent, bevel=0.004):
    cd = bpy.data.curves.new(name, 'CURVE'); cd.dimensions = '2D'; cd.fill_mode = 'BOTH'
    cd.extrude = max(depth / 2 - bevel, 0.001); cd.bevel_depth = bevel; cd.bevel_resolution = 2
    for lp in loops:
        sp = cd.splines.new('POLY'); sp.points.add(len(lp) - 1)
        for p, (x, y) in zip(sp.points, lp): p.co = (x, y, 0, 1)
        sp.use_cyclic_u = True
    o = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(o)
    o.data.materials.append(m); o.parent = parent; o.rotation_euler = (math.pi / 2, 0, 0)
    return o

def flat(name, loops, depth, m, parent, dy=0.0, bevel=0.004):
    """2D outline(s) in the tool's local (x right, z up) plane, extruded toward the camera."""
    o = _curve_obj(name, loops, depth, m, parent, bevel); o.location = (0, dy, 0); return o

def arc(cx, cz, r, a0, a1, n=24):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cz + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def circ(cx, cz, r, n=40):
    return arc(cx, cz, r, 0, 2 * math.pi, n)[:-1]

def rot2(pts, a, c=(0, 0)):
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (z - c[1]) * sa, c[1] + (x - c[0]) * sa + (z - c[1]) * ca) for x, z in pts]

def rrect(x0, z0, x1, z1, r, n=6):
    r = min(r, (x1 - x0) / 2, (z1 - z0) / 2)
    return (arc(x1 - r, z1 - r, r, 0, math.pi / 2, n) + arc(x0 + r, z1 - r, r, math.pi / 2, math.pi, n) +
            arc(x0 + r, z0 + r, r, math.pi, 1.5 * math.pi, n) + arc(x1 - r, z0 + r, r, 1.5 * math.pi, 2 * math.pi, n))

def _cr(pts, k=6):
    """Catmull-Rom resample."""
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[d] + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2 + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3) for d in (0, 1)))
    out.append(pts[-1]); return out

def stroke(path, w0, w1=None, k=6, round_ends=True):
    """Outline polygon of a variable-width stroke along a path."""
    w1 = w0 if w1 is None else w1
    p = _cr(path, k); n = len(p); L, R = [], []
    for i in range(n):
        a = p[max(i - 1, 0)]; b = p[min(i + 1, n - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dz) or 1
        nx, nz = -dz / ln, dx / ln; w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((p[i][0] + nx * w, p[i][1] + nz * w)); R.append((p[i][0] - nx * w, p[i][1] - nz * w))
    if round_ends:
        a0 = math.atan2(L[-1][1] - p[-1][1], L[-1][0] - p[-1][0])
        end = arc(p[-1][0], p[-1][1], w1 / 2, a0, a0 - math.pi, 8)[1:-1]
        a1 = math.atan2(R[0][1] - p[0][1], R[0][0] - p[0][0])
        start = arc(p[0][0], p[0][1], w0 / 2, a1, a1 - math.pi, 8)[1:-1]
        return L + end + R[::-1] + start
    return L + R[::-1]

def lathe(name, prof, m, parent, loc=(0, 0, 0), segs=28, flutes=0, fd=0.0, axis='z'):
    """Surface of revolution from (r, z) profile; optional grip flutes."""
    me = bpy.data.meshes.new(name); V = []; F = []
    for r, z in prof:
        for k in range(segs):
            t = 2 * math.pi * k / segs
            rr = r * (1 - fd * max(0.0, math.cos(flutes * t)) ** 2) if flutes else r
            V.append((rr * math.cos(t), rr * math.sin(t), z))
    for i in range(len(prof) - 1):
        for k in range(segs):
            a = i * segs + k; b = i * segs + (k + 1) % segs
            F.append((a, b, b + segs, a + segs))
    F.append(tuple(range(segs))[::-1]); F.append(tuple(range((len(prof) - 1) * segs, len(prof) * segs)))
    me.from_pydata(V, [], F); me.update()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.data.materials.append(m); o.parent = parent; o.location = loc
    if axis == 'x': o.rotation_euler = (0, math.pi / 2, 0)
    if axis == '-x': o.rotation_euler = (0, -math.pi / 2, 0)
    return o

def tube(name, pts, r, m, parent=None):
    cd = bpy.data.curves.new(name, 'CURVE'); cd.dimensions = '3D'; cd.bevel_depth = r; cd.bevel_resolution = 3
    sp = cd.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(name, cd); bpy.context.collection.objects.link(o); o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def anchor(x, z, depth, tilt=0.0, s=1.0):
    e = empty('tool', (x, BGY - 0.03 - depth * s / 2 - 0.035 * s, z)); e.rotation_euler = (0, -tilt, 0); e.scale = (s, s, s)
    return e

def hook(x, z, length=0.09):
    """Steel pegboard J-hook sticking out of the board."""
    tube('hook', [(x, BGY - 0.02, z), (x, BGY - 0.02 - length * 0.7, z - 0.004), (x, BGY - 0.02 - length, z + 0.03)], 0.008, M_SATIN)

# ---------------------------- tools ----------------------------
def comb_wrench(x, z, L=0.5, s=1.0, m=None):
    """Combination spanner hanging from its ring end (ring up, open end down)."""
    m = m or M_CHROME; e = anchor(x, z, 0.03, 0, s); d = 0.028
    R1, R2 = 0.06 * L / 0.5, 0.068 * L / 0.5
    top, bot = L / 2 - R1 * 0.4, -L / 2 + R2 * 0.6
    star = [(0 + (R1 * 0.56 if i % 2 == 0 else R1 * 0.5) * math.cos(i * math.pi / 12), top + (R1 * 0.56 if i % 2 == 0 else R1 * 0.5) * math.sin(i * math.pi / 12)) for i in range(24)]
    flat('wr_ring', [circ(0, top, R1, 36), star], d, m, e)
    j = R2 * 0.48; zr = math.sqrt(R2 * R2 - j * j)
    a0 = math.atan2(-zr, j); a1 = math.atan2(-zr, -j) + 2 * math.pi
    oe = arc(0, 0, R2, a0, a1, 30) + [(-j, 0.18 * R2), (j, 0.18 * R2)]
    oe = [(px, pz + bot) for px, pz in rot2(oe, math.radians(15))]
    flat('wr_open', [oe], d, m, e)
    w1, w2 = 0.05 * L / 0.5, 0.058 * L / 0.5
    flat('wr_shaft', [[(-w1 / 2, top - R1 * 0.7), (w1 / 2, top - R1 * 0.7), (w2 / 2, bot + R2 * 0.75), (-w2 / 2, bot + R2 * 0.75)]], d * 0.8, m, e)
    hook(x, z + (top) * s + R1 * 0.5 * s)

def screwdriver(x, z, L=0.42, m=M_RED, tip='flat', s=1.0, rack=True):
    """Hangs tip-down through a rack: handle above, shaft below."""
    e = anchor(x, z, 0.05, 0, s); hl = L * 0.42
    prof = [(0.0, 0), (0.016, 0.0), (0.021, 0.012), (0.024, hl * 0.25), (0.025, hl * 0.55), (0.023, hl * 0.85), (0.02, hl * 0.97), (0.012, hl), (0.0, hl + 0.002)]
    lathe('drv_h', prof, m, e, segs=30, flutes=6, fd=0.12)
    lathe('drv_band', [(0.0, hl * 0.30), (0.0255, hl * 0.30), (0.0262, hl * 0.62), (0.0, hl * 0.62)], M_BLACKR, e, segs=30, flutes=6, fd=0.12)
    lathe('drv_ferrule', [(0.0, -0.012), (0.012, -0.012), (0.016, 0.004), (0.0, 0.004)], M_SATIN, e, segs=20)
    sl = L - hl
    lathe('drv_shaft', [(0.0, -sl), (0.0055, -sl + 0.02), (0.0055, -0.01), (0.0, -0.01)], M_CHROME, e, segs=16)
    if tip == 'flat':
        flat('drv_tip', [[(-0.009, -sl + 0.022), (0.009, -sl + 0.022), (0.006, -sl - 0.002), (-0.006, -sl - 0.002)]], 0.004, M_CHROME, e, bevel=0.001)

def driver_rack(x0, x1, z):
    box('rack', (x1 - x0, 0.09, 0.025), ((x0 + x1) / 2, BGY - 0.065, z), M_SATIN, 0.004)
    for xx in (x0 + 0.05, x1 - 0.05):
        box('rackbr', (0.02, 0.09, 0.07), (xx, BGY - 0.065, z - 0.03), M_SATIN, 0.003)

def pliers(x, z, kind='comb', grip=M_RED, s=1.0, tilt=0.0):
    """Pliers hanging jaws-down, handles up over two hooks."""
    e = anchor(x, z, 0.03, tilt, s); d = 0.026
    jl = {'comb': 0.13, 'needle': 0.17, 'cutter': 0.07}[kind]
    for sg in (-1, 1):
        if kind == 'needle':
            jaw = stroke([(sg * 0.003, -jl), (sg * 0.006, -jl * 0.5), (0, 0)], 0.008, 0.04)
        elif kind == 'cutter':
            jaw = stroke([(sg * 0.002, -jl), (sg * 0.012, -jl * 0.55), (0, 0)], 0.02, 0.046)
        else:
            jaw = stroke([(sg * 0.005, -jl), (sg * 0.012, -jl * 0.5), (0, 0)], 0.032, 0.062)
        flat('pl_jaw', [jaw], d, M_CHROME, e, dy=sg * 0.006)
        hp = [(0, 0), (-sg * 0.018, 0.06), (-sg * 0.04, 0.16), (-sg * 0.055, 0.26), (-sg * 0.06, 0.31)]
        flat('pl_arm', [stroke(hp, 0.04, 0.024)], d, M_CHROME, e, dy=sg * 0.006)
        flat('pl_grip', [stroke(hp[1:] + [(-sg * 0.063, 0.335)], 0.036, 0.036)], d + 0.016, grip, e, dy=sg * 0.006, bevel=0.008)
    cyl('pl_rivet', 0.012, 0.05, (0, 0, 0), m=M_SATIN, parent=e, verts=16)
    hook(x - 0.055 * s, z + 0.27 * s); hook(x + 0.055 * s, z + 0.27 * s)

def hammer(x, z, s=1.0):
    """Claw hammer hanging head-up, resting on two hooks under the head."""
    e = anchor(x, z, 0.05, 0, s)
    head = [(-0.135, 0.338), (-0.128, 0.345), (-0.088, 0.345), (-0.08, 0.338), (-0.06, 0.336), (0.02, 0.338), (0.065, 0.334),
            (0.105, 0.32), (0.14, 0.296), (0.165, 0.266), (0.172, 0.252), (0.164, 0.25), (0.14, 0.272), (0.105, 0.29), (0.065, 0.298),
            (0.032, 0.296), (0.02, 0.282), (-0.06, 0.284), (-0.08, 0.278), (-0.088, 0.27), (-0.128, 0.27), (-0.135, 0.277)]
    flat('hm_head', [head], 0.046, M_SATIN, e)
    flat('hm_face', [rrect(-0.142, 0.272, -0.13, 0.343, 0.004)], 0.05, M_CHROME, e)
    flat('hm_shaft', [stroke([(-0.02, 0.29), (-0.02, 0.1), (-0.017, -0.12)], 0.034, 0.03)], 0.034, M_YEL, e, bevel=0.01)
    flat('hm_grip', [stroke([(-0.018, 0.04), (-0.017, -0.12), (-0.015, -0.16)], 0.044, 0.05)], 0.046, M_BLACKR, e, bevel=0.014)
    hook(x - 0.065 * s, z + 0.255 * s); hook(x + 0.03 * s, z + 0.255 * s)

def hacksaw(x, z, s=1.0):
    e = anchor(x, z, 0.03, 0, s)
    fw = 0.018   # straight steel frame: two posts + top bar (no curve smoothing, so it stays square)
    flat('hs_post1', [[(-0.26 - fw / 2, -0.004), (-0.26 + fw / 2, -0.004), (-0.26 + fw / 2, 0.15 + fw / 2), (-0.26 - fw / 2, 0.15 + fw / 2)]], 0.014, M_SATIN, e, bevel=0.003)
    flat('hs_top', [[(-0.26 - fw / 2, 0.15 - fw / 2), (0.2 + fw / 2, 0.15 - fw / 2), (0.2 + fw / 2, 0.15 + fw / 2), (-0.26 - fw / 2, 0.15 + fw / 2)]], 0.014, M_SATIN, e, bevel=0.003)
    flat('hs_post2', [[(0.2 - fw / 2, -0.004), (0.2 + fw / 2, -0.004), (0.2 + fw / 2, 0.15 + fw / 2), (0.2 - fw / 2, 0.15 + fw / 2)]], 0.014, M_SATIN, e, bevel=0.003)
    teeth = [(0.2 - i * 0.007, 0.0 - (0.005 if i % 2 else 0)) for i in range(67)]
    flat('hs_blade', [[(-0.262, 0.016), (0.2, 0.016)] + teeth + [(-0.262, -0.004)]], 0.003, M_CHROME, e, bevel=0.0006)
    cyl('hs_wing', 0.012, 0.03, (-0.27, 0, 0.008), (0, math.pi / 2, 0), M_SATIN, e, verts=12)
    grip = [(0.19, 0.17), (0.235, 0.17), (0.27, 0.12), (0.3, 0.02), (0.315, -0.08), (0.3, -0.125), (0.255, -0.135), (0.215, -0.11), (0.2, -0.05), (0.19, 0.0)]
    hole = rrect(0.222, -0.075, 0.262, 0.1, 0.02)
    flat('hs_grip', [grip, hole], 0.04, M_BLACKR, e, bevel=0.012)
    hook(x - 0.18 * s, z + 0.18 * s); hook(x + 0.1 * s, z + 0.18 * s)

def tape_measure(x, z, s=1.0):
    e = anchor(x, z, 0.075, 0, s)
    flat('tm_body', [rrect(-0.085, -0.08, 0.075, 0.085, 0.035)], 0.07, M_YEL, e, bevel=0.012)
    flat('tm_over', [rrect(0.035, -0.088, 0.095, 0.093, 0.04)], 0.078, M_BLACKR, e, bevel=0.014)
    flat('tm_bump', [rrect(-0.098, -0.092, -0.05, -0.05, 0.014)], 0.08, M_BLACKR, e, bevel=0.012)
    cyl('tm_screw', 0.009, 0.074, (-0.02, 0, 0.005), m=M_SATIN, parent=e, verts=16)
    flat('tm_tape', [[(-0.09, -0.066), (-0.15, -0.07), (-0.15, -0.084), (-0.09, -0.082)]], 0.024, M_YEL, e, bevel=0.001)
    flat('tm_hook', [[(-0.148, -0.058), (-0.156, -0.058), (-0.156, -0.096), (-0.148, -0.096)]], 0.03, M_CHROME, e, bevel=0.001)
    flat('tm_lock', [rrect(-0.045, 0.075, 0.015, 0.098, 0.009)], 0.03, M_BLACKR, e, dy=-0.022)
    hook(x, z + 0.1 * s)

def multimeter(x, z, s=1.0):
    e = anchor(x, z, 0.06, 0, s)
    flat('mm_holster', [rrect(-0.105, -0.2, 0.105, 0.2, 0.035), rrect(-0.085, -0.18, 0.085, 0.18, 0.02)], 0.06, M_ORANGE, e, bevel=0.012)
    flat('mm_body', [rrect(-0.086, -0.181, 0.086, 0.181, 0.02)], 0.048, M_GREY, e, bevel=0.006)
    flat('mm_lcdbez', [rrect(-0.07, 0.06, 0.07, 0.165, 0.008)], 0.052, M_BLACKR, e)
    flat('mm_lcd', [rrect(-0.06, 0.07, 0.06, 0.155, 0.004)], 0.054, M_LCD, e)
    for i, xx in enumerate((-0.035, -0.012, 0.012, 0.035)):          # big LCD digits as dark bars
        flat('mm_dig', [rrect(xx - 0.008, 0.088, xx + 0.008, 0.138, 0.002), rrect(xx - 0.004, 0.092, xx + 0.004, 0.110, 0.001), rrect(xx - 0.004, 0.116, xx + 0.004, 0.134, 0.001)], 0.0545, M_BLACKR, e, bevel=0.0005)
    cyl('mm_dial', 0.05, 0.03, (0, -0.02, -0.03), m=M_BLACKR, parent=e, verts=40)
    flat('mm_ptr', [rrect(-0.006, -0.03, 0.006, 0.04, 0.003)], 0.07, M_SATIN, e, bevel=0.001).location = (0, -0.006, -0.03)
    for i, xx in enumerate((-0.06, -0.02, 0.02, 0.06)):
        cyl('mm_jack', 0.012, 0.056, (xx, 0, -0.145), m=M_RED if i == 3 else M_BLACKR, parent=e, verts=16)
    hook(x, z + 0.21 * s)
    # test leads looping down to a second hook
    for xx, mm, sag in ((0.06, M_WIRE['#C62828'], 0.45), (0.02, M_WIRE['#1C1C1F'], 0.38)):
        X, Z, Y = x + xx * s, z - 0.15 * s, BGY - 0.07
        tube('lead', [(X, Y - 0.02, Z), (X + 0.02, Y - 0.03, Z - sag * 0.5 * s), (x + 0.16 * s, Y - 0.02, z - sag * s), (x + 0.2 * s, Y - 0.03, z - 0.05 * s), (x + 0.19 * s, Y - 0.02, z + 0.06 * s)], 0.0065 * s, mm)

def caliper(x, z, s=1.0):
    e = anchor(x, z, 0.02, 0, s)
    flat('cl_beam', [[(-0.22, 0.0), (0.24, 0.0), (0.24, 0.032), (-0.22, 0.032)]], 0.006, M_CHROME, e, bevel=0.001)
    flat('cl_jaw', [[(-0.22, 0.032), (-0.22, -0.12), (-0.205, -0.13), (-0.19, -0.04), (-0.19, 0.0), (-0.19, 0.032)]], 0.008, M_CHROME, e, bevel=0.001)
    flat('cl_ujaw', [[(-0.22, 0.032), (-0.212, 0.075), (-0.204, 0.075), (-0.2, 0.032)]], 0.006, M_CHROME, e, bevel=0.001)
    flat('cl_slide', [[(-0.175, -0.012), (-0.07, -0.012), (-0.07, 0.048), (-0.175, 0.048)]], 0.024, M_GREY, e, bevel=0.004)
    flat('cl_sjaw', [[(-0.175, -0.012), (-0.172, -0.13), (-0.187, -0.12), (-0.188, -0.03)]], 0.008, M_CHROME, e, bevel=0.001)
    flat('cl_lcd', [rrect(-0.165, 0.006, -0.1, 0.04, 0.003)], 0.028, M_LCD, e)
    for xx in (-0.088, -0.078):
        cyl('cl_btn', 0.005, 0.03, (xx, 0, 0.022), m=M_BLACKR, parent=e, verts=12)
    hook(x - 0.1 * s, z + 0.05 * s); hook(x + 0.15 * s, z + 0.05 * s)

def scissors(x, z, grip=M_ORANGE, s=1.0):
    e = anchor(x, z, 0.02, 0, s)
    for sg in (-1, 1):
        blade = [(0, 0.0), (sg * 0.012, -0.02), (sg * 0.006, -0.17), (0.0, -0.19), (-sg * 0.004, -0.12), (-sg * 0.006, 0.0)]
        flat('sc_blade', [blade], 0.006, M_CHROME, e, dy=sg * 0.004, bevel=0.001)
        cx = sg * 0.035
        flat('sc_loop', [[(px, pz) for px, pz in circ(cx, 0.075, 0.042, 32)], [(px, pz) for px, pz in circ(cx, 0.075, 0.027, 28)]], 0.016, grip, e, dy=sg * 0.004, bevel=0.005)
        flat('sc_neck', [stroke([(0, 0.0), (cx * 0.6, 0.035)], 0.02, 0.022)], 0.014, grip, e, dy=sg * 0.004)
    cyl('sc_pin', 0.007, 0.03, (0, 0, 0), m=M_SATIN, parent=e, verts=12)
    hook(x, z + 0.11 * s)

def spool_rod(x0, x1, z, colours):
    cyl('spoolrod', 0.012, x1 - x0 + 0.1, ((x0 + x1) / 2, BGY - 0.12, z), (0, math.pi / 2, 0), M_SATIN, verts=12)
    for xx in (x0 - 0.03, x1 + 0.03):
        box('spoolbr', (0.02, 0.13, 0.05), (xx, BGY - 0.075, z), M_SATIN, 0.003)
    n = len(colours); w = (x1 - x0) / n
    for i, c in enumerate(colours):
        e = empty('spool', (x0 + w * (i + 0.5), BGY - 0.12, z))
        fl = 0.012; hw = w / 2 - 0.006
        lathe('sp_wire', [(0.0, -hw + fl), (0.068, -hw + fl), (0.071, 0), (0.068, hw - fl), (0.0, hw - fl)], M_WIRE[c], e, segs=36, axis='x')
        for sg in (-1, 1):
            lathe('sp_flange', [(0.0, sg * hw - fl / 2), (0.1, sg * hw - fl / 2), (0.1, sg * hw + fl / 2), (0.0, sg * hw + fl / 2)], M_BLACKR, e, segs=36, axis='x')

def wrench_set(x0, z, sizes, gap=0.085, s=1.0):
    for i, L in enumerate(sizes):
        comb_wrench(x0 + i * gap * s, z - (sizes[-1] - L) * 0.0 * s - L / 2 * s, L, s)

def drill(x, z, s=1.0):
    """Cordless drill sitting in a pegboard holster, chuck pointing left."""
    e = anchor(x, z, 0.08, 0, s)
    body = rrect(-0.14, 0.04, 0.1, 0.14, 0.045)
    flat('dr_body', [body], 0.075, M_GREY, e, bevel=0.016)
    flat('dr_handle', [stroke([(0.05, 0.06), (0.035, -0.04), (0.03, -0.11)], 0.065, 0.06, round_ends=False)], 0.066, M_BLACKR, e, bevel=0.014)
    flat('dr_batt', [rrect(-0.025, -0.175, 0.105, -0.11, 0.014)], 0.085, M_VIO, e, bevel=0.012)
    flat('dr_trig', [rrect(-0.008, 0.0, 0.012, 0.04, 0.006)], 0.03, M_BLACKR, e)
    lathe('dr_chuck', [(0.0, 0), (0.032, 0), (0.034, 0.03), (0.026, 0.07), (0.012, 0.085), (0.0, 0.085)], M_BLACKR, e, loc=(-0.13, 0, 0.09), segs=24, flutes=10, fd=0.06, axis='-x')
    lathe('dr_bit', [(0.0, 0), (0.005, 0), (0.005, 0.08), (0.0, 0.09)], M_CHROME, e, loc=(-0.212, 0, 0.09), segs=12, axis='-x')
    flat('dr_vent', [rrect(0.045, 0.075, 0.085, 0.115, 0.01)], 0.078, M_BLACKR, e)
    box('dr_shelf', (0.26, 0.14, 0.02), (x + 0.04 * s, BGY - 0.08, z - 0.185 * s), M_SATIN, 0.003)

def hex_keys(x, z, s=1.0):
    e = anchor(x, z, 0.03, 0, s)
    flat('hx_hold', [rrect(-0.11, -0.02, 0.11, 0.02, 0.01)], 0.03, M_BLACKR, e)
    for i in range(9):
        xx = -0.095 + i * 0.024; L = 0.06 + i * 0.014; w = 0.006 + i * 0.0012
        flat('hx', [[(xx - w / 2, 0.02), (xx + w / 2, 0.02), (xx + w / 2, -0.02 - L + w), (xx + 0.03 + i * 0.002, -0.02 - L + w), (xx + 0.03 + i * 0.002, -0.02 - L), (xx - w / 2, -0.02 - L)]], w, M_SATIN, e, bevel=0.0008)
    hook(x - 0.06 * s, z + 0.03 * s); hook(x + 0.06 * s, z + 0.03 * s)
