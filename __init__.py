bl_info = {
    "name": "NodeExporter",
    "author": "KrazyGFX",
    "version": (1, 9),
    "blender": (3, 6, 0),
    "location": "Node Editor > N-Panel > NodeExporter",
    "description": "Exporta Geometry y Shader Nodes a JSON y auto-ejecuta el visor HTML",
    "category": "Node",
}

import bpy
import json
import os
import webbrowser
import shutil

def get_all_trees(self, context):
    items = []
    for ng in bpy.data.node_groups:
        items.append(("GROUP__" + ng.name, "Group: " + ng.name, "Geometry o Shader Group", 'NODETREE', len(items)))
    
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.node_tree:
            items.append(("MAT__" + mat.name, "Mat: " + mat.name, "Shader Material", 'MATERIAL', len(items)))
            
    if not items:
        items.append(("NONE", "Ninguno", "", 'ERROR', 0))
        
    return items

class KRAZY_PG_Settings(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="Carpeta Export",
        description="Carpeta destino para guardar la captura",
        default="C:\\CapturasBlender",
        subtype='DIR_PATH'
    )
    selected_tree: bpy.props.EnumProperty(
        name="Árbol",
        description="Selecciona el Geometry Node o Material (Shader) a exportar",
        items=get_all_trees
    )

class KRAZY_OT_ExportNodes(bpy.types.Operator):
    bl_idname = "node.krazy_export"
    bl_label = "Exportar y Abrir Visor"
    bl_description = "Exporta a JSON y abre automáticamente el HTML"

    def execute(self, context):
        settings = context.scene.krazy_settings
        tree_val = settings.selected_tree
        tree = None
        proyecto_nombre = "Proyecto"

        if tree_val.startswith("GROUP__"):
            name = tree_val.replace("GROUP__", "", 1)
            if name in bpy.data.node_groups:
                tree = bpy.data.node_groups[name]
                proyecto_nombre = name
        elif tree_val.startswith("MAT__"):
            name = tree_val.replace("MAT__", "", 1)
            if name in bpy.data.materials:
                tree = bpy.data.materials[name].node_tree
                proyecto_nombre = name
                
        if not tree:
            self.report({'WARNING'}, "¡Selecciona un árbol de nodos válido primero!")
            return {'CANCELLED'}

        carpeta_destino = bpy.path.abspath(settings.export_path)

        if not os.path.exists(carpeta_destino):
            try: os.makedirs(carpeta_destino)
            except: 
                self.report({'ERROR'}, "Ruta de carpeta inválida.")
                return {'CANCELLED'}

        datos_exportados = {"proyecto": proyecto_nombre, "nodos": [], "cables": []}

        for nodo in tree.nodes:
            abs_x = nodo.location.x
            abs_y = nodo.location.y
            p = nodo.parent
            while p:
                abs_x += p.location.x
                abs_y += p.location.y
                p = p.parent

            color_fondo = list(nodo.color) if nodo.use_custom_color else None

            puertos_entrada = []
            for e in nodo.inputs:
                if not getattr(e, 'enabled', True): continue
                valor = None
                if not e.is_linked and hasattr(e, 'default_value'):
                    val = e.default_value
                    if type(val).__name__ in ['Vector', 'Euler', 'Color']:
                        valor = [f"{v:.3f}" for v in val]
                    elif isinstance(val, bool): valor = val 
                    elif isinstance(val, float): valor = f"{val:.3f}" 
                    elif isinstance(val, int): valor = str(val) 
                    elif hasattr(val, '__iter__') and not isinstance(val, str):
                        valor = [f"{v:.3f}" if isinstance(v, float) else str(v) for v in val]

                puertos_entrada.append({
                    "nombre": e.name, "tipo_dato": e.type, "conectado": e.is_linked, "valor": valor,
                    "oculto": getattr(e, 'hide', False) # INYECCIÓN: Lee puertos ocultos nativos
                })

            puertos_salida = [
                {"nombre": s.name, "tipo_dato": s.type, "conectado": s.is_linked, "oculto": getattr(s, 'hide', False)}
                for s in nodo.outputs if getattr(s, 'enabled', True)
            ]

            opciones_lista = []
            propiedades_desplegables = ['data_type', 'interpolation_type', 'operation', 'domain', 'distance_type', 'mode', 'blend_type', 'mapping', 'direction', 'distribution_type', 'target_element']
            for prop_name in propiedades_desplegables:
                if hasattr(nodo, prop_name):
                    try:
                        prop_rna = nodo.bl_rna.properties[prop_name]
                        if prop_rna.type == 'ENUM':
                            val = getattr(nodo, prop_name)
                            item = prop_rna.enum_items.get(val)
                            if item and item.name and item.name != 'None':
                                opciones_lista.append(item.name)
                    except Exception: pass

            color_ramp_data = None
            rgb_color = None
            if nodo.bl_idname == 'ShaderNodeValToRGB':
                color_ramp_data = []
                if hasattr(nodo, 'color_ramp'):
                    for elem in nodo.color_ramp.elements:
                        color_ramp_data.append({"pos": elem.position, "color": [elem.color[0], elem.color[1], elem.color[2], elem.color[3]]})
            elif nodo.bl_idname == 'ShaderNodeRGB':
                if len(nodo.outputs) > 0 and hasattr(nodo.outputs[0], 'default_value'):
                    color = nodo.outputs[0].default_value
                    rgb_color = [color[0], color[1], color[2], color[3]]

            info_nodo = {
                "id_interno": nodo.name, "tipo": nodo.bl_idname, "etiqueta": nodo.label if nodo.label else nodo.name,
                "posicion": {"x": abs_x, "y": abs_y}, "dimensiones": {"ancho": nodo.width, "alto": getattr(nodo, 'height', 150)},
                "es_marco": nodo.type == 'FRAME', "color_fondo": color_fondo, "puertos_entrada": puertos_entrada,
                "puertos_salida": puertos_salida, "opciones_lista": opciones_lista, "color_ramp_data": color_ramp_data,
                "rgb_color": rgb_color, "padre": nodo.parent.name if nodo.parent else None,
                "minimizado": getattr(nodo, 'hide', False) 
            }
            datos_exportados["nodos"].append(info_nodo)

        for cable in tree.links:
            datos_exportados["cables"].append({
                "desde_nodo": cable.from_node.name, "desde_puerto": cable.from_socket.name,
                "hacia_nodo": cable.to_node.name, "hacia_puerto": cable.to_socket.name
            })

        blend_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend', '')
        if not blend_name: blend_name = "Untitled"
        safe_proyecto = "".join(x for x in proyecto_nombre if x.isalnum() or x in " _-")
        
        addon_dir = os.path.dirname(__file__)
        html_origen = os.path.join(addon_dir, "visor.html")
        
        ruta_html_destino = os.path.join(carpeta_destino, "NodeExporter_Viewer.html")
        ruta_js = os.path.join(carpeta_destino, "data_export.js")
        ruta_json = os.path.join(carpeta_destino, f"{blend_name}_{safe_proyecto}.json")

        with open(ruta_json, 'w', encoding='utf-8') as archivo:
            json.dump(datos_exportados, archivo, indent=4, ensure_ascii=False)

        json_string = json.dumps(datos_exportados, ensure_ascii=False)
        with open(ruta_js, 'w', encoding='utf-8') as js_file:
            js_file.write(f"const INJECTED_DATA = {json_string};")

        if os.path.exists(html_origen):
            shutil.copy(html_origen, ruta_html_destino)
            webbrowser.open('file://' + ruta_html_destino.replace('\\', '/'))
            self.report({'INFO'}, "¡Exportado y Visor Abierto!")
        else:
            self.report({'ERROR'}, "Instalación corrupta: Falta el archivo visor.html en el Add-on.")

        return {'FINISHED'}

