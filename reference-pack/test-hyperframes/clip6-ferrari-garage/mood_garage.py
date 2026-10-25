# Style frame per lo spot "Garage" (Ferrari 488, test non ufficiale): garage buio, saracinesca socchiusa,
# drone che entra controluce, auto sotto un telo (simulazione cloth). La 488 vera arriverà da un modello 3D.
# Uso: Blender -b --factory-startup -t 2 -P mood_garage.py -- <cartella/m_> [samples]
import bpy, sys, math, random
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
out = argv[0]; SAMPLES = int(argv[1]) if len(argv) > 1 else 32
random.seed(4)
ASSET = argv[2] if len(argv) > 2 else __import__('os').path.expanduser('~/Desktop/DIGITALIZA/render-clip6/asset')
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, color, rough, emit=None, estr=0.0, metal=0.0, noise=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    if noise:  # cemento lucido a chiazze: la rugosita' varia, i riflessi diventano "pozzanghere"
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = noise; n.inputs['Detail'].default_value = 8
        r = nt.nodes.new('ShaderNodeValToRGB')
        r.color_ramp.elements[0].position = 0.42; r.color_ramp.elements[0].color = (0.08, 0.08, 0.08, 1)
        r.color_ramp.elements[1].position = 0.62; r.color_ramp.elements[1].color = (0.75, 0.75, 0.75, 1)
        nt.links.new(n.outputs['Fac'], r.inputs[0]); nt.links.new(r.outputs[0], p.inputs['Roughness'])
        b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = 0.08
        nt.links.new(n.outputs['Fac'], b.inputs['Height']); nt.links.new(b.outputs[0], p.inputs['Normal'])
    return m
def pbr(name, tex, tile=2.0, tint=1.0, rough_mul=1.0):
    """materiale PBR da texture Poly Haven, proiezione a box in coordinate oggetto (niente UV)"""
    import os
    d = os.path.join(ASSET, 'tex', tex)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / tile, 1 / tile, 1 / tile)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def img(kind, color=True):
        f = os.path.join(d, f'{tex}_{kind}_2k.jpg')
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(f); n.projection = 'BOX'; n.projection_blend = 0.2
        if not color: n.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector']); return n
    dif = img('diff'); hsv = nt.nodes.new('ShaderNodeHueSaturation'); hsv.inputs['Value'].default_value = tint
    nt.links.new(dif.outputs['Color'], hsv.inputs['Color']); nt.links.new(hsv.outputs['Color'], p.inputs['Base Color'])
    rg = img('rough', False); mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'MULTIPLY'; mr.inputs[1].default_value = rough_mul
    nt.links.new(rg.outputs['Color'], mr.inputs[0]); nt.links.new(mr.outputs[0], p.inputs['Roughness'])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nr = img('nor_gl', False)
    nt.links.new(nr.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    return m
def box(name, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m); return o
def cyl(name, loc, r, h, m, rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); return o

m_floor = pbr('pavimento_garage', 'garage_floor', 2.5, 0.6, 0.55)
m_wall = pbr('blocchi', 'concrete_block_wall', 2.0, 0.55)
m_metal = mat('metallo', (0.25, 0.25, 0.26), 0.35, metal=1.0)
m_door = pbr('saracinesca', 'corrugated_iron_02', 1.5, 0.7)
m_day = mat('esterno', (1, 1, 1), 1.0, emit=(1.0, 0.93, 0.85), estr=12.0)
m_tube = mat('neon', (1, 1, 1), 0.3, emit=(0.85, 0.92, 1.0), estr=0.0)
m_cloth = mat('telo', (0.09, 0.09, 0.1), 0.85)
m_tire = mat('gomma', (0.02, 0.02, 0.02), 0.7)
m_cab = mat('cassettiera', (0.12, 0.12, 0.13), 0.4, metal=0.6)
m_drone = mat('drone', (0.02, 0.02, 0.022), 0.4)
m_led_g = mat('led_verde', (0, 0, 0), 0.5, emit=(0.1, 1, 0.2), estr=20)
m_led_r = mat('led_rosso', (0, 0, 0), 0.5, emit=(1, 0.05, 0.03), estr=20)
m_led_w = mat('led_bianco', (0, 0, 0), 0.5, emit=(1, 1, 1), estr=40)

w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
wn = w.node_tree; bgn = wn.nodes['Background']
env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(ASSET + '/hdri/abandoned_garage_2k.exr')
wn.links.new(env.outputs['Color'], bgn.inputs['Color']); bgn.inputs['Strength'].default_value = 0.035  # solo riflessi, il garage resta buio

# --- garage 8 x 12 m, alto 4 m; saracinesca sul fondo (y = 6) alzata per 0.9 m
W, L, H = 8.0, 12.0, 4.0
box('pavimento', (0, 0, -0.05), (W + 4, L + 4, 0.1), m_floor)
box('muro_sx', (-W / 2, 0, H / 2), (0.2, L, H), m_wall); box('muro_dx', (W / 2, 0, H / 2), (0.2, L, H), m_wall)
box('muro_dietro', (0, -L / 2, H / 2), (W, 0.2, H), m_wall); box('soffitto', (0, 0, H), (W, L, 0.2), m_wall)
DW, OPEN = 4.6, 1.3
box('fondo_sx', (-(W + DW) / 4, L / 2, H / 2), ((W - DW) / 2, 0.2, H), m_wall)
box('fondo_dx', ((W + DW) / 4, L / 2, H / 2), ((W - DW) / 2, 0.2, H), m_wall)
box('architrave', (0, L / 2, (3.0 + H) / 2), (DW, 0.2, H - 3.0), m_wall)
for i in range(int((3.0 - OPEN) / 0.1)):  # lamelle della saracinesca
    box('lamella', (0, L / 2 - 0.05, OPEN + 0.05 + i * 0.1), (DW, 0.04, 0.1), m_door)
ext = box('esterno', (0, L / 2 + 4, 1.5), (14, 0.1, 6), m_day); ext.visible_shadow = False
box('asfalto_fuori', (0, L / 2 + 2, -0.04), (10, 4, 0.05), m_floor)
sun = bpy.data.lights.new('sole', 'SUN'); sun.energy = 6; sun.color = (1, 0.9, 0.78); sun.angle = math.radians(0.8)
so = bpy.data.objects.new('sole', sun); sc.collection.objects.link(so)
so.rotation_euler = Vector((0.2, -0.93, -0.28)).to_track_quat('-Z', 'Y').to_euler()
# neon a soffitto (spenti nel primo fotogramma, uno acceso nel secondo)
tubes = []
for x in (-2.0, 2.0):
    for y in (-3.5, 0.0, 3.5):
        box('plafoniera', (x, y, H - 0.15), (0.18, 1.6, 0.06), m_metal)
        tubes.append(box('tubo', (x, y, H - 0.19), (0.06, 1.5, 0.03), m_tube))
# oggetti del garage: cassettiera, pile di gomme, scaffale, tubo dell'aria arrotolato
box('cassettiera', (-W / 2 + 0.45, -2.5, 0.55), (0.6, 1.4, 1.1), m_cab)
for k in range(5):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.3, minor_radius=0.12, location=(W / 2 - 0.6, -3.8, 0.12 + k * 0.24))
    t = bpy.context.object; t.data.materials.append(m_tire)
