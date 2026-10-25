# Spot "Sotto il telo" (Ferrari 488 GTB, test portfolio non ufficiale): scena animata completa, 30 s a 30 fps.
# Costruisce la scena, calcola il telo (cloth) in cache su disco e salva un .blend da renderizzare a blocchi.
# Uso: Blender -b --factory-startup -t 2 -P spot_garage.py -- <cartella_lavoro> <animatic|final> [fino_secondi=30]
#   solo la prima scena (0-6 s, fotogrammi 1-180):  ... -- ~/Desktop/DIGITALIZA/render-clip6/scena1 final 6
#   poi: ./render_blocchi.sh ~/Desktop/DIGITALIZA/render-clip6/scena1/spot_garage.blend ~/Desktop/DIGITALIZA/render-clip6/scena1 1 180 30
#   poi: ./render_blocchi.sh <cartella_lavoro>/spot_garage.blend <cartella_lavoro> 1 900 30
# Modello: "Ferrari 488 gtb" di Turbostuart (Sketchfab, CC BY). Asset CC0: Poly Haven.
import bpy, bmesh, sys, os, math, random
from mathutils import Vector, Euler, Matrix, Quaternion
argv = sys.argv[sys.argv.index('--') + 1:]
WORK = os.path.abspath(argv[0]); MODE = argv[1] if len(argv) > 1 else 'animatic'
FINO = float(argv[2]) if len(argv) > 2 else 30.0   # secondi da preparare: 6 = solo la prima scena (C1_saracinesca)
HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.expanduser('~/Desktop/DIGITALIZA/render-clip6/asset')
GLB = os.path.join(HERE, 'modello', 'ferrari_488_gtb.glb')
sys.path.insert(0, HERE)
import car488
import garage_v2 as g2
random.seed(4)
os.makedirs(WORK, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
FPS = 30
sc.render.fps = FPS
def F(t): return int(round(t * FPS)) + 1
sc.frame_start, sc.frame_end = 1, F(FINO) - 1
FINAL = MODE == 'final'

# ------------------------------------------------------------------ materiali e utilita'
def mat(name, color, rough, emit=None, estr=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emit: p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    return m
def pbr(name, tex, tile=2.0, tint=1.0, rough_mul=1.0):
    d = os.path.join(ASSET, 'tex', tex)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / tile,) * 3
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def img(kind, color=True):
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.join(d, f'{tex}_{kind}_2k.jpg'))
        n.projection = 'BOX'; n.projection_blend = 0.2
        if not color: n.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector']); return n
    hsv = nt.nodes.new('ShaderNodeHueSaturation'); hsv.inputs['Value'].default_value = tint
    nt.links.new(img('diff').outputs['Color'], hsv.inputs['Color']); nt.links.new(hsv.outputs['Color'], p.inputs['Base Color'])
    mr = nt.nodes.new('ShaderNodeMath'); mr.operation = 'MULTIPLY'; mr.inputs[1].default_value = rough_mul
    nt.links.new(img('rough', False).outputs['Color'], mr.inputs[0]); nt.links.new(mr.outputs[0], p.inputs['Roughness'])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(img('nor_gl', False).outputs['Color'], nm.inputs['Color'])
    nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    return m
def link(o): sc.collection.objects.link(o); return o
def box(name, loc, size, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m); return o
def cyl(name, loc, r, h, m, rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); return o
def keyval(sock_owner, attr, pairs, interp=None):
    for f, v in pairs:
        setattr(sock_owner, attr, v); sock_owner.keyframe_insert(attr, frame=f)
def emis(m): return m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
def visible(o, f_on=None, f_off=None):
    """o visibile solo tra f_on e f_off (None = da sempre / per sempre)"""
    o.hide_render = f_on is not None; o.keyframe_insert('hide_render', frame=1)
    if f_on: o.hide_render = False; o.keyframe_insert('hide_render', frame=f_on)
    if f_off: o.hide_render = True; o.keyframe_insert('hide_render', frame=f_off)

m_floor = g2.floor_material(ASSET)   # v2: cemento 4K con giunti, gomme, olio, pozze
m_asphalt = pbr('asfalto', 'garage_floor', 2.5, 0.45, 0.8)
m_wood = mat('legno_banco', (0.22, 0.15, 0.09), 0.6)
m_wall = pbr('blocchi', 'concrete_block_wall', 2.0, 0.32)
m_ceil = mat('soffitto', (0.035, 0.035, 0.037), 0.85)
m_door = pbr('saracinesca', 'corrugated_iron_02', 1.5, 0.7)
m_metal = mat('metallo', (0.2, 0.2, 0.21), 0.6, metal=0.6)   # acciaio opaco: non specchia la saracinesca
m_day = mat('esterno', (1, 1, 1), 1.0, emit=(1.0, 0.93, 0.85), estr=8.0)
m_tube = mat('neon', (0.03, 0.03, 0.032), 0.9, emit=(0.85, 0.92, 1.0), estr=0.0)   # spento: scuro, non bianco
m_cloth = g2.cloth_material(ASSET)   # v2: trama di tessuto e polvere
m_tire = mat('gomma', (0.02, 0.02, 0.02), 0.7)
m_cab = mat('cassettiera', (0.12, 0.12, 0.13), 0.4, metal=0.6)
m_drone = mat('drone', (0.02, 0.02, 0.022), 0.4)
m_led_g = mat('led_verde', (0, 0, 0), 0.5, emit=(0.1, 1, 0.2), estr=20)
m_led_r = mat('led_rosso', (0, 0, 0), 0.5, emit=(1, 0.05, 0.03), estr=20)
m_led_w = mat('led_bianco', (0, 0, 0), 0.5, emit=(1, 1, 1), estr=40)

