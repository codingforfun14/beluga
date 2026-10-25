# Test spot "Impatto": scarpa nel vuoto nero, caduta, "dopo il disastro" (stile Bullpadel), ritmo misurato.
import bpy, sys, math, random
from mathutils import Vector, Euler
argv = sys.argv[sys.argv.index('--') + 1:]
glb, hdri, out, mode = argv[0], argv[1], argv[2], argv[3]  # mode: preview | final
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
FPS = 25
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, 312

# --- prodotto
bpy.ops.import_scene.gltf(filepath=glb)
meshes = [o for o in sc.objects if o.type == 'MESH']
root = bpy.data.objects.new('shoe_root', None); sc.collection.objects.link(root)
for o in sc.objects:
    if o.parent is None and o is not root:
        o.parent = root
root.scale = (3, 3, 3)  # ~0.9 m: piu comodo per le distanze di camera
shoe = root

# --- mondo nero con HDRI molto bassa (solo riflessi)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdri)
nt.links.new(env.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.08
lp = nt.nodes.new('ShaderNodeLightPath'); mix = nt.nodes.new('ShaderNodeMixShader')
blk = nt.nodes.new('ShaderNodeBackground'); blk.inputs[0].default_value = (0, 0, 0, 1)
out_n = nt.nodes['World Output']
nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs[0]); nt.links.new(bg.outputs[0], mix.inputs[1])
nt.links.new(blk.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out_n.inputs[0])

def mat(name, color, rough, metal=0.0, noise=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if noise:
        n = m.node_tree.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 40
        r = m.node_tree.nodes.new('ShaderNodeValToRGB')
        r.color_ramp.elements[0].color = (color[0] * .5, color[1] * .5, color[2] * .5, 1)
        r.color_ramp.elements[1].color = (*color, 1)
        m.node_tree.links.new(n.outputs[0], r.inputs[0]); m.node_tree.links.new(r.outputs[0], p.inputs['Base Color'])
        b = m.node_tree.nodes.new('ShaderNodeBump'); b.inputs['Strength'].default_value = 0.4
        m.node_tree.links.new(n.outputs[0], b.inputs['Height']); m.node_tree.links.new(b.outputs[0], p.inputs['Normal'])
    return m

concrete = mat('concrete', (0.025, 0.025, 0.027), 0.8, noise=True)
shard_m = mat('shard', (0.05, 0.05, 0.055), 0.7, noise=True)
dark = mat('crater', (0.01, 0.01, 0.01), 1.0)

# --- pavimento
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0)); floor = bpy.context.object; floor.data.materials.append(concrete)

# --- cratere e schegge: compaiono solo "dopo" (dal frame 151)
IMPACT = 150
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1.1, fill_type='NGON', location=(0, 0, 0.002))
crater = bpy.context.object; crater.data.materials.append(dark)
for v in crater.data.vertices:
    if v.co.length > 0.01:
        k = 0.6 + random.random() * 0.7; v.co.x *= k; v.co.y *= k
after = [crater]
for i in range(70):
    a = random.random() * math.tau; r = 0.7 + random.random() ** 0.6 * 2.6
    s = 0.03 + random.random() * 0.16 * (1.6 - r / 3.3)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=s, location=(math.cos(a) * r, math.sin(a) * r, s * 0.3))
    o = bpy.context.object; o.scale = (1, random.uniform(.4, 1), random.uniform(.2, .6))
    o.rotation_euler = Euler([random.random() * math.tau for _ in range(3)]); o.data.materials.append(shard_m)
    after.append(o)
# crepe radiali: listelli sottili e scuri
for i in range(14):
    a = i / 14 * math.tau + random.uniform(-.15, .15); L = random.uniform(1.5, 3.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(a) * L / 2, math.sin(a) * L / 2, 0.003))
    o = bpy.context.object; o.scale = (L, random.uniform(.006, .016), .004); o.rotation_euler.z = a
    o.data.materials.append(dark); after.append(o)
for o in after:
    o.hide_render = True; o.keyframe_insert('hide_render', frame=IMPACT)
    o.hide_render = False; o.keyframe_insert('hide_render', frame=IMPACT + 1)

# --- animazione scarpa: sospesa che ruota piano, poi cade
def key(obj, f, loc=None, rot=None):
    if loc is not None: obj.location = loc; obj.keyframe_insert('location', frame=f)
    if rot is not None: obj.rotation_euler = rot; obj.keyframe_insert('rotation_euler', frame=f)
key(shoe, 1, (0, 0, 0.9), (0, 0, math.radians(-30)))
key(shoe, 124, (0, 0, 1.0), (0, 0, math.radians(25)))
key(shoe, 125, (0, 0, 2.6), (math.radians(-8), 0, math.radians(20)))
key(shoe, IMPACT, (0, 0, 0.0), (0, 0, math.radians(20)))
key(shoe, 312, (0, 0, 0.0), (0, 0, math.radians(20)))
def fcurves(obj):
    from bpy_extras import anim_utils
    ad = obj.animation_data
    cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    return cb.fcurves
