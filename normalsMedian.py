import numpy as np
import cv2
import argparse
import os
import glob
import shutil
import matplotlib.pyplot as plt

def load_image(path):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image.dtype == "uint8":
        bit_depth = 8
    elif image.dtype == "uint16":
        bit_depth = 16
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)/np.float64(2**bit_depth - 1)

def load_normal(path):
    image = load_image(path)
    normal = image * 2.0 - 1.0  # Convert to range [-1, 1]
    normal[:,:,1] = -normal[:,:,1] # y axis is flipped
    normal[:,:,2] = -normal[:,:,2] # z axis is flipped
    return normal

def save_image(image, path, bit_depth=8):
    image = (image * np.float64(2**bit_depth - 1))
    image = np.clip(image, 0, 2**bit_depth - 1)
    if bit_depth == 8:
        image = image.astype(np.uint8)
    elif bit_depth == 16:
        image = image.astype(np.uint16)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

def save_normal(normal, path, bit_depth=8):
    normal[:,:,1] = -normal[:,:,1] # y axis is flipped
    normal[:,:,2] = -normal[:,:,2] # z axis is flipped
    image = (normal + 1) / 2
    save_image(image, path, bit_depth=bit_depth)

def geodesic_distances(points):

    # Convert the 3D points to spherical coordinates
    lat1, lon1 = points[:, 0], points[:, 1]
    lat2, lon2 = lat1[:, np.newaxis], lon1[:, np.newaxis]

    # Compute the differences in longitude and latitude
    dlon = lon2 - lon1.T
    dlat = lat2 - lat1.T

    # Compute the geodesic distance using the provided function
    aux = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    distances = 2 * np.arctan2(np.sqrt(aux), np.sqrt(1 - aux))

    return distances

def normal_median(normals):
    """
    Compute the median normal vector from a set of normal vectors.
    The median normal is the vector that minimizes the sum of the geodesic distances between
    the median normal and the other normals.
    """
    # Normalize the normals to unit length
    normals_ = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # Get spherical coordinates
    lat = np.arccos(normals_[:,2])
    lon = np.arctan2(normals_[:,1], normals_[:,0])
    points_sph = np.stack((lat, lon), axis=1)

    # Compute the geodesic distance between all normals
    distances = geodesic_distances(points_sph)
    
    # Sum the distances on each row
    distances_sum = distances.sum(axis=0)

    # Find the normal with the minimum sum of distances
    median = normals[distances_sum.argmin(),:]
    dist_median = distances[distances_sum.argmin(),:]

    # Plot in 3D the normals and the median normal
    if False:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(normals_[:,0], normals_[:,1], normals_[:,2], c='b', marker='o')
        median_ = normals_[distances_sum.argmin(),:]
        ax.scatter(median_[0], median_[1], median_[2], c='r', marker='o', linewidths=10)
        plt.show()

    return median, dist_median

def main(args):

    # ARGS
    NORMALS_DIR = args.normals_dir
    SOURCE_DIR = args.source_dir
    NUM_VIEW = args.num_view
    OUTPUT_DIR = args.output_dir

    # Split NORMALS_DIR to get the last folder name
    normal_dir_split = NORMALS_DIR.split("/")
    SCENE_NAME = normal_dir_split[-1]

    # Create output directory
    OUTPUT_VIEW_DIR = os.path.join(OUTPUT_DIR, f"{SCENE_NAME}_{NUM_VIEW:02d}.data")
    if not os.path.exists(OUTPUT_VIEW_DIR):
        os.makedirs(OUTPUT_VIEW_DIR)

    # Load mask
    MASK_PATH = os.path.join(SOURCE_DIR, SCENE_NAME, f"view_{NUM_VIEW:02d}", "mask.png")
    mask = load_image(MASK_PATH) > 0.5
    if len(mask.shape) == 3:
        mask = mask[:, :, 0]

    # Load normal maps
    n_exps = 100
    normal_maps = np.zeros((512,612,3,n_exps), dtype=np.float32)
    albedo_maps = np.zeros((512,612,3,n_exps), dtype=np.float32)
    for i in range(n_exps):

        # Get normal map
        data_folder = os.path.join(NORMALS_DIR,f"{i+1:04d}","results",f"{SCENE_NAME}_{NUM_VIEW:02d}.data")
        normal_map = load_normal(os.path.join(data_folder,'normal.png'))
        albedo_map = load_image(os.path.join(data_folder,'baseColor.png'))

        # Save normal map
        normal_maps[:,:,:,i] =  normal_map
        albedo_maps[:,:,:,i] =  albedo_map

    # Get number of rows and columns
    n_rows, n_cols, _, _ = normal_maps.shape

    # Compute median normals
    median_normal_map = normal_map
    for i in range(n_rows):
        for j in range(n_cols):
            if mask[i,j]:
                median_normal_map[i,j,:], distances = normal_median(normal_maps[i,j,:,:].T)

    # Save median normal map
    save_normal(median_normal_map, os.path.join(OUTPUT_VIEW_DIR, "normal.png"), bit_depth=16)

    # Save median albedo map
    median_albedo_map = np.median(albedo_maps, axis=3)
    save_image(median_albedo_map, os.path.join(OUTPUT_VIEW_DIR, "baseColor.png"), bit_depth=16)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=".")
    parser.add_argument("--normals_dir", help="Path to the normals map (RGB) input image.")
    parser.add_argument("--source_dir", help="Path to the source directory.")
    parser.add_argument("--num_view", type=int, default=1, help="Number of views.")
    parser.add_argument("--output_dir", help="Path to the output directory.")
    args = parser.parse_args()
    main(args)