g2.world(sc, ASSET)   # v2: fuori dalla saracinesca si vede un cortile industriale vero (HDRI)

# ------------------------------------------------------------------ garage 8 x 12 m, saracinesca sul fondo (y = +6)
W, L, H = 8.0, 12.0, 4.0
floor = box('pavimento', (0, 0, -0.05), (W + 4, L + 4, 0.1), m_floor)
box('muro_sx', (-W / 2, 0, H / 2), (0.2, L, H), m_wall); box('muro_dx', (W / 2, 0, H / 2), (0.2, L, H), m_wall)
box('muro_dietro', (0, -L / 2, H / 2), (W, 0.2, H), m_wall); box('soffitto', (0, 0, H), (W, L, 0.2), m_ceil)
DW, DH, OPEN = 4.6, 3.0, 1.3
box('fondo_sx', (-(W + DW) / 4, L / 2, H / 2), ((W - DW) / 2, 0.2, H), m_wall)
box('fondo_dx', ((W + DW) / 4, L / 2, H / 2), ((W - DW) / 2, 0.2, H), m_wall)
box('architrave', (0, L / 2, (DH + H) / 2), (DW, 0.2, H - DH), m_wall)
door = link(bpy.data.objects.new('saracinesca', None))
for i in range(int(DH / 0.1)):
    s_ = box('lamella', (0, L / 2 - 0.05, 0.05 + i * 0.1), (DW, 0.04, 0.1), m_door); s_.parent = door
# saracinesca: chiusa, si alza di 1.3 m tra 0.4 e 3.0 s (le lamelle in alto spariscono dentro l'architrave)
keyval(door, 'location', [(1, Vector((0, 0, 0))), (F(0.4), Vector((0, 0, 0))), (F(3.0), Vector((0, 0, OPEN)))])
box('asfalto_fuori', (0, L / 2 + 12, -0.04), (40, 24, 0.05), m_asphalt)
dl = bpy.data.lights.new('luce_porta', 'AREA'); dl.shape = 'RECTANGLE'; dl.size = DW; dl.size_y = 1.0; dl.energy = 0
dl.color = (1.0, 0.88, 0.72)   # luce calda del giorno che entra dalla fessura
dlo = link(bpy.data.objects.new('luce_porta', dl)); dlo.location = (0, L / 2 + 0.3, 0.6); dlo.rotation_euler = (math.radians(-90), 0, 0)
keyval(dl, 'energy', [(1, 0), (F(0.4), 0), (F(3.0), 700)])
sun = bpy.data.lights.new('sole', 'SUN'); sun.energy = 6; sun.color = (1, 0.9, 0.78); sun.angle = math.radians(0.8)
so = link(bpy.data.objects.new('sole', sun)); so.rotation_euler = Vector((0.2, -0.93, -0.3)).to_track_quat('-Z', 'Y').to_euler()
amb = bpy.data.lights.new('ambiente', 'AREA'); amb.energy = 35; amb.size = 6; amb.color = (0.75, 0.82, 1.0); amb.use_shadow = False
ao = link(bpy.data.objects.new('ambiente', amb)); ao.location = (0, -2, H - 0.3)

tubes, tube_lights = [], []
for x in (-2.0, 2.0):
    for y in (-3.5, 0.0, 3.5):
        box('plafoniera', (x, y, H - 0.15), (0.18, 1.6, 0.06), m_metal)
        tm = m_tube.copy(); t = box('tubo', (x, y, H - 0.19), (0.06, 1.5, 0.03), tm); tubes.append(t)
        l = bpy.data.lights.new('neon', 'AREA'); l.shape = 'RECTANGLE'; l.size = 0.1; l.size_y = 1.5; l.energy = 0
        l.color = (0.85, 0.92, 1.0); l.use_shadow = (x < 0 and y == 0.0)   # una sola ombra: Eevee resta leggero
        lo = link(bpy.data.objects.new('neon', l)); lo.location = (x, y, H - 0.25); tube_lights.append(l)
