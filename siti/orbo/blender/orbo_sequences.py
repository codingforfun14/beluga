"""Sequenze per lo scroll: bilancia che pesa l'auricolare e custodia che si apre.

Uso:
  python orbo_sequences.py --seq scale --out /tmp/scale --samples 64 --res 1600 1000
  python orbo_sequences.py --seq case --out /tmp/case --samples 64 --res 1600 1000

Scrive out/f_0001.png ... e, per la bilancia, out/lcd.json con il rettangolo
del display in coordinate schermo normalizzate (le cifre le disegna l'HTML).
"""
import argparse
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbo_model as om  # noqa: E402
import orbo_plan_renders as pr  # noqa: E402


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


# Bilancia: 60 frame. 1-8 fermo, 8-36 l'auricolare scende, 36-60 il piatto
# cede un poco e torna su. Il display (HTML) segue la stessa tabella.
SCALE_FRAMES = 60
BUD_REST = -0.0005
BUD_START = 0.020


def scale_state(f):
    drop = smooth((f - 8) / 28.0)
    z = BUD_START + (BUD_REST - BUD_START) * drop
    dip = 0.0
    if f > 36:
        t = (f - 36) / 24.0
        dip = -0.0006 * math.exp(-5 * t) * math.cos(9 * t) - 0.00012 * smooth(t * 3)
    tilt = (1 - drop) * math.radians(14)
    return z, dip, tilt


def setup_scale(scene):
    cam = pr.shot_scale2(scene, digits_on=False, bud_z=BUD_START)
    bud = bpy.data.objects[scene["scale_bud"]]
    lcd = bpy.data.materials["lcd"].node_tree.nodes["Principled BSDF"]
    lcd.inputs["Roughness"].default_value = 0.45
    lcd.inputs["Coat Weight"].default_value = 0.25
    lcd.inputs["Coat Roughness"].default_value = 0.3
    movers = [bpy.data.objects["plate"], bpy.data.objects["pedestal"]]
    base = {o.name: o.location.z for o in movers}
    rot0 = tuple(bud.rotation_euler)

    def apply(f):
        z, dip, tilt = scale_state(f)
        bud.location.z = z + dip
        bud.rotation_euler = (rot0[0], rot0[1] + tilt, rot0[2])
        for o in movers:
            o.location.z = base[o.name] + dip
    return cam, apply, SCALE_FRAMES


CASE_FRAMES = 40


def setup_case(scene):
    cam = pr.shot_case(scene)
    hinge = bpy.data.objects["hinge"]
    led = bpy.data.materials["led"].node_tree.nodes["Emission"]

    def apply(f):
        t = smooth((f - 4) / 30.0)
        hinge.rotation_euler = (math.radians(-105) * t, 0, 0)
        led.inputs["Strength"].default_value = 12 * ease_out((f - 20) / 14.0)
    return cam, apply, CASE_FRAMES


def lcd_rect(scene):
    lcd = bpy.data.objects["lcd"]
    pts = [world_to_camera_view(scene, scene.camera, lcd.matrix_world @ Vector(v))
           for v in lcd.bound_box]
    xs = [p.x for p in pts]
    ys = [1 - p.y for p in pts]
    return {"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", choices=("scale", "case"), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--res", type=int, nargs=2, default=(1600, 1000))
    ap.add_argument("--frames", type=int, nargs="*")
    args = ap.parse_args(sys.argv[1:])
    os.makedirs(args.out, exist_ok=True)

    scene = om.reset_scene()
    floor = om.studio(scene)
    if args.seq == "scale":
        floor.location.z = -0.032
        (cam_loc, target, lens), apply, n = setup_scale(scene)
    else:
        floor.location.z = -0.0125
        (cam_loc, target, lens), apply, n = setup_case(scene)
    om.camera(scene, cam_loc, target, lens=lens)
    scene.camera.data.dof.aperture_fstop = 16
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = args.res

    if args.seq == "scale":
        bpy.context.view_layer.update()
        with open(os.path.join(args.out, "lcd.json"), "w") as fh:
            json.dump(lcd_rect(scene), fh, indent=1)

    for f in args.frames or range(1, n + 1):
        apply(f)
        scene.render.filepath = os.path.join(args.out, "f_%04d.png" % f)
        bpy.ops.render.render(write_still=True)
        print("frame", f, "done", flush=True)


if __name__ == "__main__":
    main()
