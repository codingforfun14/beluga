# Spot "Peso" per PRATICA (brand inventato): monolite di carta nel vuoto nero, caduta, cratere fratturato,
# i fogli si alzano e diventano una card luminosa. Base: clip4-blender-impatto/spot_impatto.py.
# Uso: Blender -b --factory-startup -P spot_peso.py -- <cartella/f_> <modo> [fps]
#   modo: stills (fotogrammi di prova 960x540) | final (animazione 1920x1080 JPEG) | track (solo card_track.json)
import bpy, bmesh, sys, math, random, json, os
from mathutils import Vector, Euler, Quaternion, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
out, mode = argv[0], argv[1]
FPS = int(argv[2]) if len(argv) > 2 else 60
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
def F(sec):  # secondi -> fotogramma (1 = 0.0 s)
    return int(round(sec * FPS)) + 1
END = F(15.5) - 1          # oltre 15.5 s lavora solo HyperFrames
sc.frame_start, sc.frame_end = 1, END
IMPACT = F(6.0)            # contatto col pavimento

# ---------------------------------------------------------------- materiali
def mat(name, color, rough, emit=None, estr=0.0, bands=False, noise=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    if noise or bands:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        r = nt.nodes.new('ShaderNodeValToRGB')
        r.color_ramp.elements[0].color = (color[0] * .55, color[1] * .55, color[2] * .55, 1)
        r.color_ramp.elements[1].color = (*color, 1)
        if bands:   # bordi dei fogli: righe fitte lungo Z dell'oggetto
            w = nt.nodes.new('ShaderNodeTexWave'); w.bands_direction = 'Z'
            w.inputs['Scale'].default_value = 90; w.inputs['Distortion'].default_value = 2.5
            w.inputs['Detail'].default_value = 3
            nt.links.new(tc.outputs['Object'], w.inputs['Vector'])
            r.color_ramp.elements[0].position = 0.25
            src = w.outputs['Fac']
        else:       # cemento: rumore su UV fisse (non scivola quando i pezzi si muovono)
            n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 9
            n.inputs['Detail'].default_value = 8
            nt.links.new(tc.outputs['UV'], n.inputs['Vector'])
            src = n.outputs['Fac']
        nt.links.new(src, r.inputs[0]); nt.links.new(r.outputs[0], p.inputs['Base Color'])
        b = nt.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = 0.35 if noise else 0.15
        nt.links.new(src, b.inputs['Height']); nt.links.new(b.outputs[0], p.inputs['Normal'])
    return m

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

PAPER = srgb('#EDEAE3'); ORANGE = srgb('#FF5A1F')
m_concrete = mat('concrete', (0.03, 0.03, 0.032), 0.8, noise=True)
m_paper_e = mat('paper_edges', PAPER, 0.75, bands=True)
m_paper = mat('paper', PAPER, 0.7)
m_grey = mat('binder_grey', (0.11, 0.115, 0.12), 0.55)
m_grey2 = mat('binder_grey2', (0.05, 0.05, 0.055), 0.5)
m_blue = mat('binder_blue', (0.008, 0.02, 0.07), 0.45)
m_ink = mat('ink', (0.05, 0.05, 0.05), 0.6)
m_red = mat('stamp', (0.62, 0.025, 0.02), 0.6)
m_metal = mat('clip', (0.8, 0.8, 0.82), 0.25); m_metal.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1
m_pit = mat('pit', (0, 0, 0), 1.0)
m_card = mat('card', srgb('#161618'), 0.35, emit=srgb('#FFF6EA'), estr=0.0)
m_edge = mat('card_edge', ORANGE, 0.4, emit=ORANGE, estr=0.0)

# ---------------------------------------------------------------- mondo: nero con un filo di ambiente per i riflessi
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.004, 0.0045, 0.005, 1); bg.inputs[1].default_value = 1

def link(o):
    sc.collection.objects.link(o); return o
def key(obj, f, loc=None, rot=None, scale=None):
    if loc is not None: obj.location = loc; obj.keyframe_insert('location', frame=f)
    if rot is not None: obj.rotation_euler = rot; obj.keyframe_insert('rotation_euler', frame=f)
    if scale is not None: obj.scale = scale; obj.keyframe_insert('scale', frame=f)
def fcurves(idblock):
    from bpy_extras import anim_utils
    ad = idblock.animation_data
    return anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves
def set_interp(idblock, mapping):  # mapping: frame -> ('CONSTANT'|'LINEAR'|('QUAD','EASE_IN')...)
    for fc in fcurves(idblock):
        for kp in fc.keyframe_points:
            v = mapping(int(round(kp.co.x)))
            if v is None: continue
            if isinstance(v, tuple): kp.interpolation, kp.easing = v
            else: kp.interpolation = v
def show_between(o, f_on, f_off=None):
    o.hide_render = True; o.keyframe_insert('hide_render', frame=1)
    o.hide_render = False; o.keyframe_insert('hide_render', frame=f_on)
    if f_off:
        o.hide_render = True; o.keyframe_insert('hide_render', frame=f_off)
    o.hide_viewport = o.hide_render

