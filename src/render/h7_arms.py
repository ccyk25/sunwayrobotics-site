
# ---------- arms: planar arm + wrist-pitch gripper ----------
# Parts wait lying flat on the floor (logo face up). The gripper picks them pointing down,
# then the wrist pitches 90 degrees so the gripper faces the board and the part swings
# upright onto it, logo facing the camera.
L1, L2, L3 = 3.2, 3.0, 0.42
GL = 0.51                      # pitch pivot -> grip point, along the tool axis
YA = YP - GL                   # arm plane: tool pointing at the board puts the part on YP
FINGERS = {}; PITCH = {}; ROLL = {}
def build_arm(tag, sx):
    base = empty(tag + '_base', (sx, YA, 0))
    box(tag + '_plate', (1.1, 1.0, 0.12), (0, 0, 0.06), M_DARK, 0.03, base)
    cyl(tag + '_col', 0.24, 1.48, (0, 0, 0.86), (0, 0, 0), M_METAL, base)
    torus(tag + '_ring0', 0.25, 0.018, (0, 0, 0.2), M_GLOW, base).rotation_euler = (0, 0, 0)
    sh = empty(tag + '_sh', (0, 0, 1.6), base)
    cyl(tag + '_j1', 0.34, 0.5, (0, 0, 0), m=M_DARK, parent=sh)
    torus(tag + '_r1', 0.25, 0.022, (0, -0.26, 0), M_GLOW, sh)
    box(tag + '_l1', (L1 + 0.2, 0.34, 0.36), (L1 / 2, 0, 0), M_METAL, 0.09, sh)
    el = empty(tag + '_el', (L1, 0, 0), sh)
    cyl(tag + '_j2', 0.27, 0.44, (0, 0, 0), m=M_DARK, parent=el)
    torus(tag + '_r2', 0.19, 0.018, (0, -0.23, 0), M_GLOW, el)
    box(tag + '_l2', (L2 + 0.14, 0.28, 0.28), (L2 / 2, 0, 0), M_METAL, 0.07, el)
    wr = empty(tag + '_wr', (L2, 0, 0), el)
    cyl(tag + '_j3', 0.19, 0.36, (0, 0, 0), m=M_DARK, parent=wr)
    torus(tag + '_r3', 0.13, 0.014, (0, -0.19, 0), M_GLOW, wr)
    box(tag + '_l3', (L3, 0.2, 0.2), (L3 / 2, 0, 0), M_METAL, 0.05, wr)
    # pitch joint at the end of L3: axis = world X (wr-local z)
    pv = empty(tag + '_pitch', (L3, 0, 0), wr)
    cyl(tag + '_j4', 0.14, 0.34, (0, 0, 0), (0, 0, 0), M_DARK, pv)              # axis along local z (= world X)
    for zz in (-0.175, 0.175):
        torus(tag + '_r4', 0.1, 0.012, (0, 0, zz), M_GLOW, pv).rotation_euler = (0, 0, 0)
    rl = empty(tag + '_roll', (0, 0, 0), pv)                                     # roll about the tool axis (local x)
    cyl(tag + '_flange', 0.13, 0.14, (0.09, 0, 0), (0, math.pi / 2, 0), M_METAL, rl)
    torus(tag + '_rf', 0.135, 0.012, (0.17, 0, 0), M_GLOW, rl).rotation_euler = (0, math.pi / 2, 0)
    box(tag + '_body', (0.18, 0.26, 0.5), (0.24, 0, 0), M_DARK, 0.04, rl)
    box(tag + '_rail', (0.06, 0.2, 1.26), (0.35, 0, 0), M_METAL, 0.02, rl)
    box(tag + '_railglow', (0.015, 0.21, 1.2), (0.385, 0, 0), M_GLOW, 0.0, rl)
    fingers = []
    for sgn in (-1, 1):
        f = empty(tag + '_fpiv%d' % sgn, (0.36, 0, 0), rl)
        box(tag + '_finger', (0.3, 0.2, 0.07), (0.15, 0, 0), M_METAL, 0.015, f)
        box(tag + '_pad', (0.16, 0.18, 0.02), (0.17, 0, -sgn * 0.042), M_GLOW, 0.006, f)
        fingers.append((f, sgn))
    ROLL[tag] = rl
    FINGERS[tag] = fingers; PITCH[tag] = pv
    return sh, el, wr
LS, RS = (-4.1, 1.6), (4.1, 1.6)
armL = build_arm('L', LS[0]); armR = build_arm('R', RS[0])
CLAMP = [0]

def ik(S0, pivot, sign):
    Wx, Wz = pivot[0], pivot[1] + L3              # wrist joint straight above the pitch pivot
    dx, dz = Wx - S0[0], Wz - S0[1]; d = math.hypot(dx, dz)
    if d > L1 + L2 - 0.02 or d < abs(L1 - L2) + 0.02: CLAMP[0] += 1
    d = min(max(d, abs(L1 - L2) + 1e-3), L1 + L2 - 1e-3)
    phi = math.atan2(dz, dx)
    a = math.acos((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))
    t1 = phi + sign * a
    Ex, Ez = S0[0] + L1 * math.cos(t1), S0[1] + L1 * math.sin(t1)
    t2abs = math.atan2(Wz - Ez, Wx - Ex)
    return t1, t2abs - t1, -math.pi / 2 - t2abs

