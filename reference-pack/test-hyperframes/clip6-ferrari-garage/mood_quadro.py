# Style frame del quadro strumenti: contagiri rosso a fondo scala, schermo con 375 km/h,
# un diavolo di linee al neon che esce dal quadrante. Uso:
#   Blender -b --factory-startup -t 2 -P mood_quadro.py -- <file.jpg> [samples]
import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
out = argv[0]; SAMPLES = int(argv[1]) if len(argv) > 1 else 32
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
FONT = None
try: FONT = bpy.data.fonts.load('/System/Library/Fonts/HelveticaNeue.ttc')
except Exception: pass

def mat(name, color, rough, emit=None, estr=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit: p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    return m
m_face = mat('quadrante', (0.55, 0.015, 0.012), 0.35, emit=(0.6, 0.01, 0.01), estr=0.6)
m_tick = mat('tacche', (1, 1, 1), 0.3, emit=(1, 0.95, 0.9), estr=4)
m_red = mat('zona_rossa', (1, 1, 1), 0.3, emit=(1, 0.85, 0.2), estr=6)
m_needle = mat('lancetta', (1, 1, 1), 0.3, emit=(1, 0.55, 0.12), estr=5)
m_black = mat('nero', (0.012, 0.012, 0.013), 0.35)
m_carbon = mat('carbonio', (0.02, 0.02, 0.022), 0.25, metal=0.3)
m_screen = mat('schermo', (0.003, 0.003, 0.004), 0.1, emit=(0.02, 0.02, 0.03), estr=1)
m_digit = mat('cifre', (1, 1, 1), 0.3, emit=(1, 1, 1), estr=8)
m_devil = mat('diavolo', (1, 1, 1), 0.3, emit=(1, 0.22, 0.03), estr=2.6)
m_core = mat('diavolo_core', (1, 1, 1), 0.3, emit=(1, 0.55, 0.2), estr=3.5)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)

def text(body, loc, size, m, rot=0.0, align='CENTER'):
    c = bpy.data.curves.new('t', 'FONT'); c.body = body; c.size = size; c.align_x = align; c.align_y = 'CENTER'
    if FONT: c.font = FONT
    o = bpy.data.objects.new('t', c); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = (0, 0, rot)
    o.data.materials.append(m); return o
def box(loc, size, m, rotz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rotz))
    o = bpy.context.object; o.scale = size; o.data.materials.append(m); return o

# quadro sul piano XY (z = profondita' verso la camera)
R = 1.0
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R, depth=0.05, location=(0, 0, 0)); face = bpy.context.object; face.data.materials.append(m_face)
bpy.ops.mesh.primitive_torus_add(major_radius=R + 0.04, minor_radius=0.05, location=(0, 0, 0.03)); bpy.context.object.data.materials.append(m_carbon)
A0, A1 = math.radians(225), math.radians(-45)   # scala 0-10 (x1000 giri) su 270 gradi
for i in range(0, 101):
    a = A0 + (A1 - A0) * i / 100
    big = i % 10 == 0; L = 0.14 if big else 0.06
    m = m_red if i >= 90 else m_tick
    c = Vector((math.cos(a), math.sin(a), 0)) * (R - 0.06 - L / 2)
    box((c.x, c.y, 0.03), (L, 0.012 if big else 0.006, 0.004), m, rotz=a)
    if big:
        p = Vector((math.cos(a), math.sin(a), 0)) * (R - 0.32)
        text(str(i // 10), (p.x, p.y, 0.03), 0.15, m)
text('x1000 RPM', (0, -0.42, 0.03), 0.06, m_tick)
# lancetta a fondo scala (zona rossa)
a = A0 + (A1 - A0) * 0.97
nd = box((math.cos(a) * 0.42, math.sin(a) * 0.42, 0.05), (0.86, 0.02, 0.01), m_needle, rotz=a)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.1, depth=0.06, location=(0, 0, 0.06)); bpy.context.object.data.materials.append(m_black)
# palpebra e schermi laterali
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.2, depth=0.8, location=(0, 0.25, 0.25), rotation=(math.radians(90), 0, 0))
hood = bpy.context.object; hood.scale = (1.9, 1, 1); hood.data.materials.append(m_black)
bpy.ops.object.modifier_add(type='BOOLEAN'); hood.modifiers[-1].operation = 'DIFFERENCE'
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.6, 0.25)); cut = bpy.context.object; cut.scale = (6, 1.8, 2)
hood.modifiers[-1].object = cut; cut.hide_render = True; cut.hide_viewport = True
hood.hide_render = True  # semplice: niente palpebra nel fotogramma di prova
box((1.75, 0, -0.01), (1.25, 0.95, 0.02), m_screen); box((-1.75, 0, -0.01), (1.25, 0.95, 0.02), m_screen)
text('375', (1.7, 0.08, 0.01), 0.42, m_digit); text('km/h', (1.7, -0.25, 0.01), 0.12, m_tick)
text('9800', (-1.75, 0.08, 0.01), 0.3, m_digit); text('RPM', (-1.75, -0.22, 0.01), 0.1, m_tick)