for z in (0.5, 1.3, 2.1):
    box('ripiano', (W / 2 - 0.35, 1.5, z), (0.5, 2.4, 0.04), m_metal)
    for k in range(6):
        box('scatola', (W / 2 - 0.35, 0.5 + k * 0.38, z + 0.15), (0.4, 0.3, 0.26), m_wall)

# --- auto coperta: sagoma con le proporzioni della 488 (4.57 x 1.95 x 1.21 m) + telo simulato
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.72)); body = bpy.context.object
body.scale = (1.95, 4.57, 1.15)
sub = body.modifiers.new('s', 'SUBSURF'); sub.levels = 4; sub.render_levels = 4
bpy.ops.object.modifier_apply(modifier='s')
def profilo(y):  # altezza relativa della sagoma lungo l'auto (+y = muso)
    pts = [(-0.5, 0.52), (-0.42, 0.6), (-0.2, 0.78), (-0.08, 1.0), (0.05, 1.0), (0.17, 0.62), (0.3, 0.46), (0.5, 0.3)]
    for (y0, h0), (y1, h1) in zip(pts, pts[1:]):
        if y0 <= y <= y1: t = (y - y0) / (y1 - y0); t = t * t * (3 - 2 * t); return h0 + (h1 - h0) * t
    return 0.3
for v in body.data.vertices:
    y = max(-0.5, min(0.5, v.co.y * 1.0 / max(1e-6, 1.0)))
    zt = (v.co.z + 0.5) * profilo(v.co.y)
    v.co.z = -0.5 + zt
    if zt > 0.55:  # abitacolo piu' stretto della carrozzeria
        v.co.x *= 1 - 0.38 * (zt - 0.55) / 0.45
body.data.materials.append(m_cloth)
for x in (-0.93, 0.93):
    for y in (-1.35, 1.25):
        cyl('ruota', (x, y, 0.34), 0.34, 0.28, m_tire, rot=(0, math.radians(90), 0))
for o in [body] + [o for o in sc.objects if o.name.startswith('ruota')] + [sc.objects['pavimento']]:
    o.modifiers.new('c', 'COLLISION'); o.collision.thickness_outer = 0.025