class KRAZY_OT_GetActiveTree(bpy.types.Operator):
    bl_idname = "node.krazy_get_active"
    bl_label = "Usar Nodo en Pantalla"
    bl_description = "Selecciona automáticamente el árbol de nodos activo"

    def execute(self, context):
        area = next((a for a in context.screen.areas if a.type == 'NODE_EDITOR'), None)
        if area:
            space = area.spaces.active
            if hasattr(space, 'id') and isinstance(space.id, bpy.types.Material):
                context.scene.krazy_settings.selected_tree = "MAT__" + space.id.name
                self.report({'INFO'}, f"Material '{space.id.name}' cargado.")
                return {'FINISHED'}
            
            if space.edit_tree and space.edit_tree.name in bpy.data.node_groups:
                context.scene.krazy_settings.selected_tree = "GROUP__" + space.edit_tree.name
                self.report({'INFO'}, f"Grupo '{space.edit_tree.name}' cargado.")
                return {'FINISHED'}

        self.report({'WARNING'}, "Abre un editor de nodos con un Material o Geometry Node activo.")
        return {'FINISHED'}

class KRAZY_PT_Panel(bpy.types.Panel):
    bl_label = "NodeExporter"
    bl_idname = "KRAZY_PT_Panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeExporter'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.krazy_settings
        
        layout.operator("node.krazy_get_active", icon='RESTRICT_SELECT_OFF')
        layout.prop(settings, "selected_tree", text="")
        
        layout.separator()
        layout.label(text="Destino del JSON y Captura:")
        layout.prop(settings, "export_path", text="")
        
        layout.separator()
        row = layout.row()
        row.scale_y = 1.5 
        row.operator("node.krazy_export", icon='EXPORT')

classes = (
    KRAZY_PG_Settings,
    KRAZY_OT_ExportNodes,
    KRAZY_OT_GetActiveTree,
    KRAZY_PT_Panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.krazy_settings = bpy.props.PointerProperty(type=KRAZY_PG_Settings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.krazy_settings

if __name__ == "__main__":
    register()