# il diavolo: linee al neon (corna, volto a V, occhi, coda) che escono dal quadrante verso la camera
def neon(points, m, z0, bevel=0.012, closed=False):
    cu = bpy.data.curves.new('neon', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = bevel; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(points) - 1); sp.use_cyclic_u = closed
    for bp, (x, y, z) in zip(sp.bezier_points, points):
        bp.co = (x, y, z0 + z); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new('neon', cu); sc.collection.objects.link(o); o.data.materials.append(m); return o
Z = 0.55
for s_ in (-1, 1):
    neon([(s_ * 0.3, 0.36, 0.0), (s_ * 0.55, 0.62, 0.05), (s_ * 0.5, 0.95, 0.1), (s_ * 0.36, 1.1, 0.14)], m_devil, Z, 0.016)  # corna
    neon([(s_ * 0.36, 0.16, 0.06), (s_ * 0.1, 0.04, 0.08)], m_core, Z, 0.013)  # occhi obliqui, cattivi
neon([(-0.4, 0.4, 0.0), (-0.44, 0.05, 0.03), (-0.3, -0.4, 0.06), (0.0, -0.78, 0.09), (0.3, -0.4, 0.06), (0.44, 0.05, 0.03), (0.4, 0.4, 0.0)], m_devil, Z, 0.016)
neon([(-0.2, -0.2, 0.08), (-0.08, -0.3, 0.09), (0.08, -0.3, 0.09), (0.2, -0.2, 0.08)], m_core, Z, 0.011)  # ghigno
light = bpy.data.lights.new('bagliore', 'POINT'); light.energy = 60; light.color = (1, 0.35, 0.1)
lo = bpy.data.objects.new('bagliore', light); sc.collection.objects.link(lo); lo.location = (0, 0.1, 1.2)
# scintille
import random; random.seed(2)
for i in range(40):
    a = random.random() * math.tau; r = random.uniform(0.3, 1.8)
    box((math.cos(a) * r, math.sin(a) * r * 0.7, random.uniform(0.3, 1.6)), (0.006, 0.006, 0.006), m_core)

cam = bpy.data.cameras.new('c'); cam.lens = 50; cam.dof.use_dof = True; cam.dof.aperture_fstop = 2.2
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); co.location = (0.85, -1.2, 6.6); co.rotation_euler = (math.radians(9), 0, math.radians(4))
t = bpy.data.objects.new('t', None); sc.collection.objects.link(t); t.location = (0.25, 0.05, 0.4)
cam.dof.focus_distance = 6.1; sc.camera = co
sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
for attr, val in [('taa_render_samples', SAMPLES), ('use_raytracing', True)]:
    if hasattr(e, attr): setattr(e, attr, val)
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - High Contrast'
except Exception: pass
# bagliore (glare) nel compositor, se disponibile
try:
    sc.use_nodes = True; nt = sc.node_tree
    rl = nt.nodes.get('Render Layers'); comp = nt.nodes.get('Composite')
    g = nt.nodes.new('CompositorNodeGlare'); g.glare_type = 'FOG_GLOW'; g.size = 8; g.threshold = 0.8
    nt.links.new(rl.outputs['Image'], g.inputs['Image']); nt.links.new(g.outputs['Image'], comp.inputs['Image'])
except Exception as ex:
    print('glare non disponibile:', ex)
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
