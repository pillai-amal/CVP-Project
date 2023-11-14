import bpy
import os

# Clear existing mesh objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

decimate_ratio = 0.5
context = bpy.context
models = ["airplane.obj"]
for model in models:
    #filepath = os.path.join(os.path.dirname(__file__), model)
    #print("Importing:", filepath)

    # Import OBJ file
    bpy.ops.import_scene.obj(
        filepath= "/Users/pillai_amal/CVP Projekt/dataset/airplane.obj",
        axis_forward='-Z',
        axis_up='Y',
        filter_glob="*.obj;*.mtl"
    )

    # Select the imported object
    imported_object = context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

    # Scale the object to a unit sphere
    bpy.ops.transform.resize(value=(1, 1, 1))
    
    # Decimate the mesh
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = decimate_ratio
    bpy.ops.object.modifier_apply(
                                    {"object": imported_object}, 
                                    modifier="Decimate"
                                )


    # Center the object
    bpy.ops.object.location_clear(clear_delta=False)
    
    # Add a cloth simulation
    bpy.ops.object.modifier_add(type='CLOTH')
    bpy.context.object.modifiers["Cloth"].settings.quality = 5  # Increase quality if needed
    #bpy.context.object.modifiers["Cloth"].settings.quality_shear = 0.5
  # Adjust shear for cloth behavior


    # Deselect the object
    bpy.context.view_layer.objects.active = None

print("Import and transformation complete.")
