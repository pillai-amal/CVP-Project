import bpy
import os
import re

def import_and_setup_model(filepath):
    directory = re.sub(r"\\[^\\]*$", "", filepath)
    bpy.ops.wm.obj_import(filepath=filepath,directory=directory)
    
    obj_name = bpy.context.object.name
    max_dim = max(bpy.data.objects.get(obj_name).dimensions)
    
    bpy.context.object.scale[0] = 1/max_dim
    bpy.context.object.scale[1] = 1/max_dim
    bpy.context.object.scale[2] = 1/max_dim

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.modifier_add(type='COLLISION')
    bpy.context.view_layer.objects.active = None

def setup_cloth_simulation():
    bpy.ops.mesh.primitive_plane_add(
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 12),
        scale=(2, 2, 1)
    )
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=100)
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object mode
    bpy.ops.object.modifier_add(type='CLOTH')
    
    # Additional cloth settings which can be turned on if necessary 

    #bpy.context.object.modifiers["Cloth"].settings.quality = 20
    # bpy.context.object.modifiers["Cloth"].settings.use_pressure = True
    # bpy.context.object.modifiers["Cloth"].settings.uniform_pressure_force = 1.0  
    # bpy.ops.object.modifier_apply({"object": cloth_object}, modifier="Cloth")

    # Bake cloth simulation
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 200  # Adjust frame_end as needed
    bpy.ops.ptcache.bake_all(bake=True)

def export_mesh(obj, filepath):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.obj_export(filepath=filepath)


def main():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    context = bpy.context
    models = ["FinalBaseMesh.obj"]

    for model in models:
        import_and_setup_model(model)
        setup_cloth_simulation()

        cloth_object = bpy.context.collection.objects[0]
        cloth_export_path = os.path.join(os.getcwd(), f"{model}_cloth.obj")
        export_mesh(cloth_object, cloth_export_path)

        original_object = bpy.context.collection.objects[1]
        original_export_path = os.path.join(os.getcwd(), f"{model}_original.obj")
        export_mesh(original_object, original_export_path)

    bpy.ops.render.render(write_still=True)

    print("Import, Transformation, and Cloth Simulation completed.")
    print(f"Cloth saved at: {cloth_export_path}")
    print(f"Object saved at: {original_export_path}")

main()