def box_into(bm, center, size, rotz=0.0, mat_idx=0, side_idx=None):
    """aggiunge un parallelepipedo al bmesh; side_idx = materiale delle facce laterali"""
    res = bmesh.ops.create_cube(bm, size=1.0)
    vs = res['verts']
    M = Matrix.Translation(center) @ Matrix.Rotation(rotz, 4, 'Z') @ Matrix.Diagonal((*size, 1))
    bmesh.ops.transform(bm, matrix=M, verts=vs)
    faces = {f for v in vs for f in v.link_faces}
    for f in faces:
        f.normal_update()
        f.material_index = mat_idx if (side_idx is None or abs(f.normal.z) > 0.9) else side_idx
    return faces

def mesh_obj(name, bm, mats):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    o = bpy.data.objects.new(name, me); link(o)
    for p in me.polygons: p.use_smooth = False
    return o

# ---------------------------------------------------------------- monolite: risme, raccoglitori, fogli sfusi (un'unica mesh)
MW, MD, MH = 1.6, 1.2, 3.0
m_strap = mat('elastico', (0.012, 0.012, 0.012), 0.6)
mats_mono = [m_paper, m_paper_e, m_grey, m_grey2, m_blue, m_strap]
NOTE_Z = 1.55
bm = bmesh.new(); z = 0.0; items = []   # items: (centro locale, size, rotz, tipo) -> riusati come detriti
def tilted_sheet(c, rz, tx, ty, size=(0.297, 0.21, 0.003)):
    fs = box_into(bm, Vector(), size, 0, 0)
    vs = list({v for f in fs for v in f.verts})
    M = Matrix.Translation(c) @ Euler((tx, ty, rz)).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=M, verts=vs)
while z < MH - 0.04:
    kind = random.choices(['ream', 'binder', 'loose'], [0.4, 0.42, 0.18])[0]
    h = {'ream': 0.052, 'binder': 0.075, 'loose': 0.03}[kind] * random.uniform(0.9, 1.15)
    nx, ny = 4, 3
    lshift = Vector((random.uniform(-.03, .03), random.uniform(-.03, .03), 0))
    for i in range(nx):
        for j in range(ny):
            cx = (i + 0.5) / nx * MW - MW / 2 + random.uniform(-.03, .03)
            cy = (j + 0.5) / ny * MD - MD / 2 + random.uniform(-.03, .03)
            rz = random.uniform(-0.1, 0.1)
            c = Vector((cx, cy, z + h / 2)) + lshift
            if kind == 'binder':
                mi = random.choices([2, 3, 4], [0.55, 0.35, 0.1])[0]
                s = (MW / nx * 0.97, MD / ny * 0.97, h * 0.96)
                box_into(bm, c, s, rz, mi)
                # dorso con etichetta bianca e foro ad anello sulle facce esterne
                for side, ok in [((1, 0), i == nx - 1), ((-1, 0), i == 0), ((0, 1), j == ny - 1), ((0, -1), j == 0)]:
                    if not ok: continue
                    wdt = s[1] if side[0] else s[0]
                    off = Vector(((s[0] / 2 + 0.002) * side[0], (s[1] / 2 + 0.002) * side[1], 0.004))
                    off.rotate(Euler((0, 0, rz)))
                    lab = (0.004, wdt * 0.42, h * 0.5) if side[0] else (wdt * 0.42, 0.004, h * 0.5)
                    box_into(bm, c + off, lab, rz, 0)
                    ring = (0.005, 0.03, 0.03) if side[0] else (0.03, 0.005, 0.03)
                    off2 = Vector(((s[0] / 2 + 0.003) * side[0] + 0.12 * side[1], (s[1] / 2 + 0.003) * side[1] + 0.12 * side[0], 0))
                    off2.rotate(Euler((0, 0, rz))); box_into(bm, c + off2, ring, rz, 3)
            else:
                s = (MW / nx * random.uniform(0.88, 0.99), MD / ny * random.uniform(0.88, 0.99), h * 0.97)
                box_into(bm, c, s, rz, 0, 1)
            if random.random() < 0.22:   # cinghia elastica nera attorno al pacco
                box_into(bm, c + Vector((random.uniform(-.08, .08), 0, 0)), (0.018, s[1] + 0.006, h + 0.006), rz, 5)
            items.append((c.copy(), s, rz, kind))
    # fogli sporgenti e storti su ogni strato (non davanti al foglio URGENTE)
    for _ in range(random.choice([1, 1, 2, 3])):
        a = random.choice([0, 1, 2, 3])
        dx, dy = [(MW / 2, 0), (-MW / 2, 0), (0, MD / 2), (0, -MD / 2)][a]
        if dy < 0 and abs(z - NOTE_Z) < 0.4: continue
        pos = Vector((dx * 0.92 + random.uniform(-.5, .5) * MW * (dy != 0), dy * 0.92 + random.uniform(-.4, .4) * MD * (dx != 0), z + h))
        pos += Vector((dx, dy, 0)).normalized() * random.uniform(0.02, 0.12)
        tilted_sheet(pos, random.uniform(-0.6, 0.6), random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25))
    z += h
