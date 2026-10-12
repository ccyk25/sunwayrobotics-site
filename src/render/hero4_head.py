import bpy, bmesh, math, sys, os
from mathutils import Vector

# ---------- settings ----------
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = args[0] if args else '/tmp/hero/frame_'
RES = (int(args[1]), int(args[2])) if len(args) > 2 else (1920, 1080)
FSTART = int(args[3]) if len(args) > 3 else 1
FEND = int(args[4]) if len(args) > 4 else 360
SAMPLES = int(args[5]) if len(args) > 5 else 32
ENGINE = args[6] if len(args) > 6 and not args[6].startswith('--') else 'CYCLES'
FPS = 24
N = 288                       # 12 s loop
S = 0.01                      # svg unit -> metres

def P(x, y):                  # svg (x right, y down; floor y=590) -> blender (X, Z)
    return ((x - 500) * S, (590 - y) * S)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = ENGINE
sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.1
sc.cycles.diffuse_bounces = 2
sc.render.use_persistent_data = True
sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 0
sc.cycles.volume_bounces = 0
sc.cycles.caustics_reflective = False
sc.cycles.caustics_refractive = False
sc.render.resolution_x, sc.render.resolution_y = RES
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N
sc.render.image_settings.file_format = 'PNG'
try:
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass

world = bpy.data.worlds.new('W'); sc.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.003, 0.008, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

# ---------- materials ----------
def mat(name, base, metal=0.0, rough=0.4, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = estr
    return m

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)

M_FLOOR = mat('floor', srgb('#0B0B0E'), 0.0, 0.36)
M_METAL = mat('metal', srgb('#3A3A42'), 0.85, 0.32)
M_DARK = mat('dark', srgb('#16161B'), 0.6, 0.45)
M_GLOW = mat('glow', srgb('#A98BF5'), 0.0, 0.3, srgb('#A98BF5'), 2.6)
M_FRAME = mat('frame', srgb('#A98BF5'), 0.0, 0.3, srgb('#A98BF5'), 0.0)

def part_mat(name, top, bottom):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Metallic'].default_value = 0.35
    b.inputs['Roughness'].default_value = 0.22
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    ramp.color_ramp.elements[0].color = (*bottom, 1)
    ramp.color_ramp.elements[1].color = (*top, 1)
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = 0.35
    return m

M_SQ = part_mat('sq', srgb('#2A1D48'), srgb('#9B7BEA'))      # dark top -> light bottom (as logo)
M_TRI = part_mat('tri', srgb('#9B7BEA'), srgb('#2A1D48'))    # light top -> dark bottom

# ---------- helpers ----------
def box(name, size, loc=(0, 0, 0), m=None, bevel=0.03, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new('bev', 'BEVEL'); mod.width = bevel; mod.segments = 3
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    bpy.ops.object.shade_smooth()
    return o

def cyl(name, r, depth, loc=(0, 0, 0), rot=(math.pi / 2, 0, 0), m=None, parent=None, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object; o.name = name
    mod = o.modifiers.new('bev', 'BEVEL'); mod.width = min(0.02, r * 0.2); mod.segments = 2
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    bpy.ops.object.shade_smooth()
    return o

def torus(name, R, r, loc, m, parent=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=(math.pi / 2, 0, 0), major_segments=64, minor_segments=12)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    if parent: o.parent = parent
    bpy.ops.object.shade_smooth()
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(o)
    o.location = loc
    if parent: o.parent = parent
    return o

def prism(name, pts_svg, depth, m):
    pts = [P(x, y) for x, y in pts_svg]
    cx = sum(p[0] for p in pts) / len(pts); cz = sum(p[1] for p in pts) / len(pts)
    bm = bmesh.new()
    vs = [bm.verts.new((p[0] - cx, -depth / 2, p[1] - cz)) for p in pts]
    f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    nv = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, depth, 0), verts=nv)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    mod = o.modifiers.new('bev', 'BEVEL'); mod.width = 0.025; mod.segments = 3; mod.limit_method = 'ANGLE'
    o.data.materials.append(m)
    return o, (cx, cz)

