# Importa la 488 GTB (Turbostuart, Sketchfab, CC BY), la porta a 4,57 m, vernice Rosso Corsa e gomme scure.
# Il guscio nero (Object_70/72) si sovrapponeva alla carrozzeria: la carrozzeria (Object_78) viene spinta fuori di 4 mm.
# uso: DARK=1 SPP=96 python prepara_488.py <file.glb> <out.png> a|b|top
import bpy, sys, math, os
from mathutils import Vector
glb, out, mode = sys.argv[-3], sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
for o in meshes:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
root = bpy.data.objects.new('root', None); sc.collection.objects.link(root)
for o in sc.objects:
    if o.parent is None and o is not root: o.parent = root
s = 4.57 / (mx.y - mn.y); c = (mn + mx) / 2
root.scale = (s, s, s); root.location = (-c.x * s, -c.y * s, -mn.z * s)
H = (mx.z - mn.z) * s
def P(n): return bpy.data.materials[n].node_tree.nodes['Principled BSDF']
p = P('body1'); p.inputs['Base Color'].default_value = (0.42, 0.005, 0.004, 1); p.inputs['Roughness'].default_value = 0.25
p.inputs['Metallic'].default_value = 0.2; p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.03
b = bpy.data.objects['Object_78']; d = b.modifiers.new('fuori', 'DISPLACE'); d.direction = 'NORMAL'; d.mid_level = 0; d.strength = float(os.environ.get('OFF','0.004')) / s
for n in ('Tyre_Side', 'Profiel02', 'material', 'material_8', 'material_8_1'):
    q = P(n); q.inputs['Base Color'].default_value = (0.015, 0.015, 0.015, 1); q.inputs['Roughness'].default_value = 0.7
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 32; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.view_settings.view_transform = 'AgX'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0.6
bpy.ops.mesh.primitive_plane_add(size=40)
l = bpy.data.lights.new('k', 'AREA'); l.energy = 3000; l.size = 6
lo = bpy.data.objects.new('k', l); lo.location = (4, -4, 6); sc.collection.objects.link(lo)
lo.rotation_euler = (Vector((0,0,0.5)) - lo.location).to_track_quat('-Z','Y').to_euler()
cd = bpy.data.cameras.new('c'); cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
def look(t): cam.rotation_euler = (Vector(t) - cam.location).to_track_quat('-Z', 'Y').to_euler()
if os.environ.get('DARK'):
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.01
    fl = bpy.data.objects['Plane']; fm = bpy.data.materials.new('fl'); fm.use_nodes = True
    q = fm.node_tree.nodes['Principled BSDF']; q.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1); q.inputs['Roughness'].default_value = 0.25
    fl.data.materials.append(fm); lo.data.energy = 0
    for i, x in enumerate((-2.2, 0, 2.2)):
        a = bpy.data.lights.new(f'n{i}', 'AREA'); a.shape = 'RECTANGLE'; a.size = 0.25; a.size_y = 3.5; a.energy = 900
        ao = bpy.data.objects.new(f'n{i}', a); ao.location = (x, 0, 3.6); sc.collection.objects.link(ao)
    r = bpy.data.lights.new('rim', 'AREA'); r.size = 3; r.energy = 1500; r.color = (1, 0.85, 0.7)
    ro = bpy.data.objects.new('rim', r); ro.location = (-5, 4, 1.5); sc.collection.objects.link(ro)
    ro.rotation_euler = (Vector((0, 0, 0.6)) - ro.location).to_track_quat('-Z', 'Y').to_euler()
if mode == 'a':
    cam.location = (5.5, -5.5, 1.6); cd.lens = 40; look((0, 0, 0.55))
elif mode == 'b':
    cam.location = (-5.5, 5.5, 1.6); cd.lens = 40; look((0, 0, 0.55))
else:  # dall'alto, tetto tagliato: si vede se l'abitacolo c'e'
    cam.location = (0, 0, H + 3); cam.rotation_euler = (0, 0, 0); cd.type = 'ORTHO'; cd.ortho_scale = 5
    cd.clip_start = 3 + 0.18 * H; lo.location = (0, 0, H + 2.5); lo.rotation_euler = (0, 0, 0)
import os
for n in os.environ.get('HIDE','').split(','):
    if n: bpy.data.objects[n].hide_render = True
sc.cycles.samples = int(os.environ.get('SPP','32')); sc.render.resolution_percentage = int(os.environ.get('PCT','100'))
print('H', H)
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