def set_arm(arm, angs, f):
    for o, a in zip(arm, angs):
        o.rotation_euler = (0, -a, 0); o.keyframe_insert('rotation_euler', frame=f)

def grip_point(pivot, pitch_deg):
    p = math.radians(pitch_deg)
    return (pivot[0], YA + GL * math.sin(p), pivot[1] - GL * math.cos(p))

# ---------- parts waiting flat on the floor, each turned the wrong way ----------
from mathutils import Matrix
FLATZ = DEPTH / 2 + 0.004
WX = {'sq': -3.05, 'llt': -1.75, 'urt': 2.2}
TH0 = {'sq': math.radians(40), 'urt': math.radians(180), 'llt': math.radians(35)}
SPIN_DZ = {'sq': (0.6, 0.22), 'urt': (0.6, 0.22), 'llt': (0.25, 0.1)}   # how far below its slot each piece spins   # how each piece lies on the floor
for k, x in WX.items():
    box('pad', (1.1, 1.1, 0.012), (x, YA, 0.006), M_DARK, 0.004)
PICK = {k: (x, FLATZ + GL) for k, x in WX.items()}
PLACE = {k: (PL[k][0], PL[k][1]) for k in PL}
FLAT0 = {k: Matrix.Rotation(TH0[k], 4, 'Z') @ Matrix.Rotation(-math.pi / 2, 4, 'X') for k in PL}

def ease(u): return u * u * u * (u * (u * 6 - 15) + 10)
def up(p, d): return (p[0], p[1] + d)
LREST = ((-2.5, 3.7), 0, 0); RREST = ((2.5, 3.7), 0, 0)
def carry(k, t0, tail):
    pk, pl, r0 = PICK[k], PLACE[k], -math.degrees(TH0[k])
    return [(t0, up(pk, 1.0), 0, r0), (t0 + .035, pk, 0, r0), (t0 + .065, pk, 0, r0), (t0 + .10, up(pk, 1.2), 0, r0),
            (t0 + .15, (pl[0], pl[1] - SPIN_DZ[k][0]), 90, r0),          # wrist flips to face the board, piece still turned
            (t0 + .19, (pl[0], pl[1] - SPIN_DZ[k][1]), 90, 0),          # wrist rolls: piece spins into the right orientation
            (t0 + .215, pl, 90, 0), (t0 + .23, pl, 90, 0),     # seat it
            (t0 + .25, (pl[0] + tail * 0.35, pl[1] - 0.2), 25, 0), (t0 + .275, (pl[0] + tail, pl[1] - 0.6), 0, 0)]
Lway = [(0,) + LREST, (.03,) + LREST] + carry('sq', .06, -1.5) + carry('llt', .36, -1.3) + [(.70,) + LREST, (1,) + LREST]
Rway = [(0,) + RREST, (.16,) + RREST] + carry('urt', .19, 1.4) + [(.53,) + RREST, (1,) + RREST]
GRIPS = {'L': [('sq', .06 + .045, .06 + .222), ('llt', .36 + .045, .36 + .222)], 'R': [('urt', .19 + .045, .19 + .222)]}
CARRY = {}
for tag, lst in GRIPS.items():
    for k, c, r in lst: CARRY[k] = (tag, c, r)

def interp(way, u):
    for (u0, p0, a0, r0), (u1, p1, a1, r1) in zip(way, way[1:]):
        if u0 <= u <= u1:
            k = ease((u - u0) / (u1 - u0)) if u1 > u0 else 1
            return (p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k), a0 + (a1 - a0) * k, r0 + (r1 - r0) * k
    return way[-1][1], way[-1][2], way[-1][3]

def finger_state(tag, u):
    lst = GRIPS[tag]
    for k, c, r in lst:
        if u <= r + 0.012: return k, (c - 0.008) <= u <= r
    return lst[-1][0], False

for f in range(1, N + 1):
    u = (f - 1) / N
    poses = {}
    for tag, arm, way, S0, sgn in (('L', armL, Lway, LS, 1), ('R', armR, Rway, RS, -1)):
        pv, pitch, roll = interp(way, u)
        set_arm(arm, ik(S0, pv, sgn), f)
        PITCH[tag].rotation_euler = (0, 0, math.radians(pitch)); PITCH[tag].keyframe_insert('rotation_euler', frame=f)
        ROLL[tag].rotation_euler = (math.radians(roll), 0, 0); ROLL[tag].keyframe_insert('rotation_euler', frame=f)
        part, closed = finger_state(tag, u)
        for piv, s_ in FINGERS[tag]:
            piv.location.z = s_ * (HW[part] + 0.055 + (0 if closed else 0.13)); piv.keyframe_insert('location', frame=f)
        poses[tag] = (pv, pitch, roll)
    for k, (tag, c, r) in CARRY.items():
        o = OBJ[k]
        if u < c:
            M = Matrix.Translation((WX[k], YA, FLATZ)) @ FLAT0[k]
        elif u <= r:
            pv, pitch, roll = poses[tag]; g = grip_point(pv, pitch)
            rp = -math.degrees(TH0[k])
            R = Matrix.Rotation(math.radians(pitch), 4, 'X') @ Matrix.Rotation(-math.radians(roll - rp), 4, 'Z') @ FLAT0[k]
            M = Matrix.Translation(g) @ R
        else:
            M = Matrix.Translation((PL[k][0], YP, PL[k][1]))
        o.matrix_world = M
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_euler', frame=f)
print('IK CLAMPED FRAMES:', CLAMP[0])