def neon_on(i, t0, flicker=True):
    m = tubes[i].data.materials[0]; e = emis(m); l = tube_lights[i]
    seq = [(t0 - 0.01, 0), (t0, 1), (t0 + 0.07, 0.1), (t0 + 0.13, 1), (t0 + 0.2, 0.3), (t0 + 0.3, 1)] if flicker else [(t0 - 0.01, 0), (t0, 1)]
    for t, v in [(0, 0)] + seq:
        f = max(1, F(t)); e.default_value = 3.0 * v; e.keyframe_insert('default_value', frame=f)
        l.energy = 60 * v; l.keyframe_insert('energy', frame=f)
# un neon si accende tremolando nel POV (7.5 s); alla rivelazione si accendono tutti in sequenza
neon_on(2, 7.5)
for k, i in enumerate([1, 4, 0, 3, 5]):
    neon_on(i, 15.25 + 0.22 * k)
# interpolazione a gradino: con le curve morbide i neon si "accendevano" gia' prima del tempo (curva che anticipa il valore)
from bpy_extras import anim_utils
for idb in [t.data.materials[0].node_tree for t in tubes] + tube_lights:
    ad = idb.animation_data
    if not ad or not ad.action: continue
    for fc in anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves:
        for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
# oggetti del garage (v2: modelli CC0 di Poly Haven)
g2.props(ASSET, W, L, H, box, m_metal, m_wood)

# ------------------------------------------------------------------ la 488 (muso verso -Y, coda verso la saracinesca)
car = car488.load(GLB)
car_meshes = [o for o in car.children_recursive if o.type == 'MESH' and not o.hide_render]
glass_objs = [o for o in car_meshes if any(m and m.surface_render_method == 'BLENDED' and m.name != 'Color_A08' for m in o.data.materials)]
# collisore per il telo: sagoma CHIUSA ricavata dalle misure vere dell'auto (la carrozzeria del glb e' un guscio aperto
# e il telo ci passava attraverso). Per ogni fetta lungo Y: altezza e larghezza massime, piu' 3 cm di margine.
pts = []
for o in car_meshes:
    mw = o.matrix_world
    for v in o.data.vertices: pts.append(mw @ v.co)
ymin = min(p.y for p in pts); ymax = max(p.y for p in pts); NB = 36
hb = [0.0] * NB; wb = [0.0] * NB
mir = {1: [], -1: []}
for p in pts:
    i = min(NB - 1, int((p.y - ymin) / (ymax - ymin) * NB))
    if abs(p.x) < 0.5: hb[i] = max(hb[i], p.z)
    if abs(p.x) < 1.0 and p.z > 0.25: wb[i] = max(wb[i], abs(p.x))
    if abs(p.x) >= 1.0 and p.z > 0.6: mir[1 if p.x > 0 else -1].append(p)
for i in range(NB):   # niente buchi tra le fette
    if hb[i] == 0: hb[i] = hb[i - 1] if i else 0.5
    if wb[i] == 0: wb[i] = wb[i - 1] if i else 0.8
bm = bmesh.new(); rings = []; NS = 20; M = 0.03
for i in range(NB + 1):
    y = ymin - M + (ymax - ymin + 2 * M) * i / NB; k = min(i, NB - 1)
    h = hb[k] + M; wd = wb[k] + M; z0 = 0.14
    ring = []
    for j in range(NS):
        a_ = j / NS * math.tau
        cx, cz = math.cos(a_), math.sin(a_)
        x = wd * math.copysign(abs(cx) ** 0.5, cx)                 # sezione "squadrata" tipo superellisse
        z = z0 + (h - z0) * (0.5 + 0.5 * math.copysign(abs(cz) ** 0.6, cz))
        ring.append(bm.verts.new((x, y, z)))
    rings.append(ring)
for r0, r1 in zip(rings, rings[1:]):
    for j in range(NS): bm.faces.new((r0[j], r0[(j + 1) % NS], r1[(j + 1) % NS], r1[j]))
bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
me = bpy.data.meshes.new('collisore_auto'); bm.to_mesh(me); bm.free()
col = link(bpy.data.objects.new('collisore_auto', me))
for sgn, pp in mir.items():   # specchietti
    if not pp: continue
    lo_ = Vector((min(q.x for q in pp), min(q.y for q in pp), min(q.z for q in pp))); hi_ = Vector((max(q.x for q in pp), max(q.y for q in pp), max(q.z for q in pp)))
    mb = box('collisore_specchio', (lo_ + hi_) / 2, (hi_ - lo_) + Vector((0.06, 0.06, 0.06)), m_cloth)
    mb.hide_render = True; mb.display_type = 'WIRE'; mb.modifiers.new('c', 'COLLISION'); mb.collision.thickness_outer = 0.02
CAR_H = max(hb)
col.hide_render = True; col.display_type = 'WIRE'
for o in (col, floor):
    o.modifiers.new('c', 'COLLISION'); o.collision.thickness_outer = 0.02

