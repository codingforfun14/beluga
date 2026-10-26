"""Render per i mockup del piano v2: pezzo singolo, finiture, bilancia, custodia.

Uso:  python orbo_plan_renders.py --shot driver|finishes|scale|case --out x.png
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbo_model as om  # noqa: E402
import orbo_explode as oe  # noqa: E402

FINISHES = {
    # nome: (guscio, rugosita', anello)
    "graphite": ((0.018, 0.018, 0.02), 0.38, (0.86, 0.58, 0.42)),
    "bone": ((0.62, 0.58, 0.52), 0.42, (0.80, 0.81, 0.83)),
    "midnight": ((0.012, 0.022, 0.05), 0.36, (0.92, 0.74, 0.40)),
}


def finish_mats(name):
    shell_c, rough, ring_c = FINISHES[name]
    mats = om.make_materials()
    shell = om.material("shell_" + name, shell_c, rough, coat=0.25, coat_rough=0.25)
    om.micro_noise(shell)
    mats["shell"] = shell
    mats["metal"] = om.material("ring_" + name, ring_c, 0.22, metal=1.0, aniso=0.6)
    return mats


def shot_driver(scene):
    mats = om.make_materials()
    _, parts = oe.build_parts(mats)
    for name, g in parts.items():
        if name != "driver":
            for c in g.children_recursive:
                bpy.data.objects.remove(c)
    parts["driver"].rotation_euler = (math.radians(118), math.radians(-14), math.radians(20))
    # Il metallo riflette solo le luci: serve un pannello grande davanti.
    om.area("fill", (0.03, -0.09, 0.09), (0, 0, -0.004), 0.12, 0.12, size_y=0.06)
    return (0.0, -0.12, 0.035), (0, 0, 0.0), 120


def shot_finishes(scene):
    for i, name in enumerate(["graphite", "bone", "midnight"]):
        bud = om.build_bud("bud_" + name, finish_mats(name))
        bud.location = ((i - 1) * 0.03, 0, 0)
        bud.rotation_euler = (math.radians(64), 0, math.radians(-18))
    return (0.0, -0.30, 0.09), (0, 0, 0.0), 85


def shot_scale(scene):
    steel = om.material("plate", (0.16, 0.16, 0.17), 0.32, metal=1.0, aniso=0.7)
    plate = om.lathe("plate", [(0.0, -0.0135), (0.032, -0.0135), (0.0325, -0.014),
                               (0.0325, -0.0165), (0.0, -0.0165)])
    om.assign(plate, steel)
    bud = om.build_bud("bud", om.make_materials())
    bud.rotation_euler = (math.radians(70), 0, math.radians(-30))
    bud.location.z = -0.0005
    return (0.0, -0.17, 0.07), (0, 0, -0.004), 85


def shot_case(scene):
    mats = om.make_materials()
    rx, ry, rz = 0.031, 0.024, 0.0125
    base = om.superellipsoid("case_base", rx, ry, rz, e1=0.5, e2=0.7,
                             vmin=-math.pi / 2, vmax=0.0, rings=64)
    oe.solid(base, 0.0012)
    om.assign(base, mats["shell"])
    tray = om.superellipsoid("tray", rx - 0.0012, ry - 0.0012, 0.0004, e1=0.2,
                             e2=0.7, rings=8)
    tray.location.z = -0.0035
    om.assign(tray, om.material("tray", (0.006, 0.006, 0.007), 0.6))

    hinge = bpy.data.objects.new("hinge", None)
    bpy.context.collection.objects.link(hinge)
    hinge.location = (0, ry, 0)
    lid = om.superellipsoid("case_lid", rx, ry, rz, e1=0.5, e2=0.7, vmin=0.0,
                            vmax=math.pi / 2, rings=64)
    oe.solid(lid, 0.0012)
    om.assign(lid, mats["shell"])
    lid.parent = hinge
    lid.location = (0, -ry, 0)
    hinge.rotation_euler = (math.radians(-105), 0, 0)

    # Filo di rame lungo la giunzione e led frontale.
    band = om.lathe("band", [(0.995, -0.0004), (1.0, -0.0004), (1.0, 0.0002),
                             (0.995, 0.0002)], segments=160)
    band.scale = (rx * 1.003, ry * 1.003, 1)
    om.assign(band, mats["metal"])
    led = om.lathe("led", [(0.0, 0.0), (0.0007, 0.0), (0.0007, 0.0002),
                           (0.0, 0.0002)], segments=24)
    led.location = (0, -ry - 0.0002, -0.004)
    led.rotation_euler = (math.radians(90), 0, 0)
    glow = bpy.data.materials.new("led")
    glow.use_nodes = True
    em = glow.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.62, 0.38, 1)
    em.inputs["Strength"].default_value = 12
    glow.node_tree.links.new(em.outputs[0],
                             glow.node_tree.nodes["Material Output"].inputs[0])
    om.assign(led, glow)

    for x, flip in ((-0.0128, 1), (0.0128, -1)):
        bud = om.build_bud("bud%d" % flip, mats)
        bud.location = (x, -0.002, -0.0015)
        bud.rotation_euler = (math.radians(8), 0, math.radians(180 if flip < 0 else 0))
    return (0.0, -0.26, 0.15), (0, 0.010, 0.006), 85


def isolate(parts, keep):
    for name, g in parts.items():
        if name != keep:
            for c in g.children_recursive:
                bpy.data.objects.remove(c)


def shot_chip(scene):
    mats = om.make_materials()
    _, parts = oe.build_parts(mats)
    isolate(parts, "pcb")
    pcb = parts["pcb"]
    pcb.rotation_euler = (math.radians(34), 0, math.radians(-18))
    bpy.context.view_layer.update()
    target = pcb.matrix_world @ Vector((0, -0.0005, 0.004))
    om.area("fill", (0.04, -0.07, 0.08), tuple(target), 0.10, 0.10, size_y=0.05)
    om.area("spec", (-0.05, 0.03, 0.06), tuple(target), 0.03, 0.25, size_y=0.08,
            color=(1.0, 0.9, 0.8))
    return (0.005, -0.064, 0.038), tuple(target), 100


def shot_scale2(scene):
    body_m = om.material("anodized", (0.05, 0.05, 0.055), 0.34, metal=1.0, aniso=0.6)
    steel = om.material("plate", (0.38, 0.38, 0.40), 0.38, metal=1.0, aniso=0.8)
    glass = om.material("lcd", (0.003, 0.003, 0.004), 0.05, coat=1.0, coat_rough=0.02)
    rubber = om.material("button", (0.02, 0.02, 0.02), 0.55)
    oe.box("body", (0, 0, -0.024), (0.13, 0.11, 0.016), body_m, None, bevel=0.004)
    ped = om.lathe("pedestal", [(0.0, -0.0162), (0.006, -0.0162), (0.006, -0.0155),
                                (0.0, -0.0155)], segments=48)
    ped.location.y = 0.012
    om.assign(ped, steel)
    plate = om.lathe("plate", [(0.0, -0.0155), (0.034, -0.0155), (0.0345, -0.015),
                               (0.0345, -0.0138), (0.034, -0.0135), (0.0, -0.0135)])
    plate.location.y = 0.012
    om.assign(plate, steel)
    oe.box("lcd", (0, -0.040, -0.0159), (0.05, 0.016, 0.0006), glass, None,
           bevel=0.0004)
    digits = bpy.data.materials.new("digits")
    digits.use_nodes = True
    em = digits.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.86, 0.72, 1)
    em.inputs["Strength"].default_value = 6
    digits.node_tree.links.new(em.outputs[0],
                               digits.node_tree.nodes["Material Output"].inputs[0])
    oe.text("4.60", 0.011, (-0.003, -0.040, -0.01555), digits, None)
    oe.text("g", 0.006, (0.019, -0.0415, -0.01555), digits, None)
    label = om.material("print", (0.5, 0.5, 0.5), 0.6)
    for x, word in ((-0.044, "ON"), (0.044, "TARE")):
        b = om.lathe("btn", [(0.0, -0.016), (0.0045, -0.016), (0.0047, -0.0157),
                             (0.0045, -0.0153), (0.0, -0.0152)], segments=48)
        b.location = (x, -0.038, 0)
        om.assign(b, rubber)
        oe.text(word, 0.0022, (x, -0.0465, -0.01595), label, None)
    oe.text("ORBO LAB  0.01 g", 0.0024, (0, -0.0505, -0.01595), label, None)
    bud = om.build_bud("bud", om.make_materials())
    bud.rotation_euler = (math.radians(70), 0, math.radians(-30))
    bud.location = (0, 0.012, -0.0005)
    return (0.0, -0.30, 0.20), (0, 0.004, -0.014), 85


def sweep(mat, floor_z, back_y=0.09, radius=0.05):
    """Fondale curvo da studio fotografico."""
    import bmesh
    prof = [(-0.6, floor_z)]
    for i in range(17):
        a = math.pi / 2 * i / 16
        prof.append((back_y - radius + radius * math.sin(a),
                     floor_z + radius - radius * math.cos(a)))
    prof.append((back_y, floor_z + 0.6))
    mesh = bpy.data.meshes.new("sweep")
    bm = bmesh.new()
    rows = [[bm.verts.new((x, y, z)) for (y, z) in prof] for x in (-0.6, 0.6)]
    for j in range(len(prof) - 1):
        bm.faces.new((rows[0][j], rows[1][j], rows[1][j + 1], rows[0][j + 1]))
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("sweep", mesh)
    bpy.context.collection.objects.link(obj)
    for poly in mesh.polygons:
        poly.use_smooth = True
    om.assign(obj, mat)


def shot_finish(name):
    def shot(scene):
        mats = finish_mats(name)
        a = om.build_bud("budL", mats)
        a.location = (-0.0125, 0.004, 0)
        a.rotation_euler = (math.radians(70), 0, math.radians(-34))
        b = om.build_bud("budR", mats)
        b.location = (0.0135, -0.004, -0.002)
        b.rotation_euler = (math.radians(-60), math.radians(180), math.radians(28))
        sweep(om.material("backdrop", (0.018, 0.018, 0.019), 0.5), -0.0145)
        return (0.0, -0.21, 0.07), (0, 0, -0.001), 85
    return shot


SHOTS = {"driver": shot_driver, "finishes": shot_finishes, "scale": shot_scale,
         "chip": shot_chip, "scale2": shot_scale2,
         "finish_graphite": shot_finish("graphite"), "finish_bone": shot_finish("bone"),
         "finish_midnight": shot_finish("midnight"),
         "case": shot_case}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", choices=SHOTS, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--samples", type=int, default=96)
    ap.add_argument("--res", type=int, nargs=2, default=(1600, 1000))
    args = ap.parse_args(sys.argv[1:])

    scene = om.reset_scene()
    floor = om.studio(scene)
    if args.shot in ("driver", "chip") or args.shot.startswith("finish_"):
        bpy.data.objects.remove(floor)
    elif args.shot == "scale2":
        floor.location.z = -0.032
    else:
        floor.location.z = -0.0165 if args.shot == "scale" else -0.0125 \
            if args.shot == "case" else -0.0145
    cam_loc, target, lens = SHOTS[args.shot](scene)
    om.camera(scene, cam_loc, target, lens=lens)
    scene.camera.data.dof.aperture_fstop = 16
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.filepath = args.out
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
