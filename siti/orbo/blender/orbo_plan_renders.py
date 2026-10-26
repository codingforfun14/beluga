"""Render per i mockup del piano v2: pezzo singolo, finiture, bilancia, custodia.

Uso:  python orbo_plan_renders.py --shot driver|finishes|scale|case --out x.png
"""
import argparse
import math
import os
import sys

import bpy

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


SHOTS = {"driver": shot_driver, "finishes": shot_finishes, "scale": shot_scale,
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
    if args.shot in ("driver",):
        bpy.data.objects.remove(floor)
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
