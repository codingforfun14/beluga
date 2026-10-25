"""ORBO One: animazione dell'esploso per lo scroll del sito.

L'auricolare gira lento, si smonta lungo il suo asse e poi si ricompone.
Uso:
  python orbo_explode.py --out frames/f_#### --frames 1 120      (sequenza)
  python orbo_explode.py --out still.png --still 60                (un frame)
"""
import argparse
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbo_model as om  # noqa: E402

FRAMES = 120
# Fasi (in frame): montato, si smonta, pausa esploso, si ricompone.
EXPLODE_START, EXPLODE_END = 16, 56
REASSEMBLE_START, REASSEMBLE_END = 80, 112


def group(name, par):
    g = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(g)
    g.parent = par
    return g


def solid(obj, thickness):
    mod = obj.modifiers.new("solid", "SOLIDIFY")
    mod.thickness = thickness
    mod.offset = -1
    mod.use_even_offset = True


def build_parts(mats):
    root = bpy.data.objects.new("ORBO_explode", None)
    bpy.context.collection.objects.link(root)

    pcb_mat = om.material("pcb", (0.012, 0.03, 0.022), 0.42, coat=0.4)
    chip_mat = om.material("chip", (0.008, 0.008, 0.009), 0.3)
    smd_mat = om.material("smd", (0.55, 0.5, 0.42), 0.3, metal=1.0)
    steel = om.material("steel", (0.62, 0.62, 0.64), 0.28, metal=1.0, aniso=0.5)
    gold = om.material("gold", (0.95, 0.74, 0.42), 0.2, metal=1.0)
    cone_mat = om.material("cone", (0.02, 0.02, 0.022), 0.55, coat=0.3)

    parts = {}

    # 1. Faccia touch + anello + logo.
    cap = group("cap", root)
    for obj in om.build_bud_cap(mats):
        obj.parent = cap
    parts["cap"] = cap

    # 2. Guscio superiore: fascia aperta sopra e sotto, con spessore.
    upper = group("upper", root)
    band = om.superellipsoid("upper_shell", 0.0105, 0.0094, 0.0072, e1=0.62,
                             e2=0.92, vmin=0.0414, vmax=1.052, rings=64)
    band.location.z = 0.0
    solid(band, 0.0005)
    om.assign(band, mats["shell"])
    band.parent = upper
    mic = om.superellipsoid("mic", 0.0016, 0.0007, 0.0004, e1=0.4, e2=0.4,
                            seg=48, rings=24)
    mic.location = (0.0095, 0.0, 0.0028)
    mic.rotation_euler = (0, math.radians(68), 0)
    om.assign(mic, mats["grille"])
    mic.parent = upper
    parts["upper"] = upper

    # 3. Scheda con il chip S1.
    pcb = group("pcb", root)
    board = om.lathe("board", [(0.0, 0.0034), (0.0078, 0.0034),
                               (0.0078, 0.0040), (0.0, 0.0040)], segments=96)
    om.assign(board, pcb_mat)
    board.parent = pcb
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0, 0.0, 0.0044))
    chip = bpy.context.active_object
    chip.scale = (0.0042, 0.0042, 0.0008)
    bev = chip.modifiers.new("bevel", "BEVEL")
    bev.width = 0.00015
    bev.segments = 3
    om.assign(chip, chip_mat)
    chip.parent = pcb
    for i, (x, y, sx, sy) in enumerate([(0.0045, 0.002, 0.0012, 0.0007),
                                         (-0.0046, 0.0015, 0.0009, 0.0014),
                                         (0.003, -0.0042, 0.0016, 0.0006),
                                         (-0.0028, -0.0045, 0.0008, 0.0008),
                                         (0.0006, 0.0055, 0.0018, 0.0005),
                                         (-0.0052, -0.001, 0.0006, 0.0006)]):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.00425))
        smd = bpy.context.active_object
        smd.scale = (sx, sy, 0.0004)
        om.assign(smd, smd_mat if i % 2 else chip_mat)
        smd.parent = pcb
    parts["pcb"] = pcb

    # 4. Batteria a bottone.
    battery = group("battery", root)
    cell = om.lathe("cell", [(0.0, -0.0015), (0.0054, -0.0015),
                             (0.0057, -0.0012), (0.0057, 0.0018),
                             (0.0054, 0.0021), (0.0, 0.0021)])
    om.assign(cell, steel)
    cell.parent = battery
    parts["battery"] = battery

    # 5. Driver: cestello, membrana a cono, bobina in rame.
    driver = group("driver", root)
    basket = om.lathe("basket", [(0.0058, -0.0056), (0.0062, -0.0056),
                                 (0.0062, -0.0040), (0.0058, -0.0038),
                                 (0.0058, -0.0056)])
    om.assign(basket, steel)
    basket.parent = driver
    cone = om.lathe("cone", [(0.0, -0.0052), (0.0016, -0.0051),
                             (0.0040, -0.0046), (0.0058, -0.0043)])
    solid(cone, 0.0002)
    om.assign(cone, cone_mat)
    cone.parent = driver
    coil = om.lathe("coil", [(0.0018, -0.0062), (0.0022, -0.0062),
                             (0.0022, -0.0050), (0.0018, -0.0050),
                             (0.0018, -0.0062)])
    om.assign(coil, mats["metal"])
    coil.parent = driver
    parts["driver"] = driver

    # 6. Guscio inferiore con becco e contatti di ricarica.
    lower = group("lower", root)
    bowl = om.superellipsoid("lower_shell", 0.0105, 0.0094, 0.0072, e1=0.62,
                             e2=0.92, vmin=-math.pi / 2, vmax=0.0414, rings=64)
    solid(bowl, 0.0005)
    om.assign(bowl, mats["shell"])
    bowl.parent = lower
    nozzle = om.lathe("nozzle", [(0.0, -0.0105), (0.0024, -0.0105),
                                 (0.0027, -0.0102), (0.0029, -0.0080),
                                 (0.0034, -0.0040), (0.0040, -0.0010),
                                 (0.0040, 0.0)])
    nozzle.rotation_euler = (math.radians(-28), 0, 0)
    nozzle.location = (0.0, -0.0012, -0.0030)
    om.assign(nozzle, mats["shell"])
    nozzle.parent = lower
    for x in (-0.0042, 0.0042):
        pin = om.lathe("pin", [(0.0, 0.0), (0.0008, 0.0), (0.0008, 0.0002),
                               (0.0, 0.0002)], segments=32)
        pin.location = (x, 0.0035, -0.0068)
        pin.rotation_euler = (math.radians(180), 0, 0)
        om.assign(pin, gold)
        pin.parent = lower
    parts["lower"] = lower

    # 7. Gommino.
    tip_g = group("tip", root)
    tip = om.lathe("tip", [(0.0021, -0.0150), (0.0030, -0.0152),
                           (0.0046, -0.0146), (0.0058, -0.0130),
                           (0.0062, -0.0112), (0.0058, -0.0098),
                           (0.0048, -0.0090), (0.0030, -0.0094),
                           (0.0024, -0.0104), (0.0021, -0.0130),
                           (0.0021, -0.0150)])
    tip.rotation_euler = nozzle.rotation_euler
    tip.location = nozzle.location
    om.assign(tip, mats["silicone"])
    tip.parent = tip_g
    parts["tip"] = tip_g

    return root, parts


