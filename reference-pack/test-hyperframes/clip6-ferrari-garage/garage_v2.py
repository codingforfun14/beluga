# Garage v2 per "Sotto il telo": piu' realismo (richiesta di fede del 2026-10-25).
# Pavimento 4K con giunti, segni di gomme, macchie d'olio e pozze a bordi netti; strada vera fuori (HDRI);
# arredo con modelli CC0 di Poly Haven; telo con trama e polvere. Usato da spot_garage.py.
import bpy, os, math, random
from mathutils import Vector

def _img(nt, path, color=True, vec=None, proj='BOX'):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path)
    n.projection = proj; n.projection_blend = 0.15
    if not color: n.image.colorspace_settings.name = 'Non-Color'
    if vec is not None: nt.links.new(vec, n.inputs['Vector'])
    return n

def _math(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[i].default_value = v
        else: nt.links.new(v, n.inputs[i])
    return n.outputs[0]

def _ramp(nt, src, stops, interp='LINEAR'):
    r = nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.interpolation = interp
    for el, (pos, v) in zip(r.color_ramp.elements, stops):
        el.position = pos; el.color = (v, v, v, 1)
    nt.links.new(src, r.inputs[0]); return r.outputs[0]

def floor_material(asset):
    d = os.path.join(asset, 'tex', 'concrete_floor_worn_001')
    m = bpy.data.materials.new('pavimento_v2'); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); obj = tc.outputs['Object']
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 3.0,) * 3; nt.links.new(obj, mp.inputs['Vector'])
    dif = _img(nt, f'{d}/concrete_floor_worn_001_diff_4k.jpg', True, mp.outputs['Vector'])
    rgh = _img(nt, f'{d}/concrete_floor_worn_001_rough_4k.jpg', False, mp.outputs['Vector'])
    nor = _img(nt, f'{d}/concrete_floor_worn_001_nor_gl_4k.jpg', False, mp.outputs['Vector'])
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(obj, sep.inputs[0])
    X, Y = sep.outputs['X'], sep.outputs['Y']
    # giunti del cemento ogni 3 m (linee sottili scure)
    def joint(c):
        f = _math(nt, 'FRACT', _math(nt, 'ADD', _math(nt, 'DIVIDE', c, 3.0), 0.5))
        dd = _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', f, 0.5))
        return _math(nt, 'LESS_THAN', dd, 0.004)
    joints = _math(nt, 'MAXIMUM', joint(X), joint(Y))
    # macchie d'olio (scure, un po' lucide), soprattutto dove sta l'auto
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 0.9; n1.inputs['Detail'].default_value = 6
    nt.links.new(obj, n1.inputs['Vector'])
    oil = _ramp(nt, n1.outputs['Fac'], [(0.62, 0.0), (0.7, 1.0)])
    # segni di gomme: due fasce lungo Y (l'auto entra dalla saracinesca), spezzate dal rumore
    def band(cx):
        dd = _math(nt, 'ABSOLUTE', _math(nt, 'SUBTRACT', X, cx))
        return _math(nt, 'LESS_THAN', dd, 0.12)
    tracks = _math(nt, 'MAXIMUM', band(0.82), band(-0.82))
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 4.0; n2.inputs['Detail'].default_value = 8
    nt.links.new(obj, n2.inputs['Vector'])
    tracks = _math(nt, 'MULTIPLY', tracks, _ramp(nt, n2.outputs['Fac'], [(0.45, 0.0), (0.6, 0.55)]))
    # pozze: maschera netta (bordi a gradino), lisce e scure
    n3 = nt.nodes.new('ShaderNodeTexNoise'); n3.inputs['Scale'].default_value = 0.45; n3.inputs['Detail'].default_value = 3
    n3.inputs['Roughness'].default_value = 0.45; nt.links.new(obj, n3.inputs['Vector'])
    puddle = _ramp(nt, n3.outputs['Fac'], [(0.56, 0.0), (0.565, 1.0)], 'CONSTANT')
    # colore
    dark = nt.nodes.new('ShaderNodeMix'); dark.data_type = 'RGBA'; dark.blend_type = 'MULTIPLY'
    nt.links.new(dif.outputs['Color'], dark.inputs[6]); dark.inputs[7].default_value = (0.55, 0.55, 0.55, 1)
    nt.links.new(_math(nt, 'MAXIMUM', _math(nt, 'MULTIPLY', oil, 0.85), _math(nt, 'MAXIMUM', joints, tracks)), dark.inputs['Factor'])
    wet = nt.nodes.new('ShaderNodeMix'); wet.data_type = 'RGBA'; wet.blend_type = 'MULTIPLY'
    nt.links.new(dark.outputs[2], wet.inputs[6]); wet.inputs[7].default_value = (0.45, 0.45, 0.45, 1)
    nt.links.new(puddle, wet.inputs['Factor'])
    hsv = nt.nodes.new('ShaderNodeHueSaturation'); hsv.inputs['Value'].default_value = 0.55; hsv.inputs['Saturation'].default_value = 0.7
    nt.links.new(wet.outputs[2], hsv.inputs['Color']); nt.links.new(hsv.outputs['Color'], p.inputs['Base Color'])
    # rugosita': cemento opaco, olio un po' lucido, pozze a specchio
    r0 = _math(nt, 'MULTIPLY', rgh.outputs['Color'], 0.65)   # cemento lisciato da garage, non ghiaia
    r1 = _math(nt, 'SUBTRACT', r0, _math(nt, 'MULTIPLY', oil, 0.35))
    r2 = _math(nt, 'ADD', r1, _math(nt, 'MULTIPLY', joints, 0.3))
    rgh_mix = nt.nodes.new('ShaderNodeMix'); rgh_mix.data_type = 'FLOAT'
    nt.links.new(puddle, rgh_mix.inputs['Factor']); nt.links.new(r2, rgh_mix.inputs[2]); rgh_mix.inputs[3].default_value = 0.03
    nt.links.new(rgh_mix.outputs[0], p.inputs['Roughness'])
    # normali: dettaglio del cemento + solco dei giunti; nelle pozze la superficie e' piatta
    nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(nor.outputs['Color'], nm.inputs['Color'])
    nt.links.new(_math(nt, 'MULTIPLY', _math(nt, 'SUBTRACT', 1.0, puddle), 0.35), nm.inputs['Strength'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6; bump.invert = True
    nt.links.new(joints, bump.inputs['Height']); nt.links.new(nm.outputs['Normal'], bump.inputs['Normal'])
    nt.links.new(bump.outputs['Normal'], p.inputs['Normal'])
    return m

def cloth_material(asset):
    d = os.path.join(asset, 'tex', 'denim_fabric')
    m = bpy.data.materials.new('telo_v2'); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 0.25,) * 3
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    rg = _img(nt, f'{d}/denim_fabric_rough_1k.jpg', False, mp.outputs['Vector'])
    nr = _img(nt, f'{d}/denim_fabric_nor_gl_1k.jpg', False, mp.outputs['Vector'])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.8
    nt.links.new(nr.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    nt.links.new(_math(nt, 'ADD', _math(nt, 'MULTIPLY', rg.outputs['Color'], 0.3), 0.65), p.inputs['Roughness'])
    # polvere sulle parti rivolte verso l'alto
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Normal'], sep.inputs[0])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6; nz.inputs['Detail'].default_value = 8
    dust = _math(nt, 'MULTIPLY', _ramp(nt, sep.outputs['Z'], [(0.55, 0.0), (0.95, 0.8)]), _ramp(nt, nz.outputs['Fac'], [(0.35, 0.3), (0.7, 1.0)]))
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (0.055, 0.058, 0.065, 1); mix.inputs[7].default_value = (0.2, 0.19, 0.17, 1)
    nt.links.new(dust, mix.inputs['Factor']); nt.links.new(mix.outputs[2], p.inputs['Base Color'])
    p.inputs['Sheen Weight'].default_value = 0.3
    return m

def world(sc, asset, cam_strength=1.2, light_strength=0.03):
    """la camera vede la strada vera (HDRI) a piena luce; la luce che arriva dentro resta controllata dalle lampade"""
    w = bpy.data.worlds.new('mondo_v2'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; out = nt.nodes['World Output']; bg = nt.nodes['Background']
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(asset, 'hdri', 'factory_yard_4k.hdr'))
    mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord')
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(200))
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    bg2 = nt.nodes.new('ShaderNodeBackground')
    nt.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = light_strength
    nt.links.new(env.outputs['Color'], bg2.inputs['Color']); bg2.inputs['Strength'].default_value = cam_strength
    lp = nt.nodes.new('ShaderNodeLightPath'); mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs[0]); nt.links.new(bg.outputs[0], mix.inputs[1]); nt.links.new(bg2.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return w

def import_model(asset, name, loc, rotz=0.0, scale=1.0, link=None):
    sc = bpy.context.scene
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(asset, 'models', name, f'{name}.gltf'))
    new = [o for o in sc.objects if o not in before]
    root = bpy.data.objects.new(name, None); sc.collection.objects.link(root)
    for o in new:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler = (0, 0, rotz); root.scale = (scale,) * 3
    return root