# ------------------------------------------------------------------ telo: prima si appoggia (pre-roll), poi diventa la forma di partenza
bpy.ops.mesh.primitive_grid_add(x_subdivisions=70, y_subdivisions=95, size=1, location=(0, 0, CAR_H + 0.25))
cloth = bpy.context.object; cloth.name = 'telo'; cloth.scale = (3.9, 6.4, 1); bpy.ops.object.transform_apply(scale=True)   # misura giusta: l'orlo arriva a terra e fa pieghe, non un tappeto
cloth.data.materials.append(m_cloth)
pin_idx = [v.index for v in cloth.data.vertices if v.co.y < -3.05 and abs(v.co.x) < 0.5]
cm = cloth.modifiers.new('cloth', 'CLOTH'); cm.settings.quality = 8; cm.settings.mass = 0.4
cm.settings.tension_stiffness = 10; cm.settings.bending_stiffness = 2.5   # tela pesante: pieghe larghe
cm.collision_settings.collision_quality = 3; cm.collision_settings.distance_min = 0.012; cm.collision_settings.use_self_collision = True
cm.point_cache.frame_start, cm.point_cache.frame_end = 1, 110
for f in range(1, 111): sc.frame_set(f)
bpy.context.view_layer.objects.active = cloth
bpy.ops.object.modifier_apply(modifier='cloth')
sc.frame_set(1)
vg = cloth.vertex_groups.new(name='presa'); vg.add(pin_idx, 1.0, 'REPLACE')
grab = sum((cloth.data.vertices[i].co for i in pin_idx), Vector()) / len(pin_idx)
hook_e = link(bpy.data.objects.new('gancio', None)); hook_e.location = grab
hk = cloth.modifiers.new('gancio', 'HOOK'); hk.object = hook_e; hk.vertex_group = 'presa'; hk.center = grab
hk.matrix_inverse = Matrix.Translation(grab).inverted()
cm = cloth.modifiers.new('cloth', 'CLOTH'); cm.settings.quality = 8; cm.settings.mass = 0.4
cm.settings.tension_stiffness = 8; cm.settings.bending_stiffness = 0.6; cm.settings.vertex_group_mass = 'presa'
cm.collision_settings.collision_quality = 3; cm.collision_settings.distance_min = 0.012
# il telo e' fermo fino al tiro (12.5 s): la simulazione parte poco prima, risparmia ~18 minuti di calcolo
cm.point_cache.frame_start, cm.point_cache.frame_end = F(12.3), min(F(17), sc.frame_end)
cloth.modifiers.new('sol', 'SOLIDIFY').thickness = 0.006
cloth.modifiers.new('sub', 'SUBSURF').levels = 1
for p in cloth.data.polygons: p.use_smooth = True

# ------------------------------------------------------------------ drone: traiettoria morbida (Catmull-Rom), inclinazione in curva, micro-ondeggiamento
drone = link(bpy.data.objects.new('drone', None)); drone.rotation_mode = 'QUATERNION'
parts = [box('corpo', (0, 0, 0), (0.16, 0.22, 0.06), m_drone)]
for sx in (-1, 1):
    for sy in (-1, 1):
        parts.append(box('braccio', (sx * 0.13, sy * 0.13, 0.01), (0.2, 0.025, 0.02), m_drone, rot=(0, 0, math.atan2(sy, sx))))
        e_ = cyl('elica', (sx * 0.2, sy * 0.2, 0.04), 0.1, 0.004, m_drone); parts.append(e_)
        parts.append(box('led', (sx * 0.2, sy * 0.2, -0.01), (0.02, 0.02, 0.01), m_led_g if sy < 0 else m_led_r))
parts.append(box('faro', (0, -0.12, -0.02), (0.05, 0.02, 0.03), m_led_w))
for p in parts: p.parent = drone
spot = bpy.data.lights.new('faro', 'SPOT'); spot.energy = 1500; spot.spot_size = math.radians(30); spot.spot_blend = 0.4
spot.color = (0.95, 0.97, 1.0); spot.shadow_soft_size = 0.02
sp = link(bpy.data.objects.new('faro', spot)); sp.parent = drone; sp.location = (0, -0.14, -0.03)
sp.rotation_euler = (math.radians(-60), 0, 0)   # il faro guarda avanti e in basso
WAY = [  # (secondi, posizione) — il drone guarda nella direzione in cui vola (muso = -Y locale)
    (0.0, (0.6, 9.0, 0.5)), (3.0, (0.8, 6.8, 0.45)), (3.7, (0.7, 4.9, 0.6)), (4.6, (0.4, 2.8, 1.7)),
    (5.4, (-0.6, 0.4, 2.3)), (6.3, (-1.8, -2.2, 2.4)), (7.6, (-2.6, -1.0, 2.6)), (9.0, (1.7, -0.6, 2.4)),
    (10.6, (1.9, 1.1, 2.2)), (11.9, (0.4, -3.4, 1.5)), (12.5, (grab.x, grab.y - 0.05, grab.z + 0.25)),
    (13.0, (0.0, -2.4, 1.7)), (13.8, (0.0, 0.4, 2.7)), (14.6, (0.0, 3.3, 2.5)), (15.3, (0.4, 5.2, 1.9)),
    (16.4, (-1.2, 2.0, 2.6)), (17.6, (-1.7, -1.0, 2.6)), (18.0, (-1.7, -1.1, 2.6))]