mono = mesh_obj('monolite', bm, mats_mono)
MH = z
# il foglio "URGENTE" fissato sulla faccia frontale (y negativa), con graffetta
note = bpy.data.objects.new('nota', None); link(note); note.parent = mono
note.location = (0.18, -MD / 2 - 0.006, NOTE_Z); note.rotation_euler = (math.radians(90), math.radians(-4), 0)
bpy.ops.mesh.primitive_plane_add(size=1); sh = bpy.context.object; sh.scale = (0.21, 0.297, 1)
sh.data.materials.append(m_paper); sh.parent = note
for k in range(6):  # righe di testo stampato
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.012 + random.uniform(-.005, .005), 0.07 - k * 0.018, 0.0008))
    o = bpy.context.object; o.scale = (random.uniform(0.11, 0.16), 0.0035, 1); o.data.materials.append(m_ink); o.parent = note
txt = bpy.data.curves.new('urgente', 'FONT'); txt.body = 'URGENTE'; txt.align_x = 'CENTER'; txt.align_y = 'CENTER'
try: txt.font = bpy.data.fonts.load('/System/Library/Fonts/HelveticaNeue.ttc')
except Exception: pass
txt.size = 0.04; txt.extrude = 0.0003
to = bpy.data.objects.new('urgente', txt); link(to); to.data.materials.append(m_red); to.parent = note
to.location = (0.0, -0.08, 0.0012); to.rotation_euler = (0, 0, math.radians(11))
for (px, py, sx, sy) in [(0, 0.026, 0.19, 0.004), (0, -0.026, 0.19, 0.004), (0.095, 0, 0.004, 0.056), (-0.095, 0, 0.004, 0.056)]:
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.scale = (sx, sy, 1)
    o.data.materials.append(m_red); o.parent = to; o.location = (px, py, 0.0002)
# graffetta: polilinea con bevel
cu = bpy.data.curves.new('graffetta', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0012; cu.bevel_resolution = 3
sp = cu.splines.new('POLY')
pts = [(0.012, -0.03), (0.012, 0.028), (-0.012, 0.028), (-0.012, -0.045), (0.006, -0.045), (0.006, 0.018), (-0.005, 0.018), (-0.005, -0.02)]
sp.points.add(len(pts) - 1)
for p, (x, y) in zip(sp.points, pts): p.co = (x, y, 0.0015, 1)
cl = bpy.data.objects.new('graffetta', cu); link(cl); cl.data.materials.append(m_metal); cl.parent = note
cl.location = (-0.06, 0.135, 0); cl.rotation_euler = (0, 0, math.radians(-6))
mono_parts = [mono]

# animazione del monolite: sospeso, oscilla, trema, cade
HANG = 1.6
key(mono, 1, (0, 0, HANG), (0, 0, math.radians(-14)))
key(mono, F(4.5), (0, 0, HANG + 0.05), (0, 0, math.radians(6)))
for i, f in enumerate(range(F(4.5) + 3, F(5.45), 3)):  # tremito prima della caduta
    j = 0.004 + 0.012 * i / 20
    key(mono, f, (random.uniform(-j, j), random.uniform(-j, j), HANG + 0.05 + random.uniform(-j, j)), (0, 0, math.radians(6)))
FALL0 = F(5.43)
key(mono, FALL0, (0, 0, HANG + 0.05), (math.radians(0.6), 0, math.radians(6)))
key(mono, IMPACT, (0, 0, 0.0), (math.radians(1.5), 0, math.radians(6)))
key(mono, IMPACT + 6, (0, 0, -0.45), (math.radians(3.5), math.radians(1.5), math.radians(6)))
set_interp(mono, lambda f: ('QUAD', 'EASE_IN') if f == FALL0 else ('LINEAR' if f == IMPACT else None))
BLACK0 = IMPACT + 6          # 4 fotogrammi di nero (in montaggio), poi "dopo il disastro"
AFTER = BLACK0 + 4
mono.hide_render = False; mono.keyframe_insert('hide_render', frame=1)
mono.hide_render = True; mono.keyframe_insert('hide_render', frame=AFTER)
for ch in mono.children_recursive: show_between(ch, 1, AFTER)

# ---------------------------------------------------------------- pavimento con buco + lastra fratturata (Voronoi, bisect come Cell Fracture)
R = 2.5
def floor_uv(bm):
    uv = bm.loops.layers.uv.new('UVMap')
    for f in bm.faces:
        for l in f.loops: l[uv].uv = (l.vert.co.x * 0.25, l.vert.co.y * 0.25)
bm = bmesh.new()
inner = [bm.verts.new((R * math.cos(a), R * math.sin(a), 0)) for a in [i / 96 * math.tau for i in range(96)]]
outer = [bm.verts.new((150 * math.cos(a), 150 * math.sin(a), 0)) for a in [i / 96 * math.tau for i in range(96)]]
for i in range(96):
    bm.faces.new((inner[i], inner[(i + 1) % 96], outer[(i + 1) % 96], outer[i]))
floor_uv(bm)
floor = mesh_obj('pavimento', bm, [m_concrete])
bpy.ops.mesh.primitive_circle_add(vertices=64, radius=R + 0.05, fill_type='NGON', location=(0, 0, -1.1))
pit = bpy.context.object; pit.data.materials.append(m_pit)

def voronoi_cells(base_bm_fn, seeds):
    cells = []
    for i, s in enumerate(seeds):
        bm = base_bm_fn()
        for j, t in enumerate(seeds):
            if i == j or (s - t).length > 2.2: continue
            mid = (s + t) / 2; no = (t - s).normalized()
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=mid, plane_no=no, clear_outer=True)
            bmesh.ops.holes_fill(bm, edges=bm.edges[:], sides=0)
        if len(bm.verts) >= 4: cells.append(bm)
        else: bm.free()
    return cells

