import bpy
import os
import re

def import_and_setup_model(model_name):
    directory = re.sub(r"\\[^\\]*$", "", model_name)
    bpy.ops.wm.obj_import(filepath=model_name,directory=directory)
    
    obj_name = bpy.context.object.name
    max_dim = max(bpy.data.objects.get(obj_name).dimensions)
    
    bpy.context.object.scale[0] = 1/max_dim
    bpy.context.object.scale[1] = 1/max_dim
    bpy.context.object.scale[2] = 1/max_dim

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.modifier_add(type='COLLISION')
    bpy.context.view_layer.objects.active = None
    file_name = os.path.splitext(os.path.basename(model_name))[0]
    filepath = os.path.join(os.getcwd(), f"{file_name}_original.obj")
    bpy.ops.wm.obj_export(filepath=filepath)

def setup_cloth_simulation():
    bpy.ops.mesh.primitive_plane_add(
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 2),
        scale=(1, 1, 1)
    )
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=100)
    bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.modifier_add(type='CLOTH')


    # Bake cloth simulation
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 100  # Adjust frame_end as needed
    bpy.ops.ptcache.bake_all(bake=True)

def export_cloth_mesh(obj, filepath):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='INVERT')
    bpy.ops.object.delete()
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
    bpy.ops.wm.obj_export(filepath=filepath)


def main():
    bpy.context.view_layer.objects.active = bpy.data.objects['Light']
    bpy.ops.object.delete()
    bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
    bpy.ops.object.delete()

    context = bpy.context
    models = ["2909.obj", "Basswood_Fan_0.obj"]

    for model in models:
        print("Loading Model:", model)

        file_name = os.path.splitext(os.path.basename(model))[0]
        import_and_setup_model(model)
        setup_cloth_simulation()

        cloth_object = bpy.data.objects['Plane']
        cloth_export_path = os.path.join(os.getcwd(), f"{file_name}_cloth.obj")
        export_cloth_mesh(cloth_object, cloth_export_path)

        original_export_path = os.path.join(os.getcwd(), f"{file_name}_original.obj")
 
        print("Import, Transformation, and Cloth Simulation completed.")
        print(f"Cloth saved at: {cloth_export_path}")
        print(f"Object saved at: {original_export_path}")
    
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
    print("All processing Complete")
main()