def catmull(t):
    ts = [w_[0] for w_ in WAY]; ps = [Vector(w_[1]) for w_ in WAY]
    if t <= ts[0]: return ps[0]
    if t >= ts[-1]: return ps[-1]
    i = max(k for k in range(len(ts) - 1) if ts[k] <= t)
    p0, p1, p2, p3 = ps[max(i - 1, 0)], ps[i], ps[i + 1], ps[min(i + 2, len(ps) - 1)]
    u = (t - ts[i]) / (ts[i + 1] - ts[i]); u = u * u * (3 - 2 * u) * 0.35 + u * 0.65   # un po' di ease su ogni tratto
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
dt = 1 / FPS; yaw = math.pi
for f in range(1, F(18) + 1, 2):
    t = (f - 1) / FPS
    p = catmull(t); v = (catmull(t + dt) - catmull(t - dt)) / (2 * dt); a = (catmull(t + dt) - 2 * p + catmull(t - dt)) / (dt * dt)
    if v.xy.length > 0.15: yaw = math.atan2(-v.x, v.y) + math.pi   # muso (-Y locale) verso la direzione di volo
    tilt_f = max(-0.35, min(0.35, -v.xy.length * 0.06))            # in avanti quando accelera
    roll = max(-0.4, min(0.4, (a.x * math.cos(yaw) + a.y * math.sin(yaw)) * 0.03))
    wob = Vector((math.sin(t * 1.7) * 0.012, math.cos(t * 1.3) * 0.012, math.sin(t * 2.3) * 0.015))
    drone.location = p + wob
    drone.rotation_quaternion = Euler((tilt_f + 0.02 * math.sin(t * 2.9), roll + 0.02 * math.cos(t * 2.1), yaw)).to_quaternion()
    drone.keyframe_insert('location', frame=f); drone.keyframe_insert('rotation_quaternion', frame=f)
visible(drone, None, F(18))
for p in parts: visible(p, None, F(18))
spot.energy = 0; spot.keyframe_insert('energy', frame=1); spot.keyframe_insert('energy', frame=F(3.4))
spot.energy = 1500; spot.keyframe_insert('energy', frame=F(3.6)); spot.keyframe_insert('energy', frame=F(17.5))
spot.energy = 0; spot.keyframe_insert('energy', frame=F(17.8))
# il gancio resta sul telo fino a 12.5 s, poi segue il drone fino a 15.3 s, poi lascia
hook_e.keyframe_insert('location', frame=F(12.5))
for f in range(F(12.5) + 2, F(15.3) + 1, 2):
    hook_e.location = catmull((f - 1) / FPS) + Vector((0, 0, -0.18)); hook_e.keyframe_insert('location', frame=f)