for fc in fcurves(shoe):
    for kp in fc.keyframe_points:
        f = int(round(kp.co.x))
        if f == 124: kp.interpolation = 'CONSTANT'
        elif f == 125: kp.interpolation = 'QUAD'; kp.easing = 'EASE_IN'
        elif f >= IMPACT: kp.interpolation = 'CONSTANT'

# --- luci: rim che gira attorno (rivelazione), key fredda, piccolo spot dall'alto
def area(name, loc, energy, size, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
    c = o.constraints.new('TRACK_TO'); c.target = shoe; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    return o
rig = bpy.data.objects.new('rig', None); sc.collection.objects.link(rig)
rim = area('rim', (0, 4, 2.5), 700, 1.5, (0.85, 0.9, 1)); rim.parent = rig
key(rig, 1, rot=(0, 0, math.radians(-120))); key(rig, 75, rot=(0, 0, math.radians(10)))
key(rig, 312, rot=(0, 0, math.radians(60)))
key_l = area('key', (-3, -3, 3), 0, 2.5)
key_l.data.energy = 0; key_l.data.keyframe_insert('energy', frame=40)
key_l.data.energy = 120; key_l.data.keyframe_insert('energy', frame=75)
top = area('top', (0.3, 0.2, 5), 0, 1.2, (1, .95, .9))
top.data.energy = 0; top.data.keyframe_insert('energy', frame=IMPACT)
top.data.energy = 220; top.data.keyframe_insert('energy', frame=IMPACT + 1)

# --- camere e tagli (secondi -> frame)
def cam(name, loc, target, lens=50, fstop=None, focus=None):
    c = bpy.data.cameras.new(name); c.lens = lens
    if fstop:
        c.dof.use_dof = True; c.dof.aperture_fstop = fstop; c.dof.focus_object = focus or shoe
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o); o.location = loc
    t = bpy.data.objects.new(name + '_t', None); sc.collection.objects.link(t); t.location = target
    k = o.constraints.new('TRACK_TO'); k.target = t; k.track_axis = 'TRACK_NEGATIVE_Z'; k.up_axis = 'UP_Y'
    return o, t
shots = []
A, _ = cam('A_reveal', (2.2, -3.2, 1.3), (0, 0, 0.95), 50, 4)
key(A, 1, (2.4, -3.4, 1.3)); key(A, 75, (1.9, -2.8, 1.2)); shots.append((1, A))
B, Bt = cam('B_macro', (0.9, -0.9, 1.15), (0.1, 0, 1.0), 100, 1.8)
key(B, 76, (0.95, -0.95, 1.15)); key(B, 124, (0.75, -0.8, 1.1)); shots.append((76, B))
C, _ = cam('C_low', (2.6, -2.6, 0.25), (0, 0, 0.35), 28)
shots.append((125, C))
# camera shake all'impatto
for f, dz in [(150, 0), (151, 0.05), (152, -0.04), (153, 0.03), (155, -0.015), (158, 0)]:
    key(C, f, (2.6, -2.6, 0.25 + dz))
D, _ = cam('D_top', (0.4, -0.6, 6.5), (0, 0, 0), 35)
key(D, 176, (0.4, -0.6, 6.5)); key(D, 212, (0.3, -0.4, 5.6)); shots.append((176, D))
E1, _ = cam('E1_heel', (-1.6, 0.6, 0.35), (-0.3, 0, 0.3), 85, 2.8); shots.append((213, E1))
E2, _ = cam('E2_laces', (0.5, -0.9, 1.0), (0.1, 0, 0.45), 85, 2.8); shots.append((226, E2))
E3, _ = cam('E3_shards', (2.4, 1.6, 0.2), (0, 0, 0.25), 50, 2.8); shots.append((239, E3))
F, Ft = cam('F_hero', (3.0, -2.2, 0.9), (0, 0, 0.35), 45, 5.6)
for i, f in enumerate(range(251, 313, 10)):
    a = math.radians(-35 + i * 4)
    key(F, f, (3.4 * math.cos(a), 3.4 * math.sin(a), 0.9 - i * 0.03))
shots.append((251, F))
for f, c in shots:
    m = sc.timeline_markers.new(c.name, frame=f); m.camera = c
sc.camera = A

# --- render
sc.render.engine = 'BLENDER_EEVEE'
e = sc.eevee
for attr, val in [('taa_render_samples', 16 if mode != 'final' else 48), ('use_shadows', True), ('use_raytracing', mode == 'final')]:
    if hasattr(e, attr): setattr(e, attr, val)
sc.render.use_motion_blur = True
sc.render.resolution_x, sc.render.resolution_y = (960, 540) if mode != 'final' else (1920, 1080)
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - High Contrast'
except Exception: pass
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.render.filepath = out
if mode == 'stills':
    for f in [10, 60, 100, 140, 160, 195, 220, 232, 245, 290]:
        sc.frame_set(f); sc.render.filepath = f'{out}{f:04d}.jpg'; bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