# Spostamento lungo l'asse dell'auricolare (m), ritardo (frame), rotazione (gradi).
EXPLODE = {
    "cap":     (0.029, 0, 25),
    "upper":   (0.018, 3, -12),
    "pcb":     (0.0085, 6, 30),
    "battery": (0.000, 9, -20),
    "driver":  (-0.0095, 6, 15),
    "lower":   (-0.0205, 3, -8),
    "tip":     (-0.032, 0, 20),
}


def key(obj, frame, z, rot):
    obj.location = (0, 0, z)
    obj.rotation_euler = (0, 0, math.radians(rot))
    obj.keyframe_insert("location", frame=frame)
    obj.keyframe_insert("rotation_euler", frame=frame)


def animate(root, parts):
    for name, (dz, delay, rot) in EXPLODE.items():
        obj = parts[name]
        key(obj, EXPLODE_START + delay, 0, 0)
        key(obj, EXPLODE_END + delay, dz, rot)
        key(obj, REASSEMBLE_START + (9 - delay), dz, rot)
        key(obj, REASSEMBLE_END - delay // 3, 0, 0)

    # Inclinazione fissa e giro lento attorno all'asse verticale.
    root.rotation_mode = "ZXY"
    root.rotation_euler = (math.radians(24), math.radians(14), math.radians(-30))
    root.keyframe_insert("rotation_euler", frame=1)
    root.rotation_euler = (math.radians(24), math.radians(14), math.radians(60))
    root.keyframe_insert("rotation_euler", frame=FRAMES)

    for obj in [root] + list(parts.values()):
        for fc in obj.animation_data.action.fcurves if hasattr(
                obj.animation_data.action, "fcurves") else []:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.easing = "AUTO"
    # La rotazione del corpo resta lineare per un giro uniforme.
    action = root.animation_data.action
    for fc in getattr(action, "fcurves", []):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--still", type=int)
    ap.add_argument("--frames", type=int, nargs=2, default=(1, FRAMES))
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--res", type=int, nargs=2, default=(1920, 1080))
    args = ap.parse_args(sys.argv[1:])

    scene = om.reset_scene()
    mats = om.make_materials()
    floor = om.studio(scene)
    bpy.data.objects.remove(floor)
    root, parts = build_parts(mats)
    animate(root, parts)
    # La luce principale va spostata di lato, altrimenti la faccia di vetro
    # (che qui guarda in alto) la riflette tutta e sembra bianca.
    key = bpy.data.objects["key"]
    key.location = (-0.11, 0.02, 0.13)
    key.rotation_euler = (-key.location).to_track_quat("-Z", "Y").to_euler()
    om.camera(scene, (0.0, -0.40, 0.055), (0, 0, -0.003), lens=85)
    scene.camera.data.dof.aperture_fstop = 22

    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = args.res
    scene.render.image_settings.file_format = "PNG"
    if args.still:
        scene.frame_set(args.still)
        scene.render.filepath = args.out
        bpy.ops.render.render(write_still=True)
    else:
        scene.frame_start, scene.frame_end = args.frames
        scene.frame_step = args.step
        scene.render.filepath = args.out
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
