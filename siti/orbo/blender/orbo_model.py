"""ORBO One: modello procedurale dell'auricolare (Blender 5.x, modulo bpy).

Tutto e' generato da codice: nessun asset esterno, nessuna licenza da citare.
Uso:  python orbo_model.py --out render.png --shot hero
"""
import argparse
import math
import sys

import bpy
import bmesh
from mathutils import Vector, Matrix


# ---------------------------------------------------------------- utilita'

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    return scene


def lathe(name, profile, segments=128):
    """Rivoluzione di un profilo (r, z) attorno all'asse Z."""
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for i in range(segments):
        a = 2 * math.pi * i / segments
        ca, sa = math.cos(a), math.sin(a)
        rings.append([bm.verts.new((r * ca, r * sa, z)) for r, z in profile])
    for i in range(segments):
        r0, r1 = rings[i], rings[(i + 1) % segments]
        for j in range(len(profile) - 1):
            v = (r0[j], r1[j], r1[j + 1], r0[j + 1])
            if len({x.co.to_tuple(6) for x in v}) >= 3:
                try:
                    bm.faces.new(v)
                except ValueError:
                    pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for p in mesh.polygons:
        p.use_smooth = True
    return obj


def superellipsoid(name, rx, ry, rz, e1=0.55, e2=0.9, seg=160, rings=96,
                   vmin=-math.pi / 2, vmax=math.pi / 2):
    """Ciottolo morbido: e1 schiaccia i poli, e2 arrotonda la sezione."""
    def sgnpow(x, p):
        return math.copysign(abs(x) ** p, x)

    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    grid = []
    for i in range(rings + 1):
        v = vmin + (vmax - vmin) * i / rings
        row = []
        for j in range(seg):
            u = -math.pi + 2 * math.pi * j / seg
            x = rx * sgnpow(math.cos(v), e1) * sgnpow(math.cos(u), e2)
            y = ry * sgnpow(math.cos(v), e1) * sgnpow(math.sin(u), e2)
            z = rz * sgnpow(math.sin(v), e1)
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for i in range(rings):
        for j in range(seg):
            a, b = grid[i][j], grid[i][(j + 1) % seg]
            c, d = grid[i + 1][(j + 1) % seg], grid[i + 1][j]
            try:
                bm.faces.new((a, b, c, d))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    for p in mesh.polygons:
        p.use_smooth = True
    return obj


def material(name, base, rough, metal=0.0, coat=0.0, coat_rough=0.05,
             aniso=0.0, sss=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*base, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Coat Roughness"].default_value = coat_rough
    p.inputs["Anisotropic"].default_value = aniso
    p.inputs["Specular IOR Level"].default_value = spec
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (0.3, 0.3, 0.3)
        p.inputs["Subsurface Scale"].default_value = 0.002
    return m


def micro_noise(mat, strength=0.08, scale=900.0):
    """Leggera grana della plastica: rompe i riflessi troppo perfetti."""
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = 4
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = 0.0002
    nt.links.new(tex.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"],
                 nt.nodes["Principled BSDF"].inputs["Normal"])


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def parent(child, par):
    child.parent = par


# ------------------------------------------------------------------ modello
# Unita': metri. L'auricolare e' lungo circa 2.2 cm.

def build_bud_cap(mats, name="cap"):
    """Faccia touch, anello e logo: il 'tappo' che si stacca nell'esploso."""
    # Faccia touch: disco di vetro nero con bordo arrotondato.
    face_profile = [(0.0, 0.0071), (0.0062, 0.0071), (0.0066, 0.00705),
                    (0.0068, 0.00690), (0.0068, 0.0060)]
    face = lathe(name + "_touch", face_profile)
    face.location.z = 0.0003
    assign(face, mats["glass"])

    # Anello metallico color rame attorno alla faccia.
    ring_profile = [(0.0068, 0.0058), (0.0068, 0.0072), (0.00705, 0.00745),
                    (0.0074, 0.00745), (0.00765, 0.0072), (0.0077, 0.0064),
                    (0.0077, 0.0058)]
    ring = lathe(name + "_ring", ring_profile)
    ring.location.z = 0.0003
    assign(ring, mats["metal"])

    # Logo inciso sulla faccia.
    curve = bpy.data.curves.new(name + "_logo", "FONT")
    curve.body = "ORBO"
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = 0.0021
    curve.space_character = 1.35
    curve.extrude = 0.00002
    logo = bpy.data.objects.new(name + "_logo", curve)
    bpy.context.collection.objects.link(logo)
    logo.location = (0, 0, 0.00742)
    assign(logo, mats["metal"])

    return [face, ring, logo]


def build_bud(name="ORBO_bud", mats=None):
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)

    # Guscio: ciottolo morbido, la faccia esterna guarda +Z.
    shell = superellipsoid(name + "_shell", 0.0105, 0.0094, 0.0072,
                           e1=0.62, e2=0.92)
    assign(shell, mats["shell"])
    parent(shell, root)

    for obj in build_bud_cap(mats, name):
        parent(obj, root)

    # Becco verso il condotto uditivo, inclinato.
    nozzle_profile = [(0.0, -0.0105), (0.0024, -0.0105), (0.0027, -0.0102),
                      (0.0029, -0.0080), (0.0034, -0.0040), (0.0040, -0.0010),
                      (0.0040, 0.0)]
    nozzle = lathe(name + "_nozzle", nozzle_profile)
    nozzle.rotation_euler = (math.radians(-28), 0, 0)
    nozzle.location = (0.0, -0.0012, -0.0030)
    assign(nozzle, mats["shell"])
    parent(nozzle, root)

    # Gommino in silicone (a cupola, cavo).
    tip_profile = [(0.0021, -0.0150), (0.0030, -0.0152), (0.0046, -0.0146),
                   (0.0058, -0.0130), (0.0062, -0.0112), (0.0058, -0.0098),
                   (0.0048, -0.0090), (0.0030, -0.0094), (0.0024, -0.0104),
                   (0.0021, -0.0130), (0.0021, -0.0150)]
    tip = lathe(name + "_tip", tip_profile)
    tip.rotation_euler = nozzle.rotation_euler
    tip.location = nozzle.location
    assign(tip, mats["silicone"])
    parent(tip, root)

    # Griglia del microfono sul fianco.
    mic = superellipsoid(name + "_mic", 0.0016, 0.0007, 0.0004, e1=0.4, e2=0.4,
                         seg=48, rings=24)
    mic.location = (0.0095, 0.0, 0.0028)
    mic.rotation_euler = (0, math.radians(68), 0)
    assign(mic, mats["grille"])
    parent(mic, root)

    return root


