import bpy
import os

def import_and_setup_model(filepath, decimate_ratio):
    bpy.ops.import_scene.obj(
        filepath=filepath,
        axis_forward='-Z',
        axis_up='Y',
        filter_glob="*.obj;*.mtl"
    )

    imported_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.transform.resize(value=(1, 1, 1))
    
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = decimate_ratio
    bpy.ops.object.modifier_apply({"object": imported_object}, modifier="Decimate")

    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.modifier_add(type='COLLISION')
    bpy.context.view_layer.objects.active = None

    size_x, size_y, size_z = imported_object.dimensions

    return [size_x, size_y, size_z]

def setup_cloth_simulation(subdivisions,x,y):
    bpy.ops.mesh.primitive_plane_add(
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 60),
        scale=(x, y, 1)
    )
    
    bpy.ops.transform.resize(value=(x, y, 1))
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=21)
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object mode

    # cloth_object = bpy.context.active_object
    bpy.ops.object.modifier_add(type='CLOTH')
    
    #Additional cloth settings which can be turned on if necessary 

    # bpy.context.object.modifiers["Cloth"].settings.quality = 5
    # bpy.context.object.modifiers["Cloth"].settings.use_pressure = True
    # bpy.context.object.modifiers["Cloth"].settings.uniform_pressure_force = 1.0  
    # bpy.ops.object.modifier_apply({"object": cloth_object}, modifier="Cloth")

    # Bake cloth simulation
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 400  # Adjust frame_end as needed
    bpy.ops.ptcache.bake_all(bake=True)

def setup_lighting():
    bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 200))
    light = bpy.context.object
    light.data.energy = 1000

def export_mesh(obj, filepath):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.obj(filepath=filepath, use_selection=True)

def setup_camera():
    bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, -10, 2), rotation=(1.22, 0, 0))
    bpy.context.scene.camera = bpy.context.object

    # Set wider focal length
    bpy.data.cameras[bpy.context.camera.data.name].lens = 35  # Adjust the value as needed

def main():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    context = bpy.context
    models = ["monkey.obj"]

    for model in models:
        #import_and_setup_model(model, decimate_ratio=0.5)
        x, y, _ = import_and_setup_model(model, decimate_ratio=0.5)
        setup_cloth_simulation(22,x,y)

        cloth_object = bpy.context.active_object
        cloth_export_path = os.path.join(os.getcwd(), f"{model}_cloth.obj")
        export_mesh(cloth_object, cloth_export_path)

        original_object = bpy.context.selected_objects[0]
        original_export_path = os.path.join(os.getcwd(), f"{model}_original.obj")
        export_mesh(original_object, original_export_path)

    setup_lighting()
    setup_camera()

    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_path

    bpy.ops.render.render(write_still=True)

    print("Import, Transformation, and Cloth Simulation completed.")
    print(f"Image saved at: {output_path}")
    print(f"Cloth saved at: {cloth_export_path}")
    print(f"object saved at: {original_export_path}")

output_path = os.path.join(os.getcwd(), "rendered_image.png")
main()
