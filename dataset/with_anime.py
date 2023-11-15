import bpy
import os

def import_and_setup_model(filepath):
    bpy.ops.import_scene.obj(
        filepath=filepath,
        axis_forward='-Z',
        axis_up='Y',
        filter_glob="*.obj;*.mtl"
    )

    # Select the imported object
    imported_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

    # Scale the object to a unit sphere
    bpy.ops.transform.resize(value=(1, 1, 1))

    # Decimate the mesh
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = decimate_ratio
    bpy.ops.object.modifier_apply({"object": imported_object}, modifier="Decimate")

    # Center the object
    bpy.ops.object.location_clear(clear_delta=False)

    # Add the imported object as a collision object
    bpy.ops.object.modifier_add(type='COLLISION')

    # Deselect the imported object
    bpy.context.view_layer.objects.active = None

def setup_cloth_simulation():
    # Add a plane for cloth simulation
    bpy.ops.mesh.primitive_plane_add(
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 1100),
        scale=(1100, 1100, 1)
    )

    # Subdivide the cloth
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)

    # Add a cloth simulation
    bpy.ops.object.modifier_add(type='CLOTH')
    bpy.context.object.modifiers["Cloth"].settings.quality = 5  # Increase quality if needed
    
    return bpy.context.active_object.name

def main():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    context = bpy.context
    models = ["airplane.obj"]

    for model in models:
        import_and_setup_model(model)

        # Set up cloth simulation
        cloth = setup_cloth_simulation()

    # Set up animation parameters
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames

    bpy.ops.object.mode_set(mode='OBJECT')  # Switch to Object Mode

    # Bake cloth simulation
    obj = bpy.context.scene.objects.get(cloth)
    if obj:
        bpy.context.scene.objects.active = bpy.context.scene.objects[cloth]
        bpy.ops.ptcache.bake({'scene': bpy.context.scene}, bake=True)
    else:
        print(f"Object with name '{cloth}' not found in the scene.")

    # Set up rendering settings
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.filepath = output_path

    # Render animation
    bpy.ops.render.render(animation=True)

    print("Import, transformation, and cloth simulation complete.")
    print(f"Video saved at: {output_path}")

# Parameters
decimate_ratio = 0.5
subdivisions = 22  # Number of subdivisions for the plane
frames = 150  # Number of frames for the animation
output_path = "/Users/pillai_amal/CVP Projekt/dataset/video.mp4"

# Run the script
main()