def make_materials():
    shell = material("shell_graphite", (0.018, 0.018, 0.02), 0.38,
                     coat=0.25, coat_rough=0.25)
    micro_noise(shell)
    return {
        "shell": shell,
        "glass": material("touch_glass", (0.005, 0.005, 0.006), 0.06,
                          coat=1.0, coat_rough=0.02, spec=0.6),
        "metal": material("ring_copper", (0.86, 0.58, 0.42), 0.22, metal=1.0,
                          aniso=0.6),
        "silicone": material("tip_silicone", (0.035, 0.035, 0.037), 0.62,
                             sss=0.15),
        "grille": material("mic_grille", (0.01, 0.01, 0.01), 0.7, metal=0.6),
    }


# ------------------------------------------------------------- set studio

def area(name, loc, target, size, power, shape="RECTANGLE", size_y=None,
         color=(1, 1, 1)):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = shape
    data.size = size
    if size_y:
        data.size_y = size_y
    data.energy = power
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    direction = Vector(target) - Vector(loc)
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


def studio(scene):
    world = bpy.data.worlds.new("black")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    scene.world = world

    # Softbox grande dall'alto, due strisce di luce ai lati per i bordi.
    area("key", (0.03, 0.10, 0.16), (0, 0, 0), 0.12, 0.7, size_y=0.08)
    area("rim_L", (-0.14, -0.05, 0.05), (0, 0, 0), 0.01, 0.9, size_y=0.18,
         color=(1.0, 0.92, 0.85))
    area("rim_R", (0.14, -0.04, 0.02), (0, 0, 0), 0.01, 0.7, size_y=0.16,
         color=(0.85, 0.9, 1.0))
    area("kick", (0.0, -0.16, -0.06), (0, 0, 0), 0.06, 0.12)

    # Pavimento nero lucido per un riflesso morbido.
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, -0.016))
    floor = bpy.context.active_object
    floor.name = "floor"
    floor_mat = material("floor", (0.004, 0.004, 0.004), 0.18, spec=0.4)
    assign(floor, floor_mat)
    return floor


def camera(scene, loc, target, lens=100):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = lens
    cam_data.clip_start = 0.001
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 18
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    direction = Vector(target) - Vector(loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    focus = bpy.data.objects.new("focus", None)
    bpy.context.collection.objects.link(focus)
    focus.location = target
    cam_data.dof.focus_object = focus
    scene.camera = cam
    return cam


# --------------------------------------------------------------- inquadrature

def shot_hero(mats):
    bud = build_bud("budA", mats)
    bud.rotation_euler = (math.radians(62), 0, math.radians(-24))
    return (0.0, -0.16, 0.05), (0, 0, 0.001)


def shot_pair(mats):
    a = build_bud("budL", mats)
    a.location = (-0.0125, 0.004, 0)
    a.rotation_euler = (math.radians(70), 0, math.radians(-34))
    b = build_bud("budR", mats)
    b.location = (0.0135, -0.004, -0.002)
    b.rotation_euler = (math.radians(-60), math.radians(180), math.radians(28))
    return (0.0, -0.24, 0.08), (0, 0, 0)


def shot_macro(mats):
    bud = build_bud("budM", mats)
    bud.rotation_euler = (math.radians(18), 0, math.radians(-10))
    return (0.01, -0.07, 0.085), (0.0, 0.0, 0.006)


SHOTS = {"hero": shot_hero, "pair": shot_pair, "macro": shot_macro}


def main():
    argv = sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--shot", default="hero", choices=SHOTS)
    ap.add_argument("--samples", type=int, default=256)
    ap.add_argument("--res", type=int, nargs=2, default=(1920, 1080))
    args = ap.parse_args(argv)

    scene = reset_scene()
    mats = make_materials()
    studio(scene)
    cam_loc, target = SHOTS[args.shot](mats)
    camera(scene, cam_loc, target, lens=100 if args.shot != "macro" else 120)

    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.filepath = args.out
    scene.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