def slab():
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=R, radius2=R, depth=0.32)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, -0.16))
    return bm
seeds = []
while len(seeds) < 56:
    r = R * random.random() ** 0.75; a = random.random() * math.tau
    p = Vector((r * math.cos(a), r * math.sin(a), 0))
    if all((p - q).length > 0.22 for q in seeds): seeds.append(p)
cells = []
for k, cb in enumerate(voronoi_cells(slab, seeds)):
    floor_uv(cb)
    c = sum((v.co for v in cb.verts), Vector()) / len(cb.verts)
    bmesh.ops.translate(cb, verts=cb.verts, vec=-c)
    o = mesh_obj(f'cella{k}', cb, [m_concrete]); o.location = c
    cells.append(o)
# cratere: le celle affondano e si inclinano verso il centro, il bordo si solleva
D0 = 0.75
for o in cells:
    c = o.location.copy(); r = c.xy.length; th = math.atan2(c.y, c.x)
    u = min(r / R, 1)
    depth = D0 * (1 - u * u) ** 1.3 + random.uniform(0, 0.08) * (1 - u)
    lift = 0.06 * math.exp(-((u - 0.93) / 0.07) ** 2)
    slope = 2 * D0 * u / R * 1.6 + 0.05
    n = Vector((-math.cos(th) * math.sin(slope), -math.sin(th) * math.sin(slope), math.cos(slope)))
    q = Vector((0, 0, 1)).rotation_difference(n)
    jitter = Euler([random.uniform(-.12, .12) * (1.4 - u) for _ in range(3)]).to_quaternion()
    o.rotation_mode = 'QUATERNION'
    o.keyframe_insert('location', frame=IMPACT); o.keyframe_insert('rotation_quaternion', frame=IMPACT)
    o.keyframe_insert('scale', frame=IMPACT)
    o.location = c + Vector((math.cos(th), math.sin(th), 0)) * 0.05 * u + Vector((0, 0, -depth + lift))
    o.rotation_quaternion = jitter @ q
    o.scale = (0.975, 0.975, 1)
    for f in (IMPACT + 5, ):
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_quaternion', frame=f); o.keyframe_insert('scale', frame=f)
    set_interp(o, lambda f: ('EXPO', 'EASE_OUT') if f == IMPACT else None)

# crepe che escono dal cratere: polilinee spezzate, scure
for i in range(18):
    a = i / 18 * math.tau + random.uniform(-.12, .12)
    cu = bpy.data.curves.new(f'crepa{i}', 'CURVE'); cu.dimensions = '2D'; cu.extrude = 0.0
    cu.bevel_depth = 0.0; sp = cu.splines.new('POLY')
    L = random.uniform(1.2, 4.5); steps = 14
    pts = []; ang = a
    for s in range(steps + 1):
        rr = R - 0.05 + L * s / steps; ang += random.uniform(-.05, .05)
        pts.append((rr * math.cos(ang), rr * math.sin(ang)))
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts): p.co = (x, y, 0.003, 1)
    cu.offset = 0; cu.bevel_mode = 'ROUND'
    o = bpy.data.objects.new(f'crepa{i}', cu); link(o)
    o.data.dimensions = '3D'; o.data.bevel_depth = random.uniform(0.006, 0.014); o.data.materials.append(m_pit)
    o.scale = (1, 1, 0.15)
    show_between(o, IMPACT + 1)

# schegge: frammenti Voronoi di un cubo, proiettati all'impatto e fermi dopo
def cube_bm():
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=0.5); return bm
cseeds = [Vector((random.uniform(-.25, .25), random.uniform(-.25, .25), random.uniform(-.25, .25))) for _ in range(26)]
frag_meshes = []
for k, cb in enumerate(voronoi_cells(cube_bm, cseeds)):
    floor_uv(cb)
    c = sum((v.co for v in cb.verts), Vector()) / len(cb.verts)
    bmesh.ops.translate(cb, verts=cb.verts, vec=-c)
    me = bpy.data.meshes.new(f'fr{k}'); cb.to_mesh(me); cb.free(); me.materials.append(m_concrete); frag_meshes.append(me)
for i in range(90):
    o = bpy.data.objects.new(f'scheggia{i}', random.choice(frag_meshes)); link(o)
    s = random.uniform(0.25, 1.0) ** 1.5; o.scale = (s, s, s)
    a = random.random() * math.tau; r1 = R * random.uniform(0.7, 1.9) ** 1.2
    p0 = Vector((0.3 * math.cos(a), 0.3 * math.sin(a), 0.1))
    p1 = Vector((r1 * math.cos(a), r1 * math.sin(a), 0.03 * s))
    r0 = Euler([random.random() * math.tau for _ in range(3)])
    key(o, IMPACT, p0, r0)
    for f in range(IMPACT + 1, IMPACT + 7):  # volo balistico nei 6 fotogrammi visibili
        t = (f - IMPACT) / 6
        p = p0.lerp(p1, t ** 0.6); p.z += 1.6 * t * (1 - t) * random.uniform(.5, 1.2)
        key(o, f, p, Euler([r0.x + t * 4, r0.y + t * 3, r0.z]))
    key(o, AFTER, p1, Euler([random.random() * math.tau, random.random() * math.tau, r0.z]))
    show_between(o, IMPACT + 1)

