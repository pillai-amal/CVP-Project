import os

import open3d as o3d
import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

def load_obj(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    vertices = np.asarray(mesh.vertices)
    return mesh, vertices

def find_nearest_points(mesh1_points, mesh2_points):
    tree = KDTree(mesh2_points)
    nearest_points_mesh2 = np.zeros_like(mesh1_points)

    for i, point in enumerate(mesh1_points):
        _, index = tree.query(point)
        nearest_points_mesh2[i] = mesh2_points[index]

    return nearest_points_mesh2

def calculate_distances(mesh1_points, nearest_points):
    distances = np.linalg.norm(mesh1_points - nearest_points, axis=1)
    return distances

def color_mesh_by_distances(mesh, distances):
    normalized_distances = np.clip(1 - distances / 0.1, 0, 1)
    colormap = plt.cm.gray(normalized_distances)

    colored_mesh = o3d.geometry.TriangleMesh()
    colored_mesh.vertices = mesh.vertices
    colored_mesh.triangles = mesh.triangles
    colored_mesh.vertex_colors = o3d.utility.Vector3dVector(colormap[:, :3])

    return colored_mesh


def main():
    folder_path_cloth = 'cloth'
    folder_path_obj = 'objects'
    output_folder = 'distance'
    cloth_mesh_files = [f for f in os.listdir(folder_path_cloth) if f.endswith(('.obj'))]
    objects_mesh_files = [f for f in os.listdir(folder_path_obj) if f.endswith(('.obj'))]

    for cloth_mesh_path, obj_mesh_path in zip(cloth_mesh_files, objects_mesh_files):
        handle_meshes(cloth_mesh_path, obj_mesh_path, folder_path_cloth, folder_path_obj, output_folder)

def handle_meshes(cloth_mesh_name, obj_mesh_name, folder_path_cloth, folder_path_obj, output_folder):
    output_path = os.path.join(output_folder, f"{os.path.splitext(cloth_mesh_name)[0]}.obj")
    cloth_mesh_path = os.path.join(folder_path_cloth, cloth_mesh_name)
    obj_mesh_path = os.path.join(folder_path_obj, obj_mesh_name)
    cloth_mesh, cloth_points = load_obj(cloth_mesh_path)
    object_points = load_obj(obj_mesh_path)[1]

    nearest_points = find_nearest_points(cloth_points, object_points)
    distances = calculate_distances(cloth_points, nearest_points)

    colored_mesh = color_mesh_by_distances(cloth_mesh, distances)
    #o3d.visualization.draw_geometries([colored_mesh])

    # Save the colored mesh as .obj file
    o3d.io.write_triangle_mesh(output_path, colored_mesh, write_triangle_uvs=True)

if __name__ == "__main__":
    main()