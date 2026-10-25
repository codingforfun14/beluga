# Importa e prepara la Ferrari 488 GTB (modello CC BY di Turbostuart su Sketchfab, credito obbligatorio).
# Il glb arriva da SketchUp: unita' in pollici, carrozzeria rosa segnaposto ("body1"), vetri come alpha.
# Uso da un altro script:  import car488; car = car488.load(path)  -> empty 'car' a terra, centrato, muso verso +Y
import bpy, math
from mathutils import Vector

def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

ROSSO_CORSA = srgb('#C80000')
USE_DISPLACE = False   # in Eevee il Displace crea artefatti sui passaruota: per ora spento

def unlink(m, p, names=('Base Color', 'Roughness', 'Metallic', 'Alpha')):
    # i materiali glTF spesso hanno il colore collegato ai colori dei vertici: lo stacchiamo
    for n in names:
        for l in list(p.inputs[n].links): m.node_tree.links.remove(l)

def paint(m):
    m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; unlink(m, p)
    p.inputs['Base Color'].default_value = (*ROSSO_CORSA, 1)
    p.inputs['Roughness'].default_value = 0.32; p.inputs['Metallic'].default_value = 0.0
    p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.02
    p.inputs['Specular IOR Level'].default_value = 0.6

def glass(m, tint=0.02):
    m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; unlink(m, p)
    p.inputs['Base Color'].default_value = (tint, tint, tint * 1.1, 1); p.inputs['Roughness'].default_value = 0.02
    p.inputs['Alpha'].default_value = 0.3; p.inputs['Coat Weight'].default_value = 1.0
    m.surface_render_method = 'BLENDED'; m.use_transparency_overlap = False

def satin(m, v, rough=0.45, metal=0.0):
    m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']; unlink(m, p)
    p.inputs['Base Color'].default_value = (v, v, v, 1); p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal

def load(path):
    sc = bpy.context.scene
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in sc.objects if o not in before]
    root = bpy.data.objects.new('car', None); sc.collection.objects.link(root)
    for o in new:
        if o.parent is None: o.parent = root
    root.scale = (0.0254,) * 3          # pollici -> metri
    bpy.context.view_layer.update()
    meshes = [o for o in new if o.type == 'MESH']
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
    for o in meshes:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    c = (mn + mx) / 2
    pivot = bpy.data.objects.new('car_pivot', None); sc.collection.objects.link(pivot)
    root.parent = pivot; root.location = (-c.x, -c.y, -mn.z)
    # materiali
    for m in {m for o in meshes for m in o.data.materials if m}:
        if not m.use_nodes: continue
        p = m.node_tree.nodes.get('Principled BSDF')
        if p is None: continue
        bc = p.inputs['Base Color'].default_value; a = p.inputs['Alpha'].default_value
        if m.name == 'body1': paint(m)
        elif a < 0.6 and m.name not in ('Color_A08',): glass(m)
        elif m.name == 'Color_A08':   # fanali posteriori rossi traslucidi
            p.inputs['Emission Color'].default_value = (1, 0.02, 0.01, 1); p.inputs['Emission Strength'].default_value = 0.0
        elif m.name == 'Tyre_Side': satin(m, 0.025, 0.75)
        elif m.name in ('material_0', 'Color_B05_3', 'Color_C03'): satin(m, 0.02, 0.35)
        elif m.name == 'black2':
            satin(m, 0.015, 0.8); m.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value = 0.05   # plastica opaca: lucida rifletteva la luce del giorno come un pannello azzurro   # griglie e diffusore (nel glb chiari)
        elif m.name in ('Profiel02', 'material', 'material_8', 'material_8_1'): satin(m, 0.015, 0.7)   # gomme e plastiche bianche nel glb
        elif m.name in ('Chrome_Trim1', 'Metal_Corrogated_Shiny'): satin(m, 0.9, 0.12, 1.0)
        elif tuple(round(x, 2) for x in bc[:3]) == (1.0, 1.0, 1.0): satin(m, 0.03, 0.4)   # parti bianche SketchUp = plastiche/carbonio
        else: p.inputs['Roughness'].default_value = min(p.inputs['Roughness'].default_value, 0.5)
    for o in meshes:
        if len(o.data.polygons) == 0: o.hide_render = True; o.hide_viewport = True; continue
        for poly in o.data.polygons: poly.use_smooth = True
        mod = o.modifiers.new('smooth', 'NODES')
        try:
            bpy.context.view_layer.objects.active = o
            o.modifiers.remove(mod)
            with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o]):
                bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
        except Exception:
            pass
    # il guscio nero (Object_70/72) si sovrappone alla carrozzeria: Object_78 spinta fuori di 4 mm
    b = bpy.data.objects.get('Object_78')
    if b and USE_DISPLACE:
        d = b.modifiers.new('fuori', 'DISPLACE'); d.direction = 'NORMAL'; d.mid_level = 0; d.strength = 0.004 / 0.0254
    pivot['size'] = tuple(mx - mn)
    return pivot