# granelli di polvere (moti balistici con attrito) + nuvola volumetrica
m_dust = mat('polvere', (0.25, 0.24, 0.22), 1.0)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.008); grain = bpy.context.object; grain.data.materials.append(m_dust)
grain.hide_render = True; grain.hide_viewport = True
for i in range(260):
    o = bpy.data.objects.new(f'granello{i}', grain.data); link(o)
    s = random.uniform(0.5, 2.0); o.scale = (s, s, s)
    a = random.random() * math.tau; sp_ = random.uniform(1.5, 7.0); up = random.uniform(1.0, 5.5)
    p = Vector((R * 0.4 * math.cos(a), R * 0.4 * math.sin(a), 0.05)); v = Vector((math.cos(a) * sp_, math.sin(a) * sp_, up))
    dt = 1 / FPS; f = IMPACT
    while f < F(9.5):
        if (f - IMPACT) % 4 == 0: key(o, f, p.copy())
        v.z -= 9.81 * dt * 0.35; v *= 0.965
        p += v * dt
        if p.z < 0.004: p.z = 0.004; v *= 0.3
        f += 1
    show_between(o, IMPACT + 1)
vol_cube = bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.8)); dust = bpy.context.object
dust.scale = (7, 7, 1.8); dm = bpy.data.materials.new('nuvola'); dm.use_nodes = True; dust.data.materials.append(dm)
nt = dm.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Color'].default_value = (0.5, 0.47, 0.43, 1)
nt.links.new(pv.outputs[0], nt.nodes['Material Output'].inputs['Volume'])
tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'
nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 5
nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'
nt.links.new(tc.outputs['Object'], gr.inputs['Vector'])
mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
cr = nt.nodes.new('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.45; cr.inputs['From Max'].default_value = 0.75
nt.links.new(nz.outputs['Fac'], cr.inputs['Value'])
nt.links.new(cr.outputs['Result'], mul.inputs[0]); nt.links.new(gr.outputs['Fac'], mul.inputs[1])
dens = nt.nodes.new('ShaderNodeMath'); dens.operation = 'MULTIPLY'
nt.links.new(mul.outputs[0], dens.inputs[0]); nt.links.new(dens.outputs[0], pv.inputs['Density'])
dk = dens.inputs[1]
for f, v in [(IMPACT, 0.0), (IMPACT + 3, 2.2), (AFTER + 20, 1.1), (F(8.5), 0.35), (F(10), 0.08), (F(12), 0.0)]:
    dk.default_value = v; dk.keyframe_insert('default_value', frame=f)
for f, v in [(IMPACT, 0.0), (F(12), 2.5)]:
    nz.inputs['W'].default_value = v; nz.inputs['W'].keyframe_insert('default_value', frame=f)
key(dust, IMPACT, scale=(4, 4, 1.0)); key(dust, F(10), scale=(8.5, 8.5, 2.4))
show_between(dust, IMPACT + 1, F(12))

# ---------------------------------------------------------------- detriti di carta: risme e raccoglitori sparsi, fogli ovunque
debris = []
for (c, s, rz, kind) in random.sample(items, 90):
    bm = bmesh.new()
    if kind == 'binder': box_into(bm, Vector(), s, 0, random.choices([2, 3, 4], [.55, .35, .1])[0])
    else: box_into(bm, Vector(), s, 0, 0, 1)
    o = mesh_obj('detrito', bm, mats_mono)
    a = random.random() * math.tau; r = R * random.uniform(0.0, 1.05) ** 0.8
    u = min(r / R, 1)
    zbed = -D0 * (1 - u * u) ** 1.3 + s[2] / 2 + random.uniform(0, 0.35) * (1 - u)
    o.location = (r * math.cos(a), r * math.sin(a), zbed)
    o.rotation_euler = (random.uniform(-.5, .5), random.uniform(-.5, .5), random.random() * math.tau)
    show_between(o, AFTER); debris.append(o)

bpy.ops.mesh.primitive_plane_add(size=1); sheet_proto = bpy.context.object
sheet_proto.scale = (0.21, 0.297, 1); bpy.ops.object.transform_apply(scale=True)
sheet_proto.data.materials.append(m_paper); sheet_proto.hide_render = True; sheet_proto.hide_viewport = True
# la card: rettangolo arrotondato luminoso con bordo arancione (unico accento)
CW, CH = 1.0, 0.62
def rounded_rect(w, h, r, z, segs=6):
    bm = bmesh.new(); vs = []
    for cx, cy, a0 in [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]:
        for k in range(segs + 1):
            a = math.radians(a0 + 90 * k / segs); vs.append(bm.verts.new((cx + r * math.cos(a), cy + r * math.sin(a), z)))
    bm.faces.new(vs); return bm
card = bpy.data.objects.new('card', None); link(card)
face = mesh_obj('card_face', rounded_rect(CW, CH, 0.06, 0.006), [m_card]); face.parent = card
edge = mesh_obj('card_edge', rounded_rect(CW + 0.05, CH + 0.05, 0.085, 0.0), [m_edge]); edge.parent = card
back = mesh_obj('card_back', rounded_rect(CW + 0.05, CH + 0.05, 0.085, -0.004), [m_grey2]); back.parent = card
# luce emessa dalla card
cl_light = bpy.data.lights.new('card_light', 'AREA'); cl_light.size = 1.0; cl_light.color = (1, 0.95, 0.88)
cll = bpy.data.objects.new('card_light', cl_light); link(cll); cll.parent = card; cll.location = (0, 0, 0.08); cll.rotation_euler = (math.pi, 0, 0)  # illumina davanti, non la card

E0, E1 = F(8.5), F(12.0)
CARD_C = Vector((0, 0, 1.35))
card_rot = Euler((math.radians(62), 0, math.radians(-25)))
card_q = card_rot.to_quaternion()
sheets = []
NS = 150
for i in range(NS):
    o = bpy.data.objects.new(f'foglio{i}', sheet_proto.data); link(o); o.rotation_mode = 'QUATERNION'
    a = random.random() * math.tau; r = random.uniform(0.15, 3.6) ** 1.0
    u = min(r / R, 1)
    zr = (-D0 * (1 - u * u) ** 1.3 + 0.03 + random.uniform(0, 0.3)) if r < R else 0.002 + random.uniform(0, .004)
    p0 = Vector((r * math.cos(a), r * math.sin(a), zr))
    tilt = 0.35 if r < R else 0.04
    q0 = Euler((random.uniform(-tilt, tilt), random.uniform(-tilt, tilt), random.random() * math.tau)).to_quaternion()
    # ritardo: prima i fogli vicini, poi gli altri; arrivo scaglionato
    ts = E0 + int((r / 3.6) * 0.9 * FPS + random.uniform(0, 0.5) * FPS)
    dur = int(random.uniform(1.6, 2.1) * FPS)
    te = min(ts + dur, E1 - int(0.35 * FPS) - random.randint(0, int(0.4 * FPS)))
    spin = random.choice([1, 1, 1, -1]) * random.uniform(1.2, 2.2) * math.pi
    off = Vector((random.uniform(-.25, .25), random.uniform(-.15, .15), random.uniform(-.02, .02)))
    target = CARD_C + card_q @ off
    key_f = list(range(ts, te + 1, 3)) + [te]
    o.location = p0; o.rotation_quaternion = q0; o.scale = (1, 1, 1)
    o.keyframe_insert('location', frame=AFTER); o.keyframe_insert('rotation_quaternion', frame=AFTER); o.keyframe_insert('scale', frame=AFTER)
    for f in key_f:
        u = (f - ts) / max(te - ts, 1); e = u * u * (3 - 2 * u)
        th = a + spin * e; rad = r * (1 - e) ** 1.4
        pp = Vector((rad * math.cos(th), rad * math.sin(th), 0))
        pp = pp.lerp(target, e ** 1.6); pp.z = p0.z + (target.z - p0.z) * (1 - (1 - e) ** 2) + 0.9 * math.sin(math.pi * e) * (1 - e)
        flut = Euler((math.sin(u * 9 + i) * 0.9 * (1 - e), math.cos(u * 7 + i) * 0.7 * (1 - e), th * 0.3 * (1 - e))).to_quaternion()
        qq = q0.slerp(card_q, e) @ flut
        sc_ = 1.0 if u < 0.82 else max(0.001, 1 - (u - 0.82) / 0.18)
        o.location = pp; o.rotation_quaternion = qq; o.scale = (sc_, sc_, sc_)
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_quaternion', frame=f); o.keyframe_insert('scale', frame=f)
    show_between(o, AFTER, te + 1)
    sheets.append((o, te))
# la card cresce man mano che i fogli arrivano, poi viene verso la camera (F: 12-15.5 s)
arr = sorted(te for _, te in sheets)
card.rotation_mode = 'QUATERNION'
card.location = CARD_C; card.rotation_quaternion = card_q
for f in range(E0, E1 + 1, 4):
    k = sum(1 for t in arr if t <= f) / NS
    s = 0.001 + 0.999 * k ** 1.3
    card.scale = (s, s, s); card.keyframe_insert('scale', frame=f)
card.scale = (1, 1, 1); card.keyframe_insert('scale', frame=E1)
card.keyframe_insert('location', frame=E1); card.keyframe_insert('rotation_quaternion', frame=E1)
CAM_F = Vector((0, -5.6, 1.55))
CARD_F = Vector((0, -3.55, 1.55))
q_front = Euler((math.radians(90), 0, 0)).to_quaternion()
ARRIVE = F(13.0)
card.location = CARD_F; card.rotation_quaternion = q_front
card.keyframe_insert('location', frame=ARRIVE); card.keyframe_insert('rotation_quaternion', frame=ARRIVE)
for f in range(ARRIVE + 15, END + 1, 15):  # galleggia appena
    t = (f - ARRIVE) / FPS
    card.location = CARD_F + Vector((0, 0, 0.008 * math.sin(t * 1.7)))
    card.rotation_quaternion = Euler((math.radians(90 + 0.6 * math.sin(t * 1.3)), 0, math.radians(0.5 * math.sin(t * 1.1)))).to_quaternion()
    card.keyframe_insert('location', frame=f); card.keyframe_insert('rotation_quaternion', frame=f)
set_interp(card, lambda f: ('CUBIC', 'EASE_OUT') if f == E1 else None)
for f, v in [(E0, 0), (E1 - 40, 0.15), (E1, 0.3), (ARRIVE, 0.22)]:
    for m, mul_ in [(m_card, 0.0), (m_edge, 5.0)]:
        s = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']; s.default_value = v * mul_; s.keyframe_insert('default_value', frame=f)
    cl_light.energy = v * 900; cl_light.keyframe_insert('energy', frame=f)
show_between(card, E0)
for ch in card.children: show_between(ch, E0)

# ---------------------------------------------------------------- luci
def area(name, loc, energy, size, color=(1, 1, 1), target=None):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new(name, l); link(o); o.location = loc
    tgt = target or bpy.data.objects.new(name + '_t', None)
    if target is None: link(tgt); tgt.location = (0, 0, 1.2)
    c = o.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    return o
rig = bpy.data.objects.new('rig', None); link(rig)
keyl = area('key_calda', (5.5, 0, 3.4), 0, 1.2, (1, 0.86, 0.7), target=mono); keyl.parent = rig
# la luce di taglio scopre il monolite: entra da dietro e gira verso destra
for f, e_ in [(1, 0), (F(0.5), 0), (F(2.0), 900), (F(4.5), 900), (IMPACT, 900), (AFTER, 650), (E0, 650), (E1, 420)]:
    keyl.data.energy = e_; keyl.data.keyframe_insert('energy', frame=f)
key(rig, 1, rot=(0, 0, math.radians(70))); key(rig, F(2.5), rot=(0, 0, math.radians(5))); key(rig, F(15.5), rot=(0, 0, math.radians(-15)))
rim = area('rim_fredda', (-3.5, 4.5, 4.0), 0, 2.0, (0.75, 0.85, 1.0))
for f, e_ in [(1, 0), (F(1.2), 0), (F(2.5), 500), (E1, 500), (ARRIVE, 260)]:
    rim.data.energy = e_; rim.data.keyframe_insert('energy', frame=f)
top = area('alto', (0.4, 0.3, 7), 0, 3.0, (1, 0.96, 0.92))
for f, e_ in [(1, 0), (AFTER - 1, 0), (AFTER, 330), (E0, 300), (E1, 120)]:
    top.data.energy = e_; top.data.keyframe_insert('energy', frame=f)
fill = area('riempimento', (-4, -5, 2.5), 0, 4.0, (0.85, 0.9, 1.0))
for f, e_ in [(1, 0), (F(2.0), 60), (E1, 60)]:
    fill.data.energy = e_; fill.data.keyframe_insert('energy', frame=f)

# ---------------------------------------------------------------- camere
def cam(name, loc, target, lens=50, fstop=None, focus=None):
    c = bpy.data.cameras.new(name); c.lens = lens; c.clip_start = 0.02
    o = bpy.data.objects.new(name, c); link(o); o.location = loc
    t = bpy.data.objects.new(name + '_t', None); link(t); t.location = target
    k = o.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    if fstop:
        c.dof.use_dof = True; c.dof.aperture_fstop = fstop; c.dof.focus_object = focus or t
    return o, t
shots = []
A, At = cam('A_rivela', (2.0, -7.0, 1.2), (0, 0, HANG + 1.45), 30, 5.6)
key(A, 1, (2.2, -7.4, 1.1)); key(A, F(2.5), (1.7, -6.3, 1.3)); shots.append((1, A))
B1, B1t = cam('B1_bordi', (1.2, -1.15, HANG + 0.5), (MW / 2, -MD / 2, 0.6), 85, 2.2)
B1t.parent = mono; B1t.location = (MW / 2 - 0.05, -MD / 2, 0.45); B1t.matrix_parent_inverse = Matrix()
key(B1, F(2.5) + 1, (1.35, -1.3, HANG + 0.35)); key(B1, F(3.15), (1.15, -1.45, HANG + 0.95))
B1t.keyframe_insert('location', frame=F(2.5) + 1); B1t.location = (MW / 2 - 0.1, -MD / 2, 1.05); B1t.keyframe_insert('location', frame=F(3.15))
shots.append((F(2.5) + 1, B1))
STAMP = Vector((0.18, -MD / 2, NOTE_Z - 0.075))
Bs, Bst = cam('B1b_timbro', (0.3, -MD / 2 - 1.2, HANG + NOTE_Z - 0.1), STAMP, 85, 4.0)
Bst.parent = mono; Bst.location = STAMP; Bst.matrix_parent_inverse = Matrix()
key(Bs, F(3.15) + 1, (0.42, -MD / 2 - 1.25, HANG + NOTE_Z - 0.12)); key(Bs, F(3.8), (0.36, -MD / 2 - 1.0, HANG + NOTE_Z - 0.1))
shots.append((F(3.15) + 1, Bs))
B2, B2t = cam('B2_graffetta', (-0.1, -0.85, HANG + NOTE_Z + 0.25), (0.13, -MD / 2, NOTE_Z + 0.13), 100, 1.8)
B2t.parent = mono; B2t.location = (0.12, -MD / 2, NOTE_Z + 0.12); B2t.matrix_parent_inverse = Matrix()
key(B2, F(3.8) + 1, (-0.12, -1.08, HANG + NOTE_Z + 0.3)); key(B2, F(4.5), (0.0, -0.98, HANG + NOTE_Z + 0.22))
shots.append((F(3.8) + 1, B2))
C, Ct = cam('C_basso', (5.2, -6.2, 0.28), (0, 0, 1.25), 24)
key(C, F(4.5) + 1, (5.4, -6.4, 0.28)); key(C, IMPACT, (5.1, -6.0, 0.26))
for f, dz in [(IMPACT + 1, 0.09), (IMPACT + 2, -0.07), (IMPACT + 3, 0.05), (IMPACT + 4, -0.03), (IMPACT + 5, 0.015), (IMPACT + 6, 0)]:
    key(C, f, (5.1 + dz * 0.5, -6.0, 0.26 + dz))
shots.append((F(4.5) + 1, C))
Dc, Dt = cam('D_alto', (0.5, -0.8, 8.2), (0, 0, -0.3), 32)
key(Dc, BLACK0, (0.5, -0.8, 8.2)); key(Dc, E0, (0.3, -0.5, 7.2)); shots.append((BLACK0, Dc))
EF, EFt = cam('EF_rivelazione', (3.2, -4.0, 4.2), (0, 0, 0.2), 40, 4.0)
key(EF, E0 + 1, (3.6, -4.4, 4.6)); key(EF, E1 - 60, (1.2, -5.2, 2.0)); key(EF, E1, CAM_F); key(EF, END, CAM_F + Vector((0, 0.25, 0)))
EFt.location = (0, 0, 0.3); EFt.keyframe_insert('location', frame=E0 + 1)
EFt.location = CARD_C; EFt.keyframe_insert('location', frame=E1 - 60)
EFt.location = CARD_F; EFt.keyframe_insert('location', frame=E1)
EF.data.dof.focus_object = None; EF.data.dof.focus_distance = 5.0
EF.data.dof.keyframe_insert('focus_distance', frame=E0 + 1)
EF.data.dof.focus_distance = (CAM_F - CARD_F).length; EF.data.dof.keyframe_insert('focus_distance', frame=ARRIVE)
EF.data.dof.focus_distance = (CAM_F - CARD_F).length - 0.25; EF.data.dof.keyframe_insert('focus_distance', frame=END)
shots.append((E0 + 1, EF))
for f, c in shots:
    m = sc.timeline_markers.new(c.name, frame=f); m.camera = c
sc.camera = A

# ---------------------------------------------------------------- traccia della card per HyperFrames (angoli in pixel)
def track(path):
    data = {'fps': FPS, 'w': 1920, 'h': 1080, 'card_mm': [1000, 620], 'frames': {}}
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    for f in range(E1 - 30, END + 1):
        sc.frame_set(f); camo = sc.camera
        M = face.matrix_world
        pts = []
        for x, y in [(-CW / 2, CH / 2), (CW / 2, CH / 2), (CW / 2, -CH / 2), (-CW / 2, -CH / 2)]:
            v = world_to_camera_view(sc, camo, M @ Vector((x, y, 0.006)))
            pts.append([round(v.x * 1920, 2), round((1 - v.y) * 1080, 2)])
        data['frames'][f - 1] = pts   # chiave = indice 0-based del fotogramma video
    with open(path, 'w') as fh: json.dump(data, fh)

# ---------------------------------------------------------------- render
sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
for attr, val in [('taa_render_samples', 16 if mode == 'stills' else 32), ('use_shadows', True),
                  ('use_raytracing', True), ('volumetric_tile_size', '8'), ('volumetric_samples', 48)]:
    if hasattr(e, attr):
        try: setattr(e, attr, val)
        except Exception: pass
sc.render.use_motion_blur = True
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 90
if mode == 'track':
    track(out)
elif mode == 'stills':
    track(os.path.join(os.path.dirname(out), 'card_track.json'))
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    secs = [float(s) for s in (argv[3].split(',') if len(argv) > 3 else
            '1.0,2.2,3.0,4.0,5.2,5.9,6.05,7.0,8.3,9.5,10.6,11.6,12.5,14.5'.split(','))]
    for s in secs:
        f = F(s); sc.frame_set(f); sc.render.filepath = f'{out}{f:04d}.jpg'; bpy.ops.render.render(write_still=True)
else:
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    if len(argv) > 3:
        a, b = argv[3].split('-'); sc.frame_start, sc.frame_end = int(a), int(b)
    sc.render.filepath = out
    sc.render.use_overwrite = False; sc.render.use_placeholder = True  # riprende senza rifare i fotogrammi esistenti
    bpy.ops.render.render(animation=True)
