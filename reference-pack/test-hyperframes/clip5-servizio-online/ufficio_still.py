# Ufficio calmo per il finale v2 di "Peso": scrivania vuota, telefono con la card arancione, veneziane.
# Solo still (il movimento lo fa HyperFrames). Uso:
#   Blender -b --factory-startup -t 2 -P ufficio_still.py -- <cartella/u_> [samples]
import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
out = argv[0]; SAMPLES = int(argv[1]) if len(argv) > 1 else 32
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
def mat(name, color, rough, emit=None, estr=0.0, metal=0.0, noise=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    if noise:   # venatura leggera (legno, intonaco)
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 3; n.inputs['Detail'].default_value = 6
        tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 12, 1)
        nt.links.new(tc.outputs['Object'], mp.inputs[0]); nt.links.new(mp.outputs[0], n.inputs['Vector'])
        r = nt.nodes.new('ShaderNodeValToRGB')
        r.color_ramp.elements[0].color = (*[c * (1 - noise) for c in color], 1); r.color_ramp.elements[1].color = (*color, 1)
        nt.links.new(n.outputs['Fac'], r.inputs[0]); nt.links.new(r.outputs[0], p.inputs['Base Color'])
    return m
def box(name, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m); return o
def cyl(name, loc, r, h, m, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

m_floor = mat('parquet', (0.30, 0.21, 0.14), 0.45, noise=0.35)
m_wall = mat('muro', (0.42, 0.39, 0.35), 0.9)
m_desk = mat('scrivania', (0.55, 0.42, 0.30), 0.4, noise=0.25)
m_metal = mat('metallo', (0.05, 0.05, 0.055), 0.35, metal=1.0)
m_slat = mat('veneziana', (0.75, 0.73, 0.70), 0.5)
m_sky = mat('esterno', (1, 1, 1), 1.0, emit=(1.0, 0.86, 0.68), estr=6.0)
m_grey = mat('raccoglitore', (0.11, 0.115, 0.12), 0.55)
m_dark = mat('raccoglitore_scuro', (0.04, 0.04, 0.045), 0.5)
m_label = mat('etichetta', srgb('#EDEAE3'), 0.7)
m_mug = mat('tazza', (0.8, 0.79, 0.76), 0.25)
m_phone = mat('telefono', (0.02, 0.02, 0.022), 0.3, metal=0.4)
m_screen = mat('schermo', (0.01, 0.01, 0.012), 0.15, emit=(0.02, 0.02, 0.025), estr=1.0)
m_card = mat('card', srgb('#FF5A1F'), 0.4, emit=srgb('#FF5A1F'), estr=2.2)
m_white = mat('bianco', (1, 1, 1), 0.4, emit=(1, 1, 1), estr=3.0)
m_seat = mat('sedia', (0.035, 0.035, 0.04), 0.7)
m_leaf = mat('foglia', (0.05, 0.12, 0.04), 0.6)
m_pot = mat('vaso', (0.5, 0.47, 0.42), 0.8)

w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.05, 0.045, 0.04, 1)

# stanza: pavimento, parete di fondo con finestra (4 pezzi attorno al vano), parete destra
box('pavimento', (0, 1, -0.01), (12, 10, 0.02), m_floor)
WX0, WX1, WZ0, WZ1, WY = -1.6, 1.0, 0.9, 2.5, 3.0
box('muro_sx', ((-6 + WX0) / 2, WY, 1.6), (WX0 + 6, 0.15, 3.2), m_wall)
box('muro_dx', ((WX1 + 6) / 2, WY, 1.6), (6 - WX1, 0.15, 3.2), m_wall)
box('muro_basso', ((WX0 + WX1) / 2, WY, WZ0 / 2), (WX1 - WX0, 0.15, WZ0), m_wall)
box('muro_alto', ((WX0 + WX1) / 2, WY, (WZ1 + 3.2) / 2), (WX1 - WX0, 0.15, 3.2 - WZ1), m_wall)
box('muro_destro', (3.2, 0, 1.6), (0.15, 8, 3.2), m_wall)
box('soffitto', (0, 0, 3.2), (12, 10, 0.05), m_wall)
ext = box('esterno', ((WX0 + WX1) / 2, WY + 1.5, 1.7), (6, 0.05, 4), m_sky); ext.visible_shadow = False
for i in range(30):  # lamelle delle veneziane, inclinate
    z = WZ0 + 0.03 + i * (WZ1 - WZ0) / 30
    box(f'lamella{i}', ((WX0 + WX1) / 2, WY - 0.12, z), (WX1 - WX0 - 0.04, 0.05, 0.003), m_slat, rot=(math.radians(-35), 0, 0))
# scrivania vuota e in ordine
DZ = 0.75
box('piano', (0, 1.5, DZ), (1.7, 0.8, 0.035), m_desk)
for x in (-0.8, 0.8):
    for y in (1.15, 1.85):
        box('gamba', (x, y, DZ / 2), (0.035, 0.035, DZ), m_metal)