bpy.ops.mesh.primitive_grid_add(x_subdivisions=90, y_subdivisions=110, size=1, location=(0, 0, 1.45))
cloth = bpy.context.object; cloth.scale = (3.4, 6.2, 1); bpy.ops.object.transform_apply(scale=True)
cloth.data.materials.append(m_cloth)
cm = cloth.modifiers.new('cloth', 'CLOTH'); cm.settings.quality = 10; cm.collision_settings.collision_quality = 4; cm.settings.mass = 0.4
cm.settings.tension_stiffness = 8; cm.settings.bending_stiffness = 0.6
cm.collision_settings.distance_min = 0.012; cm.collision_settings.use_self_collision = False
cloth.modifiers.new('sol', 'SOLIDIFY').thickness = 0.006
cloth.modifiers.new('sub', 'SUBSURF').levels = 1
bpy.ops.object.shade_smooth()
sc.frame_start, sc.frame_end = 1, 90
cm.point_cache.frame_end = 90
for f in range(1, 91):  # calcola la simulazione
    sc.frame_set(f)
body.hide_render = False

# --- drone: corpo, 4 bracci, eliche, LED e faro
drone = bpy.data.objects.new('drone', None); sc.collection.objects.link(drone)
parts = [box('corpo', (0, 0, 0), (0.16, 0.22, 0.06), m_drone)]
for sx in (-1, 1):
    for sy in (-1, 1):
        a = box('braccio', (sx * 0.13, sy * 0.13, 0.01), (0.2, 0.025, 0.02), m_drone, rot=(0, 0, math.atan2(sy, sx)))
        e = cyl('elica', (sx * 0.2, sy * 0.2, 0.04), 0.1, 0.004, m_drone); parts += [a, e]
        parts.append(box('led', (sx * 0.2, sy * 0.2, -0.01), (0.02, 0.02, 0.01), m_led_g if sy > 0 else m_led_r))
parts.append(box('faro', (0, -0.12, -0.02), (0.05, 0.02, 0.03), m_led_w))
for p in parts: p.parent = drone
spot = bpy.data.lights.new('faro', 'SPOT'); spot.energy = 1500; spot.spot_size = math.radians(28); spot.spot_blend = 0.4
spot.color = (0.95, 0.97, 1.0); spot.shadow_soft_size = 0.02
sp = bpy.data.objects.new('faro', spot); sc.collection.objects.link(sp); sp.parent = drone; sp.location = (0, -0.14, -0.03)

amb = bpy.data.lights.new('ambiente', 'AREA'); amb.energy = 40; amb.size = 6; amb.color = (0.75, 0.82, 1.0)
ao = bpy.data.objects.new('ambiente', amb); sc.collection.objects.link(ao); ao.location = (0, -2, H - 0.3)
# --- nebbia per i raggi di luce
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, H / 2)); fog = bpy.context.object
fog.scale = (W, L + 6, H); fm = bpy.data.materials.new('nebbia'); fm.use_nodes = True; fog.data.materials.append(fm)
nt = fm.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.06
nt.links.new(pv.outputs[0], nt.nodes['Material Output'].inputs['Volume'])

def cam(name, loc, target, lens, fstop=None, focus=None):
    c = bpy.data.cameras.new(name); c.lens = lens
    if fstop: c.dof.use_dof = True; c.dof.aperture_fstop = fstop; c.dof.focus_distance = focus
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o); o.location = loc
    t = bpy.data.objects.new(name + '_t', None); sc.collection.objects.link(t); t.location = target
    k = o.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    return o

sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
for attr, val in [('taa_render_samples', SAMPLES), ('use_shadows', True), ('use_raytracing', True),
                  ('volumetric_tile_size', '4'), ('volumetric_samples', 96), ('volumetric_end', 40.0), ('use_volumetric_shadows', True), ('volumetric_shadow_samples', 32)]:
    if hasattr(e, attr):
        try: setattr(e, attr, val)
        except Exception: pass
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - High Contrast'
except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.frame_set(90)

# 1) il drone entra da sotto la saracinesca, controluce; l'auto coperta in primo piano
drone.location = (0.9, L / 2 - 1.0, 1.0); drone.rotation_euler = (math.radians(-8), 0, math.radians(180))
sc.camera = cam('C1_ingresso', (1.9, -4.2, 0.6), (-0.9, L / 2, 0.9), 24, 2.8, 9.5)
sc.render.filepath = f'{out}01_drone_entra.jpg'; bpy.ops.render.render(write_still=True)
# 2) il drone sopra il telo, il faro scopre la forma; un neon acceso tremolante
drone.location = (1.3, 1.6, 2.3); drone.rotation_euler = (math.radians(35), 0, math.radians(140))
tubes[3].data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3.0
sc.camera = cam('C2_telo', (3.6, -3.4, 1.0), (0.0, 0.3, 0.7), 35, 2.0, 4.9)
sc.render.filepath = f'{out}02_telo.jpg'; bpy.ops.render.render(write_still=True)
