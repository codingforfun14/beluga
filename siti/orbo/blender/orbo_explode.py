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


def text(body, size, loc, mat, par, rot_z=0.0):
    curve = bpy.data.curves.new("txt_" + body, "FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = size
    curve.extrude = 0.000004
    obj = bpy.data.objects.new("txt_" + body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (0, 0, rot_z)
    om.assign(obj, mat)
    obj.parent = par
    return obj


def box(name, loc, size, mat, par, bevel=0.0, rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.rotation_euler = (0, 0, rot_z)
    if bevel:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    om.assign(obj, mat)
    obj.parent = par
    return obj


def build_pcb(pcb, pcb_mat, chip_mat, smd_mat, gold):
    """Scheda rotonda: chip S1 con scritta, piste di rame, pad dorati,
    condensatori, quarzo e cavo flessibile."""
    top = 0.0040
    board = om.lathe("board", [(0.0, 0.0034), (0.0078, 0.0034),
                               (0.0078, top), (0.0, top)], segments=128)
    om.assign(board, pcb_mat)
    board.parent = pcb
    rim = om.lathe("rim", [(0.0072, top), (0.0078, top), (0.0078, top + 0.00003),
                           (0.0072, top + 0.00003)], segments=128)
    om.assign(rim, gold)
    rim.parent = pcb

    copper = om.material("copper_trace", (0.85, 0.5, 0.32), 0.3, metal=1.0)
    label = om.material("laser", (0.16, 0.16, 0.17), 0.75)
    ceramic = om.material("ceramic", (0.42, 0.33, 0.22), 0.5)
    tin = om.material("tin", (0.75, 0.75, 0.76), 0.25, metal=1.0)
    amber = om.material("polyimide", (0.75, 0.38, 0.06), 0.35, coat=0.6)

    # Chip principale con la scritta incisa.
    box("chip_S1", (0, 0.0004, top + 0.0004), (0.0040, 0.0040, 0.0008), chip_mat,
        pcb, bevel=0.00012)
    text("ORBO", 0.00062, (0, 0.0009, top + 0.000801), label, pcb)
    text("S1", 0.0011, (0, -0.0001, top + 0.000801), label, pcb)
    text("2611 A7", 0.00028, (0, -0.0011, top + 0.000801), label, pcb)

    # Piste: dal bordo del chip ai pad sul perimetro, a L.
    n = 28
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        ca, sa = math.cos(a), math.sin(a)
        r0, r1 = 0.0026, 0.0063
        mid = 0.0043
        p0 = (r0 * ca, r0 * sa + 0.0004)
        p1 = (mid * ca, mid * sa + 0.0004)
        bend = a + 0.18
        p2 = (r1 * math.cos(bend), r1 * math.sin(bend) + 0.0002)
        for (x0, y0), (x1, y1) in ((p0, p1), (p1, p2)):
            length = math.hypot(x1 - x0, y1 - y0)
            box("trace", ((x0 + x1) / 2, (y0 + y1) / 2, top + 0.000015),
                (length, 0.00011, 0.00003), copper, pcb,
                rot_z=math.atan2(y1 - y0, x1 - x0))
        pad = om.lathe("pad", [(0.0, 0.0), (0.00022, 0.0), (0.00022, 0.00004),
                               (0.0, 0.00004)], segments=16)
        pad.location = (p2[0], p2[1], top)
        om.assign(pad, gold)
        pad.parent = pcb

    # Chip di memoria, quarzo, condensatori.
    box("mem", (0.0042, -0.0030, top + 0.00025), (0.0016, 0.0022, 0.0005),
        chip_mat, pcb, bevel=0.00008, rot_z=0.5)
    box("xtal", (-0.0040, -0.0032, top + 0.0003), (0.0018, 0.0011, 0.0006),
        tin, pcb, bevel=0.0002, rot_z=-0.4)
    caps = [(-0.0046, 0.0018, 0.3), (-0.0050, 0.0004, 0.3), (0.0047, 0.0022, -0.2),
            (0.0034, 0.0044, 1.1), (-0.0022, 0.0050, 1.6), (0.0006, -0.0047, 0.0),
            (-0.0012, -0.0049, 0.0), (0.0052, -0.0006, 1.4)]
    for x, y, rz in caps:
        box("cap_body", (x, y, top + 0.00016), (0.0006, 0.0003, 0.0003), ceramic,
            pcb, rot_z=rz)
        for e in (-1, 1):
            box("cap_end", (x + e * 0.00026 * math.cos(rz),
                            y + e * 0.00026 * math.sin(rz), top + 0.00016),
                (0.00012, 0.00032, 0.00032), tin, pcb, rot_z=rz)

    # Cavo flessibile che esce dal bordo.
    box("flex", (0.0, -0.0084, top - 0.00025), (0.0024, 0.0040, 0.00008), amber,
        pcb)
    for k in range(5):
        box("flex_pin", (-0.0008 + k * 0.0004, -0.0098, top - 0.0002),
            (0.00018, 0.0010, 0.00002), gold, pcb)


def build_parts(mats):
    root = bpy.data.objects.new("ORBO_explode", None)
    bpy.context.collection.objects.link(root)

    pcb_mat = om.material("pcb", (0.012, 0.03, 0.022), 0.42, coat=0.4)
    chip_mat = om.material("chip", (0.008, 0.008, 0.009), 0.3)
    smd_mat = om.material("smd", (0.55, 0.5, 0.42), 0.3, metal=1.0)
    steel = om.material("steel", (0.62, 0.62, 0.64), 0.28, metal=1.0, aniso=0.5)
    gold = om.material("gold", (0.95, 0.74, 0.42), 0.2, metal=1.0)
    cone_mat = om.material("cone", (0.012, 0.012, 0.013), 0.4, coat=0.6, coat_rough=0.15)

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
    for ang, z in ((150, 0.0034), (250, 0.0022)):
        m2 = mic.copy()
        m2.data = mic.data
        bpy.context.collection.objects.link(m2)
        r = math.radians(ang)
        m2.location = (0.0095 * math.cos(r) * 0.98, 0.0086 * math.sin(r), z)
        m2.rotation_euler = (0, math.radians(68), r)
        m2.parent = upper
    parts["upper"] = upper

    # 3. Scheda con il chip S1.
    pcb = group("pcb", root)
    build_pcb(pcb, pcb_mat, chip_mat, smd_mat, gold)
    parts["pcb"] = pcb

    # 4. Batteria a bottone.
    battery = group("battery", root)
    cell = om.lathe("cell", [(0.0, -0.0015), (0.0054, -0.0015),
                             (0.0057, -0.0012), (0.0057, 0.0018),
                             (0.0054, 0.0021), (0.0, 0.0021)])
    om.assign(cell, steel)
    cell.parent = battery
    ink = om.material("battery_print", (0.012, 0.012, 0.014), 0.85)
    text("ORBO", 0.0012, (0, 0.0013, 0.00211), ink, battery)
    text("Li-ion 3.85 V", 0.0007, (0, -0.0002, 0.00211), ink, battery)
    text("62 mAh", 0.0007, (0, -0.0013, 0.00211), ink, battery)
    nickel = om.material("nickel", (0.7, 0.68, 0.62), 0.3, metal=1.0)
    box("tab_pos", (0.0062, 0.0, 0.0021), (0.0034, 0.0016, 0.00008), nickel, battery)
    box("tab_neg", (-0.0062, 0.0, -0.0015), (0.0034, 0.0016, 0.00008), nickel,
        battery)
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
    dome = om.lathe("dome", [(0.0, -0.0049), (0.0008, -0.0050), (0.0014, -0.0052),
                             (0.0017, -0.00525)])
    oe_solid = dome.modifiers.new("solid", "SOLIDIFY")
    oe_solid.thickness = 0.0001
    om.assign(dome, mats["metal"])
    dome.parent = driver
    for side in (-1, 1):
        box("lead", (side * 0.0040, 0.0, -0.0058), (0.0040, 0.00012, 0.00012),
            mats["metal"], driver)
    magnet = om.lathe("magnet", [(0.0, -0.0080), (0.0036, -0.0080),
                                 (0.0038, -0.0078), (0.0038, -0.0064),
                                 (0.0036, -0.0062), (0.0, -0.0062)])
    om.assign(magnet, om.material("chrome", (0.9, 0.9, 0.92), 0.08, metal=1.0))
    magnet.parent = driver
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


def write_track(scene, parts, path):
    """Per ogni frame, il centro di ogni pezzo in coordinate schermo (0-1,
    origine in alto a sinistra). Il sito lo usa per agganciare le etichette."""
    import json
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector

    def centre(group):
        pts = []
        for child in group.children_recursive:
            if child.type in {"MESH", "FONT"}:
                pts += [child.matrix_world @ Vector(c) for c in child.bound_box]
        return sum(pts, Vector()) / len(pts)

    out = {"frames": FRAMES, "parts": {k: [] for k in parts}}
    for f in range(1, FRAMES + 1):
        scene.frame_set(f)
        for name, group in parts.items():
            co = world_to_camera_view(scene, scene.camera, centre(group))
            out["parts"][name].append([round(co.x, 4), round(1 - co.y, 4)])
    with open(path, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--still", type=int)
    ap.add_argument("--track", help="scrive in JSON la posizione a schermo dei pezzi")
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
    if args.track:
        write_track(scene, parts, args.track)
        return
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