def props(asset, W, L, H, box, m_metal, m_wood):
    """arredo: banco con morsa e trapano a colonna, cassettiera, scaffali pieni, taniche, estintore, gomme, scala, cavi, travi e tubi"""
    random.seed(9)
    hw, hl = W / 2, L / 2
    # banco da lavoro sulla parete sinistra
    box('banco_piano', (-hw + 0.45, 0.6, 0.9), (0.75, 2.2, 0.06), m_wood)
    for y in (-0.4, 1.6):
        for x in (-hw + 0.15, -hw + 0.75): box('banco_gamba', (x, y, 0.45), (0.06, 0.06, 0.9), m_metal)
    box('banco_ripiano', (-hw + 0.45, 0.6, 0.25), (0.7, 2.1, 0.03), m_wood)
    import_model(asset, 'bench_vice_01', (-hw + 0.45, 1.3, 0.93), math.radians(90))
    import_model(asset, 'metal_toolbox', (-hw + 0.4, 0.0, 0.93), math.radians(80))
    import_model(asset, 'oil_tin', (-hw + 0.35, 0.55, 0.93), 0.4)
    import_model(asset, 'drill_press_01', (-hw + 0.45, 2.3, 0.0), math.radians(90))
    import_model(asset, 'metal_tool_chest', (-hw + 0.45, -2.4, 0.0), math.radians(90))
    import_model(asset, 'garden_hose_wall_mounted_01', (-hw + 0.1, -0.9, 1.5), math.radians(90))
    import_model(asset, 'plastic_broom', (-hw + 0.2, -3.6, 0.0), 0.2)
    import_model(asset, 'ladder_sectioned_01', (-hw + 0.5, -hl + 0.3, 0.0), 0.0)
    # scaffali pieni sulla parete destra
    for z in (0.5, 1.3, 2.1):
        box('ripiano', (hw - 0.35, 1.5, z), (0.5, 2.4, 0.04), m_metal)
    for x_, y_ in ((hw - 0.12, 0.32), (hw - 0.58, 0.32), (hw - 0.12, 2.68), (hw - 0.58, 2.68)):
        box('montante', (x_, y_, 1.15), (0.04, 0.04, 2.3), m_metal)
    shelf_items = ['cardboard_box_01', 'plastic_crate_01', 'oil_tin', 'metal_jerrycan', 'cardboard_box_01', 'metal_toolbox']
    for z in (0.52, 1.32, 2.12):
        y = 0.55
        while y < 2.5:
            nm = random.choice(shelf_items)
            import_model(asset, nm, (hw - 0.35, y, z), random.uniform(-0.3, 0.3) + math.radians(90))
            y += random.uniform(0.38, 0.5)
    # pavimento: taniche, carrello, barile, gomme, estintore vicino alla saracinesca
    import_model(asset, 'metal_jerrycan', (hw - 0.4, 3.2, 0.0), 0.3)
    import_model(asset, 'metal_jerrycan_green', (hw - 0.75, 3.3, 0.0), -0.2)
    import_model(asset, 'industrial_storage_cart', (hw - 0.6, -1.5, 0.0), math.radians(95))
    import_model(asset, 'barrel_03', (hw - 0.5, hl - 0.6, 0.0), 0.0)
    for k in range(4):
        import_model(asset, 'old_tyre', (hw - 0.6, -3.8, 0.0 + k * 0.2), random.uniform(0, 3))
    import_model(asset, 'korean_fire_extinguisher_01', (-2.55, hl - 0.25, 0.0), math.radians(180))
    # soffitto: travi d'acciaio, tubi e canaline con cavi
    for y in (-4.5, -1.5, 1.5, 4.5):
        box('trave', (0, y, H - 0.25), (W, 0.12, 0.3), m_metal)
    import_model(asset, 'modular_industrial_pipes_01', (hw - 0.4, 0.0, H - 0.45), math.radians(90))
    import_model(asset, 'modular_electric_cables', (-hw + 0.15, 0.0, H - 0.6), math.radians(90))
