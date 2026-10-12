
# frame glow: draws in early, pulses when the last part lands
fr_b = M_FRAME.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
for u, v in ((0, 0.4), (.03, 0.4), (.09, 2.2), (.64, 2.2), (.67, 7), (.73, 3), (1, 3)):
    fr_b.default_value = v; fr_b.keyframe_insert('default_value', frame=1 + int(u * (N - 1)))

# ---------- lights ----------
def area(name, loc, rot, size, power, color):
    bpy.ops.object.light_add(type='AREA', location=loc, rotation=rot)
    l = bpy.context.object; l.name = name; l.data.size = size; l.data.energy = power; l.data.color = color
    return l
area('key', (-4, -8, 8), (math.radians(50), 0, math.radians(-28)), 4, 1100, (1, 0.97, 0.95))
area('fill', (7, -6, 3), (math.radians(75), 0, math.radians(50)), 5, 260, srgb('#C9B6FF'))
area('rimL', (-8, 4, 5), (math.radians(80), 0, math.radians(-120)), 4, 700, srgb('#9B7BEA'))
area('rimR', (8, 4, 5), (math.radians(80), 0, math.radians(120)), 4, 700, srgb('#9B7BEA'))
area('top', (0, -1, 10), (0, 0, 0), 5, 450, (0.9, 0.88, 1.0))

# ---------- camera: straight-on front view, slow push, then zoom onto the finished logo ----------
bpy.ops.object.camera_add()
cam = bpy.context.object; sc.camera = cam
tgt = empty('tgt', (0, 0, 0))
con = cam.constraints.new('TRACK_TO'); con.target = tgt; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'
LOGOZ = PZ
if CAMMODE == 'portrait':
    cam.data.sensor_fit = 'HORIZONTAL'; cam.data.lens = float(os.environ.get('LENS', '30'))
    D = float(os.environ.get('CD', '12.0')); DZ = float(os.environ.get('DZ', '3.4')); H = float(os.environ.get('H', '3.0')); TZ = float(os.environ.get('TGTZ', '2.85'))
else:
    cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 36 * 9 / 16; cam.data.lens = float(os.environ.get('LENS', '38'))
    D = float(os.environ.get('CD', '12.0')); DZ = float(os.environ.get('DZ', '7.2')); H = float(os.environ.get('H', '3.1')); TZ = float(os.environ.get('TGTZ', '2.9'))
Z0, Z1 = float(os.environ.get('ZOOM0', '0.68')), float(os.environ.get('ZOOM1', '0.84'))
def camstate(u):
    if u <= Z0:
        k = u / Z0; d = D * (1 - 0.05 * k); return d, H, TZ
    k = ease(min(1.0, (u - Z0) / (Z1 - Z0)))
    d0 = D * 0.95
    return d0 + (DZ - d0) * k, H + (LOGOZ + 0.1 - H) * k, TZ + (LOGOZ - TZ) * k
for f in range(1, N + 1):
    d, h, tz = camstate((f - 1) / N)
    cam.location = (0, YP - d, h); cam.keyframe_insert('location', frame=f)
    tgt.location = (0, YP, tz); tgt.keyframe_insert('location', frame=f)
cam.data.dof.use_dof = True; cam.data.dof.focus_object = tgt; cam.data.dof.aperture_fstop = 5.6

if os.environ.get('DBGCAM'):
    v = [float(x) for x in os.environ['DBGCAM'].split(',')]
    cam.animation_data_clear(); tgt.animation_data_clear()
    cam.location = v[0:3]; tgt.location = v[3:6]; cam.data.lens = v[6]; cam.data.sensor_fit = 'AUTO'; cam.data.dof.use_dof = False
sc.render.filepath = OUT
sc.frame_start, sc.frame_end = FSTART, FEND
sc.frame_step = int(os.environ.get('STEP', '1'))
sc.render.use_overwrite = False; sc.render.use_placeholder = False
if '--render' in sys.argv:
    bpy.ops.render.render(animation=True)