# telefono con la card arancione e la spunta sullo schermo
ph = box('telefono', (0.18, 1.35, DZ + 0.022), (0.075, 0.155, 0.008), m_phone, rot=(0, 0, math.radians(-12)))
bev = ph.modifiers.new('b', 'BEVEL'); bev.width = 0.006; bev.segments = 6
scr = box('schermo', (0, 0, 0.51), (0.92, 0.95, 0.02), m_screen); scr.parent = ph
crd = box('card', (0, 0.05, 0.53), (0.78, 0.34, 0.02), m_card); crd.parent = ph
cu = bpy.data.curves.new('spunta', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0011
sp = cu.splines.new('POLY'); pts = [(-0.012, 0.0), (-0.003, -0.009), (0.014, 0.01)]
sp.points.add(2)
for p, (x, y) in zip(sp.points, pts): p.co = (x, y, 0, 1)
chk = bpy.data.objects.new('spunta', cu); sc.collection.objects.link(chk); chk.data.materials.append(m_white)
chk.location = (0.18 + 0.003, 1.35 + 0.004, DZ + 0.027); chk.rotation_euler = (0, 0, math.radians(-12))
# tazza, un solo raccoglitore chiuso, lampada da tavolo spenta
cyl('tazza', (-0.35, 1.62, DZ + 0.065), 0.04, 0.095, m_mug)
box('raccoglitore', (-0.35, 1.25, DZ + 0.035), (0.29, 0.32, 0.05), m_grey, rot=(0, 0, math.radians(8)))
# scaffale a destra con raccoglitori dritti e in ordine
SX = 2.6
for z in (0.4, 1.0, 1.6, 2.2):
    box('ripiano', (SX, 1.6, z), (0.35, 1.6, 0.025), m_desk)
box('fianco', (SX, 0.8, 1.3), (0.35, 0.025, 2.6), m_desk); box('fianco', (SX, 2.4, 1.3), (0.35, 0.025, 2.6), m_desk)
import random; random.seed(3)
for z in (0.4, 1.0, 1.6):
    y = 0.86
    while y < 2.3:
        wdt = 0.075; m = random.choice([m_grey, m_grey, m_dark])
        box('dorso', (SX - 0.02, y + wdt / 2, z + 0.16), (0.29, wdt * 0.95, 0.3), m)
        box('etichetta', (SX - 0.168, y + wdt / 2, z + 0.2), (0.003, wdt * 0.6, 0.11), m_label)
        y += wdt
# lampada da tavolo accesa, luce calda
cyl('base_lampada', (-0.7, 1.75, DZ + 0.03), 0.07, 0.025, m_metal)
box('braccio', (-0.7, 1.72, DZ + 0.24), (0.015, 0.015, 0.42), m_metal, rot=(math.radians(-12), 0, 0))
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.09, radius2=0.035, depth=0.13, location=(-0.7, 1.6, DZ + 0.44), rotation=(math.radians(-40), 0, 0))
sh = bpy.context.object; sh.data.materials.append(m_metal)
lb = bpy.data.lights.new('lampadina', 'POINT'); lb.energy = 25; lb.color = (1, 0.75, 0.45); lb.shadow_soft_size = 0.03
lo = bpy.data.objects.new('lampadina', lb); sc.collection.objects.link(lo); lo.location = (-0.7, 1.57, DZ + 0.4)
# pianta e sedia
cyl('vaso', (-2.2, 2.5, 0.22), 0.16, 0.44, m_pot)
for i in range(14):
    a = i / 14 * math.tau
    box('foglia', (-2.2 + 0.12 * math.cos(a), 2.5 + 0.12 * math.sin(a), 0.75), (0.05, 0.02, 0.6), m_leaf,
        rot=(0.35 * math.sin(a), 0.35 * math.cos(a), a))
box('seduta', (0.05, 2.15, 0.48), (0.5, 0.48, 0.07), m_seat); box('schienale', (0.05, 2.42, 0.85), (0.48, 0.06, 0.6), m_seat)
cyl('colonna', (0.05, 2.15, 0.24), 0.025, 0.45, m_metal)

# luce: sole caldo radente attraverso le veneziane, fill freddo dall'interno, neon spento
sun = bpy.data.lights.new('sole', 'SUN'); sun.energy = 7; sun.color = (1, 0.82, 0.6); sun.angle = math.radians(1.2)
so = bpy.data.objects.new('sole', sun); sc.collection.objects.link(so)
so.rotation_euler = Vector((0.22, -0.85, -0.34)).to_track_quat('-Z', 'Y').to_euler()  # radente, attraverso le veneziane
fl = bpy.data.lights.new('fill', 'AREA'); fl.energy = 60; fl.size = 4; fl.color = (0.8, 0.86, 1)
fo = bpy.data.objects.new('fill', fl); sc.collection.objects.link(fo); fo.location = (0.5, -2.5, 2.6); fo.rotation_euler = (math.radians(60), 0, 0)

def cam(name, loc, target, lens, fstop, focus):
    c = bpy.data.cameras.new(name); c.lens = lens
    c.dof.use_dof = True; c.dof.aperture_fstop = fstop; c.dof.focus_distance = focus
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o); o.location = loc
    t = bpy.data.objects.new(name + '_t', None); sc.collection.objects.link(t); t.location = target
    k = o.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    return o
shots = {
    'largo': cam('largo', (-1.9, -1.3, 1.3), (0.75, 1.55, 0.95), 30, 1.4, 1.6),       # claim: scrivania a destra
    'telefono': cam('telefono', (0.42, 0.95, 1.2), (0.12, 1.42, DZ), 50, 2.0, 0.62),  # end card: telefono a destra
}
sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
for attr, val in [('taa_render_samples', SAMPLES), ('use_shadows', True), ('use_raytracing', True)]:
    if hasattr(e, attr): setattr(e, attr, val)
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
for name, c in shots.items():
    sc.camera = c; sc.render.filepath = f'{out}{name}.jpg'; bpy.ops.render.render(write_still=True)