# ------------------------------------------------------------------ nebbia (solo nel finale) e luce che corre sulla carrozzeria
if FINAL:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, H / 2)); fog = bpy.context.object
    fog.scale = (W, L + 6, H); fm = bpy.data.materials.new('nebbia'); fm.use_nodes = True; fog.data.materials.append(fm)
    nt = fm.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
    pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.015
    nt.links.new(pv.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
sw = bpy.data.lights.new('striscia', 'AREA'); sw.shape = 'RECTANGLE'; sw.size = 3.0; sw.size_y = 0.15; sw.energy = 0
swo = link(bpy.data.objects.new('striscia', sw)); swo.rotation_euler = (0, 0, 0)
for t, y, e_ in [(15.4, -3.5, 0), (15.6, -3.0, 250), (17.4, 3.2, 250), (17.6, 3.6, 0)]:
    swo.location = (0, y, 2.6); swo.keyframe_insert('location', frame=F(t)); sw.energy = e_; sw.keyframe_insert('energy', frame=F(t))

# ------------------------------------------------------------------ il quadro strumenti (set separato, lontano dal garage)
QX = Vector((100, 0, 0))
m_face = mat('quadrante', (0.55, 0.015, 0.012), 0.35, emit=(0.6, 0.01, 0.01), estr=0.6)
m_tick = mat('tacche', (1, 1, 1), 0.3, emit=(1, 0.95, 0.9), estr=4)
m_redz = mat('zona_rossa', (1, 1, 1), 0.3, emit=(1, 0.85, 0.2), estr=6)
m_needle = mat('lancetta', (1, 1, 1), 0.3, emit=(1, 0.55, 0.12), estr=5)
m_black = mat('nero', (0.012, 0.012, 0.013), 0.35)
m_carbon = mat('carbonio', (0.02, 0.02, 0.022), 0.25, metal=0.3)
m_screen = mat('schermo', (0.003, 0.003, 0.004), 0.1, emit=(0.02, 0.02, 0.03), estr=1)
m_digit = mat('cifre', (1, 1, 1), 0.3, emit=(1, 1, 1), estr=8)
m_devil = mat('diavolo', (1, 1, 1), 0.3, emit=(1, 0.22, 0.03), estr=2.6)
m_core = mat('diavolo_core', (1, 1, 1), 0.3, emit=(1, 0.55, 0.2), estr=3.5)
FONT = None
try: FONT = bpy.data.fonts.load('/System/Library/Fonts/HelveticaNeue.ttc')
except Exception: pass
def text(body, loc, size, m):
    c = bpy.data.curves.new('t', 'FONT'); c.body = body; c.size = size; c.align_x = 'CENTER'; c.align_y = 'CENTER'
    if FONT: c.font = FONT
    o = link(bpy.data.objects.new('t', c)); o.location = QX + Vector(loc); o.data.materials.append(m); return o
R = 1.0
cyl('quadrante', QX, R, 0.05, m_face, verts=96)
bpy.ops.mesh.primitive_torus_add(major_radius=R + 0.04, minor_radius=0.05, location=QX + Vector((0, 0, 0.03))); bpy.context.object.data.materials.append(m_carbon)
A0, A1 = math.radians(225), math.radians(-45)
for i in range(0, 101):
    a = A0 + (A1 - A0) * i / 100; big = i % 10 == 0; Ln = 0.14 if big else 0.06
    c = Vector((math.cos(a), math.sin(a), 0)) * (R - 0.06 - Ln / 2)
    box('tacca', QX + Vector((c.x, c.y, 0.03)), (Ln, 0.012 if big else 0.006, 0.004), m_redz if i >= 90 else m_tick, rot=(0, 0, a))
    if big:
        p = Vector((math.cos(a), math.sin(a), 0)) * (R - 0.32); text(str(i // 10), (p.x, p.y, 0.03), 0.15, m_redz if i >= 90 else m_tick)
text('x1000 RPM', (0, -0.42, 0.03), 0.06, m_tick)
piv = link(bpy.data.objects.new('perno', None)); piv.location = QX + Vector((0, 0, 0.05))
nd = box('lancetta', (0.42, 0, 0), (0.86, 0.02, 0.01), m_needle); nd.parent = piv; nd.location = (0.42, 0, 0)
cyl('mozzo', QX + Vector((0, 0, 0.06)), 0.1, 0.06, m_black, verts=48)
box('schermo_dx', QX + Vector((1.75, 0, -0.01)), (1.25, 0.95, 0.02), m_screen); box('schermo_sx', QX + Vector((-1.75, 0, -0.01)), (1.25, 0.95, 0.02), m_screen)
text('km/h', (1.7, -0.25, 0.01), 0.12, m_tick); text('RPM', (-1.75, -0.22, 0.01), 0.1, m_tick)
# lancetta: giro di prova a 20.5 s, poi sale a fondo scala tra 22.2 e 24 s
def ang(x): return A0 + (A1 - A0) * x
for t, x in [(0, 0), (20.5, 0), (20.9, 0.55), (21.4, 0.08), (22.2, 0.08), (23.2, 0.7), (24.0, 0.97), (24.2, 0.95), (24.4, 0.97), (27, 0.97)]:
    piv.rotation_euler = (0, 0, ang(x)); piv.keyframe_insert('rotation_euler', frame=F(t))
# numero della velocita': Geometry Nodes (valore animato -> testo), 0 -> 375 km/h
def number_obj(name, loc, size, pairs):
    me = bpy.data.meshes.new(name); o = link(bpy.data.objects.new(name, me)); o.location = QX + Vector(loc)
    me.materials.append(m_digit)
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    n = ng.nodes; li = ng.links
    gout = n.new('NodeGroupOutput'); val = n.new('ShaderNodeValue')
    v2s = n.new('FunctionNodeValueToString'); s2c = n.new('GeometryNodeStringToCurves'); rl = n.new('GeometryNodeRealizeInstances')
    fill = n.new('GeometryNodeFillCurve'); sm = n.new('GeometryNodeSetMaterial'); sm.inputs['Material'].default_value = m_digit
    s2c.inputs['Size'].default_value = size
    for k, v in (('align_x', 'CENTER'), ('align_y', 'MIDDLE')):
        if hasattr(s2c, k): setattr(s2c, k, v)
        else:
            sock = s2c.inputs.get('Align ' + k[-1].upper())
            if sock is not None:
                try: sock.default_value = v.title()
                except Exception:
                    try: sock.default_value = v
                    except Exception: pass
    if FONT:
        if 'Font' in s2c.inputs: s2c.inputs['Font'].default_value = FONT
        elif hasattr(s2c, 'font'): s2c.font = FONT
    li.new(val.outputs[0], v2s.inputs['Value']); li.new(v2s.outputs['String'], s2c.inputs['String'])
    li.new(s2c.outputs['Curve Instances'], rl.inputs['Geometry']); li.new(rl.outputs['Geometry'], fill.inputs['Curve'])
    li.new(fill.outputs['Mesh'], sm.inputs['Geometry']); li.new(sm.outputs['Geometry'], gout.inputs['Geometry'])
    mod = o.modifiers.new('numero', 'NODES'); mod.node_group = ng
    out_ = val.outputs[0]
    for f, v in pairs: out_.default_value = v; out_.keyframe_insert('default_value', frame=f)
    return o
number_obj('velocita', (1.7, 0.1, 0.02), 0.42, [(F(22.2), 0), (F(23.0), 120), (F(23.7), 300), (F(24.1), 375)])
number_obj('giri', (-1.75, 0.1, 0.02), 0.3, [(F(22.2), 800), (F(24.0), 9800)])
# il diavolo: linee al neon che si disegnano (24-25.5 s) e vengono verso la camera (25.5-27 s)
devil = link(bpy.data.objects.new('diavolo', None)); devil.location = QX + Vector((0, 0, 0.55))
def neon(points, m, bevel):
    cu = bpy.data.curves.new('neon', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = bevel; cu.bevel_resolution = 4
    cu.bevel_factor_mapping_end = 'SPLINE'
    s_ = cu.splines.new('BEZIER'); s_.bezier_points.add(len(points) - 1)
    for bp, (x, y, z) in zip(s_.bezier_points, points):
        bp.co = (x, y, z); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = link(bpy.data.objects.new('neon', cu)); o.data.materials.append(m); o.parent = devil
    cu.bevel_factor_end = 0.0; cu.keyframe_insert('bevel_factor_end', frame=F(24.0))
    cu.bevel_factor_end = 1.0; cu.keyframe_insert('bevel_factor_end', frame=F(25.4))
    return o
for s_ in (-1, 1):
    neon([(s_ * 0.3, 0.36, 0.0), (s_ * 0.55, 0.62, 0.05), (s_ * 0.5, 0.95, 0.1), (s_ * 0.36, 1.1, 0.14)], m_devil, 0.016)
    neon([(s_ * 0.36, 0.16, 0.06), (s_ * 0.1, 0.04, 0.08)], m_core, 0.013)
neon([(-0.4, 0.4, 0.0), (-0.44, 0.05, 0.03), (-0.3, -0.4, 0.06), (0.0, -0.78, 0.09), (0.3, -0.4, 0.06), (0.44, 0.05, 0.03), (0.4, 0.4, 0.0)], m_devil, 0.016)
neon([(-0.2, -0.2, 0.08), (-0.08, -0.3, 0.09), (0.08, -0.3, 0.09), (0.2, -0.2, 0.08)], m_core, 0.011)
keyval(devil, 'location', [(F(25.4), QX + Vector((0, 0, 0.55))), (F(27.0), QX + Vector((0, 0.1, 3.2)))])
keyval(devil, 'scale', [(F(25.4), Vector((1, 1, 1))), (F(27.0), Vector((1.6, 1.6, 1.6)))])
glow = bpy.data.lights.new('bagliore', 'POINT'); glow.energy = 0; glow.color = (1, 0.35, 0.1)
go = link(bpy.data.objects.new('bagliore', glow)); go.parent = devil; go.location = (0, 0.1, 0.6)
keyval(glow, 'energy', [(F(24.0), 0), (F(25.0), 60), (F(27.0), 120)])
sparks = []
for i in range(40):
    a = random.random() * math.tau; r = random.uniform(0.3, 1.8)
    s_ = box('scintilla', QX + Vector((math.cos(a) * r, math.sin(a) * r * 0.7, random.uniform(0.3, 1.6))), (0.006,) * 3, m_core)
    visible(s_, F(24.5), None); sparks.append(s_)
    z0 = s_.location.z
    keyval(s_, 'location', [(F(24.5), s_.location.copy()), (F(27.0), s_.location + Vector((0, 0, 1.5 + random.random())))])

# ------------------------------------------------------------------ camere e tagli
def cam(name, lens, fstop=None):
    c = bpy.data.cameras.new(name); c.lens = lens; c.clip_start = 0.02
    if fstop: c.dof.use_dof = True; c.dof.aperture_fstop = fstop
    o = link(bpy.data.objects.new(name, c)); t = link(bpy.data.objects.new(name + '_t', None))
    k = o.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    c.dof.focus_object = t
    return o, t
def path(o, t_, keys):  # keys: (secondi, posizione camera, punto guardato)
    for t, p, q in keys:
        o.location = p; o.keyframe_insert('location', frame=F(t)); t_.location = q; t_.keyframe_insert('location', frame=F(t))
shots = []
c1, t1 = cam('C1_saracinesca', 24, 2.8)
path(c1, t1, [(0, (1.9, -4.4, 0.6), (-0.9, 6, 0.9)), (6.0, (1.7, -3.9, 0.62), (-0.6, 6, 1.2))]); shots.append((0, c1))
c2, t2 = cam('C2_POV_drone', 18)
path(c2, t2, [(6.0, (2.4, 4.8, 1.8), (3.0, 2.0, 1.4)), (6.8, (3.0, 2.6, 1.4), (2.9, 0.0, 1.2)), (7.6, (3.0, 0.4, 1.3), (2.6, -2.8, 1.0)),
              (8.4, (2.5, -2.4, 1.0), (0.6, -3.6, 0.8)), (9.0, (1.6, -3.6, 1.1), (0.0, -1.5, 0.6))]); shots.append((6.0, c2))
c3, t3 = cam('C3_orbita', 20, 4.0)
# orbita davanti al muso, dentro le pareti e lontano dall'arredo (prima usciva dal muro destro)
orb = [(9.0 + i * 0.5, (3.3 * math.cos(math.radians(-135 + i * 15)), 3.95 * math.sin(math.radians(-135 + i * 15)), 1.75), (0, 0.2, 1.1)) for i in range(7)]
path(c3, t3, orb); shots.append((9.0, c3))
c4, t4 = cam('C4_telo', 26, 4.0)
path(c4, t4, [(12.0, (-3.0, -5.3, 1.2), (0, 0.3, 0.8)), (15.0, (-2.8, -5.0, 1.1), (0, 0.6, 0.9))])   # lato sinistro: a destra gomme e carrello coprivano l'auto; shots.append((12.0, c4))
c5, t5 = cam('C5_rivelazione', 30, 2.8)
path(c5, t5, [(15.0, (3.4, -3.9, 0.55), (0, -0.4, 0.55)), (18.0, (2.9, -3.3, 0.5), (0, -0.2, 0.55))]); shots.append((15.0, c5))
c6, t6 = cam('C6_POV_finestrino', 20)
path(c6, t6, [(18.0, (2.6, -0.7, 1.8), (0.8, -0.5, 0.9)), (19.0, (1.6, -0.4, 1.15), (0.5, -0.6, 0.95)),
              (19.6, (1.05, -0.35, 1.02), (0.4, -0.9, 0.9)), (20.6, (0.45, -0.3, 0.98), (0.38, -1.2, 0.85)),
              (22.0, (0.42, -0.62, 0.93), (0.38, -1.2, 0.85))]); shots.append((18.0, c6))
for g in glass_objs: visible(g, None, F(18)); g.hide_render = False; g.keyframe_insert('hide_render', frame=F(22))
c7, t7 = cam('C7_quadro', 50, 2.2)
path(c7, t7, [(22.0, QX + Vector((0.6, -1.0, 6.2)), QX + Vector((0.2, 0.0, 0.4))), (27.0, QX + Vector((0.45, -0.8, 5.4)), QX + Vector((0.2, 0.05, 0.6)))])
shots.append((22.0, c7))
c8, t8 = cam('C8_nero', 50)
path(c8, t8, [(27.0, (300, 0, 5), (300, 0, 0))]); shots.append((27.0, c8))
for t, c in shots:
    m = sc.timeline_markers.new(c.name, frame=F(t)); m.camera = c
sc.camera = c1

# ------------------------------------------------------------------ render
sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
settings = [('taa_render_samples', 24 if FINAL else 8), ('use_shadows', True), ('use_raytracing', FINAL),
            ('volumetric_tile_size', '8'), ('volumetric_samples', 64), ('use_volumetric_shadows', FINAL)]
for attr, val in settings:
    if hasattr(e, attr):
        try: setattr(e, attr, val)
        except Exception: pass
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
sc.render.use_simplify = True; sc.render.simplify_subdivision_render = 2
try: sc.render.simplify_image_limit = '2048'
except Exception: pass
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - High Contrast'
except Exception: pass
sc.render.resolution_x, sc.render.resolution_y = (1920, 1080) if FINAL else (640, 360)
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.render.use_overwrite = False; sc.render.use_placeholder = True

# salva e calcola il telo in cache su disco (serve un .blend salvato)
blend = os.path.join(WORK, 'spot_garage.blend')
bpy.ops.wm.save_as_mainfile(filepath=blend)
if FINO < 12.5:
    # prima del tiro (12.5 s) il telo e' fermo sull'auto: niente simulazione, resta la forma gia' appoggiata (risparmia ~9 min)
    cloth.modifiers.remove(cm)
else:
    cm.point_cache.use_disk_cache = True
    with bpy.context.temp_override(scene=sc, point_cache=cm.point_cache):
        bpy.ops.ptcache.bake(bake=True)
bpy.ops.wm.save_as_mainfile(filepath=blend)
print('SALVATO', blend)
